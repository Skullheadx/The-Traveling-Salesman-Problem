from graph import distance, find_MST, calculate_route
from queue import Queue


def linker2(points):
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
        if len(graph[end]) > 2:
            a = start
            for ind, i in enumerate(graph[end]):
                if i != a and ((len(direct) == len(points) - 1 and i == head) or i not in seen):
                    b = i
                    seen.add(i)
                    break
        else:
            a, b = graph[end]
            if b in seen:
                b = head
            seen.add(b)
        if a == start:
            current = (end, b)
        else:
            current = (end, a)

        if end == head:
            break

    return direct

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


    multigraph = perfect_matching + mst
    # print(f"{odd_degree_vertices=}")
    # print(f"{mst=}")
    # print(f"{perfect_matching=}")
    # print(f"{multigraph=}")

    eulerian_tour = linker2(multigraph)

    print(eulerian_tour)

    # print(g)
    return eulerian_tour

"""


((396, 559), (300, 438)), 1
((300, 438), (141, 520)), 2
((300, 438), (490, 227)), 
((300, 438), (24, 97)), 
((396, 559), (141, 520)), 3
((24, 97), (490, 227))"""

