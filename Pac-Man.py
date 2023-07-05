from Boards import boards
import pygame
import math

pygame.init()


WIDTH = 810
HEIGHT = 850
tile_h = ((HEIGHT - 40) // 32)
tile_w = (WIDTH // 30)
PI = math.pi
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = boards
color = 'blue'
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'Sprites/Pac-Man_Sprite/pac_man_{i}.png'), (32, 32)))
player_x = 385
player_y = 595
counter = 0
direction = 0
flicker = False
# R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
startup_counter = 0
moving = False
lives = 3

def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 820))
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (24, 24)), (650+ i *40, 818))


def check_collisions(score1, power, power_count, eaten_ghosts):

    if 0 < player_x < 770:
        if level[center_y // tile_h][center_x // tile_w] == 1:
            level[center_y // tile_h][center_x // tile_w] = 0
            score1 += 10
        if level[center_y // tile_h][center_x // tile_w] == 2:
            level[center_y // tile_h][center_x // tile_w] = 0
            score1 += 50
            power = True
            power_count = 0
            eaten_ghosts =[False, False, False, False]
    return score1, power, power_count, eaten_ghosts







def draw_board():
    """
    Draws the board using a tile approach based on boards matrix

    :return: None
    """

    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', ((j * tile_w + (0.5 * tile_w)), i * tile_h + (0.5 * tile_h)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', ((j * tile_w + (0.5 * tile_w)), i * tile_h + (0.5 * tile_h)), 8)
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
    """
    Draws the animated player onto the screen in corresponding direction

    :return: None

    """
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], -90), (player_x, player_y))

def check_position(centerx, centery):
    """
    :param centerx: the current x-coord center of the pac-man player
    :param centery: the current y-coord center of the pac-man player
    :return: turns: an array of booleans indicating whether the character
    can make a turn (up, down, left, or right)

    """
    turns = [False, False, False, False]
    allowance = 12

    if centerx // 30 < 26:
        if direction == 0:
            if level[centery // tile_h][(centerx - allowance) // tile_w] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // tile_h][(centerx + allowance) // tile_w] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + allowance) // tile_h][centerx // tile_w] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - allowance) // tile_h][centerx // tile_w] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 10 <= centerx % tile_w <= 16:
                if level[(centery + allowance) // tile_h][centerx // tile_w] < 3:
                    turns[3] = True
                if level[(centery - allowance) // tile_h][centerx // tile_w] < 3:
                    turns[2] = True
            if 10 <= centery % tile_h <= 16:
                if level[centery // tile_h][(centerx - tile_w) // tile_w] < 3:
                    turns[1] = True
                if level[centery // tile_h][(centerx + tile_w) // tile_w] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 10 <= centerx % tile_w <= 16:
                if level[(centery + tile_h) // tile_h][centerx // tile_w] < 3:
                    turns[3] = True
                if level[(centery - tile_h) // tile_h][centerx // tile_w] < 3:
                    turns[2] = True
            if 10 <= centery % tile_h <= 16:
                if level[centery // tile_h][(centerx - allowance) // tile_w] < 3:
                    turns[1] = True
                if level[centery // tile_h][(centerx + allowance) // tile_w] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


def move_player(play_x, play_y):
    """
    :param play_x: x-coord of player
    :param play_y: y-coord of player
    :return: play_x, play_y: New coords of player after moving
    # 0:right, 1:left, 2:up, 3:down
    """
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y


run = True
while run:
    timer.tick(fps)

# Reset counter after the 4 images have each been displayed for 5 frames i.e. 0-19 counter iterations
    if counter < 19:
        counter += 1
        if counter > 12:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180:
        moving = False
        startup_counter += 1
    else:
        moving = True


    screen.fill('black')
    draw_board()
    draw_player()
    draw_misc()
    center_x = player_x + 17
    center_y = player_y + 17
    pygame.draw.circle(screen, 'white', (center_x, center_y), 2)
    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                direction_command = 0
            if event.key in (pygame.K_LEFT, pygame.K_a):
                direction_command = 1
            if event.key in (pygame.K_UP, pygame.K_w):
                direction_command = 2
            if event.key in (pygame.K_DOWN, pygame.K_s):
                direction_command = 3
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_RIGHT, pygame.K_d) and direction_command == 0:
                direction_command = direction
            if event.key in (pygame.K_LEFT, pygame.K_a) and direction_command == 1:
                direction_command = direction
            if event.key in (pygame.K_UP, pygame.K_w) and direction_command == 2:
                direction_command = direction
            if event.key in (pygame.K_DOWN, pygame.K_s) and direction_command == 3:
                direction_command = direction

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if player_x > 800:
        player_x = -36
    elif player_x < -50:
        player_x = 797





    pygame.display.flip()
pygame.quit()