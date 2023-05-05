"""Strategy."""


class Strategy:
    """Strategy."""

    def __init__(self, teams, days, initial_resources, initial_production, exploration_cost, interim_reports, name):
        """The initial parameters are given at the start."""
        self.name = name
        self.teams = teams
        self.days = days
        self.resources = initial_resources
        self.production = initial_production
        self.exp_cost = exploration_cost
        self.reports = interim_reports + [self.days]
        self.planets = []
        self.current = 0

        self.working_on = None
        self.teams_left = 0
        self.actions = []
        self.days_left = 0
        self.done = False

    def finish_working_on(self):
        """Finish working on."""
        if self.done:
            return
        if self.working_on:
            print(f"Working on: {self.working_on[0]}")
            amount_to_colonize = min(self.teams_left, self.working_on[1], self.resources // self.working_on[2])
            self.working_on[1] -= amount_to_colonize
            self.teams_left -= amount_to_colonize
            self.resources -= amount_to_colonize * self.working_on[2]
            self.actions += [self.working_on[0]] * amount_to_colonize
            if self.working_on[1] > 0:
                print("Didn't finish work")
                self.done = True
                return
            self.production += self.working_on[3]
            print("Finished work")
            self.working_on = None

    def check_new_planets(self):
        """Check new planets."""
        if self.done:
            return
        for planet in self.planets[:len(self.planets) // 5]:
            if planet[1] == 0:
                continue
            if self.teams_left == 0:
                break
            if self.resources // planet[2] == 0:
                break
            amount_to_colonize = min(self.teams_left, planet[1], self.resources // planet[2])

            # If not enough resources to finish
            if amount_to_colonize < planet[1] and len(self.reports) > 1:
                total_teams = self.teams_left + self.days_left * self.teams
                total_resources = self.resources + self.days_left * self.production
                if planet[1] > total_teams or planet[1] * planet[2] > total_resources:
                    continue

            self.actions += [planet[0]] * amount_to_colonize
            self.teams_left -= amount_to_colonize
            self.resources -= amount_to_colonize * planet[2]
            planet[1] -= amount_to_colonize
            if planet[1] == 0:
                self.production += planet[3]
            elif len(self.reports) > 1:
                self.working_on = planet
                self.done = True
                return

    def explore(self):
        """Explore."""
        if self.done:
            return
        exp_amount = min(self.teams_left, self.resources // self.exp_cost)
        self.resources -= exp_amount * self.exp_cost
        self.actions += ['explore'] * exp_amount
        self.done = True

    def get_actions(self):
        """
        Called at the beginning of each day.

        Return a list of actions describing what your teams will do.
        (you may return less actions than you have teams, but not more)

        If you wish to explore with a team,
        then the corresponding list element
        should be the string "explore".

        If you wish to work towards colonizing a planet,
        then the corresponding list element
        should be an integer with the planet's ID.
        """
        self.teams_left = self.teams
        self.actions = []
        self.days_left = min([day for day in self.reports if day >= self.current]) - self.current - 1
        self.done = False
        print(f"Days left: {self.days_left}")

        self.finish_working_on()
        self.check_new_planets()
        self.explore()
        return self.actions

    def give_results(self, results):
        """
        Called at the end of each day.

        'results' will be a list, describing what each of your teams did.

        If the corresponding team was sent out to explore,
        then the element will be a list of 4 int's describing the planet that they found. [ID, N, R, T]

        If the corresponding team was sent out to colonize a planet,
        then the element will simply be none.
        """
        for result in results:
            if isinstance(result, list):
                self.planets.append(result)
                print(result)

    def sync(self, days_past, days_left, resources, production, planets):
        """
        Called each day after 'give_results'.

        It is completely possible to keep your data
        about the galaxy and humanity's resources in sync with reality
        using only the 'init', 'get_actions' and 'give_results' functions,
        but if you for some reason don't want to do that,
        then this function should give you all of the information
        about the current state of the galaxy.

        If you keep track of it yourself,
        feel free to ignore this function,
        it is only meant to simplify things for those,
        who are unsure of their ability to track said information correctly.

        days_past will be an int that describes how many days have passed.
        days_left will be an int that describes how many days are left until POTUS'es report.
        resources will be an int describing how many resources humanity has at their disposal currently
        production will be an int describing how many resources humanity gets each day
        (production for the day that just passed has already been added to resources)
        planets will be a list of all the planets,
        that humanity has discovered,
        where the index, is the same as the ID
        and each element will be a list [N_l, R, T],
        where N_l, is the amount of days left,
        for the planet to be colonized.
        If N_l is 0, then the planet is colonized and is producing resources.
        """
        self.resources += self.production
        self.planets = sorted(self.planets, key=lambda x: (x[1] * x[2]) / x[3] if x[3] > 0 else 999999999999999)
        self.current += 1
