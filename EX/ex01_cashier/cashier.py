"""Cashier."""
sum = int(input("Enter a sum: "))
cent_list = [50, 20, 10, 5, 1]
remainder = sum
amount = 0
for cent in cent_list:
    amount += remainder // cent
    remainder = remainder % cent
print("Amount of coins needed: " + str(amount))
