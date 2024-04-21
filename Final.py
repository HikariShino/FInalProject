import pygame


pygame.init()


fpsClock = pygame.time.Clock()
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invader")

background = (22, 20, 87)
fps = 60
light_green = (200, 224, 69)
red = (228, 8, 10)

player_image = pygame.image.load('Assets/Player.png')
player_image = pygame.transform.scale(player_image, (50, 50))
player_image = pygame.transform.rotate(player_image, 180)
player_rect = player_image.get_rect()


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = player_rect.copy()
        self.rect.topleft = (self.x, self.y)
        self.speed = 6

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.move_ip(self.speed, 0)


class Laser:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 2, 10)
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed


player = Player(175, 520)
lasers = []

run = True
while run:
    fpsClock.tick(fps)
    screen.fill(background)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                lasers.append(Laser(player.rect.centerx, player.rect.top))

    player.move()
    screen.blit(player_image, player.rect)

    for laser in lasers[:]:
        laser.update()
        pygame.draw.rect(screen, light_green, laser.rect)
        if laser.rect.bottom < 0:
            lasers.remove(laser)

    pygame.display.update()


pygame.quit()
