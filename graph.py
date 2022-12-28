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


def print_info(route: list, time: float, method_name: str, r=0) -> None:
    print(
        f"""
        Traveling Salesman Problem
        Method Used: {method_name}
        Time Used: {round(time, r):,} seconds
        Number of Nodes: {(len(route) - 1):,}
        Distance: {round(calculate_route(route), r):,} 
        """)


def find_shortest_route(routes: list) -> list:
    shortest_distance = None
    shortest_route = []
    for route in routes:
        d = calculate_route(route)
        print(d)
        if shortest_distance is None or d < shortest_distance:
            shortest_distance = d
            shortest_route = route
    return shortest_route
