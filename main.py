import pygame
import os
import csv

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Kings and Pigs')

clock = pygame.time.Clock()
FPS = 60

RED = (255, 0, 0)
GRAVITY = 0.75
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 24

moving_left = False
moving_right = False
moving_down = False

#хранить плитки в списке
img_list = []
for x  in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

class Hero(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, speed, anim_speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.anim_speed = anim_speed
        self.health = 3
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = {}
        self.frame_index = 0
        self.action = 'idle'
        self.update_time = pygame.time.get_ticks()
        self.status = None
        self.image_index = 0
        self.facing_right = True

        animation_types = ['idle', 'run', 'jump', 'fall', 'attack', 'die']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i+1}.png')
                img = pygame.transform.scale(img, (int(img.get_width()), int(img.get_height())))
                temp_list.append(img)
            self.animation_list[animation] = temp_list

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
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
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.bottom + dy > 300:
            dy = 300 -self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    def attack(self) -> None:
        self.status = "attack"
        self.image_index = 0
        left_shift = 49 if self.facing_right else -49
        self.attack_rect = pygame.Rect((self.rect.left + left_shift, self.rect.top), (50, self.rect.height))

    def update_animation(self):
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
        if self.health == 0:
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
        #перебирать каждое значение в level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >=0 and tile <= 21:
                        self.obstacle_list.append(tile_data) #препятствия
                    elif tile > 22:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration) #украшение

                    elif tile == 22:#create player
                        player = Hero('player', x * TILE_SIZE, y * TILE_SIZE, 5, 100)
                    """
                    elif tile == 23:#create pig
                        player = Hero('pig', x * TILE_SIZE, y * TILE_SIZE,...)
                    elif tile == 23:#create diamond
                        diamond = Diamond('Diamond', x * TILE_SIZE, y * TILE_SIZE,...)
                    
                    """

        return player

    def draw(self):
        if self.obstacle_list:
            for tile in self.obstacle_list:
                screen.blit(tile[0], tile[1])
        else:
            print("No tiles to draw")

class Decoration(pygame.sprite.Sprite):
    def __init__(self, item_tipe, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

pig = Hero('player', 400, 200, 5, 100)

decoration_group = pygame.sprite.Group()

#создать пустой список плиток
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

#загружаем данные и создаем мир
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



        screen.fill((144, 201, 120))
        world.draw()
        pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))
        player.update_animation()
        decoration_group.update()
        player.draw()
        pig.draw()
        decoration_group.draw(screen)
        player.move(moving_left, moving_right)
        pygame.display.update()
        clock.tick(FPS)

pygame.quit()


















