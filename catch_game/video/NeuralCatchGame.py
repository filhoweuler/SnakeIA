from __future__ import division, print_function
import collections
import numpy as np
import pygame
import json
import time
import random
import NeuralNet
import os
from pygame.locals import *

x = 1
y = 40
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

class CatchGame(object):
    
    def __init__(self):
        # run pygame in headless mode
#        os.environ["SDL_VIDEODRIVER"] = "dummy"
        
        pygame.init()
        pygame.key.set_repeat(10, 100)
        
        # set constants
        self.COLOR_WHITE = (255, 255, 255)
        self.COLOR_BLACK = (0, 0, 0)
        self.GAME_WIDTH = 800
        self.GAME_HEIGHT = 400
        self.BALL_WIDTH = 20
        self.BALL_HEIGHT = 20
        self.PADDLE_WIDTH = 100
        self.PADDLE_HEIGHT = 10
        self.GAME_FLOOR = 350
        self.GAME_CEILING = 10
        # based on experimentation, the ball tends to move 4 times
        # between each paddle movement. Since here we alternate ball
        # and paddle movement, we make ball move 4x faster.
        self.BALL_VELOCITY = 10
        self.PADDLE_VELOCITY = 20
        self.FONT_SIZE = 30
#        self.MAX_TRIES_PER_GAME = 100
        self.MAX_TRIES_PER_GAME = 3
        self.CUSTOM_EVENT = pygame.USEREVENT + 1
        self.font = pygame.font.SysFont("Comic Sans MS", self.FONT_SIZE)
        

    def reset(self, epoch):
        self.epoch = epoch
        self.frames = collections.deque(maxlen=4)
        self.game_over = False
        # initialize positions
        self.paddle_x = self.GAME_WIDTH // 2
        self.game_score = 0
        self.reward = 0
        self.ball_x = random.randint(0, self.GAME_WIDTH)
        self.ball_y = self.GAME_CEILING
        self.num_tries = 0
        # set up display, clock, etc
        self.screen = pygame.display.set_mode(
                (self.GAME_WIDTH, self.GAME_HEIGHT))
        self.clock = pygame.time.Clock()
    
    def step(self, action):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        pygame.event.pump()
        
        if action == 0:   # move paddle left
            self.paddle_x -= self.PADDLE_VELOCITY
            if self.paddle_x < 0:
                # bounce off the wall, go right
                self.paddle_x = self.PADDLE_VELOCITY
        elif action == 2: # move paddle right
            self.paddle_x += self.PADDLE_VELOCITY
            if self.paddle_x > self.GAME_WIDTH - self.PADDLE_WIDTH:
                # bounce off the wall, go left
                self.paddle_x = self.GAME_WIDTH - self.PADDLE_WIDTH - self.PADDLE_VELOCITY
        else:             # dont move paddle
            pass

        self.screen.fill(self.COLOR_BLACK)
        score_text = self.font.render("Geração: {:d},Score: {:d}, Ball: {:d}".format(self.epoch, self.game_score, self.num_tries), True, self.COLOR_WHITE)
        self.screen.blit(score_text, 
            ((self.GAME_WIDTH - score_text.get_width()) // 2,
                (self.GAME_FLOOR + self.FONT_SIZE // 2 - 10)))
                
        # update ball position
        self.ball_y += self.BALL_VELOCITY
        ball = pygame.draw.rect(self.screen, self.COLOR_WHITE,
                                pygame.Rect(self.ball_x, self.ball_y,
                                            self.BALL_WIDTH,
                                            self.BALL_HEIGHT))
        # update paddle position
        paddle = pygame.draw.rect(self.screen, self.COLOR_WHITE,
                                  pygame.Rect(self.paddle_x, 
                                              self.GAME_FLOOR,
                                              self.PADDLE_WIDTH,
                                              self.PADDLE_HEIGHT))
        
        # check for collision and update reward
        if self.ball_y >= self.GAME_FLOOR - self.BALL_WIDTH // 2:
            if ball.colliderect(paddle):
                self.reward += 1
                self.game_score += 1
            else:
                self.num_tries += 1
                
            self.ball_x = random.randint(100, self.GAME_WIDTH - 100 )
            self.ball_y = self.GAME_CEILING
            
        pygame.display.flip()
            
        frame = pygame.surfarray.array2d(self.screen)
        
        if self.num_tries >= self.MAX_TRIES_PER_GAME:
            self.game_over = True
            
        self.clock.tick(30)
        return frame, self.reward, self.game_over
        

    def get_frames(self):
        return np.array(list(self.frames))

    def get_ambient_data(self):
        return [ self.ball_x , self.paddle_x + self.PADDLE_WIDTH/2.0 ]
    

if __name__ == "__main__":   
    game = CatchGame()
    NAME = 'weuler'
    
    for epoch in range(1,173):
        with open('w1_-' + str(epoch)) as f:
            w1 = json.load(f)

        with open('w2_-' + str(epoch)) as f:
            w2 = json.load(f)
        brain = NeuralNet.NeuralNet([], [], 2, 20, 1, saved_weight1=w1, saved_weight2=w2)

        game.reset(epoch)
        input_t = game.get_frames()
        game_over = False

        report = []

        while not game_over:
            output = brain.get_output(game.get_ambient_data())

            if output > 0.5:
                action = 2
            else:
                action = 0

            
            input_tp1, reward, game_over = game.step(action)

        print(action, reward, game_over)

        # out_name = 'base-' + NAME + '-' + str(int(time.time()))
        # print('Game info to %s' % out_name)
        # with open(out_name, 'w') as out:
        #     json.dump(report, out)