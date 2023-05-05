"""Booksortation."""


def booksortation(books: list) -> dict:
    """
    Given a list of books (strings). Your task is to categorize and sort them.

    There are five books categories: spell books, history books, relics books, potion books and other books.

    If a book doesn't belong to any named categories, it goes to 'other books' category.

    However, if one book belongs to multiple categories, they should appear in only one
    (starting from up, whichever occurs first).

    :param books: given books as a list, list contains of strings
    :return: categorised and sorted books as a dict, where keys are categories and values are
    list of books that match this category. Lists should be sorted alphabetically.
    """
    book_dict = {}
    books.sort()
    for book in books:
        if is_spell_book(book):
            add_book_to_category(book, "spell books", book_dict)
        elif is_history_book(book):
            add_book_to_category(book, "history books", book_dict)
        elif is_relics_book(book):
            add_book_to_category(book, "relics books", book_dict)
        elif is_potion_book(book):
            add_book_to_category(book, "potion books", book_dict)
        else:
            add_book_to_category(book, "other books", book_dict)
    return book_dict


def add_book_to_category(book: str, category: str, categorised_books: dict) -> dict:
    """Param book."""
    if category not in categorised_books.keys():
        categorised_books[category] = []
    categorised_books[category].append(book)
    return categorised_books


def is_spell_book(book: str) -> bool:
    """
    Book is a spell book if its title starts with '*' (a star, without quotes) and ends with '*' (a star, no quotes).

    However, if the starting and ending star is the same star, it is not a spell book.

    For example: '*The Horrible Spells*' is a spell book.

    :param book: given book as a string
    :return: True if given book is a spell book, False otherwise
    """
    if len(book) == 0:
        return False
    if book[0] == "*" and book[-1] == "*" and book != "*":
        return True
    pass


def is_history_book(book: str) -> bool:
    """
    Book is a history book if its title matches the pattern where each new word does not start with a lowercase letter.

    Word is considered anything after a whitespace.

    For example: 'The Mighty King' and 'The Age Of The Wonderbolts' are both history books.
    Then again, 'the Ugly Duckling' isn't a history books because the word 'the' doesn't start with a capital letter.

    :param book: given book as a string
    :return: True if given book is a history book, False otherwise
    """
    x = book.split()
    for word in x:
        if word[0].islower():
            return False
    return True


def is_relics_book(book: str) -> bool:
    """
    Book is a relics book if its title matches the uppercase-lowercase-uppercase-lowercase... pattern.

    It can start from both upper- and lowercase letters.
    PS! Pay attention to whitespaces.

    For example: 'ThE StAfF' and 'rAiNiNg dUmPlInGs' are both relics books.
    However 'ThE sTaFf' and 'rAiNiNg DuMpLiNgS' are not relics books.

    :param book: given book as a string
    :return: True if given book is a relics book, False otherwise
    """
    even_str = book[::2]
    odd_str = book[1::2]
    even_str = "".join(list(filter(lambda x: x.isalpha(), even_str)))
    odd_str = "".join(list(filter(lambda x: x.isalpha(), odd_str)))
    if len(even_str) == 0:
        return True
    if len(odd_str) == 0:
        return True
    if even_str[0].isupper():
        if even_str.isupper() and odd_str.islower():
            return True
    if even_str[0].islower():
        if even_str.islower() and odd_str.isupper():
            return True
    return False


def is_potion_book(book: str) -> bool:
    """
    Book is a potion book if its title contains the same amount of vowels and consonants or the amount differs by one.

    However, it may contain as many symbols as it likes.

    The vowels are a, e, i, o, u.
    The consonants are b, c, d, f, g, h, j, k, l, m, n, p, q, r, s, t, v, x, z, w, y.

    For example: 'The Banana Juice' is a potion book (7 vowels, 7 consonants)
    and so is 'The tomato potion' (7 vowels, 8 consonants -> differ by 1).
    However, 'The Green Liquid' isn't a potion book (6 vowels, 8 consonants -> differ by 2).

    :param book: given book as a string
    :return: True if given book is a potion book, False otherwise
    """
    vowel = 0
    consonant = 0
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvxzwy"
    for letter in book:
        if letter.lower() in vowels:
            vowel += 1
        elif letter.lower() in consonants:
            consonant += 1

    if consonant == vowel or abs(consonant - vowel) == 1:
        return True
    else:
        return False


if __name__ == '__main__':
    # All True.
    print(is_spell_book('*kana*'))
    print(is_history_book('This Is A History Book'))
    print(is_relics_book('ThE StAfF'))
    print(is_potion_book('The Banana Juice'))
    print(is_potion_book("Green dandelion"))
