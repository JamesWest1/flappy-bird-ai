import os
import pygame

class Bird:
    def __init__(self, screensize):
        self.x = 60
        self.y = 300
        self.vel = 0
        self.accel = 2400
        self.screensize = screensize
        self.img = pygame.image.load(os.path.join('images', 'bird.png'))
        self.img = pygame.transform.rotozoom(self.img, 0, 2)
        self.height = 30
        self.width = 44
    def jump(self):
        self.vel = -550
    def update(self, dt):
        self.y += self.vel * dt + 1/2 * self.accel * dt**2
        self.vel = self.accel * dt + self.vel
        self.vel = min(self.vel, 450)
    def checkCollision(self, pipe):
        if pipe.x < self.x + self.width / 2 and  self.x - self.width / 2 < pipe.x + pipe.width:
            return (not (self.y + self.height / 2 < pipe.height)) or (not (self.y - self.height / 2 > pipe.height - pipe.middleGap))
        return False
    def hitGround(self):
        return self.y > self.screensize - self.height - 50
    def draw(self, screen):
        screen.blit(self.img, self.img.get_rect(center=(self.x, self.y)))