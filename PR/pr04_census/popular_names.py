"""Order names by popularity."""


def read_from_file() -> list:
    """
    Create the list of all the names.

    :return: list
    """
    names = []
    with open("popular_names.txt", encoding='utf-8') as file:
        for line in file:
            names.append(line.strip())
    return names


def to_dictionary(names: list) -> dict:
    """
    Make a dictionary from a list of names.

    :param names: list of all the names
    :return: dictionary {"name:sex": number}
    """
    names_dict = {}
    for name in names:
        if name not in names_dict.keys():
            names_dict[name] = 1
        else:
            names_dict[name] += 1
    return names_dict


def to_sex_dicts(names_dict: dict) -> tuple:
    """
    Divide the names by sex to 2 different dictionaries.

    :param names_dict: dictionary of names
    :return: two dictionaries {"name": number}, {"name": number}
    first one is male names, seconds is female names.
    """
    male_dict = {}
    female_dict = {}
    for name in names_dict.keys():
        value = names_dict[name]
        name = name.split(":")
        if name[1] == "M":
            male_dict[name[0]] = value
        elif name[1] == "F":
            female_dict[name[0]] = value
    return male_dict, female_dict


def most_popular(names_dict: dict) -> str:
    """
    Find the most popular name in the dictionary.

    If the dictionary is empty, return "Empty dictionary."
    :param names_dict: dictionary of names (key is name, value is count)
    :return: string
    """
    value = 0
    popular = ""
    if len(names_dict) == 0:
        return "Empty dictionary."
    for name in names_dict.keys():
        if names_dict[name] > value:
            value = names_dict[name]
            popular = name
    return popular


def number_of_people(names_dict: dict) -> int:
    """
    Calculate the number of people in the dictionary.

    :param names_dict: dictionary of names (key is name, value is count)
    :return: int
    """
    return sum(names_dict.values())


def names_by_popularity(names_dict: dict) -> str:
    r"""
    Create a string used to print the names by popularity.

    Format:
        1. name: number of people + "\n"
        ...

    Example:
        1. Kati: 100
        2. Mati: 90
        3. Nati: 80
        ...

    :param names_dict: dictionary of the names (key is name, value is count)
    :return: string
    """
    popular_names = ""
    dict_items = list(names_dict.items())
    dict_items = list(reversed(sorted(dict_items, key=lambda x: x[1])))
    for i, name in enumerate(dict_items):
        popular_names += str(i + 1) + ". " + str(name[0]) + ": " + str(name[1]) + "\n"
    return popular_names
