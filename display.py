import pygame
import math
from graph import distance
from queue import PriorityQueue

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def find_MST(route: list) -> list:
    q = PriorityQueue()
    head = route[0]
    seen = set()
    mst = []
    for town in route:
        q.put((distance(town, head), head, town))
    while not q.empty():
        d, start, end = q.get()
        if end in seen:
            continue
        seen.add(end)

        mst.append((start, end))

        for town in route:
            q.put((distance(town, end), end, town))

    return mst


def find_one_tree(route: list):
    removed_vertex = route[0]
    mst = find_MST(route[1:-1])
    distances = []
    for town in route[1:-1]:
        distances.append((distance(removed_vertex, town), town))
    distances.sort()
    mst.append((distances[0][1], removed_vertex))
    mst.append((distances[1][1], removed_vertex))

    return mst, removed_vertex


class Node:
    background_colour = GRAY
    outline_colour = BLACK
    text_colour = WHITE

    radius = 6
    thickness = 1

    # font = pygame.font.SysFont("arial", 20)

    def __init__(self, position: tuple, number: int) -> None:
        self.position = pygame.Vector2(position)
        # self.text = self.font.render(str(number), True, self.text_colour)

    def draw(self, surf: pygame.Surface) -> None:
        pygame.draw.circle(surf, self.background_colour, self.position, self.radius)
        pygame.draw.circle(surf, self.outline_colour, self.position, self.radius, width=self.thickness)
        # surf.blit(self.text, self.text.get_rect(center=self.position))


class Salesman:
    background_colour = ORANGE
    outline_colour = BLACK

    radius = 7
    thickness = 1

    speed = 150  # pixels/second

    def __init__(self, route: list, start_index=0) -> None:
        self.route = route
        self.index = start_index
        self.position = pygame.Vector2(self.route[self.index])
        self.destination = self.get_destination()

    def get_destination(self) -> pygame.Vector2:
        self.index = (self.index + 1) % len(self.route)
        return pygame.Vector2(self.route[self.index])

    def update(self, delta: float) -> None:
        direction = math.atan2(self.destination.y - self.position.y, self.destination.x - self.position.x)
        step = self.speed * delta
        if abs(step * math.cos(direction)) > abs(self.destination.x - self.position.x):
            self.position.x = self.destination.x
        else:
            self.position.x += step * math.cos(direction)

        if abs(step * math.sin(direction)) > abs(self.destination.y - self.position.y):
            self.position.y = self.destination.y
        else:
            self.position.y += step * math.sin(direction)
        if self.position == self.destination:
            self.destination = self.get_destination()

    def draw(self, surf: pygame.Surface) -> None:
        pygame.draw.circle(surf, self.background_colour, self.position, self.radius)
        pygame.draw.circle(surf, self.outline_colour, self.position, self.radius, width=self.thickness)


class Display:
    pygame.display.set_caption("Traveling Salesman Problem")

    def __init__(self, path: str, route: list) -> None:
        with open(path, "r") as f:
            contents = f.read().split("\n")
            if contents[-1] == "":
                contents = contents[:-1]

        self.WIDTH, self.HEIGHT, self.N = tuple(map(int, contents[0].split(" ")))
        self.nodes = [Node(tuple(map(int, node.split(" "))), num) for num, node in enumerate(contents[1:])]
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.route = route
        self.salesman = Salesman(self.route)

        self.mst = find_MST(route[:-1])
        self.ot, self.ot_removed_point = find_one_tree(route)

    def update(self, delta: float) -> None:
        self.salesman.update(delta)

    def show(self) -> None:
        is_running = True

        clock = pygame.time.Clock()
        delta = 0
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

            self.salesman.update(delta)

            self.screen.fill(WHITE)

            pygame.draw.circle(self.screen, BLUE, self.ot_removed_point, 15)

            if len(self.route) > 1:
                for line in self.ot:  # One Tree
                    start, end = line
                    pygame.draw.line(self.screen, GREEN, start, end, 12)
                for line in self.mst:  # Minimum Spanning Tree
                    start, end = line
                    pygame.draw.line(self.screen, RED, start, end, 7)
                pygame.draw.aalines(self.screen, BLUE, True, self.route)  # Route
            for node in self.nodes:
                node.draw(self.screen)
            self.salesman.draw(self.screen)
            pygame.display.update()
            delta = clock.tick(60) / 1000  # Seconds
