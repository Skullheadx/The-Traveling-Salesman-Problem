from graph import create
from display import Display
from brute_force import brute_force
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

    graph, filename = create(GRAPH_PATH, 640, 640, 5)
    display = Display(os.path.join(GRAPH_PATH, filename))

    route = brute_force(graph)

    display.show(route)


if __name__ == "__main__":
    main()
