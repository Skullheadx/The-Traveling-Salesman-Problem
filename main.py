from graph import create, print_info
from display import Display
from brute_force import brute_force
from nearest_neighbor import nearest_neighbor
from time import perf_counter
import os

GRAPH_PATH = "graphs/"
DELETE_PREVIOUS_FILES = True


def main():
    if DELETE_PREVIOUS_FILES:
        for root, dirs, files in os.walk("graphs/"):
            for name in files:
                path = os.path.join(root, name)

                if os.path.exists(path):
                    os.remove(path)
                else:
                    print("The file does not exist")

    graph, filename = create(GRAPH_PATH, 720, 720, 100)

    time_start = perf_counter()
    # route = brute_force(graph)  # 10 nodes in 85.042 seconds. Optimal = 2,262.29
    route = nearest_neighbor(graph)  # 100 nodes in 0.5762094999663532 seconds. Distance = 6,270.568142156188
    time_end = perf_counter()

    print_info(route, time_end - time_start, "NN Heuristic", r=100)

    display = Display(os.path.join(GRAPH_PATH, filename), route)
    display.show()


if __name__ == "__main__":
    main()
