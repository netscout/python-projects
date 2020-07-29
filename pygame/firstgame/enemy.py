import pygame
from pygame.locals import (
    RLEACCEL
)
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SPRITE_SCALE
)
import random
from beam import Beam

class Enemy(pygame.sprite.Sprite):
    def __init__(self, sheet):
        super(Enemy, self).__init__()
        # self.surf = pygame.Surface((20, 10))
        # self.surf.fill((255, 255, 255))
        self.surf = sheet.get_image_name("enemyRed1.png", SPRITE_SCALE)
        self.beam = sheet.get_image_name("fire00.png", SPRITE_SCALE)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                -random.randint(0, 200)
            )
        )
        self.speed = random.randint(5, 20)

    def fire(self):
        can_fire = random.randint(0, 100) > 80
        if can_fire:
            return Beam(self.beam, self.rect.centerx, self.rect.centery)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > SCREEN_HEIGHT:
            #sprite group에서 제거
            self.kill()