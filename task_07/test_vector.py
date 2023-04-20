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




if __name__ == '__main__':
    test_equality()
    test_bool()
    vec = Vector(3, 5)
    oth = Vector(10, 20)

      # returns False

    res = vec * 3 + oth / 10

    diag = Vector.from_polar(length=10, angle=45, isdeg=True)

    one = Vector.from_polar(1, 45)
    two = Vector.from_polar(10, 135)

    angle = Vector.angle_between(one, two)
