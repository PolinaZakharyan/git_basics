from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar
from random import randrange

class FeedingBehavior(Enum):
    Omnivorous = auto()
    Carnivorous = auto()
    Herbivorous = auto()

@dataclass
class Animal:
    behavior: ClassVar[FeedingBehavior] = FeedingBehavior.Omnivorous
    weight: float

    def __post_init__(self):
        self.sounds = self.sounds[:] if hasattr(self, "sounds") else []

    def describe(self) -> str:
        return f"{self}, {self.behavior.name}, make sounds: {', '.join(self.sounds)}"

    def hi(self):
        print(self.sounds[randrange(len(self.sounds))])


@dataclass
class Pet(Animal):
    name: str

    def teach(self, word):
        self.sounds.append(word)


#######

@dataclass
class Cat(Pet):
    sounds = ["meow"]

class Dog(Pet):
    sounds = ['Woof', 'Ruff']


@dataclass
class Wolf(Animal):
    behavior = FeedingBehavior.Carnivorous
    sounds =["Woooo!"]
