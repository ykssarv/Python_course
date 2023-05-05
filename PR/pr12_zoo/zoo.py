"""A small exercise in zookeeping."""
import math


class Animal:
    """Animal."""

    def __init__(self, species: str, scientific_name: str, age_up_to: int, weight_range: tuple, height_range: tuple,
                 diet: str, habitat: str):
        """Initialize the Animal object."""
        self.species = species
        self.scientific_name = scientific_name
        self.age_up_to = age_up_to
        self.weight_range = weight_range
        self.height_range = height_range
        self.diet = diet
        self.habitat = habitat

    def __repr__(self):
        """Animal object representation."""
        return self.species


def find_smallest_animal_by_weight(animal_list: list) -> Animal:
    """
    Find the smallest animal by weight.

    As we want to know the smallest possible option, take the starting value of the weight range as a basis.
    If multiple animals are of the same weight, return the first one in the list.

    :param animal_list: input list of animals
    :return: Animal object
    """
    return min(animal_list, key=lambda x: x.weight_range[0])


def list_species_and_scientific_names(animal_list: list) -> list:
    """
    The zoo needs a list of animals with their scientific names for the public website.

    :param animal_list: input list of animals
    :return: list of tuples, where we have the species name and scientific name
    """
    return list(map(lambda x: (x.species, x.scientific_name), animal_list))


def find_how_many_pumpkins_are_needed_to_feed_animals(animal_list: list) -> int:
    """
    Find how many pumpkins are needed to feed all herbivorous and omnivorous animals in the Zoo.

    For the sake of this calculation, let's assume that there are 2 animals of each type at our zoo and each animal eats
    (on average) 6% of their body weight (average of values in the weight range) worth of pumpkins every day.
    One pumpkin weighs 3kg.
    Let's also assume that we are feeding the animals over the course of one 3-month-long winter (90 days)

    :param animal_list: input list
    :return: amount of pumpkins needed to sustain all the animals over the winter (rounded up).
    """
    return math.ceil(sum(map(lambda x: (x.weight_range[1] + x.weight_range[0]) * 5.4 if x.diet != "carnivorous" else 0, animal_list)) / 3)


def sort_alphabetically_by_scientific_name(animal_list: list) -> list:
    """
    Sort the list of animals alphabetically by scientific name.

    :param animal_list: input list
    :return: sorted list of animals
    """
    return sorted(animal_list, key=lambda x: x.scientific_name)


def find_animals_whose_height_is_less_than(animal_list: list, height_limit: int) -> list:
    """
    Find animals whose height is less than the height limit.

    As we want to account for the tallest possible version of the animals here, use the upper bound of
    the animal's height.

    :param animal_list: input list
    :param height_limit: upper limit for animal height
    :return: list of animals who do not grow taller than the height limit
    """
    return list(filter(lambda x: x.height_range[1] < height_limit, animal_list))


def filter_animals_based_on_diet(animal_list: list, diet: str) -> list:
    """
    Find animals who has this particular diet.

    :param animal_list: input list
    :param diet: the type of diet we are looking for
    :return: list of animals who eat this type of food
    """
    return list(filter(lambda x: x.diet == diet, animal_list))


def find_animal_with_longest_lifespan(animal_list: list) -> Animal:
    """
    Find the animal with the longest possible lifespan.

    If multiple animals have the same longest possible lifespan, return the first one in the list.

    :param animal_list: input list
    :return: Animal object
    """
    return max(animal_list, key=lambda x: x.age_up_to)


def create_animal_descriptions(animal_list: list) -> list:
    """
    We need to print out animal descriptions to display near the animals at our zoo.

    For each animal type, create a string in the following format, replacing the data in square brackets with data from
    the animal object:
    "[Species name] ([Scientific name]) lives in [habitat] and its diet is [diet]. These animals can live up
    to [max age] years and they weigh between [min weight] kg and [max weight] kg as adults."

    :param animal_list: input list
    :return: list of animal description strings
    """
    return list(map(lambda x: f"{x.species} ({x.scientific_name}) lives in {x.habitat} and its diet is {x.diet}. These animals can live up to {x.age_up_to} years and they weigh between {x.weight_range[0]} kg and {x.weight_range[1]} kg as adults.", animal_list))


if __name__ == '__main__':
    elephant = Animal("African bush elephant", "Loxodonta africana", 70, (3000, 6000), (2.2, 4), "herbivorous",
                      "savannah")
    fruit_bat = Animal("Little red flying-fox", "Pteropus scapulatus", 30, (0.3, 0.6), (0.24, 0.26), "herbivorous",
                       "tropics")
    giraffe = Animal("Giraffe", "Giraffa camelopardalis", 25, (1200, 1800), (4.3, 5.7), "herbivorous",
                     "savannah")
    lynx = Animal("Eurasian lynx", "Lynx lynx", 7, (60, 75), (0.55, 0.75), "carnivorous", "temperate forest")
    bear = Animal("Brown bear", "Ursus arctos", 33, (130, 217), (1.4, 2.8), "omnivorous", "temperate forest")
    animal_list = [elephant, fruit_bat, giraffe, lynx, bear]
