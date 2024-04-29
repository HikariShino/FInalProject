import pygame
import math

pygame.init()
pygame.mixer.init()

laser_sound = pygame.mixer.Sound('Assets/laser.mp3')

fpsClock = pygame.time.Clock()
screen_width = 400
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invader")

background = (22, 20, 87)
fps = 60
light_green = (200, 224, 69)
red = (228, 8, 10)
score = 0
font = pygame.font.SysFont('Arial', 20)

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
        self.speed = 5

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


alien1_image = pygame.image.load('Assets/Alien-V1.png')
alien1_image = pygame.transform.scale(alien1_image, (25, 25))
alien2_image = pygame.image.load('Assets/Alien-V2.png')
alien2_image = pygame.transform.scale(alien2_image, (25, 25))
alien3_image = pygame.image.load('Assets/Alien-V3.png')
alien3_image = pygame.transform.scale(alien3_image, (25, 25))


class Basic:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1
        self.direction = 1
        self.down_speed = 1
        self.moving_down = True

    def move(self):
        if self.moving_down:
            self.rect.y += self.down_speed
            if self.rect.top > 0:
                self.moving_down = False
        else:
            self.rect.x += self.speed * self.direction
            if self.rect.right >= screen_width or self.rect.left <= 0:
                self.direction *= -1
                self.rect.y += 50
            if score >= 500 < 1000:
                self.speed = 2
                self.down_speed = 2
            if score >= 1000:
                self.speed = 3
                self.down_speed = 3

    def reset_pos(self):
        self.rect.topleft = (1, -50)
        self.moving_down = True
        if self.rect.top > 0:
            self.moving_down = False
        if self.direction == -1:
            self.direction *= -1


class Gunner:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1
        self.speed = 1
        self.down_speed = 1
        self.moving_down = False

    def update(self):
        if score >= 500:
            self.moving_down = True
            if self.moving_down:
                self.down_speed = 1
        if self.rect.y == 50:
            self.moving_down = False
            self.rect.x += self.speed * self.direction


class Adv:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.down_speed = 1
        self.x = x
        self.y = y
        self.amplitude = 50  # gap
        self.frequency = 5  # speed for left to right

    def update(self):
        if score >= 1000:
            self.rect.y += self.down_speed
            self.rect.x = self.x + math.sin(math.radians(self.rect.y * self.frequency)) * self.amplitude

    def reset_pos(self):
        self.rect.topleft = (screen_width / 2, -75)


alien1 = Basic(0, -75, alien1_image)
alien2 = Gunner(100, 75, alien2_image)
alien3 = Adv(screen_width / 2, -50, alien3_image)
player = Player(175, 420)
lasers = []


def show_start_screen():
    screen.fill(background)
    start_font = pygame.font.SysFont('Arial', 30)
    start_text = start_font.render('Click to Start', True, (255, 255, 255))
    start_text_rect = start_text.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(start_text, start_text_rect)
    pygame.display.update()

    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                waiting = False
    return True


if show_start_screen():
    run = True
else:
    run = False
while run:
    fpsClock.tick(fps)
    screen.fill(background)
    alien1.move()
    alien3.update()
    screen.blit(alien1_image, alien1.rect)
    screen.blit(alien3_image, alien3.rect)

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 475))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                laser_sound.play()
                lasers.append(Laser(player.rect.centerx, player.rect.top))

    player.move()
    screen.blit(player_image, player.rect)

    for laser in lasers[:]:
        laser.update()
        pygame.draw.rect(screen, light_green, laser.rect)
        if laser.rect.top < 0:
            if laser in lasers:
                lasers.remove(laser)
        if laser.rect.colliderect(alien1.rect):
            if laser in lasers:
                lasers.remove(laser)
            alien1.reset_pos()
            score += 100
        if laser.rect.colliderect(alien3.rect):
            if laser in lasers:
                lasers.remove(laser)
            alien3.reset_pos()
            score += 100

    pygame.display.update()
pygame.quit()
