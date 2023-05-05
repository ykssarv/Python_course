"""Bank."""
import datetime
import random


class PersonError(Exception):
    """Person error."""

    pass


class TransactionError(Exception):
    """Transaction error."""

    pass


class Person:
    """Person class."""

    def __init__(self, first_name: str, last_name: str, age: int):
        """
        Person constructor.

        :param first_name: first name
        :param last_name: last name
        :param age: age, must be greater than 0
        """
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.bank_account = None

    @property
    def full_name(self) -> str:
        """Get person's full name. Combination of first and last name."""
        return self.first_name + " " + self.last_name

    @property
    def age(self) -> int:
        """Get person's age."""
        return self._age

    @age.setter
    def age(self, value: int):
        """Set person's age. Must be greater than 0."""
        if value <= 0:
            raise PersonError()
        self._age = value

    def __repr__(self) -> str:
        """
        Person representation.

        :return: person's full name
        """
        return self.full_name


class Bank:
    """Bank class."""

    def __init__(self, name: str):
        """
        Bank constructor.

        :param name: name of the bank
        """
        self.name = name
        self.customers = []
        self.transactions = []

    def add_customer(self, person: Person) -> bool:
        """
        Add customer to bank.

        :param person: person object
        :return: was customer successfully added
        """
        if person not in self.customers:
            person.bank_account = Account(0.0, person, self)
            self.customers.append(person)
            return True
        return False

    def remove_customer(self, person: Person) -> bool:
        """
        Remove customer from bank.

        :param person: person object
        :return: was customer successfully removed
        """
        if person in self.customers:
            person.bank_account = None
            self.customers.remove(person)
            return True
        return False

    def __repr__(self) -> str:
        """
        Bank representation.

        :return: name of the bank
        """
        return self.name


class Transaction:
    """Transaction class."""

    def __init__(self, amount: float, date: datetime.date, sender_account: 'Account', receiver_account: 'Account',
                 is_from_atm: bool):
        """
        Transaction constructor.

        :param amount: value
        :param date: date of the transaction
        :param sender_account: sender's object
        :param receiver_account: receiver's object
        :param is_from_atm: is transaction from atm
        """
        self.amount = amount
        self.date = date
        self.sender_account = sender_account
        self.receiver_account = receiver_account
        self.is_from_atm = is_from_atm

    def __repr__(self) -> str:
        """
        Transaction representation.

        :rtype: object's values displayed in a nice format
        """
        if self.is_from_atm:
            return f"({self.amount} €) ATM"
        else:
            return f"({self.amount} €) {self.sender_account.person} -> {self.receiver_account.person}"


class Account:
    """Account class."""

    def __init__(self, balance: float, person: Person, bank: 'Bank'):
        """
        Account constructor.

        :param balance: initial account balance
        :param person: person object
        :param bank: bank object
        """
        self._balance = balance
        self.person = person
        self.bank = bank
        self.transactions = []
        self.number = "EE"

        for i in range(18):
            self.number += str(random.randint(0, 9))

    @property
    def balance(self):
        """Get account's balance."""
        return self._balance

    def deposit(self, amount: float, is_from_atm: bool = True):
        """Deposit money to account."""
        if amount <= 0:
            raise TransactionError()
        else:
            self._balance += amount
            if is_from_atm:
                transaction = Transaction(amount, datetime.date.today(), self, self, True)
                self.transactions.append(transaction)
                self.bank.transactions.append(transaction)

    def withdraw(self, amount: float, is_from_atm: bool = True):
        """Withdraw money from account."""
        if amount <= 0 or amount > self._balance:
            raise TransactionError()
        else:
            self._balance -= amount
            if is_from_atm:
                transaction = Transaction(-amount, datetime.date.today(), self, self, True)
                self.transactions.append(transaction)
                self.bank.transactions.append(transaction)

    def transfer(self, amount: float, receiver_account: 'Account'):
        """Transfer money from one account to another."""
        if self.bank != receiver_account.bank:
            amount2 = amount + 5
        else:
            amount2 = amount
        if self == receiver_account or (self._balance - amount2) < 0:
            raise TransactionError()
        else:
            self.withdraw(amount2, False)
            receiver_account.deposit(amount, False)
            transaction = Transaction(amount, datetime.date.today(), self, receiver_account, False)
            self.transactions.append(transaction)
            receiver_account.transactions.append(transaction)
            if self.bank == receiver_account.bank:
                self.bank.transactions.append(transaction)
            else:
                self.bank.transactions.append(transaction)
                receiver_account.bank.transactions.append(transaction)

    def account_statement(self, from_date: datetime.date.today(), to_date: datetime.date) -> list:
        """All transactions in given period."""
        all_transactions = []
        for transaction in self.transactions:
            if from_date <= transaction.date <= to_date:
                all_transactions.append(transaction)
        return all_transactions

    def get_debit_turnover(self, from_date: datetime.date, to_date: datetime.date) -> float:
        """
        Get total income in given period.

        :param from_date: from date object (included)
        :param to_date: to date object (included)
        :return: debit turnover number
        """
        income = 0.0
        for transaction in self.transactions:
            if from_date <= transaction.date <= to_date:
                if transaction.is_from_atm:
                    if transaction.amount > 0:
                        income += transaction.amount
                else:
                    if transaction.receiver_account == self:
                        income += transaction.amount
        return income

    def get_credit_turnover(self, from_date: datetime.date, to_date: datetime.date) -> float:
        """
        Get total expenditure in given period.

        :param from_date: from date object (included)
        :param to_date: to date object (included)
        :return: credit turnover number
        """
        outcome = 0.0
        for transaction in self.transactions:
            if from_date <= transaction.date <= to_date:
                if transaction.is_from_atm:
                    if transaction.amount < 0:
                        outcome += transaction.amount
                else:
                    if transaction.sender_account == self:
                        outcome -= transaction.amount
        return outcome

    def get_net_turnover(self, from_date: datetime.date, to_date: datetime.date) -> float:
        """
        Get net turnover (income - costs) in given period.

        :param from_date: from date object (included)
        :param to_date: to date object (included)
        :return: net turnover number
        """
        return self.get_debit_turnover(from_date, to_date) + self.get_credit_turnover(from_date, to_date)

    def __repr__(self) -> str:
        """
        Account representation.

        :return: account number
        """
        return self.number
