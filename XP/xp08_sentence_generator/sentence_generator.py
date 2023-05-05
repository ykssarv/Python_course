"""Sentence generator."""


class Rule:
    """Single rule."""

    def __init__(self, rules, name):
        """Init."""
        self.name = name
        self.all_rules = rules
        self.rules = []
        self.counter = 0
        self.problematic = False
        self.punctuation = '.,?!'

    def add_rules(self, rule_string):
        """Add rule."""
        possibilities = rule_string.split(" | ")
        self.rules += [x.split(" ") for x in possibilities]
        self.problematic = True
        for rule in self.rules:
            if self.name not in [x.rstrip(self.punctuation) for x in rule]:
                self.problematic = False

    def get_result(self):
        """Get result."""
        rule = self.rules[self.counter]
        self.counter = (self.counter + 1) % len(self.rules)
        result = []
        for part in rule:
            if part.rstrip(self.punctuation) in self.all_rules.keys():
                if self.problematic:
                    res = "???"
                else:
                    raw_part = part.rstrip(self.punctuation)
                    res = self.all_rules[raw_part].get_result()
                    res = part.replace(raw_part, res)
                result.append(res)
            else:
                result.append(part)
        return " ".join(result)


class SentenceGenerator:
    """Sentence generator."""

    def __init__(self, rules_string):
        """Init."""
        self.rules = {}
        for rule in rules_string.split("\n"):
            split_rule = rule.split(" = ")
            if len(split_rule) != 2:
                continue
            name = split_rule[0].strip()
            if name not in self.rules.keys():
                self.rules[name] = Rule(self.rules, name)
            self.rules[name].add_rules(split_rule[1].strip())

    def sentence_generator(self, syntax):
        """Sentence generator."""
        rule = Rule(self.rules, None)
        rule.add_rules(syntax)
        while True:
            yield rule.get_result()


if __name__ == '__main__':
    rules = """
    a = tere | tulemast
    b = a?
    """
    g = SentenceGenerator(rules)
    gg = g.sentence_generator("a b b")
    print(next(gg))
    print(next(gg))
    print(next(gg))
    print(next(gg))
    print(next(gg))
    print(next(gg))
    print(next(gg))
