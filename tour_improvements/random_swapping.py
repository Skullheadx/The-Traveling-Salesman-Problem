from graph import calculate_route
from random import sample


def random_swap(route: list) -> list:
    r = route[:]

    a, b = sample(range(0, len(r) - 1), 2)

    temp = r[b]
    r[b] = r[a]
    r[a] = temp

    return r


def random_swapping(route: list, n: int) -> list:
    d = calculate_route(route)
    r = route[:]

    for _ in range(n):

        random_swap_route = random_swap(r)

        if calculate_route(random_swap_route) < d:
            r = random_swap_route

    return r
