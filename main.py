import pygame
import os
import csv
import random
import button

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Спасение принцессы')

clock = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
BG = (63, 56, 81)
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 27
screen_scroll = 0
bg_scroll = 0
scroll = 0
start_game = False

moving_left = False
moving_right = False
moving_down = False

# хранить плитки в списке
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()
diamonds_img = pygame.image.load('img/diamonds/25.png').convert_alpha()
diamonds_img = pygame.transform.scale(diamonds_img, (20, 17))
background = pygame.image.load('img/background/fon.png').convert_alpha()
heart_img = pygame.image.load('img/health_bar/2.png').convert_alpha()
health_bar_img = pygame.image.load('img/health_bar/1.png').convert_alpha()
health_bar_x = 10
health_bar_y = 65
bar_img = pygame.image.load('img/health_bar/3.png').convert_alpha()
bar_x = 10
bar_y = 5

font = pygame.font.SysFont('PixelifySans-Medium.ttf', 30)
font1 = pygame.font.SysFont('PixelifySans-Medium.ttf', 90)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg():
    screen.fill(BG)
    width = background.get_width()
    for x in range(4):
        screen.blit(background, ((x * width) - bg_scroll * 0.5, 0))


def reset_level():
    pig_group.empty()
    decoration_group.empty()
    exit_group.empty()
    Diamonds_group.empty()

    # создать пустой список плиток
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data


class Hero(pygame.sprite.Sprite):
    def __init__(self, char_type, health, x, y, speed, anim_speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.anim_speed = anim_speed
        self.diamonds = 0
        self.health = health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = {}
        self.frame_index = 0
        self.action = 'idle'
        self.update_time = pygame.time.get_ticks()
        self.last_hit_time = pygame.time.get_ticks()
        self.status = None
        self.image_index = 0
        self.facing_right = True
        self.attack_fm = 0
        self.last_attack_time = 0
        self.attack_delay = 2000  # Время задержки после атаки (в миллисекундах)
        # специальные переменные для ai
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0

        self.atttaakkk_fm = 0

        animation_types = ['idle', 'run', 'jump', 'fall', 'attack', 'die', 'hit']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i + 1}.png')
                img = pygame.transform.scale(img, (int(img.get_width()), int(img.get_height())))
                temp_list.append(img)
            self.animation_list[animation] = temp_list

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.terrain_collision_rect = pygame.Rect((self.rect.left + 24, self.rect.top), (50, self.rect.height))

    def update(self):
        self.update_animation()
        self.check_alive()

            # Проверка столкновения с игроком

    def update(self):
        self.update_animation()
        self.check_alive()

        if self.char_type == 'pig' and pygame.sprite.collide_rect(self, player) and pygame.sprite.collide_rect_ratio(0.8)(self, player):
            if player.alive and pygame.time.get_ticks() - self.last_hit_time > 1000:
                if self.action != 'die':  # Добавляем проверку на состояние анимации смерти
                    if player.action == 'attack':  # Проверяем, активна ли анимация атаки у игрока
                        player.attack()  # Вызываем метод атаки, чтобы игрок мог атаковать свинью
                        self.health -= 1  # Снижаем здоровье свиньи
                    else:
                        player.update_action('hit')
                        player.health -= 1
                        if player.health <= 0:
                            player.alive = False
                        else:
                            if self.rect.x < player.rect.x:
                                player.rect.x += 30
                            else:
                                player.rect.x -= 30
                    self.last_hit_time = pygame.time.get_ticks()

        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action('die')

    def move(self, moving_left, moving_right):
        screen_scroll = 0
        dx = 0
        dy = 0
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
            self.facing_right = False
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
            self.facing_right = True

        if self.jump == True and self.in_air == False:
            self.vel_y = -12
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # проверка препятсвий
        for tile in world.obstacle_list:
            # проверка препятсвий в направлении х
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if self.char_type == 'pig':
                    self.direction *= -1
                    self.move_counter = 0
            # проверка препятсвий в направлении y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                dx = 0
                # проверка, если ниже земли, то прыгает
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # проверка, если находится над землей, то падает
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

            # check for collision with exit
            level_complete = False
            if pygame.sprite.spritecollide(self, exit_group, False):
                level_complete = True

            # check if fallen off the map
            if self.rect.bottom > SCREEN_HEIGHT:
                self.health = 0

            # check if going off the edges of the screen
            if self.char_type == 'player':
                if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                    dx = 0

        self.rect.x += dx
        self.rect.y += dy

        # update scroll based on player position
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (
                    world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
                    or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action('idle')
                self.idling = True
                self.idling_counter = 50

            if self.idling == False:
                if self.direction == 1:
                    ai_moving_right = True
                else:
                    ai_moving_right = False
                ai_moving_left = not ai_moving_right
                self.move(ai_moving_left, ai_moving_right)
                self.update_action('run')
                self.move_counter += 1

                if self.move_counter > TILE_SIZE:
                    self.direction *= -1
                    self.move_counter *= -1
            else:
                self.idling_counter -= 1
                if self.idling_counter <= 0:
                    self.idling = False

        self.rect.x += screen_scroll

    def attack(self):
        f = self.attack_fm < 2
        self.attack_fm += 0.3
        self.image = self.animation_list['attack'][min(int(self.attack_fm), 1)]
        if (not f): self.attack_fm = 0

        # Проверка столкновения с каждой свиньей только если анимация атаки не активна
        if self.char_type == 'player' and not f:
            for pig in pig_group:
                if pygame.sprite.collide_rect(self, pig) and pygame.sprite.collide_rect_ratio(0.8)(self, pig):
                    pig.health -= 1  # Сокращенное условие столкновения
        return f

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0


    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action('die')

    def draw(self):
        if start_game:  # Добавлена проверка, чтобы герой прорисовывался только в игровом режиме
            if (self.image in self.animation_list['attack']):
                self.rect.x += 18 if self.direction == 1 else -55
                self.rect.y -= 30
                screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
                self.rect.x -= 18 if self.direction == 1 else -55
                self.rect.y += 30
            else:
                screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        # перебирать каждое значение в level data file
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 21:
                        self.obstacle_list.append(tile_data)  # препятствия
                    elif tile == 22:  # create player
                        player = Hero('player', 3, x * TILE_SIZE, y * TILE_SIZE, 5, 100)
                    elif tile == 25:  # create pig
                        pig = Hero('pig', 1, x * TILE_SIZE, (y + 0.6) * TILE_SIZE, 3, 100)
                        pig_group.add(pig)
                    elif tile == 24:  # create diamonds
                        diamonds = Diamonds('Diamonds', x * TILE_SIZE, y * TILE_SIZE)
                        Diamonds_group.add(diamonds)
                    elif tile == 23:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)  # украшение
                    elif tile == 26:  # create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)

        return player

    def draw(self):
        if self.obstacle_list:
            for tile in self.obstacle_list:
                tile[1][0] += screen_scroll
                screen.blit(tile[0], tile[1])


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Diamonds(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        if self.item_type == 'Diamonds':
            self.image = diamonds_img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height() * 1.5))

    def update(self):
        self.rect.x += screen_scroll
        # проверка, взял ли игрок бриллиант
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Diamonds':
                player.diamonds += 1
            self.kill()


start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)

Diamonds_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
pig_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# создать пустой список плиток
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

# загружаем данные и создаем мир
with open(f'Level0_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
player = world.process_data(world_data)

run = True


ffffffff = False
while run:
    clock.tick(FPS)
    if start_game == False:
        # draw menu
        screen.fill(BG)

        # add buttons
        if start_button.draw(screen):
            start_game = True
        if exit_button.draw(screen):
            run = False
    else:

        # update background
        draw_bg()
        # draw world map
        world.draw()

        player.update()
        #player.draw()

        # update and draw pigs
        for pig in pig_group:
            pig.ai()
            pig.update()
            pig.draw()

        # update and draw groups
        Diamonds_group.update()
        decoration_group.update()
        exit_group.update()
        decoration_group.draw(screen)
        Diamonds_group.draw(screen)
        player.move(moving_left, moving_right)
        exit_group.draw(screen)

        screen.blit(health_bar_img, (health_bar_x, health_bar_y))
        draw_text(f'{player.diamonds}', font, BLACK, 80, 90)

        screen.blit(bar_img, (bar_x, bar_y))
        for x in range(player.health):
            screen.blit(heart_img, (46 + (x * 22), 32))

        # update player actions
        if player.alive:
            if player.in_air:
                player.update_action('jump')
            elif moving_left or moving_right:
                player.update_action('run')
            else:
                player.update_action('idle')
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            # проверка, завершил ли игрок уровень
            if level_complete:
                screen_scroll = 0
                pygame.draw.rect(screen, WHITE, (
                SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 50, SCREEN_WIDTH - 265, SCREEN_HEIGHT // 2 - 225))
                pygame.draw.rect(screen, BLACK, (
                SCREEN_WIDTH // 2 - 240, SCREEN_HEIGHT // 2 - 40, SCREEN_WIDTH - 285, SCREEN_HEIGHT // 2 - 245))
                draw_text('ВЫ ВЫИГРАЛИ!', font1, WHITE, SCREEN_WIDTH // 2 - 230, SCREEN_HEIGHT // 2 - 30)
        else:
            screen_scroll = 0
            if restart_button.draw(screen):
                bg_scroll = 0
                world_data = reset_level()
                with open(f'Level0_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World()
                player = world.process_data(world_data)

            player.update_animation()


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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                ffffffff = True

    if ffffffff: ffffffff = player.attack()

    player.draw()
    pygame.display.update()

pygame.quit()


















