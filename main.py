import pygame
pygame.init()
import os

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Kings and Pigs')

#установить окно
clock = pygame.time.Clock()
FPS = 60

RED = (255, 0, 0)

GRAVITY = 0.75

#определение действий игрока
moving_left = False
moving_right = False
moving_down = False  # Добавляем переменную для движения вниз

class Hero(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, anim_speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.anim_speed = anim_speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = {}  # Инициализация пустого словаря
        self.frame_index = 0
        self.action = 'idle'  # Устанавливаем начальное действие
        self.update_time = pygame.time.get_ticks()
        #загрузить все анимации для игрока
        animation_types = ['idle', 'run', 'jump', 'fall']
        for animation in animation_types:
            #сбросить временный список изображений
            temp_list = []
            #подсчитывает количество файлов в папке
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i+1}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)  # Добавление изображений в список для текущего действия
            self.animation_list[animation] = temp_list

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        #сбросить значения переменных
        dx= 0
        dy = 0
        #назначение перемещения при перемещении влево или вправо
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        #добавление гравитации
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        if self.rect.bottom + dy > 300:
            dy = 300 -self.rect.bottom
            self.in_air = False

        #обновить положение прямоугольника
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # обновление анимации
        # обновить изображение в зависимости от текущего кадра
        self.image = self.animation_list[self.action][self.frame_index]
        # проверка, прошло ли достаточно времени с момента последнего обновления
        if pygame.time.get_ticks() - self.update_time > self.anim_speed:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()  # обновляем время
        # анимация закончилась, вернуться к началу
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            #обновить настройки анимации
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

player = Hero('player', 200, 200, 2, 5, 100)
pig = Hero('player', 400, 200, 2, 5, 100)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            elif event.key == pygame.K_RIGHT:
                moving_right = True
            elif event.key == pygame.K_UP and player.alive:
                player.jump = True
            elif event.key == pygame.K_DOWN:
                moving_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            elif event.key == pygame.K_RIGHT:
                moving_right = False
            elif event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_UP:
                moving_up = False
            elif event.key == pygame.K_DOWN:
                moving_down = False

    if player.alive:
        if player.in_air:
            player.update_action('jump')
        elif moving_left or moving_right:
            player.update_action('run')
        else:
            player.update_action('idle')

        if player.jump and player.vel_y == 0:
            player.update_action('jump')
        elif player.rect.bottom < 300:
            player.update_action('fall')

        screen.fill((144, 201, 120))
        pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))
        player.update_animation()
        player.draw()
        pig.draw()
        player.move(moving_left, moving_right)
        pygame.display.update()
        clock.tick(FPS)

pygame.quit()













