import pygame
import math
import random

pygame.init()
pygame.mixer.init()

laser_sound = pygame.mixer.Sound('Assets/laser.mp3')
Alien_Hit = pygame.mixer.Sound("Assets/Alien_Destroy.mp3")
Game_Over = pygame.mixer.Sound("Assets/Game_Over.mp3")
Alien_Pass = pygame.mixer.Sound("Assets/Warning.mp3")

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
life = 100
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
        self.speed = 1
        self.down_speed = 1
        self.moving_down = True
        if self.rect.top > 0:
            self.moving_down = False
        if self.direction == -1:
            self.direction *= -1


class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 6, 10)
        self.speed = 6

    def update(self):
        self.rect.y += self.speed


class Gunner:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y
        self.direction = 1
        self.speed = 2
        self.down_speed = 2
        self.bullets = []
        self.shoot_interval = 1000
        self.last_shot_time = pygame.time.get_ticks()

    def move(self):
        if score >= 500 and self.rect.top <= 50:
            self.rect.y += self.down_speed
        else:
            self.rect.x += self.speed * self.direction
            if self.rect.right >= screen_width or self.rect.left <= 0:
                self.direction *= -1

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_interval and self.rect.top > 0:
            new_bullet = Bullet(self.rect.centerx, self.rect.bottom)
            self.bullets.append(new_bullet)
            self.last_shot_time = current_time

    def reset_pos(self):
        self.x = random.randint(75, 350)
        self.rect.topleft = (self.x, -75)


class Adv:
    def __init__(self, y, image):
        self.image = image
        self.down_speed = 1
        self.x = random.randint(100, 300)
        self.y = y
        self.rect = self.image.get_rect(topleft=(self.x, y))
        self.amplitude = 50  # length of sin movement
        self.frequency = 2  # speed for left to right

    def move(self):
        if score >= 1000:
            self.rect.y += self.down_speed
            self.rect.x = self.x + math.sin(math.radians(self.rect.y * self.frequency)) * self.amplitude

    def reset_pos(self):
        self.x = random.randint(100, 300)
        self.rect.topleft = (self.x, -75)


alien1 = Basic(0, -75, alien1_image)
alien2 = Gunner(screen_width / 2, -75, alien2_image)
alien3 = Adv(-50, alien3_image)
player = Player(175, 420)
lasers = []
bullets = []


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


def game_over():
    screen.fill(background)
    game_over_font = pygame.font.SysFont('Arial', 30)
    game_over_text = game_over_font.render('Game Over!', True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(screen_width/2, screen_height/2))

    restart_text = game_over_font.render('Left Click to Restart', True, (255, 255, 255))
    restart_rect = game_over_text.get_rect(topleft=(100, game_over_rect.y + 50))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.update()
    pygame.time.wait(3000)

    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                waiting_for_click = False

    return True


while run:
    fpsClock.tick(fps)
    screen.fill(background)

    alien1.move()
    alien2.move()
    alien3.move()
    screen.blit(alien1_image, alien1.rect)
    screen.blit(alien2_image, alien2.rect)
    screen.blit(alien3_image, alien3.rect)

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 475))
    Lives_text = font.render(f'Health: {life}', True, (255, 255, 255))
    screen.blit(Lives_text, (300, 475))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                laser_sound.play()
                lasers.append(Laser(player.rect.centerx, player.rect.top))

    player.move()
    screen.blit(player_image, player.rect)

    for gunner in [alien2]:
        gunner.shoot()
        for bullet in gunner.bullets[:]:
            bullet.update()
            pygame.draw.rect(screen, (255, 0, 0), bullet.rect)
            if bullet.rect.bottom < 0:
                gunner.bullets.remove(bullet)

            if bullet.rect.colliderect(player.rect):
                Alien_Hit.play()
                life -= 25
                gunner.bullets.remove(bullet)

    for laser in lasers[:]:
        laser.update()
        pygame.draw.rect(screen, light_green, laser.rect)
        if laser.rect.top < 0:
            if laser in lasers:
                lasers.remove(laser)

        if laser.rect.colliderect(alien1.rect):
            Alien_Hit.play()
            if laser in lasers:
                lasers.remove(laser)
            alien1.reset_pos()
            score += 100

        if laser.rect.colliderect(alien2.rect):
            Alien_Hit.play()
            if laser in lasers:
                lasers.remove(laser)
            alien2.reset_pos()
            score += 100

        if laser.rect.colliderect(alien3.rect):
            Alien_Hit.play()
            if laser in lasers:
                lasers.remove(laser)
            alien3.reset_pos()
            score += 100

    if player.rect.colliderect(alien1.rect) or player.rect.colliderect(alien2.rect) or player.rect.colliderect(
                alien3.rect):
        Alien_Hit.play()
        life = 0

    elif (alien1.rect.bottom >= screen_height or alien2.rect.bottom >= screen_height
            or alien3.rect.bottom >= screen_height):
        Alien_Pass.play()
        life = 0

    if life <= 0:
        pygame.time.wait(1500)
        Game_Over.play()
        run = game_over()

        if run:
            score = 0
            life = 100
            alien1.reset_pos()
            alien2.reset_pos()
            alien3.reset_pos()
            alien2.bullets.clear()
            lasers.clear()

    pygame.display.update()

pygame.quit()
