from graph import create
from display import Display
import os

GRAPH_PATH = "graphs/"


def main():
    graph, filename = create(GRAPH_PATH, 640, 640, 20)
    display = Display(os.path.join(GRAPH_PATH, filename))

    display.show(graph)


if __name__ == "__main__":
    main()
