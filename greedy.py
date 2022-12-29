from graph import distance
from queue import PriorityQueue

def greedy(graph: list):
    seen = set()
    route = []

    q = PriorityQueue()

    for town1 in graph:
        for town2 in graph:
            if town1 != town2:
                q.put((distance(town1, town2), town1, town2))

    while not q.empty() and len(route) < len(graph):
        current = q.get()

        if 
