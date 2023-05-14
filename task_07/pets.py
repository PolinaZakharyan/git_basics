from dataclasses import dataclass, field
from enum import Enum, auto
from typing import ClassVar, Hashable
from random import randrange
from collections.abc import Iterator
from typing import Iterable

####################
# ABSTRACT ANIMALS #
####################

class FeedingBehavior(Enum):
    Omnivorous = auto()
    Carnivorous = auto()
    Herbivorous = auto()

@dataclass
class Animal(Hashable):
    behavior: ClassVar[FeedingBehavior] = FeedingBehavior.Omnivorous
    weight: float

    def __eq__(self, value: object) -> bool:
        return id(self) == id(value)

    def __hash__(self) -> int:
        return id(self)

    def __post_init__(self):
        self.sounds = self.sounds[:] if hasattr(self, "sounds") else []

    def describe(self) -> str:
        return f"{self}, {self.behavior.name}, make sounds: {', '.join(self.sounds)}"

    def hi(self):
        print(self.sounds[randrange(len(self.sounds))])


@dataclass
class Pet(Animal):
    name: str

    def __hash__(self) -> int:
        return super().__hash__()

    def teach(self, word):
        self.sounds.append(word)

class OwnedPets(set):
    def __init__(self, it: Iterable[Pet] = []) -> None:
        super().__init__(it)

    _wrapped_methods = {
        'copy',

        'union',
        '__or__',  '__ror__',  '__ior__',

        'intersection', 'intersection_update',
        '__and__', '__rand__', '__iand__',

        'difference', 'difference_update',
        '__sub__', '__rsub__', '__isub__',

        'symmetric_difference', 'symmetric_difference_update',
        '__xor__', '__rxor__', '__ixor__',
    }

    @classmethod
    def _wrap_method(cls, fn_name):
        def method(self, *args, **kwargs):
            result = getattr(super(cls, self), fn_name)(*args, **kwargs)
            if isinstance(result, set):
                result = cls(result)
            return result
        method.fn_name = fn_name
        setattr(cls, fn_name, method)

    def __repr__(self):
        return f"OwnedPets({list(self)})"

    def __iter__(self) -> Iterator[Pet]:
        return super().__iter__()

    def filter_by_species(self, species: type):
        return OwnedPets(filter(lambda el: isinstance(el, species), self))

for method in OwnedPets._wrapped_methods:
    OwnedPets._wrap_method(method)

##########
# HUMANS #
##########

@dataclass
class Person:
    name: str

@dataclass
class PetOwner(Person):
    pets: OwnedPets = field(default_factory=lambda: OwnedPets())


###############
# PET SPECIES #
###############

class Cat(Pet):
    sounds = ["meow"]

class Dog(Pet):
    sounds = ['Woof', 'Ruff']

class Bird(Pet):
    sounds = ["chirp"]

class Wolf(Animal):
    behavior = FeedingBehavior.Carnivorous
    sounds =["Woooo!"]

################
# MANUAL TESTS #
################

x = Cat(13, 'Lolo')
y = Cat(14, 'Toto')
z = Wolf(42)
a = Dog(15, 'Tobi')
b = Bird(0.2, 'Kesha')
y.teach('mrrr')

pets = OwnedPets([x,y,a,b])
pers = PetOwner('Bob', pets)
