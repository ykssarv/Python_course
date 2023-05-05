"""Graph."""

from investor import get_currency_rates_from_file, exchange_money
import matplotlib.pyplot as plt
from datetime import datetime


def dates_to_numbers(dates, min):
    """Convert dates to numbers."""
    dates = [int(datetime.strptime(x, '%d.%m.%Y').timestamp()) // 86400 for x in dates]
    return [date - min for date in dates]


def plot_rates_and_deals(rates, deals):
    """Plot rates and deals."""
    sorted_rates = list(sorted(rates.items(), key=lambda x: datetime.strptime(x[0], '%d.%m.%Y').timestamp()))
    for rate in sorted_rates:
        # print(int(datetime.strptime(rate[0], '%d.%m.%Y').timestamp()) // 86400)
        pass
    min_date = min([int(datetime.strptime(x[0], '%d.%m.%Y').timestamp()) // 86400 for x in sorted_rates])

    dates = dates_to_numbers([x[0] for x in sorted_rates], min_date)
    rates = [x[1] for x in sorted_rates]
    plt.plot(dates, rates)

    dates = dates_to_numbers(deals, min_date)
    rates = [x[1] for x in sorted_rates if x[0] in deals]
    plt.plot(dates, rates)

    plt.show()


def plot_rates(rates):
    """Plot rates only."""
    sorted_rates = list(sorted(rates.items(), key=lambda x: datetime.strptime(x[0], '%d.%m.%Y').timestamp()))
    for rate in sorted_rates:
        # print(int(datetime.strptime(rate[0], '%d.%m.%Y').timestamp()) // 86400)
        pass
    dates = dates_to_numbers([x[0] for x in sorted_rates])
    rates = [x[1] for x in sorted_rates]
    plt.plot(dates, rates)
    plt.show()


def plot_money(rates, deals):
    """Plot the amount of money at different times."""
    money_history = []
    date_history = []
    original = 1000
    new = 0
    for key, value in list(rates.items())[::-1]:
        date_history.append(key)
        if original == 0:
            money_history.append(new / value)
            if key in deals:
                original = new / value
                new = 0
        else:
            money_history.append(original)
            if key in deals:
                new = original * value
                original = 0
    print(rates)
    print(deals)
    # print(original_history)
    # print(new_history)
    print(date_history)
    plt.plot(date_history, money_history)
    # plt.plot(date_history, new_history)
    plt.show()


if __name__ == '__main__':
    currency, rates = get_currency_rates_from_file('currency-rates.csv')
    dates = exchange_money(rates)
    # plot_rates(rates)
    # plot_rates_and_deals(rates, dates)
    plot_money(rates, dates)
