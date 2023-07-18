from Boards import boards
import pygame
import math
import copy
pygame.init()

# Initialize game size and global constants
WIDTH = 810
HEIGHT = 850
tile_h = ((HEIGHT - 40) // 32)
tile_w = (WIDTH // 30)
PI = math.pi
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(boards)
color = 'blue'
# Load various sprites
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'Sprites/Pac-Man_Sprite/pac_man_{i}.png'), (32, 32)))
blinky_image = pygame.transform.scale(pygame.image.load(f'Sprites/Ghost_Sprites/Blinky.png'), (32, 32))
pinky_image = pygame.transform.scale(pygame.image.load(f'Sprites/Ghost_Sprites/Pinky.png'), (32, 32))
inky_image = pygame.transform.scale(pygame.image.load(f'Sprites/Ghost_Sprites/Inky.png'), (32, 32))
clyde_image = pygame.transform.scale(pygame.image.load(f'Sprites/Ghost_Sprites/Clyde.png'), (32, 32))
spooked_image = pygame.transform.scale(pygame.image.load(f'Sprites/Ghost_Sprites/powerup.png'), (32, 32))
dead_image = pygame.transform.scale(pygame.image.load(f'Sprites/Ghost_Sprites/dead.png'), (32, 32))
# Pac-man and ghost starting pos
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
# Ghosts dead or in box boolean
blinky_dead = False
inky_dead = False
pinky_dead = False
clyde_dead = False
blinky_box = False
inky_box = False
pinky_box = False
clyde_box = False
ghost_speeds = [2, 2, 2, 2]
startup_counter = 0
moving = False
lives = 3
game_over = False
game_won = False

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 16 # center of ghost relative to ghost_pos
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
        """

        :return: ghost_rect: ghost hitbox
        draws normal ghost sprite, spooked ghost sprite if powerup active, or ghost eyes if dead
        """
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_image, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_image, (self.x_pos, self.y_pos))

        # Initialize ghost hitbox
        ghost_rect = pygame.rect.Rect((self.center_x - 15, self.center_y - 15), (30, 30))
        return ghost_rect

    def check_collisions(self):
        """

        :return: self.turns: listof boolean giving which direction ghost allowed to turn
         self.in_box: boolean if ghost in spawn box
        """
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
        """
        Clyde tracking algorithm
        :return: self.x_pos: new x-position, self.y_pos: new y-position, self.direction: new direction
        """
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
        """
        Blinky tracking algorithm
        :return: self.x_pos: new x-position, self.y_pos: new y-position, self.direction: new direction
        """
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

    def move_inky(self):
        # r, l, u, d
        # inky turns up or down at any point to pursue, but left and right only on collision
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
                self.y_pos += self.speed
        if self.x_pos > 800:
            self.x_pos = -36
        elif self.x_pos < -36:
            self.x_pos = 800
        return self.x_pos, self.y_pos, self.direction

    def move_pinky(self):
        # r, l, u, d
        # inky is going to turn left or right whenever advantageous, but only up or down on collision
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
        if self.x_pos > 800:
            self.x_pos = -36
        elif self.x_pos < -36:
            self.x_pos = 800
        return self.x_pos, self.y_pos, self.direction


def draw_misc():
    """
    draws score, lives
    :return: None

    """
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 820))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 800), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (24, 24)), (650+ i *40, 818))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 700, 200], 0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 660, 160], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 700, 200], 0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 660, 160], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (100, 300))

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
    """

    :param blink_x: blinky x_pos
    :param blink_y: blinky y_pos
    :param ink_x: inky x_pos
    :param ink_y: inky y_pos
    :param pink_x: pinky x_pos
    :param pink_y: pinky y_pos
    :param clyd_x: clyde x_pos
    :param clyd_y: clyde y_pos
    :return: list of tuple for ghost active targets
    """

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
        if not blinky.dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eaten_ghost[0]:
            if blinky.in_box:
                blink_target = (380, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead and not eaten_ghost[1]:
            ink_target = (runaway_x, runaway_y)
        elif not inky.dead and eaten_ghost[1]:
            if inky.in_box:
                ink_target = (380, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead and not eaten_ghost[2]:
            pink_target = (runaway_x, runaway_y)
        elif not pinky.dead and eaten_ghost[2]:
            if pinky.in_box:
                pink_target = (380, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not eaten_ghost[3]:
            clyd_target = (runaway_x, runaway_y)
        elif not clyde.dead and eaten_ghost[3]:
            if clyde.in_box:
                clyd_target = (380, 100)
            else:
                clyd_target = (player_x, player_y)
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
        if not inky.dead:
            if inky.in_box:
                ink_target = (380, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if pinky.in_box:
                pink_target = (380, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if clyde.in_box:
                clyd_target = (380, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target

    return [blink_target, ink_target, pink_target, clyd_target]

# Main game loop
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
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True


    screen.fill('black')
    draw_board()
    center_x = player_x + 17
    center_y = player_y + 17
    if powerup:
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2]
    if eaten_ghost[0]:
        ghost_speeds[0] = 2
    if eaten_ghost[1]:
        ghost_speeds[1] = 2
    if eaten_ghost[2]:
        ghost_speeds[2] = 2
    if eaten_ghost[3]:
        ghost_speeds[3] = 2
    if blinky_dead:
        ghost_speeds[0] = 4
    if inky_dead:
        ghost_speeds[1] = 4
    if pinky_dead:
        ghost_speeds[2] = 4
    if clyde_dead:
        ghost_speeds[3] = 4

    game_won = True
    for i in range(len(level)):
        if 1 or 2 in level[i]:
            game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 18, 2)
    draw_player()
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_image, blinky_direction, blinky_dead,
                   blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_image, inky_direction, inky_dead,
                   inky_box, 0)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_image, pinky_direction, pinky_dead,
                  pinky_box, 0)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_image, clyde_direction, clyde_dead,
                   clyde_box, 0)
    draw_misc()
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)

    pygame.draw.circle(screen, 'white', (blinky.center_x, blinky.center_y), 2)
    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_clyde()

        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()


    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)

# add to if not powerup to check if eaten ghosts
    if not powerup:
        if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
            (player_circle.colliderect(inky.rect) and not inky.dead) or \
            (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
            (player_circle.colliderect(clyde.rect) and not clyde.dead):
            if lives > 0:
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 385
                player_y = 595
                counter = 0
                direction = 0
                direction_command = 0
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
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
    if powerup and player_circle.colliderect(blinky.rect) and eaten_ghost[0] and not blinky.dead:
        if lives > 0:
            lives -= 1
            startup_counter = 0
            powerup = False
            power_counter = 0
            player_x = 385
            player_y = 595
            counter = 0
            direction = 0
            direction_command = 0
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
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            pinky_dead = False
            clyde_dead = False

    if powerup and player_circle.colliderect(inky.rect) and eaten_ghost[1] and not inky.dead:
        if lives > 0:
            lives -= 1
            startup_counter = 0
            powerup = False
            power_counter = 0
            player_x = 385
            player_y = 595
            counter = 0
            direction = 0
            direction_command = 0
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
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            pinky_dead = False
            clyde_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0

    if powerup and player_circle.colliderect(pinky.rect) and eaten_ghost[2] and not pinky.dead:
        if lives > 0:
            lives -= 1
            startup_counter = 0
            powerup = False
            power_counter = 0
            player_x = 385
            player_y = 595
            counter = 0
            direction = 0
            direction_command = 0
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
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            pinky_dead = False
            clyde_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0

    if powerup and player_circle.colliderect(clyde.rect) and eaten_ghost[3] and not clyde.dead:
        if lives > 0:
            lives -= 1
            startup_counter = 0
            powerup = False
            power_counter = 0
            player_x = 385
            player_y = 595
            counter = 0
            direction = 0
            direction_command = 0
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
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            pinky_dead = False
            clyde_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0

    if powerup and player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghost[0]:
        blinky_dead = True
        eaten_ghost[0] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghost[1]:
        inky_dead = True
        eaten_ghost[1] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghost[2]:
        pinky_dead = True
        eaten_ghost[2] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghost[3]:
        clyde_dead = True
        eaten_ghost[3] = True
        score += (2 ** eaten_ghost.count(True)) * 100



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
            if event.key == pygame.K_SPACE and (game_over or game_won):
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 385
                player_y = 595
                counter = 0
                direction = 0
                direction_command = 0
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
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False
                score = 0
                lives = 3
                level = boards
                game_over = False
                game_won = False

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

    if blinky.in_box and blinky_dead:
        blinky_dead = False
    if inky.in_box and inky_dead:
        inky_dead = False
    if pinky.in_box and pinky_dead:
        pinky_dead = False
    if clyde.in_box and clyde_dead:
        clyde_dead = False

    pygame.display.flip()
pygame.quit()