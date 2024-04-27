import pygame

pygame.init()

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


alien1_image = pygame.image.load('Assets/Alien-V1.png')
alien1_image = pygame.transform.scale(alien1_image, (25, 25))


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


class Alien:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1
        self.direction = 1
        self.down_speed = 1
        self.moving_down = True

    def update(self):
        if self.moving_down:
            self.rect.y += self.down_speed
            if self.rect.top > 0:
                self.moving_down = False
        else:
            self.rect.x += self.speed * self.direction
            if self.rect.right >= screen_width or self.rect.left <= 0:
                self.direction *= -1
                self.rect.y += 50

    def reset_pos(self):
        self.rect.topleft = (0, -50)
        self.moving_down = True


alien1 = Alien(0, -50, alien1_image)
player = Player(175, 420)
lasers = []


def show_start_screen():
    screen.fill(background)
    start_font = pygame.font.SysFont('Arial', 30)
    start_text = start_font.render('Click to Start', True, (255, 255, 255))
    start_text_rect = start_text.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(start_text, start_text_rect)
    pygame.display.update()

    # Wait for a left mouse click
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

# Main game loop
while run:
    fpsClock.tick(fps)
    screen.fill(background)
    alien1.update()
    screen.blit(alien1_image, alien1.rect)

    # Display the score
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 475))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                lasers.append(Laser(player.rect.centerx, player.rect.top))

    # Move the player and draw it on the screen
    player.move()
    screen.blit(player_image, player.rect)

    # Update and draw lasers
    for laser in lasers[:]:
        laser.update()
        pygame.draw.rect(screen, light_green, laser.rect)
        if laser.rect.bottom < 0:
            lasers.remove(laser)
        if laser.rect.colliderect(alien1.rect):
            lasers.remove(laser)
            alien1.reset_pos()
            score += 100  # Increase the score when an alien is hit

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()
