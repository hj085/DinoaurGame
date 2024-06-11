import pygame
from pygame.locals import *
import time
import random
from random import choice
import math

pygame.init()

screen_width = 900
screen_height = 900
screen_d = (screen_width, screen_height)
screen = pygame.display.set_mode(screen_d)
pygame.display.set_caption("Dinosaur_round_game")
clock = pygame.time.Clock()

obstacle_image = pygame.image.load('characters/obstacle.PNG').convert_alpha()
obstacle_radius = obstacle_image.get_rect().topleft
obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))

order = 0 #needed to change image of the character
previous_degree = [0]

radius1 = 300 #radius of the green circle
radius2 = 15 #radius of the character

x = radius1+radius2 #distance from the character circle to the center of the green circle
y = radius1+radius2 ##distance from the character circle to the center of the green circle

angle = -math.pi/2

game = True
can_jump = True
jump = False
hit = 0
o_x = x


score = 0

score_f = pygame.font.SysFont("Aerial", 60)
game_over_f = pygame.font.SysFont("Aerial", 100)

def randomize():
    '''
    it is a function to randomize amount and location of the obstacle
    :return: randoom x_values for obstacles, random number of obstacles, choose one of possible arccosin values
    '''
    x_rans = []
    obstacle_ran = random.randint(1, 5)
    possible_ran_ints = []
    for i in range(obstacle_ran):
        x_ran = choice([i for i in range(150,750) if i not in range(350, 510)])
        x_rans.append(x_ran)
        possible_ran_ints.append(random.randint(0, 1))
    return x_rans, obstacle_ran, possible_ran_ints

def jumping(can_jump, jump, x, y):
    '''
    It is a function that make a player to jump
    :param can_jump: True or False that can determine if a player can jump or not
    :param jump: True or False that can determine if a player reached its highest x, y values
    :param x: distance from the character circle to the center of the green circle(needed for location)
    :param y: distance from the character circle to the center of the green circle(needed for loccation)
    :return: can_jump, jump, x, y
    '''
    if jump:
        x += 5
        y += 5

        if o_x - x == -120:
            can_jump = False
            jump = False

    if not can_jump:
        x -= 5
        y -= 5
        if x == radius1 + radius2:
            can_jump = True


    return [can_jump, jump, x, y]

def speed(s, score):
    '''
    It is a fuction to make the character to move faster has a player earns more point
    :param s: initial speed of the game
    :param score: current score that a player has
    :return: initial speed + additional speed based on player's current score
    '''
    if score == 0:
        return s*-1
    else:
        return (s*-1)+((s*score*-1)/5)

rans = randomize()
x_rans = rans[0]
obstacle_ran = rans[1]
possible_ran_ints = rans[2]

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_z:
                 screen_width = 900
                 screen_height = 900
                 angle = -math.pi / 2
                 x = radius1 + radius2
                 y = radius1 + radius2
                 score = 0
                 game = True
                 rans = randomize()
                 x_rans = rans[0]
                 obstacle_ran = rans[1]
                 possible_ran_ints = rans[2]
                 can_jump = True
                 jump = False
                 previous_degree = []


             if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                 if can_jump:
                     dino_image1 = pygame.image.load('characters/c_j.PNG').convert_alpha()
                     dino_image1 = pygame.transform.scale(dino_image1, (50, 50))
                     dino_image1 = pygame.transform.rotate(dino_image1, -1 * (math.degrees(angle)+90))

                     jump = True



    if game:


        images = ['characters/c1.PNG', 'characters/c2.PNG']
        if x == radius1 + radius2 and not jump:
            dino_image1 = pygame.image.load(images[order]).convert_alpha()
            dino_image1 = pygame.transform.scale(dino_image1, (50, 50))
            dino_image1 = pygame.transform.rotate(dino_image1, -1 * (math.degrees(angle)+90))

        if int(math.degrees(angle))%12 == 0 and int(math.degrees(angle)) not in previous_degree:
            order +=1
        previous_degree.append(int(math.degrees(angle)))

        if order > 1:
            order =0


        j = jumping(can_jump, jump, x,y)
        can_jump = j[0]
        jump = j[1]
        x = j[2]
        y = j[3]


        screen.fill((0,255,255))
        score_t = score_f.render(str(score), True, (0, 0, 0))
        screen.blit(score_t, (840, 20))

        x_centers = [] # list of the x coordinate of the center of the obstacle circles
        y_centers = [] # list of the y coordinate of the center of the obstacle circles

        for i in range(len(x_rans)):
            possible_ran = [325*math.sin(math.acos((x_rans[i]-screen_width/2)/325))+screen_height/2, 325*math.sin(math.acos((x_rans[i]-screen_width/2)/325)+math.pi)+screen_height/2]

            screen.blit(obstacle_image, (x_rans[i]-25, -25+possible_ran[possible_ran_ints[i]]))
            x_centers.append(x_rans[i])
            y_centers.append(possible_ran[possible_ran_ints[i]])

        earth = pygame.draw.circle(screen, (0,200,50), (screen_width/2, screen_height/2), radius1, radius1)
        #character = pygame.draw.circle(screen, 'red', (x * math.cos(angle) + screen_width / 2, y * math.sin(angle) + screen_height / 2), radius2, radius2)

        screen.blit(dino_image1, (x*math.cos(angle)+screen_width/2-30, y*math.sin(angle)+screen_height/2-30))

    for i in range(len(x_centers)):
        distance = math.hypot((x*math.cos(angle)+screen_width/2) - x_centers[i], (y * math.sin(angle) + screen_height / 2) - y_centers[i])
        if distance <= radius2+radius2:
            hit += 1
            if hit == 1:
                game_over_t = game_over_f.render('Game Over!', True, (0, 0, 0))
                game_restart_t = score_f.render('click z to restart', True, (0,0,0))

                screen.blit(game_over_t, (250, 350))
                screen.blit(game_restart_t, (290, 450))
                game = False
        else:
            hit = 0



    ini_s = -0.01
    angle -= speed(ini_s, score)
    if angle <= -2 * math.pi - math.pi / 2:
        angle = -math.pi / 2
        rans = randomize()
        x_rans = rans[0]
        obstacle_ran = rans[1]
        possible_ran_ints = rans[2]
        previous_degree = []

        if score == 99:
            score = 0

        else:
            score += 1

    clock.tick(60)
    pygame.display.update()
