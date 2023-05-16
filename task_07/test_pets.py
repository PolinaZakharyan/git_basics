from pets import *

def test_init_objects():
    x = Cat(13, 'Lolo')
    y = Cat(14, 'Toto')
    z = Wolf(42)
    a = Dog(15, 'Tobi')
    b = Bird(0.2, 'Kesha')
    PetOwner('Bob')
    PetOwner('Alice', OwnedPets([x, y, a, b]))

    z = Wolf(42)
    try:
        OwnedPets([z])
        assert False, "OwnedPets initialized with non-Pet object didnt fail as expected"
    except TypeError:
        pass

    print('Test_init_objects passed')

def test_teach():
    x = Cat(13, 'Lolo')
    assert x.hi() in x.sounds
    x.teach('nyam')
    assert 'nyam' in x.sounds
    for _ in range(10):
        assert x.hi() in x.sounds

    print('test_teach passed')

def test_OwnedPets():
    x = Cat(13, 'Lolo')
    y = Cat(14, 'Toto')
    a = Dog(15, 'Tobi')
    b = Bird(0.2, 'Kesha')
    pets1 = OwnedPets([x, a, b])
    pets2 = OwnedPets([y, b])

    assert (pets1 | pets2) == OwnedPets([x, y, a, b])
    assert (pets1 & pets2) == OwnedPets([b])
    assert (pets1 - pets2) == OwnedPets([x, a])
    assert (pets1 ^ pets2) == OwnedPets([x, y, a])

    pets1.add(y)
    assert y in pets1
    pets1.discard(y)
    assert y not in pets1
    pets1.clear()
    assert len(pets1) == 0
    print('test_OwnedPets passed')





if __name__ == '__main__':
    test_init_objects()
    test_teach()
    test_OwnedPets()
