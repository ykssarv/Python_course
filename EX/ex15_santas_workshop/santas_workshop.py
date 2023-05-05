"""Santa."""

import urllib.request
import json


class Main:
    """Main class."""

    def __init__(self):
        """Init."""
        self.nice_kids = {}
        self.naughty_kids = {}
        self.toys = {}
        self.countries = {}

    def read_information(self):
        """Read information."""
        self.read_nice_list()
        self.read_naughty_list()
        self.read_wishlist()

    def distribute_gifts(self):
        """Give gifts."""
        self.make_countries()
        self.make_sledges()

    def make_countries(self):
        """Make countries."""
        for kids in [self.nice_kids, self.naughty_kids]:
            for name, child in kids.items():
                country = child.habitat
                if country not in self.countries.keys():
                    self.countries[country] = Country(country, self)
                self.countries[country].add_child(child)

    def make_sledges(self):
        """Make sledges."""
        for name, country in self.countries.items():
            country.make_sledges()
            country.generate_sledge_files()

    def read_nice_list(self):
        """Read nice list."""
        nice_list = open("nice_list.csv", "r")
        nice = nice_list.readlines()
        for line in nice:
            kid = line.strip("\n").split(", ")
            self.nice_kids[kid[0]] = Child(kid[0], kid[1], "nice")

    def read_naughty_list(self):
        """Read naughty list."""
        naughty_list = open("naughty_list.csv", "r")
        nice = naughty_list.readlines()
        for line in nice:
            kid = line.strip("\n").split(", ")
            self.naughty_kids[kid[0]] = Child(kid[0], kid[1], "naughty")

    def read_wishlist(self):
        """Read wishlist."""
        wishlist = open("wishlist.csv", "r")
        wish = wishlist.readlines()
        for line in wish:
            wishes = line.strip("\n").split(", ")
            # print(wishes)
            if wishes[0] in self.nice_kids.keys():
                self.nice_kids[wishes[0]].wishes.extend(wishes[1:])
            elif wishes[0] in self.naughty_kids.keys():
                self.naughty_kids[wishes[0]].wishes.extend(wishes[1:])
            for w in wishes[1:]:
                if w not in self.toys.keys():
                    self.toys[w] = Toy(w)


class Child:
    """Sugar daddy."""

    def __init__(self, name, habitat, species):
        """Init."""
        self.name = name
        self.habitat = habitat
        self.species = species
        self.wishes = []


class Toy:
    """Toy."""

    def __init__(self, name):
        """Init."""
        self.amount = 0
        self.name = name.strip(" ")
        self.material_cost = 0
        self.production_time = 0
        self.weight_in_grams = 0
        self.toy_information()

    def toy_information(self,):
        """Toy information."""
        x = self.name.lower()
        y = x.replace(" ", "%20")
        url = "http://api.game-scheduler.com:8089/gift?name=" + y
        # print(url)
        req = urllib.request.Request(url)
        r = urllib.request.urlopen(req).read()
        cont = json.loads(r.decode('utf-8'))

        self.material_cost = cont['material_cost']
        self.production_time = cont['production_time']
        self.weight_in_grams = cont['weight_in_grams']


class Country:
    """Country."""

    def __init__(self, name, main):
        """Init."""
        self.name = name
        self.children = []
        self.sledges = []
        self.main = main

    def add_child(self, child):
        """Add child."""
        self.children.append(child)

    def make_sledges(self):
        """Make sledges."""
        for child in self.children:
            for toy in child.wishes:
                toy = self.main.toys[toy]
                done = False
                for sledge in self.sledges:
                    if sledge.has_room(toy):
                        sledge.add_toy(toy, child.name)
                        done = True
                        break
                if not done:
                    self.sledges.append(Sledge(self.name, len(self.sledges)))
                    self.sledges[-1].add_toy(toy, child.name)

    def generate_sledge_files(self):
        """Generate sledge files."""
        for sledge in self.sledges:
            sledge.generate_file()


class Sledge:
    """Sledge."""

    def __init__(self, country_name, id):
        """Init."""
        self.id = id
        self.toys = {}
        self.total_weight = 0
        self.country_name = country_name

    def has_room(self, toy):
        """Check if has room."""
        return self.total_weight + toy.weight_in_grams <= 50000

    def add_toy(self, toy, name):
        """Add toy."""
        if name not in self.toys.keys():
            self.toys[name] = []
        self.toys[name].append(toy)
        self.total_weight += toy.weight_in_grams

    def generate_file(self):
        """Generate file."""
        name = self.country_name + str(self.id) + '.txt'
        file = open(name, "w")
        file.write("DELIVERY ORDER\n")
        file.write("FROM: NORTH POLE CHRISTMAS CHEER INCORPORATED\n")
        file.write(f"TO: {self.country_name}\n\n")
        file.writelines(self.table_lines())
        file.close()

    def table_lines(self):
        """Generate table lines."""
        names = list(self.toys.keys())
        toys = {name: ', '.join([toy.name for toy in toys]) for name, toys in self.toys.items()}
        weights = {name: sum([toy.weight_in_grams for toy in toys]) for name, toys in self.toys.items()}

        max_name = max([len(name) for name in names] + [len("Name")])
        max_toys = max([len(toy) for toy in toys.values()] + [len("Gifts")])
        weight_message = "Total Weight(kg)"
        lines = []
        middle = "[]".join(["=" * x for x in [max_name + 2, max_toys + 2, len(weight_message) + 2]])
        lines.append("//" + middle + "\\\\\n")
        header = ""
        header += "||"
        header += ('{: ^' + str(max_name + 2) + '}').format("Name")
        header += "||"
        header += ('{: ^' + str(max_toys + 2) + '}').format("Gifts")
        header += "||"
        header += ('{: ^' + str(len(weight_message) + 2) + '}').format(weight_message)
        header += "||\n"
        lines.append(header)
        lines.append("|[" + middle + "]|\n")
        for name, toy in toys.items():
            line = "|| "
            line += name + " " * (max_name - len(name))
            line += " || "
            line += toy + " " * (max_toys - len(toy))
            line += " || "
            weight = str(round(weights[name] / 1000, 2))
            line += " " * (len(weight_message) - len(weight)) + weight
            line += " ||\n"
            lines.append(line)
        lines.append("\\\\" + middle + "//")
        return lines


if __name__ == '__main__':
    Toy("Crayons")
    main = Main()
    main.read_information()
    main.distribute_gifts()
    print(main.toys)
    print(main.nice_kids)
    print(main.naughty_kids)
