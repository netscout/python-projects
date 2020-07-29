import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SPRITE_SCALE
)

class Player(pygame.sprite.Sprite):
    def __init__(self, sheet):
        super(Player, self).__init__()
        #hold the images to display
        self.surf = sheet.get_image_name("playerShip1_blue.png", SPRITE_SCALE)
        #휜색 배경을 투명하게 그리도록 설정
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # self.surf = pygame.Surface((99, 75))
        # self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center = (
                (SCREEN_WIDTH - self.surf.get_width()) / 2,
                SCREEN_HEIGHT - 100
            )
        )

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            #ip stans for move in place
            self.rect.move_ip(0, -10)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 10)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT