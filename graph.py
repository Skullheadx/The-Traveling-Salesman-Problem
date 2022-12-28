import os
import random


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


def print_info(route: list, time: float, method_name: str, mst: float, ot: float, r=0) -> None:
    print(
        f"""
        Traveling Salesman Problem
        Method Used: {method_name}
        Time Used: {round(time, r):,} seconds
        Number of Nodes: {(len(route) - 1):,}
        Distance: {round(calculate_route(route), r):,}
        Minimum Spanning Tree: {round(mst, r):,}
        One Tree: {round(ot, r):,}
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
    visited = [graph[0]]
    unvisited = graph[1:]
    for i in range(len(graph) - 1):
        minimum = None
        min_town1 = None
        min_town2 = None
        for v1 in visited:
            for v2 in unvisited:
                d = distance(v1, v2)
                if minimum is None or d <= minimum:
                    minimum = d
                    min_town1 = v1
                    min_town2 = v2
        visited.append(min_town2)
        unvisited.remove(min_town2)
        mst += distance(min_town1, min_town2)
    return mst


def find_one_tree(graph: list) -> float:
    removed_vertex = graph[0]
    mst = find_MST(graph[1:])
    distances = []
    for town in graph[1:]:
        distances.append(distance(removed_vertex, town))
    distances.sort()

    return mst + distances[1]
