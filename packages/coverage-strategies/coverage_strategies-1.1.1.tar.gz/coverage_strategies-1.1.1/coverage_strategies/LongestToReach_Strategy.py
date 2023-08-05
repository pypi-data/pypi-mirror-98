import operator
from math import fabs
from coverage_strategies.coverage_strategies.Entities import Slot, Strategy, Agent, Board, assign_level_to_slots
from coverage_strategies.coverage_strategies.SpanningTreeCoverage import is_slot_shallow_obstacle


def cover_current_level(level, current: Slot, board: Board, leveled_slots):
    slots = [current]
    current_slot = current
    level_amount = len([i for i in leveled_slots.values() if i == level])

    # print("covering level %d" % leveled_slots.get(current_slot))

    leveled_neighbors = lambda slot: [i for i in current_slot.get_inbound_neighbors(board)
                                      if leveled_slots.get(i) == level]
    nonpresent_leveled_neighbors = lambda slot, l: [i for i in leveled_neighbors(slot) if i not in l]

    # go toward a neighbor of the same level, covering until having a single neighbor with level value
    uncovered_inbound_neighbors = nonpresent_leveled_neighbors(current_slot, slots)
    while uncovered_inbound_neighbors:
        current_slot = uncovered_inbound_neighbors.pop()
        slots.append(current_slot)
        uncovered_inbound_neighbors = nonpresent_leveled_neighbors(current_slot, slots)

    # if not covered all of this level, go the the opposite direction and cover until all level is covered
    doubly_covered_slots = []
    # if reached to this point, go until there is a cell with uncovered neighbor, and from there cover until done.
    # if len(set(slots)) < level_amount:
    # go until at a cell with uncovered neighbor
    previous_slot = Slot(-1, -1)
    while len(set(slots)) < level_amount:
        uncovered_leveled_slots = nonpresent_leveled_neighbors(current_slot, doubly_covered_slots)
        if not uncovered_leveled_slots:
            break

        temp = current_slot
        l = [i for i in uncovered_leveled_slots if i != previous_slot and not is_slot_shallow_obstacle(i, board.Obstacles)]
        if not l:
            return slots[1::]
        current_slot = l[0]
        previous_slot = temp
        doubly_covered_slots.append(current_slot)
        slots.append(current_slot)

    return slots[1:]


class LongestToReach_Strategy(Strategy):
    def get_steps(self, agent_r: Agent, board_size=50, agent_o: Agent = None):
        assert agent_o is not None

        # 1. perform bfs and set LEVEL values
        # 2. go to cell with highest LEVEL value
        # 3. while not all cells covered:
        #   3.1. cover current LEVEL
        #   3.2. if next level adjacent, go there
        #   3.3  if not all cells are covered, go to next level (search)

        covered_slots = []

        # get the 'farthest' cell from R's initial location
        initial_level_assignment = assign_level_to_slots(board=agent_o.gameBoard,
                                                         init=Slot(agent_o.InitPosX, agent_o.InitPosY),
                                                         levelType=4)
        farthest_slot = max(initial_level_assignment.items(), key=operator.itemgetter(1))[0]

        # 1. perform bfs
        board = agent_o.gameBoard
        leveled_slots = assign_level_to_slots(board, farthest_slot)

        # define lambda
        def there_are_cells_to_cover():
            return len(set(self.steps)) + len(board.get_shallow_obstacles()) < board.Rows * board.Cols

        def distance(a,b):
            return fabs(a.row - b.row) + fabs(a.col - b.col)

        def edges_and_distance_score(slot:Slot):
            return len(slot.get_inbound_neighbors(board)) * 10 + distance(slot, Slot(agent_r.InitPosX, agent_r.InitPosY))

        max_level = min(leveled_slots.values())
        max_leveled_slots = [i for i in leveled_slots if leveled_slots[i] == max_level]
        ordered_max_leveled_slots = sorted(max_leveled_slots, key=edges_and_distance_score)

        # 2. go to cell with highest LEVEL value
        # max_level_slot = max(leveled_slots.items(), key=operator.itemgetter(1))
        best_max_level_slot = ordered_max_leveled_slots[0]
        path_to_max_slot = Strategy.go_from_a_to_b_dijkstra(
            a=Slot(agent_r.InitPosX, agent_r.InitPosY),
            b=best_max_level_slot,
            board=board)
        self.steps.extend(path_to_max_slot)
        current_slot = best_max_level_slot
        covered_slots.append(current_slot)
        # covered_slots.extend(path_to_max_slot)

        # 3. while not all cells covered:
        while there_are_cells_to_cover():
            #   3.1. cover current LEVEL
            level_steps = cover_current_level(
                level=leveled_slots[current_slot],
                current=current_slot,
                board=board,
                leveled_slots=leveled_slots)
            self.steps.extend(level_steps)
            covered_slots.extend(level_steps)

            if level_steps:
                current_slot = level_steps[-1]

            #   3.2. if next level adjacent, go there
            preferred_n = Slot(-1, -1)
            current_slot_neighbors = [n for n in current_slot.get_inbound_neighbors(board)
                                      if not is_slot_shallow_obstacle(n, board.Obstacles)]

            if any([(leveled_slots.get(i) == leveled_slots.get(current_slot) + 1) for i in current_slot_neighbors
                    if i not in covered_slots]):
                for n in current_slot_neighbors:
                    if leveled_slots[n] == leveled_slots[current_slot] + 1:
                        if preferred_n == Slot(-1, -1) or len(n.get_inbound_neighbors(board)) < len(
                                preferred_n.get_inbound_neighbors(board)):
                            preferred_n = n

                if preferred_n != Slot(-1, -1):
                    if preferred_n.row == -1:
                        pass
                    current_slot = preferred_n
                    covered_slots.append(current_slot)
                    self.steps.append(current_slot)
                    # break
                else:
                    raise Exception("Unhandled Code! Slot: %s" % current_slot)
            else:
                # reaching this case means all current slot's neighbors are already covered. either coverage is done,
                # or we have reached a dead end, and should look for the closest uncovered cell.
                if not there_are_cells_to_cover():
                    break

                #   3.3  if next level not adjacent, and process not finished, search for next level
                #   (higher than 0) and go there
                #   3.4 from there, cover with decreasing level values until no more slots are to cover


                # find_closest_uncovered_slot
                cus = min([i for i in leveled_slots.keys() if i not in self.steps],
                          key=lambda a: distance(a, current_slot))
                current_slot = cus
                self.steps.append(current_slot)
                covered_slots.append(current_slot)
                continue
                # print("closest ucs is: %s" %cus)


        return self.steps
