import functools
import math
from itertools import zip_longest

class Vector:
    """
    Vector class with dynamic dimensionality.
    In non-uniform binary operations x[n] = 0 for all n >= len(x).
    """
    __slots__ = ('_x')

    def __init__(self, *args):
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            args = args[0]
        self._x = tuple(args)


    @property
    @functools.lru_cache(maxsize=1)
    def magnitude(self):
        return sum(map(lambda x: x ** 2, self._x)) ** 0.5


    @classmethod
    def from_polar(cls, length, angle, *, isdeg=True):
        """Make Vector from polar coordinates (length & angle)

        Args:
            length: vector length as returned by Vector.length
            angle: vector rotation in radians (if `isdeg` is False)
                   or in degrees (if `isdeg` is True or not provided)
            isdeg: angle is given in degrees (if True) or in radians
                   (if False)
        Returns:
            Vector instance
        """
        # do conversion to radians if needed
        if isdeg:
            angle = math.radians(angle)

        x = length * math.cos(angle)
        y = length * math.sin(angle)
        return cls(x, y)

    @staticmethod
    def angle_between(a: 'Vector', b: 'Vector', isdeg=True):
        angle = math.acos(Vector.dot_product(a, b) / (a.magnitude * b.magnitude))

        if isdeg:
            angle = math.degrees(angle)
        return angle

    def __repr__(self):
        clsname = self.__class__.__name__
        return f"{clsname}({', '.join(self._x)})"

    def __bool__(self):
        return bool(functools.reduce(lambda x, y: x & y, self._x, 1))

    def __add__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(f'operands {self} and {other} type mismatch')

        return type(self)(ax + bx for ax, bx in zip_longest(self._x, other._x, fillvalue=0))

    def __sub__(self, other):
        return self + (other * -1)  # call mul explicitly

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        try:
            return self.__mul__(1 / other)
        except:
            raise TypeError('unsupported operation')

    def __rdiv__(self, other):
        raise TypeError('unsupported operation')

    def scalar_product(self, scalar):
        if not isinstance(scalar, int):
            scalar = float(scalar)
        return type(self)(scalar * x for x in self._x)

    def dot_product(self, other):
        return sum(ax * bx for ax, bx in zip(self._x, other._x))

    def cross_product(self, other):

        if len(self._x) > 3 or len(other._x) > 3:
            raise NotImplementedError('cross product for dim > 3 is not defined')

        a = list(self._x) + [0] * (3 - len(self._x))
        b = list(other._x) + [0] * (3 - len(other._x))

        return Vector(
            a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0]
        )


    def __mul__(self, other):

        if not isinstance(other, type(self)):
            # if has other type
            return self.scalar_product(other)
        return self.dot_product(other)

    def __matmul__(self, other):
        return self.cross_product(other)

    def __truediv__(self, other):
        if not other:
            raise ZeroDivisionError

        return self * (1 / other)

    def __eq__(self, other):
        try:
            for ax, bx in zip_longest(self._x, other._x, fillvalue=0):
                if ax != bx:
                    return False
            return True
        except Exception:
            return False

    # __neq__ is implemented automatically

    def __len__(self):
        return 2

    def __getitem__(self, index):
        return [self.x, self.y][index]

    def __hash__(self):
        # if each object is unique
        # return id(self)
        # if it is not exactly unique and applicable to use
        # other object with same values during indexing
        return hash(self._x)


class Point(Vector):
    pass


