import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 20)
lont = pygame.font.Font('arial.ttf', 50)

class Way(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

RED = (255,0,0)
CYAN = (0,255,255)
WHITE = (255, 255, 255)
PINK = (255,0,255)
YELLOW = (255,255,0)
BLACK = (0,0,0)

SIZE = 20
SPEED = 10

class SnakeGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('put the snake in your ass')
        self.clock = pygame.time.Clock()
    
        self.way = Way.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head]
        
        self.score = 0
        self.food = None
        self.placefood()
        
    def placefood(self):
        x = random.randint(0, (self.w-SIZE )//SIZE )*SIZE 
        y = random.randint(0, (self.h-SIZE )//SIZE )*SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self.placefood()
        
    def playstep(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.way!=Way.RIGHT:
                        self.way = Way.LEFT
                elif event.key == pygame.K_RIGHT:
                    if self.way !=Way.LEFT:
                        self.way = Way.RIGHT
                elif event.key == pygame.K_UP:
                    if self.way!=Way.DOWN:
                        self.way = Way.UP
                elif event.key == pygame.K_DOWN:
                    if self.way!=Way.UP:
                        self.way = Way.DOWN
        
        self.move(self.way)
        self.snake.insert(0, self.head)
        
        gameover = False
        if self.collision():
            gameover = True
            wext=lont.render("Fuck You",True,WHITE)
            self.display.blit(wext,[self.w//3,self.h//2])
            pygame.display.flip()
            return gameover, self.score
            
        if self.head == self.food:
            self.score += 1
            self.placefood()
        else:
            self.snake.pop()
        
        self.update()
        self.clock.tick(SPEED)

        return gameover, self.score
    
    def collision(self):
        if self.head in self.snake[1:]:
            return True
        
        return False
        
    def update(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            if self.snake.index(pt)%4==0:
                pygame.draw.rect(self.display, WHITE, pygame.Rect(pt.x, pt.y, SIZE, SIZE),3)
            elif self.snake.index(pt)%3==0:
                pygame.draw.ellipse(self.display, YELLOW, pygame.Rect(pt.x, pt.y, SIZE, SIZE))
            elif self.snake.index(pt)%2==0:
                pygame.draw.rect(self.display, CYAN, pygame.Rect(pt.x, pt.y, SIZE, SIZE))
            else:
                pygame.draw.ellipse(self.display, PINK, pygame.Rect(pt.x, pt.y, SIZE, SIZE),3)

        pygame.draw.ellipse(self.display, RED, pygame.Rect(self.food.x, self.food.y, SIZE, SIZE))
        
        text = font.render("score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def move(self, way):
        x = self.head.x
        y = self.head.y
        if way == Way.RIGHT:
            x =(x+ SIZE)%self.w
        elif way == Way.LEFT:
            x = (x- SIZE)%self.w
        elif way == Way.DOWN:
            y =(y+ SIZE)%self.h
        elif way == Way.UP:
            y =(y- SIZE)%self.h
            
        self.head = Point(x, y)          

if __name__ == '__main__':
    game = SnakeGame()
    
    while True:
        gameover, score = game.playstep()
        
        if gameover == True:
            pygame.time.wait(1000)
            break
   
    pygame.quit()
