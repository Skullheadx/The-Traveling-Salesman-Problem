from graph import create, read, print_info, find_MST, find_one_tree, find_lower_bound
from display import Display
from brute_force import brute_force
from nearest_neighbor import nearest_neighbor
from greedy import greedy
from Christofides import christofides
from time import perf_counter
import os

GRAPH_PATH = "graphs/"
CREATE_NEW_GRAPHS = False


def main():
    if CREATE_NEW_GRAPHS:
        for root, dirs, files in os.walk("graphs/"):
            for name in files:
                path = os.path.join(root, name)

                if os.path.exists(path):
                    os.remove(path)
                else:
                    print("The file does not exist")

    if CREATE_NEW_GRAPHS:
        graph, filename = create(GRAPH_PATH, 640, 640, 15)
    else:
        filename = "graph1.txt"
        graph = read(GRAPH_PATH, filename)

    route_time_start = perf_counter()
    # route = brute_force(graph)  # 10 nodes in 85.042 seconds. Optimal = 2,262.29
    # route = nearest_neighbor(graph)  # 100 nodes in 0.5762094999663532 seconds. Distance = 6,270.568142156188
    # route = greedy(graph)  # 100 nodes in 0.1383088999427855 seconds. Distance = 5,523.211501332208 OTLB: 4,
    # 344.881943246125 Approx. 27.119944188995277%
    route = christofides(graph)
    route_time_end = perf_counter()

    MST_distance, MST = find_MST(graph)
    print("MST_DISTANCE:", MST_distance)
    one_tree_time_start = perf_counter()
    # lower_bound, one_tree = find_one_tree(graph)
    removed_vertex = graph[0]
    lower_bound, one_tree, removed_vertex = find_lower_bound(graph)
    one_tree_time_end = perf_counter()

    print_info(route, route_time_end - route_time_start, "Christofides Algorithm", lower_bound,
               one_tree_time_end - one_tree_time_start, r=3000, mode="direct")

    display = Display(os.path.join(GRAPH_PATH, filename), route, mst=MST, one_tree=None,
                      removed_vertex=removed_vertex, mode="direct")
    display.show()


if __name__ == "__main__":
    main()
