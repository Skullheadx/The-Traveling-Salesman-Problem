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


def calculate_route(route: list) -> float:
    town1 = route[0]
    town2 = route[-1]
    d = distance(town1, town2)
    for i, node in enumerate(route[:-1]):
        town2 = route[i + 1]
        d += distance(town1, town2)
        town1 = town2
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


def print_info(route: list, time: float, method_name: str, one_tree: float, one_tree_time: float, r=0) -> None:
    d = calculate_route(route)
    print(
        f"""
Traveling Salesman Problem
Method Used: {method_name}
Approximation ratio: {round(d/one_tree * 100 - 100,r)}%
Time Used: {round(time, r):,} seconds
Number of Nodes: {(len(route) - 1):,}
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


def find_MST(graph: list) -> float:
    mst = 0.0
    q = PriorityQueue()
    head = graph[0]
    seen = set()
    for town in graph:
        q.put((distance(town, head), head, town))
    while not q.empty():
        d, start, end = q.get()
        if end in seen:
            continue
        seen.add(end)
        mst += d
        for town in graph:
            q.put((distance(town, end), end, town))
    return mst


def find_one_tree(graph: list) -> float:
    lower_bound = None

    for removed_vertex in graph:
        g = graph[:graph.index(removed_vertex)] + graph[graph.index(removed_vertex) + 1:]
        mst = find_MST(g)
        distances = []
        for town in g:
            distances.append(distance(removed_vertex, town))
        distances.sort()
        d = mst + distances[1]
        if lower_bound is None or d < lower_bound:
            lower_bound = d
    return lower_bound
