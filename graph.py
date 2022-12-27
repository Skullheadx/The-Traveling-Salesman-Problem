import os
import random


def prune_filename(filename: str) -> int:
    return int(filename[5:-4])


def create(path: str, width: int, height: int, nodes: int):
    graph = []
    text = f"{width} {height} {nodes}\n"

    for node in range(nodes):
        x, y = (random.randint(0, width), random.randint(0, height))
        graph.append((x, y))
        text += f"{x} {y}\n"

    current_file = 0
    for root, dirs, files in os.walk(path):
        for name in files:
            current_file = max(current_file, prune_filename(name))
    filename = f"graph{current_file + 1}.txt"
    with open(os.path.join(path, filename), "w") as f:
        f.write(text[:-1])

    return graph, filename


def distance(x1: int, x2: int, y1: int, y2: int) -> float:
    return pow(pow(x1 - x2, 2) + pow(y1 - y2, 2), 0.5)


def get_distances(graph: list) -> dict:
    distances = dict()
    for i in graph:
        distances[i] = dict()
        x1, y1 = i
        for j in graph:
            x2, y2 = j
            distances[i][j] = distance(x1, x2, y1, y2)
    return distances


def calculate_distance(route: list) -> float:
    x1, y1 = route[0]
    x2, y2 = route[-1]
    d = distance(x1, x2, y1, y2)
    for i, node in enumerate(route[:-1]):
        x2, y2 = route[i + 1]
        d += distance(x1, x2, y1, y2)
        x1, y1 = x2, y2
    return d
