from graph import distance, find_shortest_route


def nearest_neighbor(graph: list) -> list:
    routes = []
    for start_index in range(len(graph)):
        routes.append(NN(graph, start_index))

    return find_shortest_route(routes)


def NN(graph: list, start_index):
    route = []
    seen = set()
    start = graph[start_index]
    route.append(start)
    seen.add(start)

    for i in range(len(graph) - 1):
        shortest_distance = None
        next_town = None
        for town in graph:
            if town in seen:
                continue
            d = distance(route[-1], town)
            if shortest_distance is None or d < shortest_distance:
                shortest_distance = d
                next_town = town
        route.append(next_town)
        seen.add(next_town)

    route.append(start)
    return route
