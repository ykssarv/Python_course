"""Primes identifier."""


def is_prime_number(number: int):
    """Prime identifier."""
    if number == 2:
        return True
    elif number < 2:
        return False
    for i in range(2, number):
        remainder = number % i
        if remainder == 0:
            return False
    return True


if __name__ == '__main__':
    print(is_prime_number(2))  # -> True
    print(is_prime_number(89))  # -> True
    print(is_prime_number(23))  # -> True
    print(is_prime_number(4))  # -> False
    print(is_prime_number(7))  # -> True
    print(is_prime_number(88))  # -> False
    print(is_prime_number(0))
    print(is_prime_number(1))
    print(is_prime_number(9))
    print(is_prime_number(121))
