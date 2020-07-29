#https://code.tutsplus.com/series/building-games-with-python-3-and-pygame--cms-1245

import os
import random
import time
from datetime import datetime, timedelta

import pygame
from pygame.rect import Rect

import misc.colors as colors
import misc.config as config
from game import Game
from game_objects.ball import Ball
from game_objects.brick import Brick
from game_objects.button import Button
from game_objects.paddle import Paddle
from game_objects.text_object import TextObject

special_effects = dict(
    long_paddle=(
        colors.ORANGE,
        lambda g: g.paddle.bounds.inflate_ip(
            config.PADDLE_WIDTH // 2, 0),
        lambda g: g.paddle.bounds.inflate_ip(
            -config.PADDLE_WIDTH // 2, 0)),
    slow_ball=(
        colors.AQUAMARINE2,
        lambda g: g.change_ball_speed(-1),
        lambda g: g.change_ball_speed(1)),
    tripple_points=(
        colors.DARKSEAGREEN4,
        lambda g: g.set_points_per_brick(3),
        lambda g: g.set_points_per_brick(1)),
    extra_life=(
        colors.GOLD1,
        lambda g: g.add_life(),
        lambda g: None))

assert os.path.isfile('sound_effects/brick_hit.wav')

class Breakout(Game):
    def __init__(self):
        super().__init__(
            '벽돌 깨기', 
            config.SCREEN_WIDTH, 
            config.SCREEN_HEIGHT, 
            config.BACKGROUND_IMAGE, 
            config.FRAME_RATE)
        self.sound_effects = {
            name: pygame.mixer.Sound(sound) \
                for name, sound in config.SOUNDS_EFFECTS.items()
        }
        self.reset_effect = None
        self.effect_start_time = None
        self.score = 0
        self.lives = config.INITIAL_LIVES
        self.start_level = False
        self.paddle = None
        self.bricks = None
        self.ball = None
        self.menu_buttons = []
        self.is_game_running = False
        self.create_objects()
        self.points_per_brick = 1

    def add_life(self):
        self.lives += 1

    def set_points_per_brick(self, points):
        self.points_per_brick = points

    def change_ball_speed(self, dy):
        self.ball.speed = \
            (self.ball.speed[0], self.ball.speed[1] + dy)

    def create_objects(self):
        self.create_bricks()
        self.create_paddle()
        self.create_ball()
        self.create_labels()
        self.create_menu()

    def create_bricks(self):
        w = config.BRICK_WIDTH
        h = config.BRICK_HEIGHT
        brick_count = config.SCREEN_WIDTH // w#(w + 1)
        #블록을 제외한 나머지 공간 / 2 -> 중앙 정렬
        offset_x = (config.SCREEN_WIDTH - brick_count * w) // 2

        bricks = []
        for row in range(config.ROW_COUNT):
            for col in range(brick_count):
                effect = None
                brick_color = config.BRICK_COLOR
                index = random.randint(0, 10)
                if index < len(special_effects):
                    brick_color, start_effect_func, reset_effect_func = \
                        list(special_effects.values())[index]
                    effect = start_effect_func, reset_effect_func

                brick = Brick(
                    offset_x + col * w,#(w + 1),
                    config.OFFSET_Y + row * h,#(h + 1),
                    w,
                    h,
                    brick_color,
                    effect
                )
                bricks.append(brick)

        self.bricks = bricks
        self.objects.extend(bricks)

    def create_paddle(self):
        paddle = Paddle(
            x=(config.SCREEN_WIDTH - config.PADDLE_WIDTH) // 2,
            y=config.SCREEN_HEIGHT - config.PADDLE_HEIGHT * 2,
            w=config.PADDLE_WIDTH,
            h=config.PADDLE_HEIGHT,
            color=config.PADDLE_COLOR,
            offset=config.PADDLE_SPEED)
        self.keydown_handlers[pygame.K_LEFT].append(paddle.handle)
        self.keydown_handlers[pygame.K_RIGHT].append(paddle.handle)
        self.keyup_handlers[pygame.K_LEFT].append(paddle.handle)
        self.keyup_handlers[pygame.K_RIGHT].append(paddle.handle)
        self.paddle = paddle
        self.objects.append(self.paddle)

    def create_ball(self):
        speed = (random.randint(-2, 2), config.BALL_SPEED)
        self.ball = Ball(
            config.SCREEN_WIDTH_CENTER,
            config.SCREEN_HEIGHT_CENTER,
            config.BALL_RADIUS,
            config.BALL_COLOR,
            speed
        )
        self.objects.append(self.ball)

    def create_labels(self):
        self.score_label = TextObject(
            x=config.SCORE_OFFSET,
            y=config.STATUS_OFFSET_Y,
            #() => "~~~"
            text_func=lambda: f'SCORE: {self.score}',
            color=config.TEXT_COLOR,
            font_name=config.FONT_NAME,
            font_size=config.FONT_SIZE
        )
        self.objects.append(self.score_label)
        self.lives_label = TextObject(
            x=config.LIVES_OFFSET,
            y=config.STATUS_OFFSET_Y,
            text_func=lambda: f'LIVES: {self.lives}',
            color=config.TEXT_COLOR,
            font_name=config.FONT_NAME,
            font_size=config.FONT_SIZE
        )
        self.objects.append(self.lives_label)

    def create_menu(self):
        def on_click_play():
            for b in self.menu_buttons:
                self.objects.remove(b)
            
            self.is_game_running = True
            self.start_level = True

        def on_click_quit():
            self.game_over = True
            self.is_game_running = False

        for i, (text, handler) \
            in enumerate(
                (
                    ('PLAY', on_click_play), 
                    ('QUIT', on_click_quit)
                )
            ):
            b = Button(
                config.MENU_OFFSET_X,
                config.MENU_OFFSET_Y \
                    + (config.MENU_BUTTON_H + 5) * i,
                config.MENU_BUTTON_W,
                config.MENU_BUTTON_H,
                text,
                handler,
                padding = 5
            )
            self.objects.append(b)
            self.menu_buttons.append(b)
            self.mouse_handlers.append(b.handle_mouse_event)

    def handle_ball_collisions(self):
        def intersect(obj, ball):
            edges = obj.edges
            collisions = list(
                edge for edge, rect in edges.items()\
                    if ball.bounds.colliderect(rect)
            )

            if not collisions:
                return None

            if len(collisions) == 1:
                return collisions[0]
            
            #겹칠 수 있는 경우는 각 모서리 4곳
            #top-left, top-right, bottom-right, bottom-left
            if 'top' in collisions:
                collisions.remove('top')
                if ball.centery <= obj.top:
                #if ball.centery >= obj.top:
                    return 'top'
                else:
                    collisions[0]
            else:
                collisions.remove('bottom')
                if ball.centery >= obj.bottom:
                    return 'bottom'
                else:
                    collisions[0]

        #Hit paddle
        s = self.ball.speed
        edge = intersect(self.paddle, self.ball)
        # if edge is not None:
        #     self.sound_effects['paddle_hit'].play()
        if edge == 'top':
            speed_x = s[0]
            speed_y = -s[1]
            if self.paddle.moving_left:
                #패들이 왼쪽으로 이동중이었다면, 왼쪽으로 가속
                speed_x -= 1
            elif self.paddle.moving_right:
                #패들이 오른쪽으로 이동중이었다면, 오른쪽으로 가속
                speed_x += 1
            self.ball.speed = (speed_x, speed_y)
        elif edge in ('left', 'right'):
            #y축은 그대로 두고 x축만 반대로
            self.ball.speed = (-s[0], s[1])
        
        #Hit floor
        if self.ball.top > config.SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives == 0:
                self.game_over = True
            else:
                self.create_ball()

        #Hit ceiling
        if self.ball.top <= 0:
            #x축 이동은 그대로 두고 y축만 반대로
            self.ball.speed = (s[0], -s[1])

        #Hit wall
        if self.ball.left <= 0 \
            or self.ball.right >= config.SCREEN_WIDTH:
            #y축은 그대로 두고 x축만 반전
            self.ball.speed = (-s[0], s[1])
        
        #Hit brick
        for brick in self.bricks:
            edge = intersect(brick, self.ball)
            if not edge:
                continue

            #self.sound_effects['brick_hit'].play()
            self.bricks.remove(brick)
            self.objects.remove(brick)
            self.score += self.points_per_brick

            if edge in ('top', 'bottom'):
                #x축은 그대로 두고 y축만 반전
                self.ball.speed = (s[0], -s[1])
            else:
                #y축을 그대로 두고, x축만 반전
                self.ball.speed = (-s[0], s[1])

            if brick.special_effect is not None:
                #기존의 효과 초기화
                if self.reset_effect is not None:
                    self.reset_effect(self)

                #효과 발동
                self.effect_start_time = datetime.now()
                brick.special_effect[0](self)
                #현재의 쵸기화 함수 등록
                self.reset_effect = brick.special_effect[1]

    def update(self):
        if not self.is_game_running:
            return

        if self.start_level:
            self.start_level = False
            self.show_message('준비!', center=True)

        if not self.bricks:
            self.show_message('승리!', center=True)
            self.is_game_running = False
            self.game_over = True

        if self.reset_effect:
            if datetime.now() - self.effect_start_time \
                >= timedelta(seconds=config.EFFECT_DURATION):
                self.reset_effect(self)
                self.reset_effect = None

        self.handle_ball_collisions()
        super().update()

        if self.game_over:
            self.show_message('게임 끗!', center=True)

    def show_message(
        self,
        text,
        color=colors.WHITE,
        font_name=config.FONT_NAME,
        font_size=20,
        center=False):
        message = TextObject(
            config.SCREEN_WIDTH_CENTER,
            config.SCREEN_HEIGHT_CENTER,
            #() => text()
            lambda: text,
            color,
            font_name,
            font_size
        )
        self.draw()
        message.draw(self.surface, center)
        pygame.display.update()
        time.sleep(config.MESSAGE_DURATION)

def main():
    Breakout().run()

#임포트 된 경우가 아니라 python 명령을 통해 직접 실행되는 경우에만
#if문에 포함된 코드를 실행하라는 명령
if __name__ == '__main__':
    main()
