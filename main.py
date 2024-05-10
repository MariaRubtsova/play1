import pygame
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Kings and Pigs')

#установить окно
clock = pygame.time.Clock()
FPS = 60

RED = (255, 0, 0)

GRAVITY = 0.6

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
        self.flip = False
        self.animation_list = [[] for _ in range(2)]  # Инициализация пустых списков
        self.frame_index = 1
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(1, 12):
            img = pygame.image.load(f'img/{self.char_type}/idle/{i}.png')
            image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animation_list[0].append(image)  # Добавление изображений в список для действия "покой"

        for i in range(1, 9):
            img = pygame.image.load(f'img/{self.char_type}/run/{i}.png')
            image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animation_list[1].append(image)  # Добавление изображений в список для действия "бег"

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

        if self.jump:
            self.vel_y = -11
            self.jump = False

        #добавление гравитации
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        if self.rect.bottom + dy > 300:
            dy = 300 -self.rect.bottom

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
        if moving_left or moving_right:
            player.update_action(1)  # 1: run
        else:
            player.update_action(0)  # 0: idle




        screen.fill((144, 201, 120))
        pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))
        player.update_animation()
        player.draw()
        pig.draw()
        player.move(moving_left, moving_right)
        pygame.display.update()
        clock.tick(FPS)

pygame.quit()





