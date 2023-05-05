import pytest
import datetime
from bank import PersonError, TransactionError, Person, Bank, Transaction, Account


def test_transfer():
    person1 = Person("Ülo", "Õun", 67)
    person2 = Person("Aime", "Ploom", 71)
    bank1 = Bank("Muu")
    bank2 = Bank("Hää")
    bank1.add_customer(person1)
    bank2.add_customer(person2)
    account1 = person1.bank_account
    account2 = person2.bank_account
    balance1 = account1.deposit(20, True)
    balance2 = account2.deposit(20, True)
    account1.transfer(5, account2)
    assert account1.get_debit_turnover(datetime.date.today(), datetime.date.today()) == 20
    assert account2.get_debit_turnover(datetime.date.today(), datetime.date.today()) == 25

def test_get_net_turnover():
    person1 = Person("Ülo", "Õun", 67)
    person2 = Person("Aime", "Ploom", 71)
    bank1 = Bank("Muu")
    bank2 = Bank("Hää")
    bank1.add_customer(person1)
    bank2.add_customer(person2)
    account1 = person1.bank_account
    account2 = person2.bank_account
    deposit1 = account1.deposit(20, True)
    deposit2 = account2.deposit(20, True)
    withdraw1 = account1.withdraw(5, True)
    withdraw2 = account2.withdraw(10, True)
    account1.transfer(5, account2)
    assert account1.get_net_turnover(datetime.date.today(), datetime.date.today()) == 10
    assert account2.get_net_turnover(datetime.date.today(), datetime.date.today()) == 15


def test_remove_customer():
    person1 = Person("Ülo", "Õun", 67)
    person2 = Person("Aime", "Ploom", 71)
    person3 = Person("Kalle", "Pirn", 58)
    bank = Bank("Hea pank")
    bank.customers = [person1, person2, person3]
    assert bank.remove_customer(person1) is True

def test_account_statement():
    person = Person("Tore", "Proge", 1)
    bank = Bank("Hää")
    bank.add_customer(person)
    account = person.bank_account
    deposit1 = account.deposit(20, True)
    deposit2 = account.deposit(10, True)
    assert len(account.account_statement(datetime.date.today(), datetime.date.today())) == 2
