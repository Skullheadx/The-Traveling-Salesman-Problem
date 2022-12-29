from queue import PriorityQueue
from graph import distance
from copy import deepcopy


def greedy(graph: list):
    lines = []
    distances = []
    for town1 in graph:
        for town2 in graph:
            if town1 != town2:
                distances.append((distance(town1, town2), town1, town2))
    distances.sort()

    g = {town: [] for town in graph}

    def detect_cycle(start, end, target, gr, seen):
        if start == target:
            gr = gr.copy()
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

    seen = set()

    for i in range(len(distances)):
        if len(lines) == len(graph):
            break

        d, start, end = distances[i]

        if (start, end) in seen:
            continue
        seen.add((start, end))
        seen.add((end, start))

        if len(lines) < len(graph) and detect_cycle(start, end, start, deepcopy(g), set()):
            continue

        lines.append((start, end))

        g[start].append(end)
        g[end].append(start)

    print(tuple(find_missing(lines)))
    # lines.append(tuple(find_missing(lines)))

    return lines

def find_missing(lines):

    counter = dict()

    for pair in lines:
        start, end = pair
        if start in counter:
            counter[start] += 1
        else:
            counter[start] = 1
        if end in counter:
            counter[end] += 1
        else:
            counter[end] = 1

    missing = []
    for i in counter:
        if counter[i] == 1:
            missing.append(i)
    return missing


# def linker():
#     def find_index(l, val):
#         for i, v in enumerate(l):
#             print(i, v[0], val)
#             if val == v[0]:
#                 return i
#
#     starts = [i[0] for i in lines]
#     ends = [i[1] for i in lines]
#     s = set()
#     for i in lines:
#         print(i)
#     print(len(lines))
#     print()
#     print(lines[0])
#     print()
#     head = lines[0]
#     current = head[:]
#     route = [head[0], head[1]]
#     while True:
#         if current[1] in starts:
#             x = starts.index(current[1])
#             current = lines[x]
#             y = 1
#
#         elif current[1] in ends:
#             x = ends.index(current[1])
#             current = lines[x]
#             y = 0
#
#         elif current[0] in starts:
#             x = starts.index(current[0])
#             current = lines[x]
#             y= 1
#
#         elif current[0] in starts:
#             x = ends.index(current[0])
#             current = lines[x]
#             y = 0
#         else:
#             break
#         print(current)
#         # del lines[x]
#         del starts[x]
#         del ends[x]
#         if current[y] not in s:
#             route.append(current[y])
#         s.add(current[y])
