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
import random

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SPRITE_SCALE
)
from sprite_sheet import SpriteSheet
from player import Player
from enemy import Enemy
from beam import Beam

#사운드 초기화
pygame.mixer.init()

pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

#스프라이트 로드
#스프라이트는 opengameart.org
sheet = SpriteSheet("sprites\\sheet.png", "sprites\\sheet.xml")

#배경 서피스 설정
bg = pygame.image.load("sprites\\bg_darkPurple.png")
bg_width = bg.get_width()
bg_height = bg.get_height()
bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
for y in range(0, SCREEN_HEIGHT, bg_height):
    for x in range(0, SCREEN_WIDTH, bg_width):
        bg_surface.blit(bg, (x, y))

#게임 속도 설정을 위한 시계
clock = pygame.time.Clock()

#event는 int로 정의되는데,
#USEREVENT가 가장 마지막에 위치하므로 +1로 새로운 이벤트 정의
ADDENEMY = pygame.USEREVENT + 1
#250ms 마다 이벤트 발생
pygame.time.set_timer(ADDENEMY, 250)

ENEMYFIRE = ADDENEMY + 1
pygame.time.set_timer(ENEMYFIRE, 300)

player = Player(sheet)

enemies = pygame.sprite.Group()
enemy_beams = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

shooting_sound = pygame.mixer.Sound("sounds\\sfx_laser2.ogg")

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy(sheet)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ENEMYFIRE:
            for enemy in enemies:
                enemy_fire = enemy.fire()
                if enemy_fire is not None:
                    enemy_beams.add(enemy_fire)
                    all_sprites.add(enemy_fire)
                    shooting_sound.play()
    
    screen.blit(bg_surface, (0, 0))

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)

    enemies.update()

    enemy_beams.update()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies) \
        or pygame.sprite.spritecollideany(player, enemy_beams):
        player.kill()
        running = False

    #update the display
    pygame.display.flip()

    #60프레임으로 설정
    clock.tick(60)

pygame.quit()