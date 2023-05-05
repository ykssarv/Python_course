import pytest
from secret_garden import Decoder, SecretGarden

filename = 'pr08_example_data.txt'
key = 'Fat Chocobo'

def test_decode():
    d = Decoder(filename, key)

    assert len(d.decode()) == 7
    assert d.decode()[0] == '-12;-1\n\nESS'
    assert d.decode()[1] == '19;-14\n\nNEWNESSEWN'

def test_find_secret_village():
    garden = SecretGarden(filename, key)

    assert garden.find_secret_locations() == [(-11, -3), (20, -13), (1, -3), (-2, -5), (10, 4), (6, -13), (2, -6)]