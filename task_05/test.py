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


def test_01(A: dict, B: dict) -> bool:
    """
    Test expression (A \ B) U (B \ A) = A xor B
    """
    msg = f'Test "(A \ B) U (B \ A) = A xor B" %s for A = {A}, B = {B}'
    assert isequivalent(union(difference(A, B), difference(B, A)), symmetric_difference(A, B)), (msg % "failed")
    print(msg % "passed")

def test_02(A: dict, B: dict) -> bool:
    """
    Test expression (A \ B) U (A and B) = A
    """
    msg = f'Test "(A \ B) U (A and B) = A" %s for A = {A}, B = {B}'
    assert isequivalent(union(difference(A, B),intersection(A, B)), A), (msg % "failed")
    print(msg % "passed")

def test_03(A: dict, B: dict) -> bool:
    """
    Test expression (A xor B) U (A and B) = A U B
    """
    msg = f'Test "(A xor B) U (A and B) = A U B" %s for A = {A}, B = {B}'
    assert isequivalent(union(symmetric_difference(A, B),intersection(A, B)), union(A, B)), (msg % "failed")
    print(msg % "passed")

def test_04(A: dict, B: dict):
    """
    Test De Morgan's law on artificial universe
    not (A or B) = (not A) and (not B)
    not (A and B) = (not A) or (not B)
    """

    # make artificial universe
    U = set("abcdefghijklmnopqrstuvwxyz0123456789") | set(A.keys()) | set(B.keys())
    U = { k: None for k in U }

    def complement(x: dict):
        return difference(U, x)

    msg = f"De Morgan's law test on artificial universe %s for A = {A}, B = {B}"
    assert isequivalent(complement(union(A, B)), intersection((complement(A)), complement(B))), (msg % "failed")
    assert isequivalent(complement(intersection(A, B)), union((complement(A)), complement(B))), (msg % "failed")
    print(msg % "passed")




if __name__ == "__main__":
    a = {'a':  1, 'b': 2}
    b = {'a':  2, 'b': 3, 'c': 3}
    c = {'a': 42, 'c': 4, 'd': 5}

    print("Demo:")
    demo_operations(a,b,c)
    demo_relation(a,a)
    demo_relation(a,b)
    demo_relation(b,a)

    print("Tests:")
    test_01(a,b)
    test_01(a,c)
    test_01(b,c)

    test_02(a,b)
    test_02(a,c)
    test_02(b,c)

    test_03(a,b)
    test_03(a,c)
    test_03(b,c)

    test_04(a,b)
    test_04(a,c)
    test_04(b,c)
