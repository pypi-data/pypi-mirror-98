from random import shuffle, random
from math import floor
from coverage_strategies import Entities


def print_graph(edges, i_o, figure_label=""):
    pass



def create_graph(edge_list):
    graph = {}
    for e1, e2 in edge_list:
        graph.setdefault(e1, []).append(e2)
        graph.setdefault(e2, []).append(e1)
    return graph


def get_shallow_graph(original_edges):
    shallow_graph = {}
    for e1, e2 in original_edges:
        shallow_e1 = Entities.Slot(floor(e1.row / 2.0), floor(e1.col / 2.0))
        shallow_e2 = Entities.Slot(floor(e2.row / 2.0), floor(e2.col / 2.0))

        if (shallow_e1.row, shallow_e1.col) == (shallow_e2.row, shallow_e2.col):
            continue

        if shallow_e1 not in shallow_graph.keys() or shallow_e2 not in shallow_graph[shallow_e1]:
            shallow_graph.setdefault(shallow_e1, []).append(shallow_e2)

        if shallow_e2 not in shallow_graph.keys() or shallow_e1 not in shallow_graph[shallow_e2]:
            shallow_graph.setdefault(shallow_e2, []).append(shallow_e1)

    return shallow_graph


# Prim's
def mst(start, graph):
    closed = set()
    edges = []
    q = [(start, start)]
    while q:
        # randomize
        shuffle(q)

        v1, v2 = q.pop()
        if v2 in closed:
            continue
        closed.add(v2)
        edges.append((v1, v2))
        for v in graph[v2]:
            if v in graph:
                q.append((v2, v))
    del edges[0]
    assert len(edges) == len(graph)-1
    return edges


def create_covering_path(mst_edges_shallow_graph, initial_slot):
    covering_path = []
    origin_slot = initial_slot
    slot = origin_slot
    counter = 0
    while True:
        counter += 1
        if counter > 100000:
            print("ERROR! Probably hit infinite loop while creating the covering path")
            return

        covering_path.append(slot)
        shallow_slot = Entities.Slot(floor(slot.row / 2.0), floor(slot.col / 2.0))
        # find to where to go next, depend on the mst edges.
        # Check how much and which corners are in the mst group, then update slot accordingly

        has_downward_edge = (shallow_slot, shallow_slot.go_south()) in mst_edges_shallow_graph or \
                            (shallow_slot.go_south(), shallow_slot) in mst_edges_shallow_graph
        has_rightward_edge = (shallow_slot, shallow_slot.go_east()) in mst_edges_shallow_graph or \
                             (shallow_slot.go_east(), shallow_slot) in mst_edges_shallow_graph
        has_leftward_edge = (shallow_slot, shallow_slot.go_west()) in mst_edges_shallow_graph or \
                            (shallow_slot.go_west(), shallow_slot) in mst_edges_shallow_graph
        has_upward_edge = (shallow_slot, shallow_slot.go_north()) in mst_edges_shallow_graph or \
                          (shallow_slot.go_north(), shallow_slot) in mst_edges_shallow_graph

        bl_corner_in_mst = False
        br_corner_in_mst = False
        ul_corner_in_mst = False
        ur_corner_in_mst = False

        if slot.row % 2 == 0 and slot.col % 2 == 0:
            if has_downward_edge or has_rightward_edge:
                br_corner_in_mst = True
            if has_upward_edge:
                br_corner_in_mst = True
                ur_corner_in_mst = True
            if has_leftward_edge:
                bl_corner_in_mst = True
                br_corner_in_mst = True
        elif slot.row % 2 == 0 and slot.col % 2 != 0:
            if has_downward_edge or has_leftward_edge:
                bl_corner_in_mst = True
            if has_upward_edge:
                bl_corner_in_mst = True
                ul_corner_in_mst = True
            if has_rightward_edge:
                bl_corner_in_mst = True
                br_corner_in_mst = True
        elif slot.row % 2 != 0 and slot.col % 2 == 0:
            if has_rightward_edge or has_upward_edge:
                ur_corner_in_mst = True
            if has_downward_edge:
                br_corner_in_mst = True
                ur_corner_in_mst = True
            if has_leftward_edge:
                ur_corner_in_mst = True
                ul_corner_in_mst = True
        elif slot.row % 2 != 0 and slot.col % 2 != 0:
            if has_leftward_edge or has_upward_edge:
                ul_corner_in_mst = True
            if has_downward_edge:
                bl_corner_in_mst = True
                ul_corner_in_mst = True
            if has_rightward_edge:
                ul_corner_in_mst = True
                ur_corner_in_mst = True

        last_slot = covering_path[len(covering_path)-2]

        # check o see if only one vertex was in the mst
        if br_corner_in_mst and not (ur_corner_in_mst or bl_corner_in_mst or ul_corner_in_mst):
            if slot.go_south() == last_slot or slot == last_slot:
                slot = slot.go_east()
            elif slot.go_east() == last_slot:
                slot = slot.go_south()
        elif ur_corner_in_mst and not (br_corner_in_mst or bl_corner_in_mst or ul_corner_in_mst):
            if slot.go_east() == last_slot or slot == last_slot:
                slot = slot.go_north()
            elif slot.go_north() == last_slot:
                slot = slot.go_east()
        elif bl_corner_in_mst and not (ul_corner_in_mst or ur_corner_in_mst or br_corner_in_mst):
            if slot.go_west() == last_slot or slot == initial_slot:
                slot = slot.go_south()
            elif slot.go_south() == last_slot:
                slot = slot.go_west()
        elif ul_corner_in_mst and not (bl_corner_in_mst or br_corner_in_mst or ur_corner_in_mst):
            if slot.go_north() == last_slot or slot == initial_slot:
                slot = slot.go_west()
            elif slot.go_west() == last_slot:
                slot = slot.go_north()
        # check to see if exactly two vertices are in the mst
        elif bl_corner_in_mst and br_corner_in_mst and not (ul_corner_in_mst or ur_corner_in_mst):
            if slot.go_west() == last_slot or slot == initial_slot:
                slot = slot.go_east()
            elif slot.go_east() == last_slot:
                slot = slot.go_west()
            else:
                print("error 1")
        elif ul_corner_in_mst and ur_corner_in_mst and not (bl_corner_in_mst or br_corner_in_mst):
            if slot.go_east() == last_slot or slot == initial_slot:
                slot = slot.go_west()
            elif slot.go_west() == last_slot:
                slot = slot.go_east()
        elif br_corner_in_mst and ur_corner_in_mst and not (bl_corner_in_mst or ul_corner_in_mst):
            if slot.go_south() == last_slot or slot == initial_slot:
                slot = slot.go_north()
            elif slot.go_north() == last_slot:
                slot = slot.go_south()
        elif bl_corner_in_mst and ul_corner_in_mst and not (br_corner_in_mst or ur_corner_in_mst):
            if slot.go_north() == last_slot or slot == initial_slot:
                slot = slot.go_south()
            elif slot.go_south() == last_slot:
                slot = slot.go_north()
        # check for exactly 3 vertices
        elif br_corner_in_mst and bl_corner_in_mst and ul_corner_in_mst and not ur_corner_in_mst:
            if slot.go_north() == last_slot or slot == initial_slot:
                slot = slot.go_east()
            elif slot.go_east() == last_slot:
                slot = slot.go_north()
        elif bl_corner_in_mst and ul_corner_in_mst and ur_corner_in_mst and not br_corner_in_mst:
            if slot.go_south() == last_slot or slot == initial_slot:
                slot = slot.go_east()
            elif slot.go_east() == last_slot:
                slot = slot.go_south()
        elif ul_corner_in_mst and ur_corner_in_mst and br_corner_in_mst and not bl_corner_in_mst:
            if slot.go_west() == last_slot or slot == initial_slot:
                slot = slot.go_south()
            elif slot.go_south() == last_slot:
                slot = slot.go_west()
        elif ur_corner_in_mst and br_corner_in_mst and bl_corner_in_mst and not ul_corner_in_mst:
            if slot.go_north() == last_slot or slot == initial_slot:
                slot = slot.go_west()
            elif slot.go_west() == last_slot:
                slot = slot.go_north()
        else:
            print("error has occurred!")

        if slot == origin_slot:
            break

    # flip path direction half of the time
    if random() < 0.5:
        covering_path = flip_path(covering_path)

    return covering_path

def flip_path(path):
    return_path = []
    return_path.append(path[0])
    return_path.extend([path[i] for i in range(len(path)-1,0,-1)])
    return return_path

def is_slot_shallow_obstacle(slot, obstacles):
    return any([(int(slot.row / 2) == int(s.row / 2) and int(slot.col / 2) == int(s.col / 2)) for s in obstacles])

def get_edges_for_full_graph(width, height, obstacles):
    edges = [(Entities.Slot(row, col), Entities.Slot(row, col).go_south())
             for row in range(height) for col in range(width)
             if not (is_slot_shallow_obstacle(Entities.Slot(row, col), obstacles)
                     or is_slot_shallow_obstacle(Entities.Slot(row, col).go_south(), obstacles))
             ]
    edges.extend([(Entities.Slot(row, col), Entities.Slot(row, col).go_east())
             for row in range(height) for col in range(width)
             if not (is_slot_shallow_obstacle(Entities.Slot(row, col), obstacles)
                     or is_slot_shallow_obstacle(Entities.Slot(row, col).go_east(), obstacles))
             ])
    inbounds = [e for e in edges if e[0].row < width and e[1].row < width and e[0].col < height and e[1].col < height ]
    return inbounds


def get_random_coverage_strategy(size, i_r, i_o=None, print_mst=False, figure_label="", obstacles=[]):
    edges = get_edges_for_full_graph(size, size, obstacles=obstacles)

    # remove edges inside, or connected to, obstacles

    shallow_graph = get_shallow_graph(edges)
    shallow_init_pos = Entities.Slot(floor(i_r.row / 2.0), floor(i_r.col / 2.0))
    mst_edges_shallow_graph = mst(shallow_init_pos, shallow_graph)
    covering_path = create_covering_path(mst_edges_shallow_graph, i_r)
    if print_mst:
        covering_path_edges = []
        for i in range(0, len(covering_path)-1):
            covering_path_edges.append((covering_path[i], covering_path[i+1]))
        print_graph(covering_path_edges, i_o, figure_label=figure_label)
    return covering_path


def display_path(covering_path):
    covering_path_edges = []
    for i in range(0, len(covering_path) - 1):
        covering_path_edges.append((covering_path[i], covering_path[i + 1]))
    print_graph(covering_path_edges, covering_path_edges[0][0])


if __name__ == '__main__':
    get_random_coverage_strategy(32, Entities.Slot(16, 16), True)
