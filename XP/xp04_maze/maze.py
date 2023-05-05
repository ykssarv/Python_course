"""Maze."""

from queue import PriorityQueue


class Node:
    """Node."""

    def __init__(self, location, cost, is_door):
        """Init."""
        self.location = location
        self.cost = cost
        self.is_door = is_door
        self.neighbours = []

    def add_neighbour(self, neighbour_location):
        """Add neighbour."""
        self.neighbours.append(neighbour_location)


class MazeSolver:
    """Solve."""

    def __init__(self, maze_str: str, configuration: dict = None):
        """
        Initialize the solver with map string and configuration.

        Map string can consist of several lines, line break separates the lines.
        Empty lines in the beginning and in the end should be ignored.
        Line can also consist of spaces, so the lines cannot be stripped.

        On the left and right sides there can be several doors (marked with "|").
        Solving the maze starts from a door from the left side and ends at the door on the right side.
        See more @solve().

        Configuration is a dict which indicates which symbols in the map string have what cost.
        Doors (|) are not shown in the configuration and are not used inside the maze.
        Door cell cost is 0.
        When a symbol on the map string is not in configuration, its cost is 0.
        Cells with negative cost cannot be moved on/through.

        Default configuration:
        configuration = {
            ' ': 1,
            '#': -1,
            '.': 2,
            '-': 5,
            'w': 10
        }

        :param maze_str: Map string
        :param configuration: Optional dictionary of symbol costs.
        """
        if configuration is None:
            configuration = {
                ' ': 1,
                '#': -1,
                '.': 2,
                '-': 5,
                'w': 10
            }
        self.nodes = {}
        self.starts = []
        self.ends = []
        self.maze = maze_str.strip(' \n').split('\n')
        for y, row in enumerate(self.maze):
            for x, symbol in enumerate(row):
                if symbol == '|':
                    if x == 0:
                        self.starts.append((y, x))
                    else:
                        self.ends.append((y, x))
                if symbol in configuration.keys() and configuration[symbol] < 0:
                    continue
                is_door = symbol == '|'
                cost = 0 if symbol not in configuration.keys() else configuration[symbol]
                self.nodes[(y, x)] = Node((y, x), cost, is_door)
                for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                    this_x = x + dx
                    this_y = y + dy
                    if this_x < 0 or this_y < 0 or this_x >= len(row) or this_y >= len(self.maze):
                        continue
                    neighbour = self.maze[this_y][this_x]
                    if neighbour in configuration.keys() and configuration[neighbour] < 0:
                        continue
                    self.nodes[(y, x)].add_neighbour((this_y, this_x))

    def get_shortest_path(self, start: tuple, goal: tuple) -> tuple:
        """
        Return shortest path and the total cost of it.

        The shortest path is the path which has the lowest cost.
        Start and end are tuples of (y, x) where the first (upper) line is y = 0.
        The path should include both the start and the end.

        If there is no path from the start to goal, the path is None and cost is -1.

        If there are several paths with the same lowest cost, return any of those.

        :param start: Starting cell (y, x)
        :param goal: Goal cell (y, x)
        :return: shortest_path, cost
        """
        explored = {}
        front = PriorityQueue()
        explored[start] = (0, None)
        for neighbour in self.nodes[start].neighbours:
            neighbour_node = self.nodes[neighbour]
            front.put((neighbour_node.cost, neighbour_node.location, start))
        while True:
            if front.empty():
                break
            cost, location, came_from = front.get()
            if location in explored.keys():
                continue
            # print(location)
            explored[location] = (cost, came_from)
            if location == goal:
                break
            for neighbour in self.nodes[location].neighbours:
                if neighbour in explored.keys():
                    continue
                neighbour_node = self.nodes[neighbour]
                front.put((cost + neighbour_node.cost, neighbour_node.location, location))
        if goal not in explored.keys():
            return None, -1
        path = []
        cost = explored[goal][0]
        current = goal
        while current is not None:
            path.append(current)
            current = explored[current][1]
        return path[::-1], cost

    def solve(self) -> tuple:
        """
        Solve the given maze and return the path and the cost.

        Finds the shortest path from one of the doors on the left side to the one of the doors on the right side.
        Shortest path is the one with the lowest cost.

        This method should use get_shortest_path method and return the same values.
        If there are several paths with the same cost, return any of those.

        :return: shortest_path, cost
        """
        solution = None
        shortest = -1
        for start in self.starts:
            for end in self.ends:
                this_solution, this_length = self.get_shortest_path(start, end)
                # print(f"{start} to {end}, path is {this_solution}")
                if shortest < 0 or 0 < this_length <= shortest:
                    if this_solution is None or this_length == shortest and len(solution) < len(this_solution):
                        continue
                    shortest = this_length
                    solution = this_solution
        return solution, shortest

    def locate(self, area: str, x: int, y: int, unknown: str = None) -> list:
        """
        Locate yourself in a already known maze.

        Note that (0, 0) is top left corner

        :param area: area you know around you.
        :param x: x-coord relative to known area
        :param y: y-coord relative to known area
        :param unknown: single char that represents unknown squares in area param

        :return list of tuple(y, x) with coordinates of your location in big/known maze (all possible locations)
        """
        area = area.split('\n')
        possibilities = []
        for dy in range(len(self.maze) - len(area) + 1):
            for dx in range(len(self.maze[0]) - len(area[0]) + 1):
                possible = True
                for this_y, row in enumerate(area):
                    for this_x, symbol in enumerate(row):
                        if symbol == unknown:
                            continue
                        if symbol != self.maze[this_y + dy][this_x + dx]:
                            possible = False
                            break
                    if not possible:
                        break
                if possible:
                    possibilities.append((y + dy, x + dx))
        return possibilities


if __name__ == '__main__':
    maze = """
####
#  |
|# #
####
"""
    solver = MazeSolver(maze)
    assert solver.solve() == ([(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7)], 6)
    assert solver.get_shortest_path((3, 0), (3, 1)) == ([(3, 0), (3, 1)], 1)
    assert solver.get_shortest_path((3, 0), (2, 0)) == (None, -1)

    maze = """
#####
#   #
| # #
# # |
#####
    """
    solver = MazeSolver(maze)
    assert solver.solve() == ([(2, 0), (2, 1), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 4)], 6)

    maze = """
#####
#   |
#   |
| # #
#####
| # |
#####
    """
    solver = MazeSolver(maze)
    print("PRESOLVE")
    print(solver.solve())
    assert solver.solve() == ([(3, 0), (3, 1), (2, 1), (2, 2), (2, 3), (2, 4)], 4)
    print(solver.get_shortest_path((3, 0), (1, 4)))
    # multiple paths possible, let's just assert the cost
    assert solver.get_shortest_path((3, 0), (1, 4))[1] == 4  # using the door at (2, 4)
    assert solver.get_shortest_path((5, 0), (5, 4)) == (None, -1)
