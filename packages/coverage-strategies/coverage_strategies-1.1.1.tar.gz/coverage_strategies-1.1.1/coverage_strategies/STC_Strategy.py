from coverage_strategies.coverage_strategies.Entities import Strategy, Slot
from coverage_strategies.coverage_strategies import SpanningTreeCoverage


class STC_Strategy(Strategy):
    # @abstractmethod
    def get_steps(self, agent_r, board_size = 50, agent_o = None,):
        return SpanningTreeCoverage.get_random_coverage_strategy(size=board_size,
                                                                 i_r=Slot(agent_r.InitPosX, agent_r.InitPosY),
                                                                 print_mst=True,
                                                                 obstacles=agent_r.gameBoard.Obstacles)

