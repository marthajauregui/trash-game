import pygame

FPS = 30
WIDTH, HEIGHT = 800, 600


class Backdrop(pygame.sprite.Sprite):
    """An object that holds the background of the scene"""
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("assets/sky_2.jpg")

        self.rect = self.image.get_rect()


class Game():
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.running = True

        self.input = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }

        self.backdrop = Backdrop()

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.backdrop)


    def update(self):
        """Updates the game"""
        self.clock.tick(FPS)

        self.handle_input()
        self.sprites.update()
        self.sprites.draw(self.screen)

        pygame.display.flip()


    def handle_input(self):
        """Updates the input dictionary"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_w:
                    self.input["up"] = True
                elif event.key == pygame.K_s:
                    self.input["down"] = True
                elif event.key == pygame.K_a:
                    self.input["left"] = True
                elif event.key == pygame.K_d:
                    self.input["right"] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.input["up"] = False
                elif event.key == pygame.K_s:
                    self.input["down"] = False
                elif event.key == pygame.K_a:
                    self.input["left"] = False
                elif event.key == pygame.K_d:
                    self.input["right"] = False


def main():
    """Main entry point for script"""
    game = Game()

    while game.running:
        game.update()


if __name__ == '__main__':
    main()