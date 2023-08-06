import collections
import functools
import os, re
import inspect
import copy
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum, unique
from typing import List, Dict, Any, Union, Collection, Iterable, Optional, Tuple
from functools import lru_cache
from itertools import product
from .orderedset import OrderedSet
import tempfile

import numpy as np
import pandas as pd

"""
This module allows you to construct a condition object in a user friendly way.

Goals
------------
This package aims to achieve the following goals:

#. Provides a user friendly way to construct condition objects. Support common operators: ``<, <=, >, >=, ==, in, not in``.
#. Supports composite conditions with ``And``, ``Or`` with arbitrary structure;
#. Supports various usage contexts, for example, pandas dataframe filtering, SQL generation and pyarrow partition filtering.

Benefits
------------
#. A condition object can be passed to the back end.
#. A condition object can be interpreted consistently in different contexts.
#. A support usage context takes care of formatting and syntax details.

"""


@unique
class Operator(Enum):
    LE = "<="
    LT = "<"
    GE = ">="
    GT = ">"
    EQ = "="
    NEQ = "!="
    IN = "in"
    NOT_IN = "not in"


# declarations for typing hints to work.
class FieldCondition:
    pass


class FieldList:
    pass


class Condition:
    pass


class FieldCondition:
    pass


class And:
    pass


class Or:
    pass


class Field:
    def __init__(self, name: str):
        self.name = name

    def __le__(self, other: Any) -> FieldCondition:
        return FieldCondition(self, Operator.LE, other)

    def __lt__(self, other: Any) -> FieldCondition:
        return FieldCondition(self, Operator.LT, other)

    def __eq__(self, other: Any) -> FieldCondition:
        if isinstance(other, str) or not isinstance(other, Collection):
            return FieldCondition(self, Operator.EQ, other)
        else:
            return FieldCondition(self, Operator.IN, self._get_collection(other))

    def __ne__(self, other: Any) -> FieldCondition:
        if isinstance(other, str) or not isinstance(other, Collection):
            return FieldCondition(self, Operator.NEQ, other)
        else:
            return FieldCondition(self, Operator.NOT_IN, self._get_collection(other))

    def __ge__(self, other: Any) -> FieldCondition:
        return FieldCondition(self, Operator.GE, other)

    def __gt__(self, other: Any) -> FieldCondition:
        return FieldCondition(self, Operator.GT, other)

    def _get_collection(self, val: Collection) -> OrderedSet:
        if not (isinstance(val, Collection)):
            raise TypeError("'%s' object is not a collection", type(val).__name__)
        if len(val) == 0:
            raise ValueError("Cannot use empty collection as filter value")
        if len({type(item) for item in val}) != 1:
            raise ValueError(
                "All elements of the collection '%s' must be" " of same type", val
            )
        values = OrderedSet(val)
        values.freeze()
        return values

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)


class FieldList:
    """
    Exposes each of the list as a field attribute which can then be used to construct field conditions.
    """

    INVALID_CHAR = re.compile("\W|^(?=\d)")

    def to_identifier(self, s: str, existing=None):
        s = self.INVALID_CHAR.sub("_", s)
        if s[0].isdigit():
            s = "_" + s
        r = s
        if existing:
            i = 0
            while r in existing:
                i += 1
                r = s + str(i)

        return r

    def __init__(self, fields: Collection[str]):
        self.fields = tuple(sorted(fields))
        self._dict = {name: Field(name) for name in fields}
        identifiers = set()
        for name in self.fields:
            id1 = self.to_identifier(name, identifiers)
            identifiers.add(id1)
            setattr(self, id1, self._dict[name])
        self._hashcode = None

    def __getitem__(self, name):
        return self._dict[name]

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> FieldList:
        """A shortcut to construct a field list from the index names and columns of the dataframe"""
        if df.index.names and df.index.names[0]:
            return FieldList(list(df.index.names) + list(df.columns))
        else:
            return FieldList(list(df.columns))

    def __repr__(self) -> str:
        return "FieldList [" + ",".join(self.fields) + "]"

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, FieldList)
            and len(self.fields) == len(other.fields)
            and self.fields == other.fields
        )

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        if not self._hashcode:
            self._hashcode = hash(tuple(self.fields))
        return self._hashcode


class ConditionApplication(ABC):
    """
    Defines behaviors for different condition application cases and to be used with
    ``condition.apply``. This enables extension of the condition for new usage contexts.
    Many built-in methods actually uses this mechanism, such as ``to_df_query()``.
    You can use the built-in classes as tutorial examples for writing your own ``ConditionApplication``.
    """

    def on_start(self, cond, **kwargs) -> Dict:
        """
        Called on the start of ``condition.apply()``. Here you can add some initialization logic,
        and add common kwargs to be used later on. You can even change the ``cond``
        Implementation of this method is optional.

        :param cond: the outmost condition object to be applied
        :param kwargs: the kwargs as in ``cond.apply(condition_application, **kwargs)``.
        :return: the possibly enriched kwargs to be passed to various apply* methods.
            You can optionally change the cond object itself with key ``cond`` as in
            ``PyarrowFilterApplication``.
        """
        return kwargs

    def on_end(self, cond, result, **kwargs):
        """
        Called on the end of ``condition.apply()``. Here you can add some finishing logic, i.e.,
        save to a file or etc.
        Implementation of this method is optional.

        :param cond: the outmost condition object to be applied
        :param result: provides a way to modify the result
        :return: the value to be returned as the result of ``cond.apply()``.
        """
        return result

    @abstractmethod
    def applyFieldCondition(self, cond: FieldCondition, **kwargs):
        """
        Actions to perform with a ``FieldCondition``.

        :param kwargs: note that you need to maintain same set of kwargs for apply* methods.
        """
        pass

    @abstractmethod
    def applyAndCondition(self, cond: And, **kwargs):
        """
        Action to perform with an ``And`` condition. You need to call ``cond.apply_to_subs(**kwar)`` in this method.

        :param kwargs: note that you need to maintain same set of kwargs for apply* methods.
        """
        pass

    @abstractmethod
    def applyOrCondition(self, cond: Or, **kwargs):
        """
        Action to perform with an ``Or`` condition. YYou need to call ``cond.apply_to_subs`` in this method.

        :param kwargs: note that you need to maintain same set of kwargs for apply* methods.
        """
        pass

    def applyEmptyCondition(self, cond, **kwargs):
        """
        Action to perform with an ``Empty`` condition, which can be a result of ``cond.split()``
        and means ``True`` or no filtering.
        In fact, it is impossible to return "no filtering" in some contexts. In such case, you
        need to check if the cond is empty before calling ``apply``. One example is ``condition.query()``.
        Implementation of this method is optional.

        :param kwargs: note that you need to maintain same set of kwargs for apply* methods.
        """
        return None


class Condition(ABC):
    """
    Represents a condition object. It is immutable.
    """

    def __init__(self):
        self.params = {}

    @abstractmethod
    def _apply_recursively(self, application: ConditionApplication, **kwargs):
        pass

    def apply(self, application: ConditionApplication, **kwargs):
        """
        Applies the ``ConditionApplication`` to this condition. This is
        an extension mechanism allowing you to implement the ``condition`` for
        different usage contexts.
        """
        kwargs = application.on_start(self, **kwargs)
        if "cond" in kwargs:
            cond = kwargs.pop("cond")
        else:
            cond = self
        result = cond._apply_recursively(application, **kwargs)
        result = application.on_end(cond, result, **kwargs)
        return result

    @staticmethod
    def register_application(name: str, application: ConditionApplication):
        """
        A syntax sugar to enable calling your ``ConditionApplication`` as if it were
        built in the ``Condition`` class. Afterwards, you can call ``cond.<name>()`` which
        is actually ``cond.apply(application())``.

        :param name: the method name. This must be unique
        :param application: your application to be called by this method.
        """
        # @functools.wraps()
        # TODO: doc ?
        def fn(condition, **kwargs):
            return condition.apply(application(), **kwargs)

        setattr(Condition, name, fn)

    def set_param(self, name: str, val: Any) -> None:
        """Sets additional param/value to pass to the end consumer. For example,
        the params can be used in sql templates.
        Note that only the top condition's params is used.

        :param name: the param name. It will be available in jinja2 SQL template.
        :param val: the value
        """
        self.params[name] = val

    def __and__(self, other: Condition) -> Condition:
        """Supports `&` operator which results in an `And` condition"""
        return And([self, other])

    def __or__(self, other: Condition) -> Condition:
        """Supports `|` operator which results in an `Or` condition"""
        return Or([self, other])

    def to_sql_where_condition(
        self, db_map: Optional[Dict[str, str]] = None, indent: int = 1
    ) -> str:
        """
        Generates a string representing the condition for used in a sql where clause.

        :param db_map: map from a field name to a db field name. Note that you can also
            pass in alias in the db field name. By default, use field names directly.
        :param indent:
        :return: condition string for sql where clause.
        """
        sa = SqlWhereApplication()
        return self.apply(sa, db_map=db_map, indent=indent)

    def get_all_field_conditions(self) -> collections.OrderedDict:
        """
        Returns all ``FieldCondition`` contained in this condition.

        :return: a dict: field name -> list of ``FieldCondition`` for this field.
        """
        visited = set()
        d = collections.OrderedDict()

        def dfs(cond):
            visited.add(cond)
            if isinstance(cond, CompositeCondition):
                for s in cond.conditions:
                    if s not in visited:
                        dfs(s)
            else:
                key = cond.field.name
                if key not in d:
                    d[key] = []
                d[key].append(cond)

        dfs(self)
        return d

    def to_sql_dict(self, dbmap: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Generates a dict to pass into a sql template.

        Before you write your sql template, you can call this method and print out the dict (keys) to get an idea of
        what are available to use in your sql template.

        See also `usage examples <usage.html#sql-with-individual-clauses>`__.

        :param dbmap: to map to the actual db field name (optionally with alias) when generating "where_condition"
        :return: the dict
        """
        kwargs = {}
        kwargs["where_condition"] = self.to_sql_where_condition(dbmap)
        kwargs["condition"] = self
        kwargs.update(self.params)
        return kwargs

    def to_df_query(self) -> str:
        """
        :return: a string representing the condition to be used in df.query()
        """
        return self.apply(DataFrameApplication())

    def query(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Queries the passed in dataframe with this condition.

        :param df: the dataframe to perform query. Each field in the condition must match a columns
            or an index level in the data frame.
        :return: a dataframe whose rows satisfy this condition.
        """
        if self == EMPTY_CONDITION:
            return df
        else:
            return df.query(self.to_df_query())

    @staticmethod
    def from_pyarrow_filter(
        filters: Optional[Union[List[Tuple], List[List[Tuple]]]] = None
    ) -> Condition:
        """
        Constructs a condition from pyarrow style filters.

        :param filters: pyarrow filters. See `pyarrow_read_table <https://arrow.apache.org/docs/python/generated/pyarrow.parquet.read_table.html>`_ .
        """
        if not filters:
            return None
        if isinstance(filters, list):
            if isinstance(filters[0], list):
                if any([not isinstance(f, list) for f in filters]):
                    raise ValueError(
                        "All the items of the filters must be a list if one item is a list"
                    )
                return Or([Condition.from_pyarrow_filter(f) for f in filters])
            else:
                if len(filters) > 1:
                    return And([Condition.from_pyarrow_filter(f) for f in filters])
                else:
                    return Condition.from_pyarrow_filter(filters[0])
        else:
            assert len(filters) == 3 and type(filters) == tuple
            f, op, val = filters
            f = Field(f)
            if op in ("=", "==", "in"):
                return f == val
            elif op in ("!=", "not in"):
                return f != val
            elif op == "<":
                return f < val
            elif op == "<=":
                return f <= val
            elif op == ">":
                return f > val
            elif op == ">=":
                return f >= val
            else:
                raise ValueError(f"Not supported operator {op}")

    def eval(self, record_dict: Dict, type_conversion: bool = False) -> bool:
        """
        Evaluates the condition against the record to a bool of True of False.
        Note that if you have a large number of records, the recommended way to evaluate all
        of them in batch mode is to create a pandas DataFrame from the records and then call
        ``condition.query(df)``. You can install ``numexpr`` package for much faster performance.

        :param record_dict: a dict from a field to a value. Used to test ``FieldCondition``.
        :param type_conversion: if True, convert value in record_dict to the ``FieldCondition``
                                value type before comparision. Sometimes such conversion
                                is needed, for example, in pyarrow partition filtering.
        """
        ea = EvalApplication()
        return self.apply(ea, record_dict=record_dict, type_conversion=type_conversion)

    def normalize(self) -> Condition:
        """
        Normalizes the condition to be one of the following:

        - a ``FieldCondition``
        - an ``And`` with a list of sub ``FieldCondition``
        - an ``Or`` with a list of sub conditions as defined above.

        In some cases, e.g., pyarrow filtering, the above restrictions must be followed.
        Any condition can be normalized to the above form in an equalivent way.

        For example, ``(a | b) & (c | d) & e`` will be normalized to
        ``(a & c & e) | (a & d & e) | (b & c & e) | (b & d& e)``.

        :return: an equivalent normalized condition.
        """
        if isinstance(self, FieldCondition):
            return self
        subs = [sub.normalize() for sub in self.conditions]
        if isinstance(self, Or):
            return Or(subs)
        # And: sub can be: FieldConditions, And, Or
        or_list = []
        field_list = []
        for sub in subs:
            if isinstance(sub, FieldCondition):
                field_list.append(sub)
            elif isinstance(sub, And):
                field_list.extend(sub.conditions)
            else:
                or_list.append(sub.conditions)
        if not or_list:
            return And(field_list)
        # all field_list as an Or with only one node
        or_list.append([And(field_list)])
        or_list2 = []
        for ands in product(*or_list):
            or_list2.append(And(ands))
        return Or(or_list2)

    def to_pyarrow_filter(self) -> Union[List[Tuple], List[List[Tuple]]]:
        """
        Generates filters that can be passed to ``pyarrow.parquet.ParquetDataset`` or ``pandas.read_parquet``
        in order to read only the selected partitions, thereby increase efficiency.
        Please note that the field conditions not matching a partition key will be
        ignored, so you should follow up
        with ``condition.query(df)`` to filter out unnecessary rows.

        See also `usage examples <usage.html#pyarrow-partition-filtering>`__.
        """
        pa = PyarrowFilterApplication()
        return self.apply(pa)

    def _date_val(self, dt: Union[str, datetime], date_format: str) -> datetime:
        dt = pd.to_datetime(dt)
        return dt.strftime(date_format) if date_format else dt

    def add_date_condition(
        self,
        date_field: Field,
        from_date: Optional[Union[str, datetime]] = None,
        to_date: Optional[Union[str, datetime]] = None,
        to_exclusive: Optional[bool] = False,
        date_format: Optional[str] = None,
    ) -> Condition:
        """
        Adds to this condition that the date field should be between the passed in date range.
        This is a convenient method for working with time series.

        :param date_field: the date field
        :param from_date: if not None, the date field must be greater than or equal to this datetime value
        :param to_date: if not None, the date field must be less than this datetime value
        :param to_exclusive: if False, the date field can be equal to the ``to_date``
        :param date_format: the date_format to convert the date to a str. The default is None so not to convert.
        """

        list = [self]
        if from_date:
            list.append(date_field >= self._date_val(from_date, date_format))
        if to_date:
            if to_exclusive:
                list.append(date_field < self._date_val(to_date, date_format))
            else:
                list.append(date_field <= self._date_val(to_date, date_format))

        return And(list)

    def add_daterange_overlap_condition(
        self,
        from_date_field: Optional[Field] = None,
        to_date_field: Optional[Field] = None,
        from_date: Optional[Union[str, datetime]] = None,
        to_date: Optional[Union[str, datetime]] = None,
        to_exclusive: Optional[bool] = False,
        date_format: Optional[str] = None,
    ) -> Condition:
        """
        Adds to this condition that the two date fields must overlap with the passed in date range.
        This is a convenient method for working with time series.

        :param from_date_field: the from date field
        :param to_date_field: the to date field
        :param from_date: if not None, the ``to_date_field`` must be greater than or equal to this datetime value
        :param to_date: if not None, the ``from_date_field`` must be less than this datetime value
        :param to_exclusive: if False, the ``from_date_field`` can be equal to the ``to_date``
        :param date_format: the date_format to convert the date to a str. The default is None so not to convert.
        """
        list = [self]
        if from_date:
            if not to_date_field:
                raise ValueError("Need to_date_field when from_date != None")
            list.append(to_date_field >= self._date_val(from_date, date_format))
        if to_date:
            if not from_date_field:
                raise ValueError("Need from_date_field when to_date != None")
            if to_exclusive:
                list.append(from_date_field < self._date_val(to_date, date_format))
            else:
                list.append(from_date_field <= self._date_val(to_date, date_format))
        return And(list)

    def visualize(self, filename=None, view: bool = False) -> Any:
        """
        Visualizes this condition structure with a 'png' image.
        This method requires ``graphviz`` package available.

        :param filename: the path to output the 'png' file.
        :param view: if True, show the picture
        """
        va = VisualizeApplication()
        return self.apply(va, filename=filename, view=view)

    def split(
        self,
        fields: Union[str, Field, FieldList, Collection[Union[str, Field]]],
        field_map: Union[Dict[str, str], Dict[Field, Field]] = None,
    ) -> Condition:
        """
        Splits the condition to a new condition which only contains the passed in fields.
        This method is used in the following scenario:

        #. A combined data item is joined from two or more sub data sources.
        #. The condition is defined on the combined data.
        #. Use this method to get a split condition to be applied to the sub data sources with the fields list in the sub data sources.
        #. There may be a field mapping from this condition to the target sub data sources. If so, the split will be mapped to the target fields.
        #. After the data is joined, apply the original condition on the combined data.

        :param fields: a ``FieldList`` or a collection of target fields (str or ``Field``) to retain.
        :param field_map: map from a field in this condition to the target field. If None, keep the
                field name.
        :return: the condition to be applied for a data source with only the passed in fields.
                Returns ``None`` if no condition should be applied, namely, assuming True for each row.
        """
        if isinstance(fields, FieldList):
            fields = fields.fields
        elif not isinstance(fields, Collection):
            fields = [str(fields)]
        field_set = {str(f) for f in fields}
        cond = copy.deepcopy(self)

        empty_cond = EMPTY_CONDITION
        # ensure key and value are both str
        field_map = {str(k): str(v) for k, v in field_map.items()} if field_map else {}

        @lru_cache()
        def _split(c):
            # note in this context, empty_cond means "True"
            if isinstance(c, FieldCondition):
                field_str = str(c.field)
                if field_str in field_map:
                    field_str = field_map[field_str]
                    return (
                        FieldCondition(Field(field_str), c.op, c.val)
                        if field_str in field_set
                        else empty_cond
                    )
                return c if field_str in field_set else empty_cond

            # for a CompositeCondition
            conds = OrderedSet()
            for cc in c.conditions:
                c1 = _split(cc)
                if c1 == empty_cond:
                    if isinstance(c, Or):
                        # in 'Or', if any sub is empty_cond(meaning True), return empty_cond
                        return c1
                else:
                    conds.add(c1)
            if len(conds) == 0:
                return empty_cond
            elif len(conds) == 1:
                return conds.pop()
            else:
                c.conditions = conds
                return c

        return _split(cond)

    @staticmethod
    def parse(
        condition_str: str, field_list: FieldList = None, field_list_name: str = "fl"
    ) -> Condition:
        """
        Parses a str to be a condition object. The parse method is safe in that no irrelvant
        function/class can be called in the string.  The ``T()`` is a shortcut of ``pd.to_datetime()``
        to convert a string to a datetime.

        Examples:
        Below, cond1, cond2 and cond3 are equivalent.

        >>> fl = FieldList(['A', 'B', 'C'])
        >>> cond1 = Condition.parse("(fl.A>T('20000101')) & (fl.B==['b1', 'b2'])  & (fl.C>=100)")
        >>> cond2 = Condition.parse("And([fl.A>T('20000101'), fl.B==['b1', 'b2'], fl.C>=100])")
        >>> cond3 = Condition.parse(repr(cond1))

        :param condition_str: the string contains condition expression.
        :param field_list: the ``FieldList`` object. If None, look up from the caller's context.
        :param field_list_name: the field list name used in ``condition_str`` parameter. Default to 'fl'.
        """

        if field_list is None:
            caller_locals = inspect.stack()[1].frame.f_locals
            if field_list_name in caller_locals:
                field_list = caller_locals[field_list_name]
            else:
                caller_globals = inspect.stack()[1].frame.f_globals
                if field_list_name in caller_globals:
                    field_list = caller_globals[field_list_name]
                else:
                    raise ValueError(
                        f"{field_list_name} does not exist in the caller's context."
                    )
        T = lambda s: pd.to_datetime(s)
        assert isinstance(
            field_list, FieldList
        ), f"Expect a FieldList, but get {type(field_list)}"
        safe_dict = {
            "T": T,
            field_list_name: field_list,
            "And": And,
            "Or": Or,
            "None": None,
        }
        try:
            return eval(condition_str, {"__builtins__": None}, safe_dict)
        except TypeError as e:
            raise RuntimeError(
                "There is a parsing error. Make sure you only have valid condition content. "
                "No unsafe reference is allowed."
            )


class FieldCondition(Condition):
    def __init__(self, field: Field, op: Operator, val: Any):
        """
        A condition which compares a field with a value or tests if a field in/not in a set of values.
        """
        super().__init__()
        self.field = field
        self.op = op
        self.val = val
        self._hashcode = None
        if (
            op not in (Operator.IN, Operator.NOT_IN)
            and not isinstance(val, str)
            and (isinstance(val, Collection))
        ):
            raise ValueError("Op '%s' not supported with a collection value", op)

    def _apply_recursively(self, application: ConditionApplication, **kwargs):
        return application.applyFieldCondition(self, **kwargs)

    def _query_val(self, repr=False) -> str:
        """
        Formats the val for sql query.
        """

        def _val(val):
            if isinstance(val, str):
                return "'" + val + "'"
            elif isinstance(val, datetime):
                s = "'" + str(val) + "'"
                if repr:
                    s = "T(" + s + ")"
                return s
            elif isinstance(val, Iterable):
                return "(" + ",".join([_val(v) for v in val]) + ")"
            else:
                return str(val)

        return _val(self.val)

    def __str__(self) -> str:
        return f"{self.field} {self.op.value} {self._query_val()}"

    def __repr__(self) -> str:
        op_str = self.op.value
        if self.op == Operator.IN:
            op_str = "=="
        elif self.op == Operator.NOT_IN:
            op_str = Operator.NEQ.value
        field = self.field.name
        field = f"fl.{field}" if field.isidentifier() else f'fl["{field}"]'
        return f"{field} {op_str} {self._query_val(True)}"

    def __eq__(self, other: Any) -> bool:
        return (
            other
            and isinstance(other, FieldCondition)
            and self.field.name == other.field.name
            and self.op == other.op
            and self.val == other.val
        )

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        if not self._hashcode:
            self._hashcode = (hash(self.field) * 31 + hash(self.op)) * 31 + hash(
                self.val
            )
        return self._hashcode


class CompositeCondition(Condition, ABC):
    def __init__(self, conditions: Optional[List[Condition]] = None):
        super().__init__()
        self.conditions: OrderedSet[Condition] = OrderedSet()
        self._hash_code = None

        def _add(sub: Condition):
            if not isinstance(sub, Condition):
                raise ValueError(
                    f"Expect a Condition object. Got a {type(sub)}. "
                    'You may need to enclose the condition in "()".'
                )
            if sub is None or sub == EMPTY_CONDITION:
                return
            if isinstance(sub, type(self)):  # flatten it.
                for c in sub.conditions:
                    # flatten the sub conditions
                    _add(c)
            else:
                self.conditions.add(sub)

        if conditions:
            for c in conditions:
                _add(c)
        self.conditions.freeze()

    def __str__(self) -> str:
        return self.to_sql_where_condition()

    def apply_to_subs(self, application: ConditionApplication, **kwargs):
        return [
            sub._apply_recursively(application, **kwargs) for sub in self.conditions
        ]

    def __repr__(self) -> str:
        if self.conditions:
            name = self.__class__.__name__  # self.class.name
            return name + "([" + ", ".join([repr(c) for c in self.conditions]) + "])"
        return ""

    def __eq__(self, other: Any) -> bool:
        return (
            other
            and isinstance(other, self.__class__)
            and self.conditions == other.conditions
        )

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        if not self._hash_code:
            self._hash_code = hash(self.conditions)
        return self._hash_code


class And(CompositeCondition):
    """
    An 'and' condition composed of a list of sub conditions.
    Usage examples:

        >>> fl = FieldList(['f1', 'f2', 'f3'])
        >>> condition = And ([
        ...            fl.f1 <= 300,
        ...            fl.f2 > pd.to_datetime('20000101'),
        ...            fl.f3 == (['val1', 'val2'])
        ...         ])

    Alternatively, it can be created as follows:

        >>> condition2 = (fl.f1 <= 300) & (fl.f2 > pd.to_datetime('20000101')) & (fl.f3 == (['val1', 'val2']))
    """

    def _apply_recursively(self, application: ConditionApplication, **kwargs):
        if self == EMPTY_CONDITION:
            return application.applyEmptyCondition(self, **kwargs)
        return application.applyAndCondition(self, **kwargs)


class Or(CompositeCondition):
    """
    An 'or' condition composed of a list of sub conditions.
    Usage examples:

        >>> fl = FieldList(['f1', 'f2', 'f3'])
        >>> condition = Or([fl.f1 <= 300,
        ...     fl.f2 > pd.to_datetime('20000101'),
        ...     fl.f3 == (['val1', 'val2'])])
        >>> condition2 = ((fl.f1 <= 300)
        ...     | (fl.f2 > pd.to_datetime('20000101'))
        ...     | (fl.f3 == (['val1', 'val2'])))
    """

    def _apply_recursively(self, application: ConditionApplication, **kwargs):
        return application.applyOrCondition(self, **kwargs)


EMPTY_CONDITION = And()  # treated as True


def get_test_df() -> pd.DataFrame:
    """Generates a dataframe for testing."""
    col_A = [f"a{i + 1}" for i in range(5)]
    col_B = [f"b{i + 1}" for i in range(5)]
    col_C = [f"c{i + 1}" for i in range(5)]
    dr = pd.date_range("2000-01-01", "2000-03-31")
    index = pd.MultiIndex.from_product(
        [dr, col_A, col_B, col_C], names="date A B C".split()
    )
    df = pd.DataFrame(
        data=np.random.randn(index.shape[0], 1), index=index, columns=["value"]
    )
    return df


class DataFrameApplication(ConditionApplication):
    def applyFieldCondition(self, cond: FieldCondition):
        field = cond.field.name
        val = cond._query_val()
        op = cond.op.value
        if op == "=":
            op = "=="
        if not field.isidentifier():
            field = f"`{field}`"
        return f"({field} {op} {val})"

    def applyAndCondition(self, cond: And):
        return "(" + "&".join(cond.apply_to_subs(self)) + ")"

    def applyOrCondition(self, cond: Or):
        return "(" + "|".join(cond.apply_to_subs(self)) + ")"


class VisualizeApplication(ConditionApplication):
    # global constants and func for visualization
    FIELD_COND_COLOR = "white"
    AND_COLOR = "floralwhite"
    OR_COLOR = None

    def next_id(self) -> str:
        self.id += 1
        return str(self.id)

    def on_start(self, cond, filename=None, view: bool = False):
        self.id = 0
        try:
            from graphviz import Digraph

            digraph_name = filename
            if digraph_name is None:
                digraph_name = f"Condition-" + tempfile.mktemp()
            digraph = Digraph(digraph_name, format="png")
        except:
            raise NotImplementedError(
                "visualize() method needs graphviz package. Please install it first."
            )
        id_dict = {}
        # initialize and add additional kwargs to be used
        return dict(
            filename=filename, view=view, id_dict=id_dict, digraph=digraph, parent=None
        )

    def _add_to_digraph(
        self, cond, id_dict, digraph, label, color, shape, parent
    ) -> bool:
        if not cond in id_dict:
            id = self.next_id()
            id_dict[cond] = id
            digraph.node(
                id,
                label=label,
                style="rounded, filled",
                fillcolor=color,
                fontname="helvetica",
                fontsize="12.0",
                shape=shape,
            )
            new_node = True
        else:
            id = id_dict[cond]
            new_node = False
        if parent:
            digraph.edge(parent, id)

        return new_node

    def applyFieldCondition(
        self, cond: FieldCondition, id_dict, digraph, parent, **kwargs
    ):
        self._add_to_digraph(
            cond,
            id_dict,
            digraph,
            label=cond.to_sql_where_condition(),
            color=self.FIELD_COND_COLOR,
            shape="box",
            parent=parent,
        )

    def _visualize_composite(
        self, cond, id_dict, color, label, digraph, parent
    ) -> None:
        new_node = self._add_to_digraph(
            cond,
            id_dict,
            digraph,
            label=label,
            color=color,
            parent=parent,
            shape="ellipse",
        )
        if new_node:
            id = id_dict[cond]
            cond.apply_to_subs(self, id_dict=id_dict, digraph=digraph, parent=id)

    def applyAndCondition(self, cond: And, id_dict, digraph, parent, **kwargs):
        self._visualize_composite(
            cond,
            color=self.AND_COLOR,
            label="And",
            id_dict=id_dict,
            digraph=digraph,
            parent=parent,
        )

    def applyOrCondition(self, cond: Or, id_dict, digraph, parent, **kwargs):
        self._visualize_composite(
            cond,
            color=self.OR_COLOR,
            label="Or",
            id_dict=id_dict,
            digraph=digraph,
            parent=parent,
        )

    def on_end(self, cond, result, filename, view, digraph, **kwargs):
        if filename or view:
            digraph.render(filename, view=view)
        return digraph


class SqlWhereApplication(ConditionApplication):
    def applyFieldCondition(
        self, cond, db_map: Optional[Dict[str, str]] = None, indent: int = 1
    ) -> str:
        if db_map and cond.field.name in db_map:
            field = db_map[cond.field.name]
            not_mapped = False
        else:
            field = cond.field.name
            not_mapped = True

        val = cond._query_val()
        op = cond.op.value
        if op == "==":
            op = "="
        if not field.isidentifier() and not_mapped:
            LEFT = os.getenv("SQL_ID_DELIM_LEFT", '"')
            RIGHT = os.getenv("SQL_ID_DELIM_RIGHT", '"')
            field = LEFT + field + RIGHT
        return f"{field} {op} {val}"

    def _to_sql_where_condition_composite(
        self,
        cond: CompositeCondition,
        op_str: str,
        db_map: Dict[str, str] = None,
        indent: int = 1,
    ) -> str:
        indents = "\n" + "\t" * indent

        sep = indents + op_str + " "
        return (
            indents
            + "("
            + sep.join(cond.apply_to_subs(self, db_map=db_map, indent=indent + 1))
            + ")"
        )

    def applyAndCondition(
        self, cond: And, db_map: Optional[Dict[str, str]] = None, indent: int = 1
    ) -> str:
        return self._to_sql_where_condition_composite(cond, "and", db_map, indent)

    def applyOrCondition(
        self, cond: Or, db_map: Optional[Dict[str, str]] = None, indent: int = 1
    ) -> str:
        return self._to_sql_where_condition_composite(cond, "or", db_map, indent)

    def applyEmptyCondition(
        self, cond, db_map: Optional[Dict[str, str]] = None, indent: int = 1
    ):
        indents = "\n" + "\t" * indent
        return indents + "1=1"


class PyarrowFilterApplication(ConditionApplication):
    def on_start(self, cond):
        cond = cond.normalize()
        # replace the current condition with its normalized version.
        return dict(cond=cond)

    def applyFieldCondition(self, cond: FieldCondition, use_list: bool = True):
        def _val(v):
            # convert datetime to a pd.Timestamp. Otherwise, pyarrow may throw
            # an error.
            return pd.to_datetime(v) if isinstance(v, datetime) else v

        if not isinstance(cond.val, str) and isinstance(cond.val, Iterable):
            val = {_val(v) for v in cond.val}
        else:
            val = _val(cond.val)
        val = (cond.field.name, cond.op.value, val)
        return [val] if use_list else val

    def applyAndCondition(self, cond: And, use_list: bool = False) -> str:
        return cond.apply_to_subs(self, use_list=False)

    def applyOrCondition(self, cond: Or, use_list: bool = False) -> str:
        return cond.apply_to_subs(self, use_list=True)


class EvalApplication(ConditionApplication):
    def applyFieldCondition(
        self,
        cond: FieldCondition,
        record_dict: Dict[str, Any],
        type_conversion: bool = False,
    ) -> bool:
        f, op, op_val = cond.field.name, cond.op, cond.val
        if f not in record_dict:
            return True
        data = record_dict[f]
        if type_conversion:
            op_type = type(op_val)
            if op in {Operator.IN, Operator.NOT_IN}:
                op_type = type(next(iter(op_val)))
            data = op_type(data)

        if op == Operator.EQ:
            return data == op_val
        if op == Operator.NEQ:
            return data != op_val
        if op == Operator.GE:
            return data >= op_val
        if op == Operator.GT:
            return data > op_val
        if op == Operator.LE:
            return data <= op_val
        if op == Operator.LT:
            return data < op_val
        if op == Operator.IN:
            return data in op_val
        if op == Operator.NOT_IN:
            return data not in op_val

        raise NotImplementedError(f"op: {op.value} Not possible to reach here")

    def applyAndCondition(
        self, cond: And, record_dict: Dict[str, Any], type_conversion: bool = False
    ) -> bool:
        return all(
            cond.apply_to_subs(
                self, record_dict=record_dict, type_conversion=type_conversion
            )
        )

    def applyOrCondition(
        self, cond: Or, record_dict: Dict[str, Any], type_conversion: bool = False
    ) -> bool:
        return any(
            cond.apply_to_subs(
                self, record_dict=record_dict, type_conversion=type_conversion
            )
        )
