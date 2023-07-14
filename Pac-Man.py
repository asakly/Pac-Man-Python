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
blinky_image = pygame.transform.scale(pygame.image.load(f'Sprites/Ghost_Sprites/Blinky.png'), (32, 32))
pinky_image = pygame.transform.scale(pygame.image.load(f'Sprites/Ghost_Sprites/Pinky.png'), (32, 32))
inky_image = pygame.transform.scale(pygame.image.load(f'Sprites/Ghost_Sprites/Inky.png'), (32, 32))
clyde_image = pygame.transform.scale(pygame.image.load(f'Sprites/Ghost_Sprites/Clyde.png'), (32, 32))
spooked_image = pygame.transform.scale(pygame.image.load(f'Sprites/Ghost_Sprites/powerup.png'), (32, 32))
dead_image = pygame.transform.scale(pygame.image.load(f'Sprites/Ghost_Sprites/dead.png'), (32, 32))
player_x = 385
player_y = 595
counter = 0
direction = 0
blinky_x = 52
blinky_y = 68
blinky_direction = 0
inky_x = 380
inky_y = 448
inky_direction = 2
pinky_x = 440
pinky_y = 398
pinky_direction = 2
clyde_x = 440
clyde_y = 448
clyde_direction = 2

flicker = False
# R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
blinky_dead = False
inky_dead = False
pinky_dead = False
clyde_dead = False
blinky_box = False
inky_box = False
pinky_box = False
clyde_box = False
ghost_speed = 2
startup_counter = 0
moving = False
lives = 3

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 16
        self.center_y = self.y_pos + 16
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_image, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_image, (self.x_pos, self.y_pos))

        ghost_rect = pygame.rect.Rect((self.center_x - 15, self.center_y - 15), (30, 30))
        return ghost_rect

    def check_collisions(self):
        allowance = 12
        self.turns = [False, False, False, False]
        if 0 < (self.center_x // 30) < 26:
            if level[(self.center_y - allowance) // tile_h][self.center_x // tile_w] == 9:
                self.turns[2] = True
            if level[self.center_y // tile_h][(self.center_x - allowance) // tile_w] < 3 \
                    or (level[self.center_y // tile_h][(self.center_x - allowance) // tile_w] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // tile_h][(self.center_x + allowance) // tile_w] < 3 \
                    or (level[self.center_y // tile_h][(self.center_x + allowance) // tile_w] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + allowance) // tile_h][self.center_x // tile_w] < 3 \
                    or (level[(self.center_y + allowance) // tile_h][self.center_x // tile_w] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - allowance) // tile_h][self.center_x // tile_w] < 3 \
                    or (level[(self.center_y - allowance) // tile_h][self.center_x // tile_w] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 10 <= self.center_x % tile_w <= 16:
                    if level[(self.center_y + allowance) // tile_h][self.center_x // tile_w] < 3 \
                        or (level[(self.center_y + allowance) // tile_h][self.center_x // tile_w] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - allowance) // tile_h][self.center_x // tile_w] < 3 \
                        or (level[(self.center_y - allowance) // tile_h][self.center_x // tile_w] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 10 <= self.center_y % tile_h <= 16:
                    if level[self.center_y // tile_h][(self.center_x - tile_w) // tile_w] < 3 \
                        or (level[self.center_y // tile_h][(self.center_x - tile_w) // tile_w] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // tile_h][(self.center_x + tile_w) // tile_w] < 3 \
                        or (level[self.center_y // tile_h][(self.center_x + tile_w) // tile_w] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
            if self.direction == 0 or self.direction == 1:
                if 10 <= self.center_x % tile_w <= 16:
                    if level[(self.center_y + allowance) // tile_h][self.center_x // tile_w] < 3 \
                        or (level[(self.center_y + allowance) // tile_h][self.center_x // tile_w] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - allowance) // tile_h][self.center_x // tile_w] < 3 \
                        or (level[(self.center_y - allowance) // tile_h][self.center_x // tile_w] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 10 <= self.center_y % tile_h <= 16:
                    if level[self.center_y // tile_h][(self.center_x - allowance) // tile_w] < 3 \
                        or (level[self.center_y // tile_h][(self.center_x - allowance) // tile_w] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // tile_h][(self.center_x + allowance) // tile_w] < 3 \
                        or (level[self.center_y // tile_h][(self.center_x + allowance) // tile_w] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 320 < self.x_pos < 490 and 320 < self.y_pos < 430:
            self.in_box = True
        else:
            self.in_box = False


        return self.turns, self.in_box

    def move_clyde(self):
        # r, l, u, d
        # clyde is going to turn whenever advantageous for pursuit
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -20:
            self.x_pos = 810
        elif self.x_pos > 810:
            self.x_pos = -20
        return self.x_pos, self.y_pos, self.direction


    def move_blinky(self):
        # Clyde is going to turn when advantageous for pursuit

        #
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos > 800:
            self.x_pos = -36
        elif self.x_pos < -36:
            self.x_pos = 800
        return self.x_pos, self.y_pos, self.direction


def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 820))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 800), 15)
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

def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if player_x < 405:
        runaway_x = 810
    else:
        runaway_x = 0
    if player_y < 405:
        runaway_y = 810
    else:
        runaway_y = 0
    return_target = (350, 378)
    if powerup:
        if not blinky.dead:
            blink_target = (runaway_x, runaway_y)
        else:
            blink_target = return_target
        if not pinky.dead:
            pink_target = (runaway_x, player_y)
        else:
            pink_target = return_target
        if not inky.dead:
            ink_target = (player_x, runaway_y)
        else:
            ink_target = return_target
        if not clyde.dead:
            clyd_target = (405, 405)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if blinky.in_box:
                blink_target = (380, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not pinky.dead:
            if pinky.in_box:
                pink_target = (380, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not inky.dead:
            if inky.in_box:
                ink_target = (380, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not clyde.dead:
            if clyde.in_box:
                clyd_target = (380, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]


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
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speed, blinky_image, blinky_direction, blinky_dead,
                   blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speed, inky_image, inky_direction, inky_dead,
                   inky_box, 0)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speed, pinky_image, pinky_direction, pinky_dead,
                  pinky_box, 0)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speed, clyde_image, clyde_direction, clyde_dead,
                   clyde_box, 0)
    draw_misc()
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)
    center_x = player_x + 17
    center_y = player_y + 17
    pygame.draw.circle(screen, 'white', (blinky.center_x, blinky.center_y), 2)
    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        inky_x, inky_y, inky_direction = inky.move_clyde()
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
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
        player_x = -30
    elif player_x < -30:
        player_x = 800





    pygame.display.flip()
pygame.quit()