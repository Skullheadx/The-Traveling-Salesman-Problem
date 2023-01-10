from graph import calculate_route, delinker, linker
from queue import Queue
from itertools import combinations


def two_opt(route:list) ->list:
    d = calculate_route(route)
    r = delinker(route)
    c = combinations(r,2)
    for edge1,edge2 in c:
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