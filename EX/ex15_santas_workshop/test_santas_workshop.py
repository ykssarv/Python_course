"""Test."""

from santas_workshop import Main, Toy, Sledge


def test_toy_creation():
    """Test."""
    toy = Toy('Crayons')
    assert toy.material_cost == 5
    assert toy.production_time == 1
    assert toy.weight_in_grams == 50


def test_read_nice_list():
    """Test."""
    main = Main()
    main.read_nice_list()
    assert len(main.nice_kids.keys()) == 291
    assert "Elle" in main.nice_kids.keys()
    assert "Australia" == main.nice_kids["Elle"].habitat


def test_read_naughty_list():
    """Test."""
    main = Main()
    main.read_naughty_list()
    assert len(main.naughty_kids.keys()) == 108
    assert "Mel" in main.naughty_kids.keys()
    assert "Sweden" == main.naughty_kids["Mel"].habitat


def test_read_information():
    """Test."""
    main = Main()
    main.read_information()
    assert "Crayons" in main.toys.keys()
    assert "Crayons" in main.nice_kids["Rhys"].wishes


def test_sledge_has_room():
    """Test."""
    sledge = Sledge("Estonia", 0)
    assert sledge.has_room(Toy("Crayons"))


def test_sledge_file_creation():
    """Test."""
    sledge = Sledge("Estonia", 0)
    sledge.add_toy(Toy("Crayons"), "Joosep")
    sledge.generate_file()
    lines = open("Estonia0.txt", "r").readlines()
    assert "Estonia" in lines[2]
    assert "||  Name  ||  Gifts  || Total Weight(kg) ||\n" in lines
    assert "|| Joosep || Crayons ||             0.05 ||\n" in lines


def test_country_sledge_making():
    """Test."""
    main = Main()
    main.read_information()
    main.distribute_gifts()
    assert "Estonia" in main.countries.keys()
    estonia = main.countries["Estonia"]
    assert len(estonia.sledges) == 2
    sledge = estonia.sledges[0]
    assert sledge.total_weight == 49954


def test_adding_toy_increases_sledge_weight():
    """Test."""
    sledge = Sledge("Estonia", 1)
    assert sledge.total_weight == 0
    sledge.add_toy(Toy("Crayons"), "Joosep")
    assert sledge.total_weight == 50
