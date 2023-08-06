from abc import ABCMeta
from abc import abstractmethod
from enum import Enum
import numpy as np

from coverage_strategies.Dijkstra import get_graph_from_board, dijkstra, shortest
from coverage_strategies.SpanningTreeCoverage import is_slot_shallow_obstacle


class Board:
    def __init__(self, rows, cols):
        self.Rows = rows
        self.Cols = cols
        self.Slots = [[Slot(y, x) for x in range(self.Rows)] for y in range(self.Cols)]
        self.Obstacles = []

    def __str__(self):
        s = ''
        for i in range(len(self.Slots)):
            for j in range(len(self.Slots[i])):
                s += str(self.Slots[i][j])
            s += '\n'
        return s

    def reset(self):
        for s in self.Slots:
            s.has_been_visited = False
            s.is_occupied = False
            s.covered_by = "*"

    def populate_with_obstacles(self, percentage: float, init_positions: list):
        import random
        obs = []

        def get_shallow_obs(b: Board, o):
            return [i for j in b.Slots for i in j if is_slot_shallow_obstacle(i, o)]

        def is_still_connected():
            leveled_slots = assign_level_to_slots(self, Slot(0, 0), levelType=4)
            return self.Rows*self.Cols - len(self.get_shallow_obstacles()) == len(leveled_slots)
            # return not any([ss not in leveled_slots and not is_slot_shallow_obstacle(ss, self.Obstacles) for ss in [i for j in self.Slots for i in j]])

        while len(self.get_shallow_obstacles()) < (percentage / 100.0) * self.Rows * self.Cols:
            o = random.choice([i for j in self.Slots for i in j
                               if i not in self.Obstacles and
                               i not in init_positions and
                               0 < i.row < self.Rows - 1 and
                               0 < i.col < self.Cols - 1])

            self.Obstacles.append(o)
            if not is_still_connected():
                self.Obstacles.remove(o)

    def get_shallow_obstacles(self):
        return [s for sl in self.Slots for s in sl if is_slot_shallow_obstacle(s, self.Obstacles)]

class Slot:
    def __init__(self, x, y):
        self.has_been_visited = False
        self.covered_by = "*"
        self.row = x
        self.col = y
        self.Name = "(" + str(x) + "," + str(y) + ")"

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __ne__(self, other):
        return self.row != other.row or self.col != other.col

    def __hash__(self):
        return hash((self.row, self.col))

    def go_west(self):
        return Slot(self.row, self.col - 1)

    def go_east(self):
        return Slot(self.row, self.col + 1)

    def go_north(self):
        return Slot(self.row - 1, self.col)

    def go_south(self):
        return Slot(self.row + 1, self.col)

    def in_bounds(self, board: Board):
        return 0 <= self.row < board.Rows and 0 <= self.col < board.Cols

    def go(self, s, opposite_direction=False):
        """
        Go South, East, North or West, according to the given parameter.
        :param s: Must by 'd', 'r','n','l'
        :param opposite_direction: False by default. Move to the opposite direction
        :return: the new slot
        """
        assert s == 'u' or s == 'd' or s == 'r' or s == 'l'

        if opposite_direction:
            if s == 'u':
                s = 'd'
            if s == 'd':
                s = 'u'
            if s == 'r':
                s = 'l'
            if s == 'l':
                s = 'r'

        if s == 'u':
            return self.go_north()
        if s == 'd':
            return self.go_south()
        if s == 'r':
            return self.go_east()
        if s == 'l':
            return self.go_west()

    def to_tuple(self):
        return self.row, self.col

    def __str__(self):
        return "({0},{1})".format(str(int(self.row)), str(int(self.col)))

    def __repr__(self):
        return str(self)

    def get_inbound_neighbors(self, board: Board):
        return [i for i in [self.go_south(), self.go_east(), self.go_west(), self.go_north()] if i.in_bounds(board)]

    def get_8_inbound_neighbors(self, board: Board):
        return [i for i in [self.go_south(),
                            self.go_east(),
                            self.go_west(),
                            self.go_north(),
                            self.go_south().go_west(),
                            self.go_north().go_west(),
                            self.go_south().go_east(),
                            self.go_north().go_east()]
                if i.in_bounds(board)]


class StrategyEnum(Enum):
    VerticalCoverageCircular = 0
    HorizontalCoverageCircular = 1
    FullKnowledgeInterceptionCircular = 2
    QuartersCoverageCircular = 3
    RandomSTC = 4
    VerticalCoverageNonCircular = 5
    SpiralingOut = 6
    SpiralingIn = 7
    VerticalFromFarthestCorner_OpponentAware = 8
    SemiCyclingFromFarthestCorner_OpponentAware = 9
    CircleOutsideFromIo = 10,
    LCP = 11,
    LONGEST_TO_REACH = 12,
    TRULY_RANDOM = 13,
    SemiCyclingFromAdjacentCorner_col_OpponentAware = 14,
    SemiCyclingFromAdjacentCorner_row_OpponentAware = 15


class Agent:
    def __init__(self, name: str, strategy_enum: StrategyEnum, x: int, y: int, board: Board = None,
                 agent_o: object = None) -> None:

        assert isinstance(strategy_enum, Enum)

        self.Name = name
        self.StrategyEnum = strategy_enum
        self.InitPosX = x
        self.InitPosY = y
        self.gameBoard = board

        from coverage_strategies.StrategyGenerator import get_strategy_from_enum
        self.Strategy = get_strategy_from_enum(strategy_enum)
        self.steps = self.Strategy.get_steps(self, len(board.Slots), agent_o)

    def get_tdv(self):
        from math import fabs
        return sum([(1 / (1 + stepI)) * (
                    fabs(self.steps[stepI].row - self.steps[0].row) + fabs(self.steps[stepI].col - self.steps[0].col))
                    for stepI in range(len(self.steps))])

    def get_frame(self):
        pass

    def get_strategy(self):
        return self.Strategy.__str__()

    def get_strategy_short(self):
        return self.get_strategy()[:5] + "..."

    def display_heat_map(self, x, y):
        arr = self.get_heatmap()
        # DisplayingClass.create_heat_map(arr, x, y, self.get_strategy_short())

    def get_heatmap(self):
        arr = np.zeros((self.gameBoard.Rows, self.gameBoard.Cols))
        for id in range(len(self.steps)):
            if arr[self.steps[id].row][self.steps[id].col] == 0:
                arr[self.steps[id].row][self.steps[id].col] = id
        return arr

    def get_cross_heatmap(self, other, probabilities=[0.5, 0.5]):
        my_hm = probabilities[0] * self.get_heatmap()
        o_hm = probabilities[1] * other.get_heatmap()
        return np.add(my_hm, o_hm)

    def get_sub_heatmap(self, other_hm, probabilities=[0.5, 0.5]):
        my_hm = probabilities[0] * self.get_heatmap()
        o_hm = probabilities[1] * other_hm
        return np.subtract(my_hm, o_hm)

    # def display_cross_heatmap(self, other, display_grid_x, display_grid_y, probabilities):
    #     c = self.get_cross_heatmap(other, probabilities)
    #     DisplayingClass.create_heat_map(c, display_grid_x, display_grid_y,
    #                                     "comb. of \n({0} and \n{1}):".format(
    #                                         str(self.get_strategy_short()), str(other.get_strategy_short())))
    #     return c

    # def display_sub_heatmap(self, other_hm, display_grid_x, display_grid_y, probabilities):
    #     c = self.get_sub_heatmap(other_hm, probabilities)
    #     #
    #     # DisplayingClass.create_heat_map(c, display_grid_x, display_grid_y,
    #     #                                 "subs. sum: {}\navg: {}\n std: {}".format(np.sum(c),
    #     #                                                                           np.average(c),
    #     #                                                                           np.std(c)))


class Game:
    def __init__(self, agent_r: Agent, agent_o: Agent, size=(100, 100)) -> None:
        self._board = agent_r.gameBoard
        self._agentR = agent_r
        self._agentO = agent_o

    def run_game(self, enforce_paths_length=False):
        steps_r = self._agentR.steps
        steps_o = self._agentO.steps

        if enforce_paths_length:
            if not len(steps_o) == len(steps_r):
                raise AssertionError(
                    "wrong length! len(steps_o)={}, len(steps_r)={}".format(len(steps_o), len(steps_r)))

        for curr_slot in [s for sl in self._board.Slots for s in sl
                          if not is_slot_shallow_obstacle(s, self._agentO.gameBoard.Obstacles)]:
            # print(self._agentO.gameBoard.Obstacles)
            # exit(1)
            ri = steps_r.index(curr_slot)
            oi = steps_o.index(curr_slot)
            curr_slot.has_been_visited = True
            curr_slot.covered_by = self._agentO.Name if oi < ri else self._agentR.Name

        # make sure all cells, which are not obstacles, are covered
        assert all([(True if self._board.Slots[i][j].has_been_visited else False)
                    for i in range(self._board.Rows) for j in range(self._board.Cols)
                    if not is_slot_shallow_obstacle(Slot(i, j), self.board.Obstacles)])
        return self.get_r_gain(), self.get_o_gain()

    def get_r_gain(self):
        return float(len([s for sl in self._board.Slots for s in sl if s.covered_by == self._agentR.Name]))

    def get_o_gain(self):
        return float(len([s for sl in self._board.Slots for s in sl if s.covered_by == self._agentO.Name]))

    @property
    def board(self):
        return self._board


class Strategy:
    __metaclass__ = ABCMeta
    steps = []  # type: list[Slot]

    def __init__(self):
        self.steps = []
        self.set_steps = set()

    def __str__(self):
        return self.__class__.__name__

    @classmethod
    @abstractmethod
    def get_steps(self, agent_r, board_size=50, agent_o=None):
        """Returns the steps agent perform to cover the world"""

    @classmethod
    def go_from_a_to_b(self, a, b):
        """
        Returns a list of steps from A to B
        :param a: First Slot
        :param b: Second Slot
        :return: list of steps from A to B
        """

        current_step = a
        steps_to_return = [current_step]

        while not current_step.row == b.row:
            current_step = current_step.go_north() if b.row < a.row else current_step.go_south()
            steps_to_return.append(current_step)

        while not current_step.col == b.col:
            current_step = current_step.go_east() if b.col > a.col else current_step.go_west()
            steps_to_return.append(current_step)

        return steps_to_return

    @classmethod
    def go_from_a_to_b_dijkstra(self, a, b, board):
        g = get_graph_from_board(board)
        dijkstra(g, g.get_vertex(a), g.get_vertex(b))

        target = g.get_vertex(b)
        path = [target.get_id()]
        shortest(target, path)

        return path[::-1]

    @classmethod
    def get_farthest_corner(self, a, board_size):
        """
        return the farthest corner from a given position
        :param a: the given position
        :param board_size: the size of the given game board
        :return: the farthest corner from A
        """
        f_row = 0 if a.row > board_size / 2 else board_size - 1
        f_col = 0 if a.col > board_size / 2 else board_size - 1
        return Slot(f_row, f_col)


def assign_level_to_slots(board: Board, init: Slot, levelType: int = 8):
    leveled_vertices = {}

    # Mark all the vertices as not visited
    visited = {i: False for j in board.Slots for i in j}
    queue = [(init, 0)]
    visited[init] = True
    while queue:
        s, l = queue.pop(0)
        leveled_vertices[s] = l

        # Get all adjacent vertices of the
        # dequeued vertex s. If a adjacent
        # has not been visited, then mark it
        # visited and enqueue it.
        # all unvisited neighbors get level value of +1 of the current level value

        neighbors = s.get_inbound_neighbors(board) if levelType == 4 else s.get_8_inbound_neighbors(board)

        for i in [i for i in neighbors if not is_slot_shallow_obstacle(i, board.Obstacles)]:
            if not visited.get(i):
                queue.append((i, l + 1))
                visited[i] = True

    return leveled_vertices


def display_board(b: Board):
    """
    takes in a board, and saves it as a csv file.
    :param b:
    :return:
    """
    import csv
    with open('./board.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        shallows = b.get_shallow_obstacles()
        writer.writerows([[(' ' if j not in shallows else '*') for j in i] for i in b.Slots])
