#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

FPS = 30
WIDTH, HEIGHT = 800, 600


class Backdrop(pygame.sprite.Sprite):
    """An object that holds the background of the scene"""
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("assets/grass_backdrop.jpg")

        self.rect = self.image.get_rect()


class Character(pygame.sprite.Sprite):
    """Main character for our demo"""
    def __init__(self, input_dict):
        super().__init__()

        self.input = input_dict

        self.images = {}
        self.images["right"] = pygame.image.load(
            "assets/character.png"
        )
        self.images["left"] = pygame.transform.flip(
            self.images["right"], True, False
        )

        self.image = self.images["right"]

        self.rect = self.image.get_rect()

        self.x, self.y = 0, 0
        self.vx, self.vy = 0, 0
        self.ax, self.ay = 0, 0

        self.a = 2.4
        self.drag = 0.22
        self.min_vel = 0.2
        self.max_vel = 12.0

        self.set_pos(self.x, self.y)
    

    def set_pos(self, x, y):
        """Sets the character's position with correct origin"""
        self.x, self.y = x, y

        self.rect.x = x - self.rect.w / 2
        self.rect.y = y - self.rect.h / 2
    

    def handle_input(self):
        """Calculates acceleration based on input values"""
        self.ax, self.ay = 0, 0

        if self.input["up"]:
            self.ay -= self.a
        if self.input["down"]:
            self.ay += self.a
        if self.input["left"]:
            self.ax -= self.a
        if self.input["right"]:
            self.ax += self.a
        

    def apply_acceleration(self):
        """Calculates the acceleration based on velocity"""
        self.vx += self.ax
        self.vy += self.ay
        

    def apply_drag(self):
        """Calculates the effect of drag on velocity"""
        self.vx *= 1 - self.drag
        self.vy *= 1 - self.drag


    def apply_velocity(self):
        """Updates position based on constrained velocity"""
        if -self.min_vel < self.vx < self.min_vel:
            self.vx = 0
        if -self.min_vel < self.vy < self.min_vel:
            self.vy = 0

        if self.vx < -self.max_vel:
            self.vx = -self.max_vel
        elif self.vx > self.max_vel:
            self.vx = self.max_vel

        self.set_pos(self.x + self.vx, self.y + self.vy)


    def update_animation(self):
        """Changes character's appearance for animation"""
        if self.vx > 0:
            self.image = self.images["right"]
        elif self.vx < 0:
            self.image = self.images["left"]
    

    def update(self):
        """Updates character sprite"""
        self.handle_input()

        self.apply_acceleration()
        self.apply_drag()
        self.apply_velocity()

        self.update_animation()


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

        self.character = Character(self.input)
        self.character.set_pos(-80, HEIGHT / 2)

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.backdrop)
        self.sprites.add(self.character)


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