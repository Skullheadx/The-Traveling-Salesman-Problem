from graph import calculate_route, delinker, linker
from queue import Queue
from itertools import combinations


def two_opt(route:list) ->list:
    original_distance = calculate_route(route)
    route_points = delinker(route)

    for i, edge1 in enumerate(route_points):
        edge_distance =
        for edge2 in route_points[i+1:]:
            s1,e1 = edge1
            s2, e2 = edge2

            print(edge1,edge2)
            temp = r[:]
            temp.remove(edge1)
            temp.remove(edge2)
            temp.append((s1, e2))
            temp.append((s2, e1))
            new_d = calculate_route(temp, mode="points")
            if new_d < d:
                r = temp[:]
    return linker(r)