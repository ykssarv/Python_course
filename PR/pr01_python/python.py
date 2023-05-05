"""Python."""
name = input("What is your name?")
year = int(input("Hello, " + name + "! What year were you born in?"))
if year > 2008:
    difference = year - 2008
    print("Python 3 was " + str(difference) + " years old when you were born.")
if year < 2008:
    age = 2008 - year
    print("You were " + str(age) + " years old when Python 3.0 was released.")
