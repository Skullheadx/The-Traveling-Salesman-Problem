from graph import create, read, print_info, find_MST, find_one_tree
from display import Display
from brute_force import brute_force
from nearest_neighbor import nearest_neighbor
from time import perf_counter
import os

GRAPH_PATH = "graphs/"
DELETE_PREVIOUS_FILES = True
CREATE_NEW_GRAPHS = True


def main():
    if DELETE_PREVIOUS_FILES:
        for root, dirs, files in os.walk("graphs/"):
            for name in files:
                path = os.path.join(root, name)

                if os.path.exists(path):
                    os.remove(path)
                else:
                    print("The file does not exist")

    if CREATE_NEW_GRAPHS:
        graph, filename = create(GRAPH_PATH, 640, 640, 100)
    else:
        filename = "graph1.txt"
        graph = read(GRAPH_PATH, filename)

    time_start = perf_counter()
    # route = brute_force(graph)  # 10 nodes in 85.042 seconds. Optimal = 2,262.29
    route = nearest_neighbor(graph)  # 100 nodes in 0.5762094999663532 seconds. Distance = 6,270.568142156188
    time_end = perf_counter()

    MST = find_MST(graph)
    ONE_TREE = find_one_tree(graph)

    print_info(route, time_end - time_start, "NN Heuristic", MST, ONE_TREE, r=100)

    display = Display(os.path.join(GRAPH_PATH, filename), route)
    display.show()


if __name__ == "__main__":
    main()
