"""
Set operations on dictionaries
"""

def union(*args: dict) -> dict:
    """N-ary dictionary union (set or)

    Repetitive key: last value choosen
    Commutativity: keys only
    Associativity: full
    """
    return { k: v for d in args for k, v in d.items() }

def intersection(*args: dict) -> dict:
    """N-ary dictionary intersection (set and)

    Repetitive key: last value choosen
    Commutativity: keys only
    Associativity: full
    """
    if 0 == len(args):
        return {}
    keys = set(args[0].keys())
    for d in args[1:]:
        keys &= set(d.keys())
    return {k: args[-1][k] for k in keys}

def difference(*args: dict) -> dict:
    """N-ary dictionary difference

    Commutativity: no
    Associativity: full
    """
    if 0 == len(args):
        return {}
    exclude = { k for d in args[1:] for k in d.keys() }
    return { k: v for k, v in args[0].items() if k not in exclude }

def symmetric_difference(*args: dict) -> dict:
    """N-ary dictionary symmetric difference (set xor)

    Commutativity: full
    Associativity: full
    """
    if 0 == len(args):
        return {}

    # unique object to mark the values to delete
    class ToExclude: pass

    alldata = {}
    for d in args:
        for k, v in d.items():
            alldata[k] = ToExclude if k in alldata else v

    return { k: v for k, v in alldata.items() if v != ToExclude }


def isequivalent(lhs: dict, rhs: dict) -> bool:
    """Binary dictionary relation: equality by keys

    Symmetric: yes
    Transitive: yes
    """
    return lhs.keys() == rhs.keys()

def issubset(lhs: dict, rhs: dict) -> bool:
    """Binary dictionary relation: subset by keys

    Symmetric: no
    Transitive: yes
    """
    for k in lhs:
        if k not in rhs:
            return False
    return True

def issuperset(lhs: dict, rhs: dict) -> bool:
    """Binary dictionary relation: superset by keys

    Symmetric: no
    Transitive: yes
    """
    return issubset(rhs, lhs)

def is_proper_subset(lhs: dict, rhs: dict) -> bool:
    """Binary dictionary relation: proper subset by keys

    Symmetric: no
    Transitive: yes
    """
    return not isequivalent(lhs, rhs) and issubset(lhs, rhs)

def is_proper_superset(lhs: dict, rhs: dict) -> bool:
    """Binary dictionary relation: proper superset by keys

    Symmetric: no
    Transitive: yes
    """
    return is_proper_subset(rhs, lhs)

def index(origin: dict) -> dict:
    """Create value index

    Create inverse dictionary { value: set of keys }
    """
    idx = {}
    for k, v in origin.items():
        idx[v] = idx.get(v, set()) | {k}
    return idx

def sorted_dict(origin: dict, by_val=False, reverse=False) -> dict:
    """Sort dictionary

    Options:
    by_val: sort by value, default = False
    reverse: sort in descending order, default = False
    """
    sort_key = 1 if by_val else 0
    return { k: v for k, v in sorted(origin.items(), key = lambda item: item[sort_key], reverse=reverse) }
