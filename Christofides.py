from graph import distance, find_MST, calculate_route, linker
from queue import Queue


def christofides(graph: list):
    route = []
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
    print(f"{odd_degree_vertices=}")

    print(f"{mst=}")
    print()
    print(f"{perfect_matching=}")
    print()
    print(f"{multigraph=}")

    eulerian_tour = linker(multigraph)

    print(eulerian_tour)

    print(g)
    return mst

"""


((396, 559), (300, 438)), 1
((300, 438), (141, 520)), 2
((300, 438), (490, 227)), 
((300, 438), (24, 97)), 
((396, 559), (141, 520)), 3
((24, 97), (490, 227))"""
