import pygame, random
import json
import time
from pygame.locals import *

NAME = 'weuler'

def on_grid_random():
    x = random.randint(10,580)
    y = random.randint(10,580)
    return (x//10 * 10, y//10 * 10)

def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

def walk(head, vector):
    '''
    Given a head position and a vector, walks the snake by 10px on that direction
    '''
    return (head[0] + 10 * vector[0], head[1] + 10 * vector[1])

def get_ambient_data(head, food, body):
    '''
    Given head position (tuple x,y) , check for:
        - Distance to wall
        - Distance to body (if found)
        - If there is food in that direction (boolean)

    Returns :
        - 1 / Distance to wall
        - 1 / Distance to body
        - 1 or 0 depending on food on that direction
    
    Convention: first 3 is UP, then RIGHT, DOWN, LEFT
    
    This will generate 12 values that will be input into the RN
    '''
    answer = [0,0,0,0,0,0,0,0,0,0,0,0]

    #distance to top wall
    answer[0] = 1/head[1]
    #distance to right wall
    answer[3] = 1/(600 - head[0])
    #distance to down wall
    answer[6] = 1/(600 - head[1])
    #distance to left wall
    answer[9] = 1/(head[0])

    for b in body[1:]:
        if b[0] == head[0] and b[1] > head[1]:
            #body found above head
            answer[1] = 1/(b[1] - head[1])
        
        if b[0] == head[0] and b[1] < head[1]:
            #body found below head
            answer[7] = 1/(head[1] - b[1])
        
        if b[1] == head[1] and b[0] > head[0]:
            #body found right to head
            answer[4] = 1/(b[0] - head[0])
        
        if b[1] == head[1] and b[0] < head[0]:
            #body found left to head
            answer[10] = 1/(head[0] - b[0])

    if food[0] == head[0] and food[1] > head[1]:
        #food found above head
        answer[2] = 1
    
    if food[0] == head[0] and food[1] < head[1]:
        #food found below head
        answer[8] = 1
    
    if food[1] == head[1] and food[0] > head[0]:
        #food found right to head
        answer[5] = 1
    
    if food[1] == head[1] and food[0] < head[0]:
        #food found left to head
        answer[11] = 1

    return answer
    

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

pygame.init()
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption('Snake')

snake = [(200, 200), (210, 200), (220,200)]
snake_skin = pygame.Surface((10,10))
snake_skin.fill((25,255,25))

wall = pygame.Surface((10,10))
wall.fill((255,255,255))

apple_pos = on_grid_random()
apple = pygame.Surface((10,10))
apple.fill((255,0,0))

font = pygame.font.SysFont('Arial', 30)
score_text = font.render('Score: ', False, (255,255,255))

my_direction = LEFT

clock = pygame.time.Clock()

score = 0

report = []

game_over = False

while True:
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_UP and my_direction != DOWN:
                my_direction = UP
            if event.key == K_DOWN and my_direction != UP:
                my_direction = DOWN
            if event.key == K_LEFT and my_direction != RIGHT:
                my_direction = LEFT
            if event.key == K_RIGHT and my_direction != LEFT:
                my_direction = RIGHT

    if collision(snake[0], apple_pos):
        score+=1
        apple_pos = on_grid_random()
        snake.append((0,0))

    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i-1][0], snake[i-1][1])

    info = []

    if my_direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - 10)
        info.append([1,0,0,0])
    if my_direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + 10)
        info.append([0,0,1,0])
    if my_direction == RIGHT:
        snake[0] = (snake[0][0] + 10, snake[0][1])
        info.append([0,1,0,0])
    if my_direction == LEFT:
        snake[0] = (snake[0][0] - 10, snake[0][1])
        info.append([0,0,0,1])

    for b in snake[1:]:
        if collision(snake[0], b):
            #collision between head and body
            game_over = True
            break
    
    if (snake[0][0] <= 0 or snake[0][0] >= 590 or snake[0][1] <= 0 or snake[0][1] >= 590):
        game_over = True

    if game_over:
        break

    info.append(get_ambient_data(snake[0], apple_pos, snake))

    screen.fill((0,0,0))
    screen.blit(apple, apple_pos)
    for pos in snake:
        screen.blit(snake_skin,pos)
    
    for x in range(0,600,10):
        screen.blit(wall,(0, x))
        screen.blit(wall,(590, x))
        screen.blit(wall,(x, 0))
        screen.blit(wall,(x, 590))
    
    score_value = font.render(str(score), False, (255,255,255))
    screen.blit(score_text,(20,550))
    screen.blit(score_value,(100,550))
    
    info.reverse()
    report.append(info)
    pygame.display.update()

out_name = 'base-' + NAME + '-' + str(int(time.time()))
print('Game info to %s' % out_name)
with open(out_name, 'w') as out:
    json.dump(report, out)