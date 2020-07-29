import pygame
from pygame.locals import (
    RLEACCEL
)
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SPRITE_SCALE
)

class Beam(pygame.sprite.Sprite):
    def __init__(self, beam_image, enemy_center_x, enemy_center_y):
        super(Beam, self).__init__()
        self.surf = beam_image
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                enemy_center_x,
                enemy_center_y
            )
        )
        self.speed = 21

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > SCREEN_HEIGHT:
            #sprite group에서 제거
            self.kill()