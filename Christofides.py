from graph import distance, find_MST, calculate_route
from queue import Queue
from collections import Counter
from copy import deepcopy

def linker2(points):
    graph = dict()

    for pair in points:
        start, end = pair
        if start in graph:
            graph[start].append(end)
        else:
            graph[start] = [end]

        if end in graph:
            graph[end].append(start)
        else:
            graph[end] = [start]
    print(graph)
    q = Queue()
    q.put([points[0][0]])
    seen = set()
    while not q.empty():
        current = q.get()

        if tuple(current) in seen:
            continue
        else:
            seen.add(tuple(current))

        if Counter(current) == Counter(points):
            return current
        print(current, points)
        for i in graph[current[-1]]:
            temp = deepcopy(current)
            temp.append(i)
            q.put(temp)

    return []

def christofides(graph: list):
    _, mst = find_MST(graph)
    g = {town: [] for town in graph}
    for i in mst:
        start, end = i
        g[start].append(end)
        g[end].append(start)

    odd_degree_vertices = []

    for town in g:
        degree = len(g[town])
        if degree % 2 == 1:
            odd_degree_vertices.append(town)

    def is_seen(points, value):
        for i in points:
            s, e = i
            if value == s or value == e:
                return True
        return False

    perfect_matching = []
    q = Queue()
    q.put([])

    min_weight = None
    while not q.empty():
        current = q.get()
        if len(current) == len(odd_degree_vertices) / 2:
            d = calculate_route(current, "points")
            if min_weight is None or d < min_weight:
                min_weight = d
                perfect_matching = current

        for i in odd_degree_vertices:
            if not is_seen(current, i):
                for j in odd_degree_vertices:
                    if j != i and not is_seen(current,j):
                        c = current[:]
                        c.append((i, j))
                        q.put(c)


    multigraph = mst + perfect_matching
    # print(f"{odd_degree_vertices=}")
    # print(f"{mst=}")
    # print(f"{perfect_matching=}")
    # print(f"{multigraph=}")

    eulerian_tour = linker2(multigraph)
    #
    print(eulerian_tour)
    #
    # print(g)
    return perfect_matching

"""


((396, 559), (300, 438)), 1
((300, 438), (141, 520)), 2
((300, 438), (490, 227)), 
((300, 438), (24, 97)), 
((396, 559), (141, 520)), 3
((24, 97), (490, 227))"""

