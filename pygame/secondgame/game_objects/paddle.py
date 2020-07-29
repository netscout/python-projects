import pygame

#import config as conf
from game_objects.game_object import GameObject
import misc.config as config

class Paddle(GameObject):
    def __init__(self, x, y, w, h, color, offset):
        super().__init__(x, y, w, h)
        self.color = color
        self.offset = offset
        self.moving_left = False
        self.moving_right = False

    def handle(self, key):
        if key == pygame.K_LEFT:
            self.moving_left = not self.moving_left
            #self.moving_right = False
        else:
            self.moving_right = not self.moving_right
            #self.moving_left = False

    def update(self):
        #화면 밖으로 나가지 않도록 처리
        if self.moving_left:
            dx = -(min(self.offset, self.left))
        elif self.moving_right:
            dx = min(self.offset, config.SCREEN_WIDTH - self.right)
        else:
            return

        self.move(dx, 0)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)