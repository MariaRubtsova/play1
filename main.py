import pygame
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Kings and Pigs')

#определение действий игрока
moving_left = False
moving_right = False
#moving_up = False
#moving_down = False

class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        img = pygame.image.load('player/idle1.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        #сбросить значения переменных
        dx= 0
        dy = 0
        #назначение перемещения при перемещении влево или вправо
        if moving_left:
            dx = -self.speed
        if moving_right:
            dx = self.speed

        #обновить положение прямоугольника
        self.rect.x += dx
        self.rect.y += dy


    def draw(self):
        screen.blit(self.image, self.rect)

player = Hero(200, 200, 2, 5)

run = True
while run:

    player.draw()

    player.move(moving_left, moving_right)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #нажатие клавиатуры
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            moving_left = True
        if event.key == pygame.K_d:
            moving_right = True
        #if event.key == pygame.K_UP:
        #    moving_up = True
        #if event.key == pygame.K_DOWN:
        #    moving_down = True

    #клавиша отпущена
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            moving_left = False
        if event.key == pygame.K_d:
            moving_right = False
        #if event.key == pygame.K_UP:
        #    moving_up = False
        #if event.key == pygame.K_DOWN:
        #    moving_down = False
        if event.key == pygame.K_ESCAPE:
            run = False

    pygame.display.update()

pygame.quit()





