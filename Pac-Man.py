from Boards import boards
import pygame
import math

pygame.init()


WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = boards
color = 'blue'
player_images = []
for i in range(1,5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'Sprites/Pac-Man_Sprite/pac_man_{i}.png'), (43, 43)))
player_x = 450
player_y = 663
counter = 0
direction = 0


def draw_board():
    tile_h = ((HEIGHT - 50) // 32)
    tile_w = (WIDTH // 30)
    PI = math.pi
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', ((j * tile_w + (0.5 * tile_w)), i * tile_h + (0.5 * tile_h)), 4)
            if level[i][j] == 2:
                pygame.draw.circle(screen, 'white', ((j * tile_w + (0.5 * tile_w)), i * tile_h + (0.5 * tile_h)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * tile_w + (0.5 * tile_w), i * tile_h),
                                                ((j * tile_w) + (0.5 * tile_w), ((i * tile_h) + tile_h)), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, ((j * tile_w), ((i * tile_h) + (0.5 * tile_h))),
                                                ((j * tile_w) + tile_w, ((i * tile_h) + (0.5 * tile_h))), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, ((j * tile_w) - (0.4 * tile_w) - 2, ((i * tile_h) + (0.5 * tile_h)),
                                                tile_w, tile_h), 0, PI/2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color, ((j * tile_w) + (0.5 * tile_w), (i * tile_h) + (0.5 * tile_h),
                                                tile_w, tile_h), PI/2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, ((j * tile_w) + (0.5 * tile_w), (i * tile_h) - (0.4 * tile_h),
                                                tile_w, tile_h), PI, 1.5 * PI, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color, ((j * tile_w) - (0.4 * tile_w) - 2, (i * tile_h) - (0.4 * tile_h),
                                                tile_w, tile_h), 1.5 * PI, 2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * tile_w, (i * tile_h) + (0.5 * tile_h)),
                                                ((j * tile_w) + tile_w, (i * tile_h) + (0.5 * tile_h)), 3)


def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False) , (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], -90), (player_x, player_y))



run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    draw_board()
    draw_player()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()