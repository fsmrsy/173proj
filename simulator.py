import pygame


class RobotSimulator:
    def __init__(self, width=900, height=700):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Robot Drawing Simulator")
        self.clock = pygame.time.Clock()

        self.background = (255, 255, 255)
        self.path_color = (0, 0, 255)
        self.robot_color = (255, 0, 0)
        self.text_color = (0, 0, 0)

        self.font = pygame.font.SysFont(None, 28)

        self.current_path = []
        self.drawn_points = []
        self.path_index = 0
        self.robot_pos = None
        self.active_symbol = None
        self.speed = 3.0
        self.running = True

    def load_trajectory(self, symbol, path):
        if not path:
            return
        self.active_symbol = symbol
        self.current_path = path
        self.drawn_points = [path[0]]
        self.path_index = 1
        self.robot_pos = [path[0][0], path[0][1]]
        print(f"Simulator loaded trajectory: {symbol}")

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        if not self.current_path or self.robot_pos is None:
            return

        if self.path_index >= len(self.current_path):
            return

        tx, ty = self.current_path[self.path_index]
        rx, ry = self.robot_pos

        dx = tx - rx
        dy = ty - ry
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist < self.speed:
            self.robot_pos = [tx, ty]
            self.drawn_points.append((tx, ty))
            self.path_index += 1
        else:
            self.robot_pos[0] += self.speed * dx / dist
            self.robot_pos[1] += self.speed * dy / dist
            self.drawn_points.append((self.robot_pos[0], self.robot_pos[1]))

    def draw(self):
        self.screen.fill(self.background)

        title = self.font.render(
            f"Simulator: {self.active_symbol if self.active_symbol else 'Idle'}",
            True,
            self.text_color,
        )
        self.screen.blit(title, (20, 20))

        if len(self.drawn_points) > 1:
            pygame.draw.lines(
                self.screen,
                self.path_color,
                False,
                [(int(x), int(y)) for x, y in self.drawn_points],
                3,
            )

        if self.robot_pos is not None:
            pygame.draw.circle(
                self.screen,
                self.robot_color,
                (int(self.robot_pos[0]), int(self.robot_pos[1])),
                8,
            )

        pygame.display.flip()
        self.clock.tick(60)

    def step(self):
        self.update()
        self.draw()

    def is_running(self):
        return self.running

    def close(self):
        pygame.quit()