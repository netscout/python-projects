import pygame

from game_objects.game_object import GameObject

class Ball(GameObject):
    def __init__(self, x, y, r, color, speed):
        """
        원의 x, y는 중심을 나타낸다.
        GameObject의 x, y는 left, top이다.
        """
        super().__init__(
            x - r, 
            y - r, 
            w=r * 2, 
            h=r * 2, 
            speed=speed)
        #반지름
        self.radius = r
        #지름
        self.diameter = r * 2
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            self.color,
            self.center,
            self.radius
        )