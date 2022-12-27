from queue import Queue
from graph import calculate_distance


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

    shortest_distance = None
    shortest_route = []
    for route in routes:
        distance = calculate_distance(route)
        if shortest_distance is None or distance < shortest_distance:
            shortest_distance = distance
            shortest_route = route

    return shortest_route
