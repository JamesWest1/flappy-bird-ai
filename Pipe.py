import pygame
import os
import random

SCROLLSPEED = -4

class Pipe:
    def __init__(self, x):
        self.x = x
        self.middleGap = 165
        self.height = 800 - random.randint(150, 550)
        self.bottomimg = pygame.image.load(os.path.join('images', 'pipe.png'))
        self.topimg = pygame.image.load(os.path.join('images', 'pipe.png'))
        self.bottomimg = pygame.transform.rotozoom(self.bottomimg, 0, 2)
        self.topimg = pygame.transform.rotozoom(self.topimg, 0, 2)
        self.topimg = pygame.transform.rotate(self.topimg, 180)
        self.width = 100
    def update(self):
        self.x += SCROLLSPEED
    def offScreen(self):
        return self.x < -100
    def draw(self, screen):
        screen.blit(self.bottomimg, self.bottomimg.get_rect(topleft=(self.x, self.height)))
        screen.blit(self.topimg, self.topimg.get_rect(bottomleft=(self.x, self.height - self.middleGap)))