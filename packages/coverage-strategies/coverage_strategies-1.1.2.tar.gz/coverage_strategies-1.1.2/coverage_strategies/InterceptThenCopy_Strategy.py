import sys

from coverage_strategies.Dijkstra import dijkstra, shortest, Graph, get_graph_from_board
from coverage_strategies.Entities import Strategy, Slot, Board, Agent
from coverage_strategies.SpanningTreeCoverage import is_slot_shallow_obstacle



def get_interception_point(steps_o, InitPosX, InitPosY, agentO:Agent):
    ip_x = -1
    ip_y = -1

    steps_counter = 0
    g = get_graph_from_board(agentO.gameBoard)
    start = Slot(InitPosX, InitPosY)
    path_to = []
    for step in steps_o:
        steps_counter += 1

        # computing the distance should be done using dijkstra, since now we allow obstacles
        # create graph from Board (with obstacles)

        dijkstra(g, g.get_vertex(start), g.get_vertex(step))

        target = g.get_vertex(step)
        path = [target.get_id()]
        shortest(target, path)
        # print('The shortest path : %s' % (path[::-1]))

        distance_from_i_r = len(path[::-1])
        if steps_counter > distance_from_i_r:
            ip_x, ip_y = step.row, step.col
            path_to = path[::-1]
            break

    assert (ip_x != -1 and ip_y != -1)

    return Slot(ip_x, ip_y), len(path_to), path_to


class InterceptThenCopy_Strategy(Strategy):
    def get_steps(self, agent_r, board_size=50, agent_o=None):
        # steps_o = StrategyGenerator.get_strategy_from_enum(agent_o.StrategyEnum).get_steps(agent_o, board_size,
        #                                                                                    board_size)
        steps_o = agent_o.steps

        # Find interception point
        (interceptionPoint_R_O, distance, path_to_interception_point) = get_interception_point(steps_o, agent_r.InitPosX, agent_r.InitPosY, agent_o)
        steps_r = run_agent_over_board_interception_strategy(steps_o, path_to_interception_point)
        return steps_r


def run_agent_over_board_interception_strategy(steps_o, path_to):
    steps = []
    steps.extend(path_to)
    steps.extend(steps_o[(steps_o.index(path_to[-1])+1):])

    return steps


# --------------------------------------
