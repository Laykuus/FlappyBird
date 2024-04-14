import pygame, random

class Bird:
    def __init__(self):
        sprite = pygame.image.load("./assets/bird_sprite.png")
        self.sprite = pygame.transform.scale(sprite, (75, 53))
        self.rect = self.sprite.get_rect()
        self.rect.topleft = [100, 100]
        self.y_velocity = 0
        self.is_dead = False
    
    def apply_gravity(self):
        if self.y_velocity > -10:
            self.y_velocity -= 0.6
        
        pos = self.rect.topleft
        self.rect.topleft = [pos[0], pos[1] - self.y_velocity]

class Pipe:
    def __init__(self, pos, sprite):
        self.sprite = sprite
        self.rect = self.sprite.get_rect()
        self.rect.topleft = pos