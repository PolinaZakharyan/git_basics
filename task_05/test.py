#! /usr/bin/env python3

from dict_set import *

def demo_operations(*args: dict):

    print("demo_operations, test dicts:\n", args)
    print("  intersection:         ", intersection(*args))
    print("  union:                ", union(*args))
    print("  difference:           ", difference(*args))
    print("  symmetric_difference: ", symmetric_difference(*args))

def demo_relation(l, r):
    print("demo_relation, test dicts:\n", l, r)
    print("  isequivalent:       ", isequivalent(l, r))
    print("  issubset:           ", issubset(l, r))
    print("  issuperset:         ", issuperset(l, r))
    print("  is_proper_subset:   ", is_proper_subset(l, r))
    print("  is_proper_superset: ", is_proper_superset(l, r))


if __name__ == "__main__":
    a = {'a':  1, 'b': 2}
    b = {'a':  2, 'b': 3, 'c': 3}
    c = {'a': 42, 'c': 4, 'd': 5}
    demo_operations(a,b,c)
    demo_relation(a,a)
    demo_relation(a,b)
    demo_relation(b,a)
