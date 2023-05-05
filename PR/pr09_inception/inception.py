"""If you're going to perform inception, you need imagination."""
import math


def countdown(n: int):
    """
    Write a simple recursive function that returns a list of numbers that count down from n.

    countdown(5) -> [5, 4, 3, 2, 1, 0]
    countdown(8) -> [8, 7, 6, 5, 4, 3, 2, 1, 0]
    countdown(-1) -> []

    :param n: start
    :return: countdown sequence
    """
    if n < 0:
        return []
    if n == 0:
        return [0]
    else:
        return [n] + countdown(n - 1)


def add_commas(n: int):
    """
    In representing large numbers, from the right side to the left.

    English texts usually use commas to separate each group of three digits in front of the decimal.
    Your challenge is to output a number n formatted with commas.

    add_commas(1245) -> '1,245'
    add_commas(123456789) -> '123,456,789'
    add_commas(1011) -> '1,011'

    :param n: int
    :return: string of the formatted int
    """
    if len(str(n)) <= 3:
        return str(n)
    else:
        p = str(n)[:-3]
        s = add_commas(int(p))
        return s + "," + str(n)[-3:]


def stonks(coins, rate, years):
    """
    Each year your crypto-investment grows.

    Write a recursive function that calculates the net worth of coins after some years.
    Rate is in percents.
    Round the answer down to the nearest integer.

    stonks(1000, 10, 10) -> 2593
    stonks(100000, 12, 3) -> 140492

    :param coins: starting amount (0-100000)
    :param rate: starting amount (0-100)
    :param years: starting amount (0-50)
    :return: coins after years
    """
    if years == 0:
        return math.floor(coins)
    return stonks(coins + coins * rate / 100, rate, years - 1)


def quic_mafs(a: int, b: int):
    """
    Write a recursive function that applies the following operations.

    i) If a=0 or b=0, return [a,b]. Otherwise, go to step (ii);
    ii) If a>=2*b, set a = a-2*b, and repeat step (i). Otherwise, go to step (iii);
    iii) If b>=2*a, set b = b-2*a, and repeat step (i). Otherwise, return [a,b].

    quic_mafs(6, 19) -> [6, 7]
    quic_mafs(2, 1) -> [0, 1]
    quic_mafs(22, 5) -> [0, 1]
    quic_mafs(8796203,7556) -> [1019,1442]

    :param a: int
    :param b: int
    :return: result
    """
    if a == 0 or b == 0:
        return [a, b]
    elif a >= 2 * b:
        a = a - 2 * b
        return quic_mafs(a, b)
    elif b >= a * 2:
        b = b - 2 * a
        return quic_mafs(a, b)
    return [a, b]


def sum_squares(nested_list):
    """
    Write a function that sums squares of numbers in list.

    That list may contain additional lists.
    (Hint use the type() or isinstance() function)

    sum_squares([1, 2, 3]) -> 14
    sum_squares([[1, 2], 3]) -> sum_squares([1, 2]) + 9 -> 1 + 4 + 9 -> 14
    sum_squares([[[[[[[[[2]]]]]]]]]) -> 4

    :param nested_list: list of lists of lists of lists of lists ... and ints
       :return: sum of squares
    """
    answer = 0
    if not nested_list:
        return 0
    if isinstance(nested_list[0], list):
        squares = sum_squares(nested_list[0])
        answer += squares
    else:
        square = nested_list[0] ** 2
        answer += square
    new_list = nested_list[1:]
    return sum_squares(new_list) + answer


if __name__ == "__main__":
    print(countdown(5))  # -> [5, 4, 3, 2, 1, 0]
    print(countdown(8))  # -> [8, 7, 6, 5, 4, 3, 2, 1, 0]
    print(countdown(-1))  # -> []

    print(add_commas(1245))  # -> '1,245'
    print(add_commas(123456789))  # -> '123,456,789'
    print(add_commas(1011))  # -> '1,011'

    print(stonks(1000, 10, 10))  # -> 2593
    print(stonks(100000, 12, 3))  # -> 140492

    print(quic_mafs(6, 19))  # -> [6, 7]
    print(quic_mafs(2, 1))  # -> [0, 1]
    print(quic_mafs(22, 5))  # -> [0, 1]
    print(quic_mafs(8796203, 7556))  # -> [1019,1442]
    print(sum_squares([1, 2, 3]))  # -> 14
    print(sum_squares([[1, 2], 3]))  # -> 14
    print(sum_squares([[[[[[[[[2]]]]]]]]]))  # -> 4
