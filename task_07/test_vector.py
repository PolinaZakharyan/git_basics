#! /usr/bin/env python3

from vector import Vector


def test_equality():
    a = Vector(2, 3)
    b = Vector(2, 3)
    c = Vector(4, 5)
    assert a == b
    assert a != c

def test_bool():
    assert not bool(Vector(0, 0))
    assert bool(Vector(1, 1))
    assert bool(Vector(-1, -1))

def test_add():
    vecsum = Vector(1, 1) + Vector(2, 2)
    assert vecsum == Vector(3, 3)
    assert (Vector(1, 1) - Vector(2, 2)) == Vector(-1, -1)

def test_mul():
    assert (Vector(1, 1) * Vector(2, 2)) == 4
    assert (Vector(1, 1) * 0.5) == Vector(0.5, 0.5)
    assert (Vector(1, 1) / 2) == Vector(.5, .5)

def test_cross():

    # collinear
    a=Vector(3,-3,1)
    b=Vector(-12,12,-4)
    assert (a @ b) == Vector(0)




if __name__ == '__main__':
    test_equality()
    test_bool()
    test_add()
    test_mul()
    test_cross()

    vec = Vector(3, 5)
    oth = Vector(10, 20)

    res = vec * 3 + oth / 10

    diag = Vector.from_polar(length=10, angle=45, isdeg=True)

    one = Vector.from_polar(1, 45)
    two = Vector.from_polar(10, 135)

    angle = Vector.angle_between(one, two)
