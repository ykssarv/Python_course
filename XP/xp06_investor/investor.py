"""Invest."""

from datetime import datetime


def get_currency_rates_from_file(filename: str) -> tuple:
    """
    Read and return the currency and exchange rate history from file.

    See web page:
    https://www.eestipank.ee/valuutakursside-ajalugu
    Note that the return value is tuple, that consists of two things:
    1) currency name given in the file.
    2) exchange rate history for the given currency.
        Note that history is returned using dictionary where keys represent dates
        and values represent exchange rates for the dates.

    :param filename: file name to read CSV data from
    :return: Tuple that consists of currency name and dict with exchange rate history
    """
    file = open(filename, 'r')
    lines = file.readlines()
    rates = {}
    currency = ''
    for line in lines:
        splited = line.strip().split(",")
        date = splited[0].strip('"')
        if len(date.split(".")) != 3:
            if splited[0] == '""':
                currency = splited[1].strip('"')
            continue
        rates[date] = float(splited[1].strip('"'))
    return currency, rates


def get_trades(data):
    """Get all minimums and maximums from data."""
    last_was = None
    mins = []
    maxes = []
    for i, line in enumerate(data):
        if i == len(data) - 1:
            continue
        if last_was == "max" and data[i + 1][1] > line[1]:
            mins.append(line)
            last_was = "min"
        elif last_was == "min" and data[i + 1][1] < line[1]:
            maxes.append(line)
            last_was = "max"
        elif last_was is None:
            if data[i + 1][1] > line[1]:
                last_was = "min"
                mins.append(line)
            elif data[i + 1][1] < line[1]:
                last_was = "max"
                maxes.append(line)
    # print(len(maxes))
    # print(len(mins))
    return combine_mins_and_maxes(mins, maxes, data)


def combine_mins_and_maxes(mins, maxes, data):
    """Combine mins and maxes."""
    if len(maxes) < len(mins):
        maxes = [data[0]] + maxes
    if len(mins) < len(maxes):
        mins = mins + [data[-1]]
    # Buy at min, sell at max
    trades = []
    for max, min in zip(maxes, mins):
        trades.append(max)
        trades.append(min)
    return trades


def find_answer(trades):
    """Find the answer from all minimums and maximums."""
    while True:
        no_bad_trades = True
        for i in range(len(trades) // 2):
            no_bad_trades = no_bad_trades and 0.99**2 * trades[i * 2][1] / trades[i * 2 + 1][1] >= 1
        if no_bad_trades:
            pass
        best_remove = 1
        best_remove_index = None
        for i in range(len(trades) - 1):
            if i % 2 == 0:
                this_remove = 1 / (0.99**2 * (trades[i][1] / trades[i + 1][1]))
            else:
                this_remove = 1 / (0.99**2 * (trades[i + 1][1] / trades[i][1]))
            if this_remove > best_remove:
                best_remove = this_remove
                best_remove_index = i
        if best_remove_index is None:
            break
        trades = [trade for i, trade in enumerate(trades) if i != best_remove_index and i != best_remove_index + 1]

        total = 1
        for profit in [0.99 ** 2 * trades[i * 2][1] / trades[i * 2 + 1][1] for i in range(len(trades) // 2)]:
            total *= profit
    return [x[2] for x in trades]


def exchange_money(exchange_rates: dict) -> list:
    """
    Find best dates to exchange money for maximum profit.

    You are given a dictionary where keys represent dates and values represent exchange
    rates for the dates. The amount you initially have is 1000 and you always use the
    maximum amount during the exchange.
    Be aware that there is 1% of service fee for every exchange. You only need to return
    the dates where you take action. That means the first action is always to buy the
    second currency and the second action is to sell it back. Repeat the sequence as
    many times as you need for maximum profit. You should always end up having the
    initial currency. That means there should always be an even number of actions. You can
    also decide that the best decision is to not make any transactions at all, if
    for example the rate is always dropping. In that case just return an empty list.

    :param exchange_rates: dictionary of dates and exchange rates
    :return: list of dates
    """
    data = [(datetime.strptime(item[0], '%d.%m.%Y').timestamp(), item[1], item[0]) for item in exchange_rates.items()]
    data.sort()
    trades = get_trades(data)
    answer = find_answer(trades)
    return answer


if __name__ == '__main__':
    currency, rates = get_currency_rates_from_file('currency-rates.csv')
    dates = exchange_money(rates)
    print(dates)
    print(len(dates))
