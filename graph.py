import os
import random
from queue import PriorityQueue


def prune_filename(filename: str) -> int:
    return int(filename[5:-4])


def create(path: str, width: int, height: int, nodes: int):
    graph = []
    text = f"{width} {height} {nodes}\n"
    seen = set()  # so that there are no duplicate points

    counter = 0
    while counter < nodes:
        x, y = (random.randint(0, width), random.randint(0, height))
        if (x, y) not in seen:
            graph.append((x, y))
            text += f"{x} {y}\n"
            seen.add((x, y))
            counter += 1

    current_file = 0
    for root, dirs, files in os.walk(path):
        for name in files:
            current_file = max(current_file, prune_filename(name))
    filename = f"graph{current_file + 1}.txt"
    with open(os.path.join(path, filename), "w") as f:
        f.write(text[:-1])

    return graph, filename


def read(path: str, filename: str) -> list:
    with open(os.path.join(path, filename)) as f:
        contents = f.read().split("\n")[1:]
        if contents[-1] == "":
            contents = contents[:-1]
    graph = [tuple(map(int, i.split(" "))) for i in contents]

    return graph


def distance(town1: tuple, town2: tuple) -> float:
    return pow(pow(town1[0] - town2[0], 2) + pow(town1[1] - town2[1], 2), 0.5)


def get_distances(graph: list) -> dict:
    distances = dict()
    for town1 in graph:
        distances[town1] = dict()
        for town2 in graph:
            if town1 != town2:
                distances[town1][town2] = distance(town1, town2)
    return distances


def calculate_route(route: list, mode="direct") -> float:
    if mode == "direct":
        town1 = route[0]
        town2 = route[-1]
        d = distance(town1, town2)
        for i, node in enumerate(route[:-1]):
            town2 = route[i + 1]
            d += distance(town1, town2)
            town1 = town2
        return d
    elif mode == "points":
        d = 0.0
        for i in route:
            start, end = i

            d += distance(start, end)
        return d


def find_shortest_route(routes: list) -> list:
    shortest_distance = None
    shortest_route = []
    for route in routes:
        d = calculate_route(route)
        if shortest_distance is None or d <= shortest_distance:
            shortest_distance = d
            shortest_route = route
    return shortest_route


def print_info(route: list, time: float, method_name: str, one_tree: float, one_tree_time: float, r=0,
               mode="direct") -> None:
    d = calculate_route(route, mode)
    if mode == "direct":
        num_nodes = (len(route) - 1)
    elif mode == "points":
        num_nodes = len(route)
    print(
        f"""
Traveling Salesman Problem
Method Used: {method_name}
Approximation ratio: {round(d / one_tree * 100 - 100, r)}%
Time Used: {round(time, r):,} seconds
Number of Nodes: {num_nodes:,}
Distance: {round(d, r):,}
One Tree Lower Bound: {round(one_tree, r):,}
One Tree Time Used: {round(one_tree_time, r):,} seconds
""")


"""
Approximation ratio (alpha) = heuristic solution / optimal solution
E.g. a = 28.2/27.0 = 1.044 = 4.4% above optimal

Compare to a lower bound

Minimum Spanning Tree (MST)
- Set of edges that connect all vertices with minimum distance and no cycles

Prim's Algorithm

MST Cost < TSP Cost
Remove any edge from the optimal solution and you get a spanning tree T
which is at least the cost of the MST
MST cost <= cost(T)

"""


def find_one_tree(graph: list, removed_vertex_index=0):
    removed_vertex = graph[removed_vertex_index]
    g = graph[:removed_vertex_index] + graph[removed_vertex_index + 1:]
    mst_distance, mst = find_MST(g)
    distances = []
    for town in g:
        distances.append((distance(removed_vertex, town), town))
    distances.sort()
    # Add the two closest nodes to the removed node
    mst.append((removed_vertex, distances[1][1]))
    mst.append((removed_vertex, distances[0][1]))

    one_tree_distance = mst_distance + distances[1][0] + distances[0][0]
    return one_tree_distance, mst


def find_lower_bound(graph: list):
    lower_bound = None
    lowest_one_tree = []
    rm_vertex = None

    for removed_vertex_index in range(len(graph)):
        one_tree_distance, one_tree = find_one_tree(graph, removed_vertex_index)

        if lower_bound is None or one_tree_distance > lower_bound:
            lower_bound = one_tree_distance
            lowest_one_tree = one_tree[:]
            rm_vertex = graph[removed_vertex_index]
    return lower_bound, lowest_one_tree, rm_vertex


def find_MST(graph: list):
    q = PriorityQueue()
    head = graph[0]
    seen = {head}
    mst = []
    mst_distance = 0.0
    for town in graph:
        if town != head:
            q.put((distance(town, head), head, town))
    while not q.empty() and len(mst) < len(graph) - 1:
        d, start, end = q.get()
        if end in seen:
            continue
        seen.add(end)

        mst.append((start, end))
        mst_distance += d

        for town in graph:
            if town != end:
                q.put((distance(town, end), end, town))

    return mst_distance, mst


def linker(points):
    p = points[:]
    direct = [p[0][0]]
    head = p[0][0]
    current = p[0]

    graph = dict()

    for pair in p:
        start, end = pair
        if start in graph:
            graph[start].append(end)
        else:
            graph[start] = [end]
        if end in graph:
            graph[end].append(start)
        else:
            graph[end] = [start]
    seen = set()
    seen.add(head)
    while True:
        start, end = current
        direct.append(end)

        a, b = graph[end]
        if a == start:
            current = (end, b)
        else:
            current = (end, a)

        if end == head:
            break

    return direct
