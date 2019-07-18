import pygame

FPS = 30
WIDTH, HEIGHT = 800, 600


class Backdrop(pygame.sprite.Sprite):
    """An object that holds the background of the scene"""
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("assets/sky_2.jpg")

        self.rect = self.image.get_rect()


# class Character(pygame.sprite.Sprite):
#     """Main character for our demo"""
#     def __init__(self, input_dict):
#         super().__init__()

#         self.input = input_dict

#         self.images = {}
#         self.images["right"] = pygame.image.load(
#             "assets/character.png"
#         )
#         self.images["left"] = pygame.transform.flip(
#             self.images["right"], True, False
#         )

#         self.image = self.images["right"]

#         self.rect = self.image.get_rect()

#         self.x, self.y = 0, 0
#         self.vx, self.vy = 0, 0
#         self.ax, self.ay = 0, 0

#         self.a = 2.4
#         self.drag = 0.22
#         self.min_vel = 0.2
#         self.max_vel = 12.0

#         self.set_pos(self.x, self.y)
    

    # def update(self):
    #     """Updates character sprite"""
    #     self.handle_input()


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

        # self.character = Character(self.input)
        # self.character.set_pos(-80, HEIGHT / 2)

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.backdrop)
        # self.sprites.add(self.character)


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