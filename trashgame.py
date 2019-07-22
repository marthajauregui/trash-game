import pygame
import random

FPS = 30
WIDTH, HEIGHT = 800, 600

# increase speed of trash creation


class Backdrop(pygame.sprite.Sprite):
    """An object that holds the background of the scene"""
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("assets/sky.jpg")

        self.rect = self.image.get_rect()


class RecyclingBin(pygame.sprite.Sprite):
    """A bin that captures recycling"""
    def __init__(self, input_dictionary):
        super().__init__()

        self.input = input_dictionary

        self.image = pygame.image.load("assets/recycling.png")

        self.rect = self.image.get_rect()
        self.collision_rect = self.image.get_rect()
        self.collision_rect.w = 0.8 * self.collision_rect.w
        self.collision_rect.h = 10

        self.x = 0
        self.y = 0


    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = self.x - self.rect.w / 2
        self.rect.y = self.y - self.rect.h / 2
        self.collision_rect.x = self.rect.x
        self.collision_rect.y = self.rect.y


    
    def update(self):
        vx = 0
        speed = 10

        if self.input["right"]:
            vx = speed
        elif self.input["left"]:
            vx = -speed

        self.set_pos(self.x + vx, self.y)



class Trash(pygame.sprite.Sprite):
    """Items of trash"""
    def __init__(self, trash_type):
        super().__init__()

        self.trash_type = trash_type
        self.trash_speed = 4

        self.trash_types = [
            "banana_peel", "boot", "broken_egg", "broken_bottle", "carboard_box", 
            "envelope_2", "foil", "milk_carton", "orange_juice", "plastic_bottle", 
            "rotten_apple", "soda_can", "spilled_water", "trash_bag", "tuna_can"
        ]

        self.images = {}
        self.images["banana_peel"] = pygame.image.load("assets/banana_peel.png")
        self.images["boot"] = pygame.image.load("assets/boot.png")
        self.images["broken_egg"] = pygame.image.load("assets/broken_egg.png")
        self.images["broken_bottle"] = pygame.image.load("assets/broken_bottle.png")
        self.images["carboard_box"] = pygame.image.load("assets/carboard_box.png")
        self.images["envelope_2"] = pygame.image.load("assets/envelope_2.png")
        self.images["foil"] = pygame.image.load("assets/foil.png")
        self.images["milk_carton"] = pygame.image.load("assets/milk_carton.png")    
        self.images["orange_juice"] = pygame.image.load("assets/orange_juice.png")
        self.images["plastic_bottle"] = pygame.image.load("assets/plastic_bottle.png")
        self.images["rotten_apple"] = pygame.image.load("assets/rotten_apple.png")
        self.images["soda_can"] = pygame.image.load("assets/soda_can.png")
        self.images["spilled_water"] = pygame.image.load("assets/spilled_water.png")
        self.images["trash_bag"] = pygame.image.load("assets/trash_bag.png")
        self.images["tuna_can"] = pygame.image.load("assets/tuna_can.png")
        
        self.image = self.images[self.trash_type]

        self.x = 0
        self.y = 0

        self.rect = self.image.get_rect()


    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = self.x - self.rect.w / 2
        self.rect.y = self.y - self.rect.h / 2


    def update(self):
        self.set_pos(self.x, self.y + self.trash_speed)

        if self.y > HEIGHT:
            self.kill()


class Game():
    def __init__(self):
        pygame.init()

        self.trash_types = [
            "banana_peel", "boot", "broken_egg", "broken_bottle", "carboard_box", 
            "envelope_2", "foil", "milk_carton", "orange_juice", "plastic_bottle", 
            "rotten_apple", "soda_can", "spilled_water", "trash_bag", "tuna_can"
        ]

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.score = 0

        self.running = True

        self.timer = 0
        self.time_limit = 20

        self.input = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }

        self.backdrop = Backdrop()

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.backdrop)

        self.recycling_bin = RecyclingBin(self.input)
        self.recycling_bin.set_pos(WIDTH / 2, HEIGHT - 96)

        self.players = pygame.sprite.Group()
        self.players.add(self.recycling_bin)

        self.trash_items = pygame.sprite.Group()


    def update(self):
        """Updates the game"""
        self.clock.tick(FPS)

        self.handle_input()
        self.update_trash()

        self.draw()


    def draw(self):
        self.sprites.update()
        self.sprites.draw(self.screen)

        self.trash_items.update()
        self.trash_items.draw(self.screen)

        self.players.update()
        self.players.draw(self.screen)

        pygame.display.flip()


    def update_trash(self):
        if self.timer >= self.time_limit:
            self.timer = 0
            trash_piece = Trash(random.choice(self.trash_types))
            trash_piece.set_pos(random.randint(0, WIDTH), -10)

            self.trash_items.add(trash_piece)
        else:
            self.timer += 1

        for trash_item in self.trash_items:
            if trash_item.rect.colliderect(self.recycling_bin.collision_rect):
                self.score += 10
                trash_item.kill()
                print(self.score)



        

        
    def handle_input(self):
        """Updates the input dictionary"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_a:
                    self.input["left"] = True
                elif event.key == pygame.K_d:
                    self.input["right"] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
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
