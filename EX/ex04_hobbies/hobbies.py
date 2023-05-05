"""Hobbies."""
import csv


def create_list_from_file(file):
    """
    Collect lines from given file into list.

    :param file: original file path
    :return: list of lines
    """
    file = open(file, "r")
    hobbies = file.readlines()
    return hobbies


def create_dictionary(file):
    """
    Create dictionary about given peoples' hobbies as Name: [hobby_1, hobby_2].

    :param file: original file path
    :return: dict
    """
    hobbies_list = set(create_list_from_file(file))
    names_dict = {}
    for line in hobbies_list:
        name_hobby = line.strip().split(":")
        if name_hobby[0] in names_dict.keys():
            names_dict[name_hobby[0]].append(name_hobby[1])
        else:
            names_dict[name_hobby[0]] = [name_hobby[1]]
    return names_dict


def find_person_with_most_hobbies(file):
    """
    Find the person (or people) who have more hobbies than others.

    :param file: original file path
    :return: list
    """
    hobbies_dict = create_dictionary(file)
    max_hobbies = 0
    most_hobbies = []
    for key, value in hobbies_dict.items():
        if len(value) > max_hobbies:
            max_hobbies = len(value)
            most_hobbies = [key]
        elif len(value) == max_hobbies:
            most_hobbies.append(key)
    return most_hobbies


def find_person_with_least_hobbies(file):
    """
    Find the person (or people) who have less hobbies than others.

    :param file: original file path
    :return: list
    """
    hobbies_dict = create_dictionary(file)
    min_hobbies = 1e50
    least_hobbies = []
    for key, value in hobbies_dict.items():
        if len(value) < min_hobbies:
            min_hobbies = len(value)
            least_hobbies = [key]
        elif len(value) == min_hobbies:
            least_hobbies.append(key)
    return least_hobbies


def find_most_popular_hobby(file):
    """
    Find the most popular hobby.

    :param file: original file path
    :return: list
    """
    hobbies_dict = create_dictionary(file)
    hobbies_list = []
    most_popular = 0
    popular_hobbies = []
    for hobbies in hobbies_dict.values():
        hobbies_list = hobbies_list + hobbies
    hobby_list = set(hobbies_list)
    for hobby in hobby_list:
        if hobbies_list.count(hobby) > most_popular:
            most_popular = hobbies_list.count(hobby)
            popular_hobbies = [hobby]
        elif hobbies_list.count(hobby) == most_popular:
            popular_hobbies.append(hobby)
    return popular_hobbies


def find_least_popular_hobby(file):
    """
    Find the least popular hobby.

    :param file: original file path
    :return: list
    """
    hobbies_dict = create_dictionary(file)
    hobbies_list = []
    least_popular = 1e50
    unpopular_hobbies = []
    for hobbies in hobbies_dict.values():
        hobbies_list = hobbies_list + hobbies
    hobby_list = set(hobbies_list)
    for hobby in hobby_list:
        if hobbies_list.count(hobby) < least_popular:
            least_popular = hobbies_list.count(hobby)
            unpopular_hobbies = [hobby]
        elif hobbies_list.count(hobby) == least_popular:
            unpopular_hobbies.append(hobby)
    return unpopular_hobbies


def write_corrected_database(file, file_to_write):
    """
    Write .csv file in a proper way. Use collected and structured data.

    :param file: original file path
    :param file_to_write: file to write result
    """
    with open(file_to_write, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        name = "Name"
        hobbies = "Hobbies"
        writer.writerow([name, hobbies])
        # your code goes here

# These examples are based on a given text file from the exercise.
