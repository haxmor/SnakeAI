import pygame
import random
import numpy as np #added for AI
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

# to enable AI we need:
# reset function
# reward agent
# play (action) -> direction
# game_iteration tracking
# if is collision

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 20 #20 origianlly

class SnakeGameAI:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset() #added for AI
        
        
        
    def reset(self): #added for AI
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0 #added for AI
    
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self, action): #added action for AI
        self.frame_iteration += 1 #added for break test
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                #comment out movement for AI
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_LEFT:
#                     self.direction = Direction.LEFT
#                 elif event.key == pygame.K_RIGHT:
#                     self.direction = Direction.RIGHT
#                 elif event.key == pygame.K_UP:
#                     self.direction = Direction.UP
#                 elif event.key == pygame.K_DOWN:
#                     self.direction = Direction.DOWN
        
        # 2. move
        #self._move(self.direction) # update for head modify for AI
        self._move(action) # updated for AI
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0 # updated for AI
        game_over = False
        #if self._is_collision(): removed for AI, doesn't check if snake not moving
        if self.is_collision() or self.frame_iteration > 100*len(self.snake): #added for AI
            game_over = True
            reward = -10 # added for AI
            return reward, game_over, self.score #added for AI
            #return game_over, self.score #removed for AI
            
        # 4. place new food or just move
        if self.head == self.food: # if food is eaten
            self.score += 1
            reward = 10 #added for AI eat food reward
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        #return game_over, self.score #removed for AI
        return reward, game_over, self.score #added for AI    
    
    #def _is_collision(self): #removed to add collision
    def is_collision(self, pt=None): #added for AI remove _ to make public
        if pt is None: #added for AI
            pt = self.head #added for AI
        # hits boundary modified for AI
        #if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]: #modified for AI
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    #def _move(self, direction): #modify for AI
    def _move(self, action): #modified for AI
        # determine the direction based on the action
        # [straight, right, left]
        #define all directions in clockwise
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP] #added for AI
        idx = clock_wise.index(self.direction) #added for AI
        
        if np.array_equal(action, [1, 0, 0]): #added for AI
            new_dir = clock_wise[idx] #no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # make right turn r-> d-> l-> u
        else: # [0,0,1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # make left turn r-> u-> l-> d
        
        self.direction = new_dir #added for AI
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT: # modified for self AI
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT: # modified for self AI
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN: # modified for self AI
            y += BLOCK_SIZE
        elif self.direction == Direction.UP: # modified for self AI
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            
#removed for AI agent to run
# if __name__ == '__main__':
#     game = SnakeGame()
#     
#     # game loop
#     while True:
#         game_over, score = game.play_step()
#         
#         if game_over == True:
#             break
#         
#     print('Final Score', score)
#         
#         
#     pygame.quit()