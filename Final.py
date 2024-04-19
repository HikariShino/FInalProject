import pygame

pygame.init()

screen_width = 400
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invader")

background = (22, 20, 87)

player_image = pygame.image.load('Assets/Player.png')
player_rect = player_image.get_rect()
player_image = pygame.transform.scale(player_image, (50, 50))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(player_image, player_rect)

    pygame.display.update()

pygame.quit()
