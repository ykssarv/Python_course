import random
import matplotlib.pyplot as plt
from strategy import Strategy
random.seed()


class Binomial:

    n_min = 200
    n_max = 400
    nc_min = 0.3
    nc_max = 0.6

    r_min = 30
    r_max = 75
    rc_min = 0.6
    rc_max = 0.9

    t_min = 5
    t_max = 10
    tc_min = 0.1
    tc_max = 0.25

    def __init__(self, dist_type):
        if dist_type == "N":
            self.n = random.randint(Binomial.n_min, Binomial.n_max)
            self.p = random.uniform(Binomial.nc_min, Binomial.nc_max)
        if dist_type == "R":
            self.n = random.randint(Binomial.r_min, Binomial.r_max)
            self.p = random.uniform(Binomial.rc_min, Binomial.rc_max)
        if dist_type == "T":
            self.n = random.randint(Binomial.t_min, Binomial.t_max)
            self.p = random.uniform(Binomial.tc_min, Binomial.tc_max)
        self.generated = []

    def get_value(self, i):
        while i >= len(self.generated):
            self.generate()
        return self.generated[i]

    def generate(self):
        value = 0
        for i in range(self.n):
            if random.random() <= self.p:
                value += 1
        self.generated.append(value)


class Galaxy:
    def __init__(self, is_interim):
        self.n, self.r, self.t = self.generate_distributions()
        self.a, self.b, self.c, self.d, self.m = self.generate_initial()
        self.interim_dates = self.generate_interim() if is_interim else []
        self.planets = []
        self.agents = []
        self.strategies = []
        self.days_past = 0

    def get_winner(self):
        return max(self.agents, key=lambda x: x.production).name

    def add_strategy(self, strategy):
        self.strategies.append(strategy)
        self.agents.append(Agent(self.c, strategy.name, self.d))

    def get_initial_params(self):
        return self.a, self.b, self.c, self.d, self.m

    def generate_interim(self):
        dates = []
        for i in range(5):
            dates.append(random.randint(0, self.b - 1))
        dates.sort()
        return dates

    def generate_initial(self):
        return random.randint(5, 15), \
               random.randint(1000, 2000), \
               random.randint(1000, 2000), \
               random.randint(100, 200), \
               random.randint(50, 100)

    def generate_distributions(self):
        return Binomial("N"), Binomial("R"), Binomial("T")

    def get_planet(self, planet_id):
        return [
            planet_id,
            self.n.get_value(planet_id),
            self.r.get_value(planet_id),
            self.t.get_value(planet_id)
        ]

    def day(self):
        self.days_past += 1
        for agent, strategy in zip(self.agents, self.strategies):
            actions = strategy.get_actions()
            answer = self.parse_actions(agent, actions)
            if isinstance(answer, str):
                return "ERROR: " + answer
            strategy.give_results(answer)
            agent.add_resources()
            strategy.sync(self.days_past, self.b - self.days_past, agent.resources, agent.production, agent.planets)
            #print(agent.planets)

    def parse_actions(self, agent, actions):
        answer = []
        planets_explored = 0
        if len(actions) > self.a:
            return f"Agent {agent.name} had too many actions"
        for action in actions:
            if action == "explore":
                agent.resources -= self.m
                planet = self.get_planet(agent.planet_count + planets_explored)
                agent.add_planet(planet[1], planet[2], planet[3])
                answer.append(planet)
                planets_explored += 1
            if isinstance(action, int):
                answer.append(None)
                if action >= agent.planet_count:
                    return f"Agent {agent.name} hasn't explored planet {action}"
                if agent.planets_left[action] == 0:
                    return f"Agent {agent.name} has already fully colonized planet {action}"
                agent.resources -= self.r.get_value(action)
                agent.planets_left[action] -= 1
                agent.planets[action][0] -= 1
                agent.colonizing[action] = agent.planets_left[action]
                if agent.planets_left[action] == 0:
                    agent.colonizing.pop(action, None)
                    agent.production += self.t.get_value(action)
        if agent.resources < 0:
            return f"Agent {agent.name} doesn't have money for those actions {actions}, missing {- agent.resources} resources"
        if self.days_past in self.interim_dates:
            if len(agent.colonizing.keys()) > 0:
                return f"Agent {agent.name} had in process colonizations after day {self.days_past}"
        agent.planet_count += planets_explored
        return answer

    def display(self):
        fig, ax = plt.subplots(2)
        for agent in self.agents:
            ax[0].plot(agent.resource_history)
            ax[1].plot(agent.production_history)
        plt.show()


class Agent:
    def __init__(self, resources, name, production):
        self.name = name
        self.resources = resources
        self.planet_count = 0
        self.planets_left = []
        self.resource_history = []
        self.production_history = []
        self.production = production
        self.planets = []
        self.colonizing = {}

    def add_planet(self, steps, to_spend, production):
        self.planets_left.append(steps)
        self.planets.append([steps, to_spend, production])

    def add_resources(self):
        self.resources += self.production
        self.resource_history.append(self.resources)
        self.production_history.append(self.production)

if __name__ == '__main__':
    is_interim = True
    galaxy = Galaxy(is_interim)
    a, b, c, d, m = galaxy.get_initial_params()
    # basic = BasicStrategy(a, b, c, d, m, galaxy.interim_dates, "Basic")
    # advanced = AdvancedStrategy(a, b, c, d, m, galaxy.interim_dates, "Advanced")
    student = Strategy(a, b, c, d, m, galaxy.interim_dates, "Student")
    # galaxy.add_strategy(basic)
    # galaxy.add_strategy(advanced)
    galaxy.add_strategy(student)
    for j in range(b):
        print(j)
        feedback = galaxy.day()
        print(j)
        if feedback:
            print(feedback)
            break
    print(student.planets)
    galaxy.display()