# union
# intersection
# difference
# symmetric_difference
# issubset
# issuperset
# isdisjoint

def union(*args: dict) -> dict:
    return { k: v for d in args for k, v in d.items() }

def intersection(*args: dict) -> dict:
    if 0 == len(args):
        return {}
    keys = set(args[0].keys())
    for d in args[1:]:
        keys &= set(d.keys())
    return {k: args[-1][k] for k in keys}

def difference(*args: dict) -> dict:
    if 0 == len(args):
        return {}
    exclude = { k for d in args[1:] for k in d.keys() }
    return { k: v for k, v in args[0].items() if k not in exclude }

def symmetric_difference(*args: dict) -> dict:
    if 0 == len(args):
        return {}
    class ToExclude: pass
    alldata = {}
    for d in args:
        for k, v in d.items():
            alldata[k] = ToExclude if k in alldata else v

    return { k: v for k, v in alldata.items() if v != ToExclude }

def print_test(*args: dict):

    print("test dicts: ", args)
    print("  intersection:         ", intersection(*args))
    print("  union:                ", union(*args))
    print("  difference:           ", difference(*args))
    print("  symmetric_difference: ", symmetric_difference(*args))

if __name__ == "__main__":
    a = {'a':  1, 'b': 2}
    b = {'a':  2, 'c': 3, 'd': 3}
    c = {'a': 42, 'c': 4, 'e': 5}
    print_test(a,b,c)
