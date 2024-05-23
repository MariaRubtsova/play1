import pygame
import os
import csv
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Kings and Pigs')

clock = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
GRAVITY = 0.75
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 26
screen_scroll = 0
bg_scroll = 0

moving_left = False
moving_right = False
moving_down = False


# хранить плитки в списке
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

diamonds_img = pygame.image.load('img/diamonds/25.png').convert_alpha()
diamonds_img = pygame.transform.scale(diamonds_img, (20, 17))
background = pygame.image.load('img/background/fon.png')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
heart_img = pygame.image.load('img/health_bar/2.png').convert_alpha()
health_bar_img = pygame.image.load('img/health_bar/1.png').convert_alpha()
health_bar_x = 10
health_bar_y = 65
bar_img = pygame.image.load('img/health_bar/3.png').convert_alpha()
bar_x = 10
bar_y = 5


font = pygame.font.SysFont('ARCADEPI', 30)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


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
        self.attack_rect = None
        #специальные переменные для ai
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0


        animation_types = ['idle', 'run', 'jump', 'fall', 'attack', 'die']
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
        if self.char_type == 'pig' and pygame.sprite.collide_rect(self, player):
            if player.alive and pygame.time.get_ticks() - self.last_hit_time > 1000:  # Проверка прошедшего времени
                player.health -= 1  # Теряется одна жизнь
                print("Player health:", player.health)
                if player.health <= 0:
                    player.alive = False
                    print("Player has died")
                else:
                    # Определение направления столкновения
                    if self.rect.x < player.rect.x:
                        # Столкновение справа, игрок двигается влево
                        player.rect.x += 30
                    else:
                        # Столкновение слева, игрок двигается вправо
                        player.rect.x -= 30

                self.last_hit_time = pygame.time.get_ticks()


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
            self.vel_y = -9
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

        self.rect.x += dx
        self.rect.y += dy

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



    def update_animation(self):
        if not isinstance(self.action, str):
            raise TypeError(f"self.action должно быть строкой, но найдено {type(self.action).__name__}")
        if not isinstance(self.frame_index, int):
            raise TypeError(f"self.frame_index должно быть целым числом, но найдено {type(self.frame_index).__name__}")

        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > self.anim_speed:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 'attack':
                    self.status = None
                    self.action = 'idle'
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
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        # перебирать каждое значение в level data file
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
                    elif tile == 25:#create pig
                        pig = Hero('pig',1,  x * TILE_SIZE, (y + 0.6) * TILE_SIZE,3, 100)
                        pig_group.add(pig)
                    elif tile == 24: #create diamonds
                        diamonds = Diamonds('Diamonds', x * TILE_SIZE, y * TILE_SIZE)
                        Diamonds_group.add(diamonds)
                    elif tile == 23:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)  # украшение

        return player

    def draw(self):
        if self.obstacle_list:
            for tile in self.obstacle_list:
                screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

class Diamonds(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        if self.item_type == 'Diamonds':
            self.image = diamonds_img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()*1.5))


    def update(self):
        #проверка, взял ли игрок бриллиант
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Diamonds':
                player.diamonds += 1
            self.kill()


Diamonds_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
pig_group = pygame.sprite.Group()




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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.attack()

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




        screen.blit(background, (0, 0))

        world.draw()
        player.update_animation()


        # update and draw player
        player.update()
        player.draw()

        # update and draw pigs
        for pig in pig_group:
            pig.ai()
            pig.update()
            pig.draw()

        Diamonds_group.update()
        decoration_group.update()
        decoration_group.draw(screen)
        Diamonds_group.draw(screen)
        player.move(moving_left, moving_right)

        screen.blit(health_bar_img, (health_bar_x, health_bar_y))
        draw_text(f'{player.diamonds}', font, BLACK, 80, 90)

        screen.blit(bar_img, (bar_x, bar_y))
        for x in range(player.health):
            screen.blit(heart_img, (46 + (x * 22), 32))

        pygame.display.update()
        clock.tick(FPS)


pygame.quit()




















