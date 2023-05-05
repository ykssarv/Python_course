"""Conversation."""

import re
import math

regex_a = r'(?<!- )(?<!\d)((- )?\d*)(?=x2)'
regex_b = r'(?<!- )(?<!\d)((- )?\d*)(?=x)(?!x2)'
regex_c = r'(?<!- )(?<!x)(?<!\d)((- )?\d+)(?!\d*x)'


class Student:
    """Student."""

    def __init__(self, biggest_number: int):
        """
        Constructor.

        save biggest number into a variable that is attainable later on.
        Create a collection of all possible results [possible_answers] <- dont rename that (can be a list or a set)
        :param biggest_number: biggest possible number(inclusive) to guess
        NB: calculating using sets is much faster compared to lists
        """
        self.biggest = biggest_number
        self.possible_answers = set([all_possible_answers for all_possible_answers in range(biggest_number + 1)])

    def decision_branch(self, sentence: str):
        """
        Regex can and should be used here.

        :param sentence: sentence to solve
        call one of the functions bellow (within this class) and return either one of the following strings:
        f"Possible answers are {sorted_list_of_possible_answers_in_growing_sequence)}." if there are multiple possibilities
        f"The number I needed to guess was {final_answer}." if the result is certain
        """
        negatives = ["is not", "does not", "doesn't", "isn't"]
        is_positive = True
        for negative in negatives:
            if negative in sentence:
                is_positive = False
        basic = {
            "prime": self.deal_with_primes,
            "composite": self.deal_with_composites,
            "fibonacci": self.deal_with_fibonacci_sequence,
            "catalan": self.deal_with_catalan_sequence
        }
        for key, function in basic.items():
            if key in sentence:
                function(is_positive)
                return self.answer()
        if "decimal value" in sentence:
            number = re.search(r'(?<=\")\d(?=\")', sentence).group()
            self.deal_with_dec_value(number)
        elif "hex value" in sentence:
            number = re.search(r'(?<=\")\d|\w(?=\")', sentence).group()
            self.deal_with_hex_value(number)
        elif "binary" in sentence:
            number = re.search(r'\d+', sentence).group()
            self.deal_with_number_of_ones(int(number)) if "one" in sentence else self.deal_with_number_of_zeroes(int(number))
        elif "order" in sentence:
            increasing = "increasing" in sentence
            self.deal_with_number_order(increasing, is_positive)
        else:
            # Ruutvõrrand
            equation = re.search(r'(?<=").*(?=")', sentence).group()
            should_multiply = "times" in sentence
            is_bigger = "bigger" in sentence
            if should_multiply:
                amount = float(re.search(r'\d+\.\d+(?= times)', sentence).group())
            else:
                amount = float(re.search(r'(?<=divided by )\d+\.\d+', sentence).group())
            self.deal_with_quadratic_equation(equation, should_multiply, amount, is_bigger)

        return self.answer()

    def answer(self):
        """Generate an answer."""
        if len(self.possible_answers) > 1:
            return f"Possible answers are {str(sorted(list(self.possible_answers)))}."
        return f"The number I needed to guess was {list(self.possible_answers)[0]}."

    def intersect_possible_answers(self, update: list):
        """Logical AND between two sets."""
        self.possible_answers = self.possible_answers.intersection(set(update))

    def exclude_possible_answers(self, update: list):
        """Logical SUBTRACTION between two sets."""
        self.possible_answers = self.possible_answers.difference(set(update))

    def deal_with_number_of_zeroes(self, amount_of_zeroes: int):
        """Filter possible_answers to match the amount of zeroes in its binary form."""
        numbers = []
        for number in self.possible_answers:
            if bin(number)[2:].count("0") == amount_of_zeroes:
                numbers.append(number)
        self.possible_answers = set(numbers)

    def deal_with_number_of_ones(self, amount_of_ones: int):
        """Filter possible answers to match the amount of ones in its binary form."""
        numbers = []
        for number in self.possible_answers:
            if bin(number)[2:].count("1") == amount_of_ones:
                numbers.append(number)
        self.possible_answers = set(numbers)

    def deal_with_primes(self, is_prime: bool):
        """Filter possible answers to either keep or remove all primes."""
        primes = find_primes_in_range(self.biggest)
        if is_prime:
            self.intersect_possible_answers(primes)
        else:
            self.exclude_possible_answers(primes)

    def deal_with_composites(self, is_composite: bool):
        """Filter possible answers to either keep or remove all composites."""
        composites = find_composites_in_range(self.biggest)
        if is_composite:
            self.intersect_possible_answers(composites)
        else:
            self.exclude_possible_answers(composites)

    def deal_with_dec_value(self, decimal_value: str):
        """Filter possible answers to remove all numbers that doesn't have the decimal_value in them."""
        self.possible_answers = set([num for num in self.possible_answers if decimal_value in str(num)])

    def deal_with_hex_value(self, hex_value: str):
        """Filter possible answers to remove all numbers that doesn't have the decimal_value in them."""
        numbers = []
        for number in self.possible_answers:
            if hex_value in hex(number)[2:]:
                numbers.append(number)
        self.possible_answers = set(numbers)

    def deal_with_quadratic_equation(self, equation: str, to_multiply: bool, multiplicative: float, is_bigger: bool):
        """
        Filter possible answers to remove all numbers that doesn't have the decimal_value in them.

        Regex can be used here.
        Call quadratic_equation_solver with variables a, b, c.
        deal_with_dec_value should be called.
        :param equation: the quadratic equation
        :param to_multiply: whether it is necessary to multiply or divide with a given multiplicative
        :param multiplicative: the multiplicative to multiply or divide with
        :param is_bigger: to use the bigger or smaller result of the quadratic equation(min or max from [x1, x2])
        """
        # print(to_multiply)
        # print(multiplicative)
        # print(equation)
        simple = normalize_quadratic_equation(equation)
        # print(simple)
        solution = quadratic_equation_solver(simple)
        # print(solution)
        if not isinstance(solution, float):
            if solution is None:
                return
            if is_bigger:
                solution = solution[1]
            else:
                solution = solution[0]
        if to_multiply:
            solution = solution * float(multiplicative)
        else:
            solution = solution / float(multiplicative)
        solution = int(round(solution))
        # print(solution)
        self.deal_with_dec_value(str(solution))

    def deal_with_fibonacci_sequence(self, is_in: bool):
        """Filter possible answers to either keep or remove all fibonacci numbers."""
        fibonaccis = find_fibonacci_numbers(self.biggest)
        if is_in:
            self.intersect_possible_answers(fibonaccis)
        else:
            self.exclude_possible_answers(fibonaccis)

    def deal_with_catalan_sequence(self, is_in: bool):
        """Filter possible answers to either keep or remove all catalan numbers."""
        catalans = find_catalan_numbers(self.biggest)
        if is_in:
            self.intersect_possible_answers(catalans)
        else:
            self.exclude_possible_answers(catalans)

    def deal_with_number_order(self, increasing: bool, to_be: bool):
        """Filter possible answers to either keep or remove all numbers with wrong order."""
        numbers = []
        for number in self.possible_answers:
            if increasing:
                if str(number) == ''.join(sorted(str(number))):
                    numbers.append(number)
            else:
                if str(number) == ''.join(sorted(str(number), reverse=True)):
                    numbers.append(number)
        if to_be:
            self.intersect_possible_answers(numbers)
        else:
            self.exclude_possible_answers(numbers)


def normalize_quadratic_equation(equation: str):
    """
    Normalize the quadratic equation.

    normalize_quadratic_equation("x2 + 2x = 3") => "x2 + 2x - 3 = 0"
    normalize_quadratic_equation("0 = 3 + 1x2") => "x2 + 3 = 0"
    normalize_quadratic_equation("2x + 2 = 2x2") => "2x2 - 2x - 2 = 0"
    normalize_quadratic_equation("0x2 - 2x = 1") => "2x + 1 = 0"
    normalize_quadratic_equation("0x2 - 2x = 1") => "2x + 1 = 0"
    normalize_quadratic_equation("2x2 + 3x - 4 + 0x2 - x1 + 0x1 + 12 - 12x2 = 4x2 + x1 - 2") => "14x2 - x - 10 = 0"

    :param equation: quadratic equation to be normalized
    https://en.wikipedia.org/wiki/Quadratic_formula
    :return: normalized equation
    """
    a, b, c = find_abc(equation)
    if a < 0 or a == 0 and b < 0 or a == 0 and b == 0 and c < 0:
        a, b, c = -a, -b, -c
    normal = ''
    normal += get_term_from_value_and_mark(a, 'x2')
    normal += get_term_from_value_and_mark(b, 'x')
    normal += get_term_from_value_and_mark(c, '')
    if normal == "":
        normal = "0 "
    if normal[:2] == "+ ":
        normal = normal[2:]
    return normal + "= 0"


def find_abc(equation):
    """Find a, b and c."""
    a_left, b_left, c_left = [], [], []
    a_right, b_right, c_right = [], [], []
    for regex, left, right in [(regex_a, a_left, a_right), (regex_b, b_left, b_right), (regex_c, c_left, c_right)]:
        split_equation = equation.split(" = ")
        for match in re.finditer(regex, split_equation[0]):
            left.append(match.group(1))
        for match in re.finditer(regex, split_equation[1]):
            right.append(match.group(1))
    return combine_lists(a_left, a_right), combine_lists(b_left, b_right), combine_lists(c_left, c_right)


def get_term_from_value_and_mark(value, after):
    """Get term."""
    if value == 0:
        return ""
    before = "+ " if value > 0 else "- "
    value = str(abs(value))
    if value == "1" and len(after) > 0:
        value = ""
    return before + value + after + " "


def match_to_int(matches):
    """Match to int."""
    ints = []
    for match in matches:
        if match == "":
            ints.append(1)
        elif match == "- ":
            ints.append(-1)
        else:
            ints.append(int(match.replace(" ", "")))
    return ints


def combine_lists(left, right):
    """Combine lists."""
    return sum(match_to_int(left)) - sum(match_to_int(right))


def quadratic_equation_solver(equation: str):
    """
    Solve the normalized quadratic equation.

    :param str: quadratic equation
    https://en.wikipedia.org/wiki/Quadratic_formula
    :return:
    if there are no solutions, return None.
    if there is exactly 1 solution, return it.
    if there are 2 solutions, return them in a tuple, where smaller is first
    all numbers are returned as floats.
    """
    a, b, c = find_abc(equation)
    if a == 0:
        if b == 0:
            return None
        return - c / b
    disk = b**2 - 4 * a * c
    if disk < 0:
        return None
    if disk == 0:
        return -b / (2 * a)
    x1 = (-b - math.sqrt(disk)) / (2 * a)
    x2 = (-b + math.sqrt(disk)) / (2 * a)
    return min(x1, x2), max(x1, x2)


def find_primes_in_range(biggest_number: int):
    """
    Find all primes in range(end inclusive).

    :param biggest_number: all primes in range of biggest_number(included)
    https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
    :return: list of primes
    """
    if biggest_number < 2:
        return []
    sieve = [True] * (biggest_number + 1)
    numbers = []
    for i in range(2, biggest_number + 1):
        if not sieve[i]:
            continue
        numbers.append(i)
        current = i * 2
        while current <= biggest_number:
            sieve[current] = False
            current += i
    return numbers


def find_composites_in_range(biggest_number: int):
    """Find all composites in range(end inclusive)."""
    primes_in_range = set(find_primes_in_range(biggest_number))
    numbers = []
    for i in range(4, biggest_number + 1):
        if i in primes_in_range:
            continue
        numbers.append(i)
    return numbers


def find_fibonacci_numbers(biggest_number: int):
    """Find all Fibonacci numbers in range(end inclusive)."""
    a = 0
    b = 1
    if biggest_number == 0:
        return [0]
    numbers = [0, 1]
    while True:
        a, b = b, a + b
        if b > biggest_number:
            return numbers
        numbers.append(b)


def find_catalan_numbers(biggest_number: int):
    """Find all Catalan numbers in range(end inclusive)."""
    numbers = []
    n = 0
    while True:
        number = int(math.factorial(2 * n) / (math.factorial(n)**2 * (n + 1)))
        if number > biggest_number:
            return numbers
        numbers.append(number)
        n += 1


if __name__ == '__main__':
    student = Student(100)
    equation = "3x - 27 = 0"
    print(student.decision_branch(f'This number is comprised of a digit where 3.0000 times the bigger result for the following quadratic equation:"{equation}" is rounded to closest integer.'))
    """
    student = Student(50)
    print(student.decision_branch("This number, that you need to guess is composite."))
    print(student.decision_branch("Number does not happen to be in fibonacci sequence."))
    print(student.decision_branch('Number is comprised of decimal value: "3".'))
    print(student.decision_branch('Number is comprised of hex value: "2".'))
    # print(student.decision_branch('This number has 3 ones in its binary form.'))
    """

    print(normalize_quadratic_equation("12x22 - 2x = x2"))
    # print(normalize_quadratic_equation("0 = 3 + 1x2"))
    # print(normalize_quadratic_equation("2x + 2 = 2x2"))
    # print(normalize_quadratic_equation("0x2 - 2x = 1"))
    # print(normalize_quadratic_equation("2x2 + 3x - 4 + 0x2 - x1 + 0x1 + 12 - 12x2 = 4x2 + x1 - 2"))
