import math
import random
import pygame
pygame.font.init()
import tkinter as tk 
from tkinter import messagebox
import os

class cube(object):
    rows = 20
    
    def __init__(self, start, dirnx=1, dirny=0, color=(43, 50, 54)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color
            
    def move(self, dirnx, dirny):
        self.dirnx =  dirnx
        self.dirny =  dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + dirny)
        
    
    def draw(self, surface, eyes=False):
        dis = size // rows
        rw = self.pos[0]
        cm = self.pos[1]
        pygame.draw.rect(surface, self.color, (rw * dis, cm * dis, dis, dis))
        if eyes:
            radius = 3
            circle_middle = (rw * dis + radius * 2, cm * dis + radius * 2)       
            circle_middle2 = (rw * dis + dis - radius * 2, cm * dis + radius * 2)
            pygame.draw.circle(surface, (255,255,255), circle_middle, radius)
            pygame.draw.circle(surface, (255,255,255), circle_middle2, radius)

class snake(object):
    body = []
    turns = {}
    deaths = 0
    longest = 3
    
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 1
        self.dirny = 0
        self.add_cube()
        self.add_cube()
        self.score()
        
    def score(self):
        if len(self.body) >= self.longest:
            self.longest = len(self.body)
        
        # os.system('cls' if os.name == 'nt' else 'clear')
        # print('Długość węża: ', len(self.body))
        # print('Najwyższy wynik: ', self.longest)
        # print('Ilość porażek: ', self.deaths)
        
        global snake_length, longest_length, deaths
        snake_length = len(self.body)
        longest_length = self.longest
        deaths = self.deaths
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_LEFT] or keys[pygame.KSCAN_A] or keys[pygame.K_a]:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_RIGHT] or keys[pygame.KSCAN_D] or keys[pygame.K_d]:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_UP] or keys[pygame.KSCAN_W] or keys[pygame.K_w]:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_DOWN] or keys[pygame.KSCAN_S] or keys[pygame.K_s]:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
    
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i  == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    self.reset()
                    break
                elif c.dirnx == 1 and c.pos[0] >= c.rows -1:
                    self.reset()
                    break
                elif c.dirny == 1 and c.pos[1] >= c.rows -1:
                    self.reset()
                    break
                elif c.dirny == -1 and c.pos[1] <= 0:
                    self.reset()
                    break
                else:
                    c.move(c.dirnx, c.dirny)
        
        for x in range(len(self.body)):
            if self.body[x].pos in list(map(lambda z: z.pos, self.body[x+1:])):
                self.reset()
                break
    
    def reset(self):
        self.deaths = self.deaths + 1
        self.score()
        self.body = []
        self.turns = {}
        self.head = cube((10, 10))
        self.body.append(self.head)
        self.dirnx = 1
        self.dirny = 0
        self.add_cube()
        self.add_cube()
        
    
    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))
            
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        
        self.score()
    
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def UI(window, sl, ll, d):
    font = pygame.font.SysFont(None, 30)
    length_text = font.render("Snake Length: " + str(sl), True, (255, 255, 255))
    longest_text = font.render("Longest Length: " + str(ll), True, (255, 255, 255))
    deaths_text = font.render("Deaths: " + str(d), True, (255, 255, 255))

    window.blit(length_text, (10, 10))
    window.blit(longest_text, (10, 35))
    window.blit(deaths_text, (10, 60))
    
    pygame.display.update()

def draw_window(surface):
    surface.fill((124, 143, 153))
    s.draw(surface)
    apple.draw(surface)
    pygame.display.update()
    
def random_apple(snake):
    position = snake.body
    
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x,y), position))) > 0:
            continue
        else:
            break
    return(x, y)

def main():

    global size, rows, s, apple, window
    size = 500
    rows = size // 25
    
    window = pygame.display.set_mode((size, size))
    
    s = snake((0, 0, 0,), (10, 10))
    apple = cube(random_apple(s), color=(255, 0, 0))
    
    flag = True
    clock= pygame.time.Clock()
    
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False

        pygame.time.delay(60)
        clock.tick(10)
        s.move()
        if s.body[0].pos == apple.pos:
            s.add_cube()
            apple = cube(random_apple(s), color=(255, 0, 0))
            
        draw_window(window)
        
        UI(window, snake_length, longest_length, deaths)

main()