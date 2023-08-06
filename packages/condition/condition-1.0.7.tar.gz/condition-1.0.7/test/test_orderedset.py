import pytest

from condition.orderedset import OrderedSet


def test_orderedset():
    oset = OrderedSet("abracadaba")
    v = "3234"
    oset.add(v)
    assert v in oset
    assert len(oset) == 6
    assert oset.pop() == v
    oset.clear()
    for c in v:
        oset.add(c)
    oset.discard("fva")
    assert set(oset) == set(list(v))
    assert list(reversed(oset)) == list("423")
    assert repr(oset) == "OrderedSet(['3', '2', '4'])"
    with pytest.raises(RuntimeError):
        hash(oset)
    oset.freeze()
    oset2 = OrderedSet("234")
    oset2.freeze()
    with pytest.raises(RuntimeError):
        oset.add("abc")
    assert hash(oset) != 0
    oset == OrderedSet("423")
    oset != OrderedSet("dfa")
    # eq and hash is order independent.
    oset == oset2
    hash(oset) == hash(oset2)


if __name__ == "__main__":
    pytest.main([__file__])
