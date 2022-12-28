import pygame
import math

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)


class Node:
    background_colour = GRAY
    outline_colour = BLACK
    text_colour = WHITE

    radius = 5
    thickness = 1

    # font = pygame.font.SysFont("arial", 12)

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
        self.nodes = [Node(node, num) for num, node in enumerate(route)]
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.route = route
        self.salesman = Salesman(self.route)

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

            if len(self.route) > 1:
                pygame.draw.aalines(self.screen, BLUE, True, self.route, 5)

            for node in self.nodes:
                node.draw(self.screen)

            self.salesman.draw(self.screen)

            pygame.display.update()
            delta = clock.tick(60) / 1000  # Seconds
