from graph import distance
from queue import PriorityQueue
from copy import deepcopy


def greedy(graph: list):
    route = []

    q = PriorityQueue()

    for i, town1 in enumerate(graph):
        for town2 in graph[i:]:
            if town1 != town2:
                q.put((distance(town1, town2), town1, town2))

    def detect_cycle(start, end, target, gr, seen):
        if start == target:
            gr = deepcopy(gr)
            gr[start].append(end)
            gr[end].append(start)

        if end == target or start in seen:
            return True

        seen.add(start)

        for x in gr[end]:
            if x != start:
                t = detect_cycle(end, x, target, gr, seen)
                if t:
                    return t
        return False

    g = {town: [] for town in graph}

    while not q.empty() and len(route) < len(graph):
        d, start, end = q.get()

        if len(g[start]) >= 2 or len(g[end]) >= 2:
            continue
        if len(route) < len(graph)-1 and detect_cycle(start, end, start, g, set()):
            continue

        route.append((start, end))
        g[start].append(end)
        g[end].append(start)

    return route
