"""Board games."""


class Statistics:
    """Statistics class."""

    def __init__(self, filename):
        """Init."""
        file = open(filename, 'r')
        lines = file.readlines()
        self.games_inf = []
        self.player_names = set()
        self.total = 0
        self.players = {}
        self.games = {}

        for line in lines:
            game = OneGame(line, self.players, self.games)
            self.games_inf.append(game)

            self.player_names = self.player_names.union(game.players)
            self.total += 1

    def get_players(self):
        """Return a list of players."""
        return list(self.player_names)

    def get_games(self):
        """Return a list of game names."""
        return list(self.games)

    def get_total(self):
        """Return total number of games played."""
        return self.total

    def get_total_of_type(self, result_type):
        """Return total number of games of a specific type."""
        return len([x for x in self.games_inf if result_type == x.type])

    def get(self, path):
        """Get."""
        split_path = path.strip("/").split("/")
        if len(split_path) == 1:
            if split_path[0] == "players":
                return self.get_players()
            elif split_path[0] == "games":
                return self.get_games()
            else:
                return self.get_total()
        elif len(split_path) == 2:
            if split_path[0] == "total":
                return self.get_total_of_type(split_path[1])
        else:
            if split_path[0] == "player":
                if split_path[2] == "amount":
                    return self.get_amount_for_player(split_path[1])
                elif split_path[2] == "favourite":
                    return self.get_favourite_game_of_player(split_path[1])
                else:
                    return self.get_wins_for_player(split_path[1])
            elif split_path[0] == "game":
                return self.get_for_game(split_path)

    def get_for_game(self, split_path):
        """Get for game."""
        if split_path[2] == "amount":
            return self.get_game_name_amount(split_path[1])
        elif split_path[2] == "player-amount":
            return self.get_game_player_amount(split_path[1])
        elif split_path[2] == "most-wins":
            return self.get_most_wins(split_path[1])
        elif split_path[2] == "most-frequent-winner":
            return self.get_most_frequent_winner(split_path[1])
        elif split_path[2] == "most-losses":
            return self.get_most_losses(split_path[1])
        elif split_path[2] == "most-frequent-loser":
            return self.get_most_frequent_loser(split_path[1])
        else:
            return self.get_record_holder(split_path[1])

    def get_amount_for_player(self, name):
        """Return the amount of games a player has played."""
        return self.players[name].amount

    def get_wins_for_player(self, name):
        """Return the amount of wins of a player."""
        return self.players[name].wins

    def get_favourite_game_of_player(self, name):
        """Get the game a player has played the most."""
        return sorted(self.players[name].games_played.items(), key=lambda x: x[1])[-1][0]

    def get_game_name_amount(self, name):
        """Get the amount of the specific game."""
        return self.games[name].amount

    def get_most_wins(self, name):
        """Get the player with most wins."""
        return sorted(self.games[name].wins_of_player.items(), key=lambda x: x[1])[-1][0]

    def get_game_player_amount(self, name):
        """The most frequent number of players."""
        return sorted(self.games[name].game_player_amount.items(), key=lambda x: x[1])[-1][0]

    def get_most_frequent_winner(self, name):
        """The most frequent winner of a specific game."""
        return sorted(self.games[name].wins_of_player.items(), key=lambda x: x[1] / self.players[x[0]].games_played[name])[-1][0]

    def get_most_losses(self, name):
        """Get the player with most losses."""
        return sorted(self.games[name].losses_of_player.items(), key=lambda x: x[1])[-1][0]

    def get_most_frequent_loser(self, name):
        """Get the most frequent loser of a game."""
        return sorted(self.games[name].losses_of_player.items(), key=lambda x: x[1] / self.players[x[0]].games_played[name])[-1][0]

    def get_record_holder(self, name):
        """Get the person that holds a record for the most points in a specific game."""
        return self.games[name].record_holder


class OneGame:
    """One game."""

    def __init__(self, raw_line, all_players, games):
        """Init."""
        self.game_inf = raw_line.strip().split(';')
        self.players = self.game_inf[1].split(',')
        self.name = self.game_inf[0]
        self.type = self.game_inf[2]
        self.games = games

        for player in self.players:
            if player not in all_players:
                all_players[player] = Player(player)
            all_players[player].amount += 1
            all_players[player].add_game(self.name)
            if all_players[player].name == self.get_winner():
                all_players[player].wins += 1

        if self.name not in self.games.keys():
            self.games[self.name] = Game(self.name)
        self.games[self.name].amount += 1

        if len(self.players) in self.games[self.name].game_player_amount.keys():
            self.games[self.name].game_player_amount[len(self.players)] += 1
        else:
            self.games[self.name].game_player_amount[len(self.players)] = 1

        if self.get_winner() in self.games[self.name].wins_of_player.keys():
            self.games[self.name].wins_of_player[self.get_winner()] += 1
        else:
            self.games[self.name].wins_of_player[self.get_winner()] = 1

        if self.get_loser() in self.games[self.name].losses_of_player.keys():
            self.games[self.name].losses_of_player[self.get_loser()] += 1
        else:
            self.games[self.name].losses_of_player[self.get_loser()] = 1

        if self.type == "points":
            scores = [int(x) for x in self.game_inf[3].split(",")]
            max_score = max(scores)
            if max_score > self.games[self.name].record:
                self.games[self.name].record = max_score
                self.games[self.name].record_holder = self.get_winner()

    def get_winner(self):
        """Get the winner."""
        if self.type == "winner":
            return self.game_inf[3]
        if self.type == "places":
            return self.game_inf[3].split(",")[0]
        if self.type == "points":
            scores = [int(x) for x in self.game_inf[3].split(",")]
            max_score = max(scores)
            index = scores.index(max_score)
            return self.players[index]

    def get_loser(self):
        """Get the loser."""
        if self.type == "places":
            return self.game_inf[3].split(",")[-1]
        if self.type == "points":
            scores = [int(x) for x in self.game_inf[3].split(",")]
            min_score = min(scores)
            index = scores.index(min_score)
            return self.players[index]


class Player:
    """Player."""

    def __init__(self, name):
        """Init."""
        self.name = name
        self.amount = 0
        self.games_played = {}
        self.wins = 0

    def add_game(self, game_name):
        """Add game."""
        if game_name in self.games_played.keys():
            self.games_played[game_name] += 1
        else:
            self.games_played[game_name] = 1


class Game:
    """Game."""

    def __init__(self, name):
        """Init."""
        self.name = name
        self.amount = 0
        self.game_player_amount = {}
        self.wins_of_player = {}
        self.losses_of_player = {}
        self.record = 0
        self.record_holder = ""


if __name__ == "__main__":
    statistics = Statistics("gristjanvoidap.txt")
    print(statistics.players)
