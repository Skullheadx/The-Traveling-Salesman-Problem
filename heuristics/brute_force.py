from queue import Queue
from graph import find_shortest_route


def brute_force(graph: list) -> list:
    routes = []
    q = Queue()
    q.put([])

    while not q.empty():
        current = q.get()
        if len(current) == len(graph):
            current.append(current[0])
            routes.append(current)
            continue

        for node in graph:
            if node not in current:
                temp = current[:]
                temp.append(node)
                q.put(temp)

    return find_shortest_route(routes)
