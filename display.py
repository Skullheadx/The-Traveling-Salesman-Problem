import pygame


pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)


class Node:
    background_colour = GRAY
    outline_colour = BLACK
    text_colour = WHITE

    radius = 15
    thickness = 1
    font = pygame.font.SysFont("arial", 15)

    def __init__(self, position: tuple, number: int) -> None:
        self.position = pygame.Vector2(position)
        self.text = self.font.render(str(number), True, self.text_colour)

    def draw(self, surf: pygame.Surface) -> None:
        pygame.draw.circle(surf, self.background_colour, self.position, self.radius)
        pygame.draw.circle(surf, self.outline_colour, self.position, self.radius, width=self.thickness)
        surf.blit(self.text, self.text.get_rect(center=self.position))


class Display:
    pygame.display.set_caption("Traveling Salesman Problem")

    def __init__(self, path: str) -> None:
        with open(path, "r") as f:
            contents = f.read().split("\n")
            if contents[-1] == "":
                contents = contents[:-1]

        self.WIDTH, self.HEIGHT, self.N = tuple(map(int, contents[0].split(" ")))
        self.nodes = [Node(tuple(map(int, node.split(" "))), num) for num, node in enumerate(contents[1:])]
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.is_running = True

        self.clock = pygame.time.Clock()
        self.delta = 0

    def show(self, route: list) -> None:
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            self.screen.fill(WHITE)

            if len(route) > 1:
                pygame.draw.aalines(self.screen, BLUE, True, route, 5)

            for node in self.nodes:
                node.draw(self.screen)

            pygame.display.update()
            self.delta = self.clock.tick(60)
