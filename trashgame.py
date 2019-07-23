import pygame
import random
from constants import *

# increase speed of trash creation

score = 0;


class Backdrop(pygame.sprite.Sprite):
    """An object that holds the background of the scene"""
    def __init__(self, backdrop_type):
        super().__init__()

        self.images = {}
        self.images[SKY_BACKGROUND] = pygame.image.load("assets/sky.jpg")
        # self.images[] = pygame.image.load("assets/")  
        
        self.image = self.images[backdrop_type]

        self.rect = self.image.get_rect()



class Button(pygame.sprite.Sprite):
    """The buttons that control the game"""
    def __init__(self, button_type):
        super().__init__()

        self.button_type = button_type
        
        self.images = {}
        self.images[START_BUTTON] = pygame.image.load("assets/start_button.png")
        self.images[HOW_TO_PLAY_BUTTON] = pygame.image.load("assets/how_to_play_button.png")  
        
        self.image = self.images[button_type]

        self.rect = self.image.get_rect()


    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = self.x - self.rect.w / 2
        self.rect.y = self.y - self.rect.h / 2
         
       


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
    """controls the actual game"""
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
        self.time_limit = 50

        self.difficulty_timer = 0
        self.difficulty_time_limit = 240

        self.input = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
        }

        self.sky_backdrop = Backdrop(SKY_BACKGROUND)
       

        self.play_backgrounds = pygame.sprite.Group()
        self.play_backgrounds.add(self.sky_backdrop)

        self.recycling_bin = RecyclingBin(self.input)
        self.recycling_bin.set_pos(WIDTH / 2, HEIGHT - 96)

        self.players = pygame.sprite.Group()
        self.players.add(self.recycling_bin)

        self.trash_items = pygame.sprite.Group()

        self.start_button = Button(START_BUTTON)
        self.start_button.set_pos(WIDTH/2, HEIGHT/2)

        self.how_to_play_button = Button(HOW_TO_PLAY_BUTTON)
        self.how_to_play_button.set_pos(WIDTH/2, HEIGHT/2 + 120)
        
        self.start_buttons = pygame.sprite.Group()
        self.start_buttons.add(self.start_button)

        self.start_buttons.add(self.how_to_play_button)

        self.game_section = START

    def update(self):
        """Updates the game"""
        self.clock.tick(FPS)
        self.handle_input()

        if self.game_section == PLAY:
            self.update_trash()
            self.draw_play_screen()
        elif self.game_section == START:
            self.start_buttons.update()
            self.start_buttons.draw(self.screen)
        elif self.game_section == HOW_TO:
            pass

        pygame.display.flip()

    def draw_play_screen(self):
        """presents the play screen"""
        self.play_backgrounds.update()
        self.play_backgrounds.draw(self.screen)

        self.trash_items.update()
        self.trash_items.draw(self.screen)

        self.players.update()
        self.players.draw(self.screen)
        size = width, height = 800,500
        
        myfont = pygame.font.SysFont("monospace", 16)
        scoretext = myfont.render("Score = "+ str(score), 1, (0,0,0))
        self.screen.blit(scoretext, (5, 10))
    
    def texts(self, score, screen):
            font=pygame.font.Font(None,30)
            scoretext=font.render("Score:"+str(score), 1,(255,255,255))
            screen.blit(scoretext, (500, 457))

    def update_trash(self):
        
        if self.time_limit > 20:
            if self.difficulty_timer >= self.difficulty_time_limit:
                self.difficulty_timer = 0
                self.time_limit -= 2
            else:
                self.difficulty_timer += 1

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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for button in self.start_buttons:
                    if button.rect.collidepoint(pos):
                        if button.button_type == START_BUTTON:
                            self.game_section = PLAY
                        elif button.button_type == HOW_TO_PLAY_BUTTON:
                            self.game_section == HOW_TO


def main():
    """Main entry point for script"""
    game = Game()

    while game.running:
        game.update()
       

if __name__ == '__main__':
    main()
