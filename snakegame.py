"""
Snake game - singleplayer, or multiplayer up to 3 players at total.
Author - David Z., I. year of Bc. MFF UK Charles university, informatics.
Programování I. winter semester 2020/2021

"""

import sys           
import os                
import random
import pygame
from pygame import Rect, Vector2, Color


def fix_path(p):
    return os.path.dirname(os.path.realpath(__file__)) + "/" + p        # help with links

def create_board(d = 857, i = 0, j = 0):            # draw squares -- board, d is exactly the number needed to draw them all 
    for n in range(d):
        pygame.draw.polygon(screen, (255,255,255), [(i,j), (i+40,j), (i+40,j+40), (i,j+40), (i,j)], width=3)
        if i != width:
            i = i + 40
        else:
            j = j + 40
            i = -i


"""
                        ----
        APPLE
                        ----
"""


apple_position = []             # coordinates of all apples
class Apple:
    def __init__(self):
        self.alive = False
        self.apple = pygame.image.load(fix_path("image - APPLE.jpg"))
        self.applerect = self.apple.get_rect()

    def draw(self):
        if self.alive == False:                         # no apple is on the board, apple is yet to be drawn; random coordinates, which do not collide with other objects - such as snakes or poison jars                            
            while True:
                self.x = random.randint(20,940)
                self.y = random.randint(20,700)
                coord = [self.x, self.y]
                if self.x / 20 in [i for i in range(50) if i%2 !=0] and self.y / 20 in [i for i in range(50) if i%2 !=0]:       # math - we need our images to possibly spawn 40px to 40px from (0,0) each 40px
                    if (coord not in poison_position) and ([coord[0]-20, coord[1]-20] not in snake_position1) and ([coord[0]-20, coord[1]-20] not in snake_position2) and ([coord[0]-20, coord[1]-20] not in snake_position3):          # so we don't spawn it on poison or snake
                        self.applerect.center = self.x, self.y
                        self.alive = True
                        apple_position.append(coord)    # adding to a separate list, later on to determine if the head of snake eats the apple
                        break
        if self.alive == True:                          # apple is fresh and ready to eat, we just have to draw it on the screen                      
            screen.blit(self.apple,self.applerect)

    def check_if_apple_eaten(self):                     # if a snake ate an apple, we switch alive to False, so we will generate a new one
        global a
        if a == 0:
            self.alive = False
            a = 1


"""
                        ----
        POISON
                        ----
"""



i = 0                           # counting every frame; to add more poison over time
poison_position = []            # coords of all poison jars
class Poison:
    def __init__(self):
        self.alive = False
        self.poison = pygame.image.load(fix_path("image - POISON.jpg"))
        self.poisonrect = self.poison.get_rect()

    def draw(self):
        global i
        if i == 60:                                     # after a solid time we will add a new poison jar
            i = 0
            self.alive = False                 
        if self.alive == False:                         # snake ate a poison jar, what to do?                     
            while True:
                self.x = random.randint(20,940)
                self.y = random.randint(20,700)         # center of the poison jar picture - to fit a random square in my board
                coord = [self.x, self.y]             
                if self.x / 20 in [i for i in range(50) if i%2 !=0] and self.y / 20 in [i for i in range(50) if i%2 !=0]:       # math - same as apple
                    if (coord not in apple_position) and ([coord[0]-20, coord[1]-20] not in snake_position1) and ([coord[0]-20, coord[1]-20] not in snake_position2) and ([coord[0]-20, coord[1]-20] not in snake_position3):                                                                             # check - we don't want to spawn poison onto an already existing apple
                        self.alive = True
                        poison_position.append(coord)          
                        break
        if self.alive == True:                          # snake haven't eaten a poison jar yet - we keep drawing it
            for c in poison_position:
                self.x = c[0]
                self.y = c[1]
                self.poisonrect.center = self.x, self.y
                screen.blit(self.poison,self.poisonrect)
        

"""                                     
                                            ----
            SNAKE FOR PLAYER 1
                                            ----
"""  


length1 = 1                 # length of the snake
a = 1                       # apple reaction - we switch it to 0 if snake eats the apple, apple will redraw at the new position and a will return to 1
p = 1                       # poison reaction - snake is alive = 1, snake is dead = 0
queue1 = []                 # protection of snake comitting suicide
snake_road1 = []            # all coord of the snake's route
snake_position1 = []        # actual coords of the body - check if head collides with the rest of its body
class Snake1:
    def __init__(self, coord_x, coord_y):
        self.head = [coord_x, coord_y]
        self.head_checking = [coord_x + 20, coord_y + 20]
        self.alive = True

    def draw(self):                             # we take last couple of coords of the snake's road equivalent to snake's head and apples he has eaten so far, we draw it 
        snake_road1.append(self.head)
        if length1 > 0:
            for i in range(1, length1 + 1):
                x = snake_road1[-i]
                pygame.draw.rect(screen, (255,0,0), (x[0], x[1], 40,40))
                snake_position1.append(x)
        while len(snake_position1) != length1:  # we get the momentarily coordination of the snake to a new list
            snake_position1.pop(0)            
    
    def movement(self):                         # function to regulate direction
        global player1_movement_x, player1_movement_y, queue1   
        if len(queue1) == 0:
            pass
        else:
            if queue1[0] == "UP":
                if player1_movement_y == 40:            # QUEUE - double clicking could make our snake kill itself - he would turn on the same line
                    queue1.pop(0)
                else:
                    player1_movement_y = -40
                    player1_movement_x = 0
                    queue1.pop(0)
            elif queue1[0] == "DOWN":
                if player1_movement_y == -40:
                    queue1.pop(0)
                else:
                    player1_movement_y = +40
                    player1_movement_x = 0
                    queue1.pop(0)
            elif queue1[0] == "RIGHT":
                if player1_movement_x == -40:
                    queue1.pop(0)
                else:
                    player1_movement_x = 40
                    player1_movement_y = 0
                    queue1.pop(0)
            elif queue1[0] == "LEFT":
                if player1_movement_x == 40:
                    queue1.pop(0)
                else:
                    player1_movement_x = -40
                    player1_movement_y = 0
                    queue1.pop(0)
   
    def eat_apple(self):                                    # if apple is eaten, then we add to the score, length of our snake and we reset apple 
        global a, player1_score, length1
        if self.head_checking in apple_position:
            apple_position.remove(self.head_checking)
            player1_score += 1
            length1 += 1
            a = 0
            
    def eat_poison(self):                                   # if poison is eaten, then we remove poison and we kill our snake
        global p
        if self.head_checking in poison_position:
            poison_position.remove(self.head_checking)
            p = 0
    
    def collision_border(self):                             # collision with border or with snake itself kills our snake
        global p
        if self.head_checking[0] > 960 or self.head_checking[0] < 0:
            p = 0
        if self.head_checking[1] > 720 or self.head_checking[1] < 0:
            p = 0 
        if snake_position1.count(self.head) > 1:
            p = 0

    def collision_with_players(self):                       # collision with players - snake kills itself
        global p
        if self.head in snake_position2:
            p = 0
        if self.head in snake_position3:
            p = 0



"""                                     
                                            ----
            SNAKE FOR PLAYER 2
                                            ----
"""  


length2 = 1                 # length of the snake
a = 1                       # apple reaction
q = 1                       # poison reaction - snake is alive
queue2 = []                 # protection of snake comitting suicide
snake_road2 = []            # all coord of the snake's route
snake_position2 = []        # actual coords of the body - check if head collides with the rest of its body
class Snake2:
    def __init__(self, coord_x, coord_y):
        self.head = [coord_x, coord_y]
        self.head_checking = [coord_x + 20, coord_y + 20]
        self.alive = True

    def draw(self):                               # we take last coords of the snake's road and we draw exactly how many apples we have eaten 
        snake_road2.append(self.head)
        if length2 > 0:
            for i in range(1, length2 + 1):
                x = snake_road2[-i]
                pygame.draw.rect(screen, (0,255,0), (x[0], x[1], 40,40))
                snake_position2.append(x)
        while len(snake_position2) != length2:    # we get the momentarily coordination of the snake to a new list
            snake_position2.pop(0)            
    
    def movement(self):                           # function to regulate direction
        global player2_movement_x, player2_movement_y, queue2    
        if len(queue2) == 0:
            pass
        else:
            if queue2[0] == "UP":
                if player2_movement_y == 40:            # QUEUE - double clicking could make our snake kill itself
                    queue2.pop(0)
                else:
                    player2_movement_y = -40
                    player2_movement_x = 0
                    queue2.pop(0)
            elif queue2[0] == "DOWN":
                if player2_movement_y == -40:
                    queue2.pop(0)
                else:
                    player2_movement_y = +40
                    player2_movement_x = 0
                    queue2.pop(0)
            elif queue2[0] == "RIGHT":
                if player2_movement_x == -40:
                    queue2.pop(0)
                else:
                    player2_movement_x = 40
                    player2_movement_y = 0
                    queue2.pop(0)
            elif queue2[0] == "LEFT":
                if player2_movement_x == 40:
                    queue2.pop(0)
                else:
                    player2_movement_x = -40
                    player2_movement_y = 0
                    queue2.pop(0)
   
    def eat_apple(self):                                    # if apple is eaten, then we add to the score, length of our snake and we reset apple 
        global a, player2_score, length2
        if self.head_checking in apple_position:
            apple_position.remove(self.head_checking)
            player2_score += 1
            length2 += 1
            a = 0
            
    def eat_poison(self):                                   # if poison is eaten, then we remove poison and we kill our snake
        global q
        if self.head_checking in poison_position:
            poison_position.remove(self.head_checking)
            q = 0
    
    def collision_border(self):                             # collision with border or with snake itself kills our snake
        global q
        if self.head_checking[0] > 960 or self.head_checking[0] < 0:
            q = 0
        if self.head_checking[1] > 720 or self.head_checking[1] < 0:
            q = 0 
        if snake_position2.count(self.head) > 1:
            q = 0

    def collision_with_players(self):
        global q
        if self.head in snake_position1:
            q = 0
        if self.head in snake_position3:
            q = 0



"""                                     
                                            ----
            SNAKE FOR PLAYER 3
                                            ----
"""                                     

length3 = 1                 # length of the snake
a = 1                       # apple reaction
r = 1                       # poison reaction - snake is alive
queue3 = []                 # protection of snake comitting suicide
snake_road3 = []            # all coord of the snake's route
snake_position3 = []        # actual coords of the body - check if head collides with the rest of its body
class Snake3:
    def __init__(self, coord_x, coord_y):
        self.head = [coord_x, coord_y]
        self.head_checking = [coord_x + 20, coord_y + 20]
        self.alive = True

    def draw(self):                               # we take last coords of the snake's road and we draw exactly how many apples we have eaten 
        snake_road3.append(self.head)
        if length3 > 0:
            for i in range(1, length3 + 1):
                x = snake_road3[-i]
                pygame.draw.rect(screen, (0,0,255), (x[0], x[1], 40,40))
                snake_position3.append(x)
        while len(snake_position3) != length3:    # we get the momentarily coordination of the snake to a new list
            snake_position3.pop(0)            
    
    def movement(self):                           # function to regulate direction
        global player3_movement_x, player3_movement_y, queue3    
        if len(queue3) == 0:
            pass
        else:
            if queue3[0] == "UP":
                if player3_movement_y == 40:            # QUEUE - double clicking could make our snake kill itself
                    queue3.pop(0)
                else:
                    player3_movement_y = -40
                    player3_movement_x = 0
                    queue3.pop(0)
            elif queue3[0] == "DOWN":
                if player3_movement_y == -40:
                    queue3.pop(0)
                else:
                    player3_movement_y = +40
                    player3_movement_x = 0
                    queue3.pop(0)
            elif queue3[0] == "RIGHT":
                if player3_movement_x == -40:
                    queue3.pop(0)
                else:
                    player3_movement_x = 40
                    player3_movement_y = 0
                    queue3.pop(0)
            elif queue3[0] == "LEFT":
                if player3_movement_x == 40:
                    queue3.pop(0)
                else:
                    player3_movement_x = -40
                    player3_movement_y = 0
                    queue3.pop(0)
   
    def eat_apple(self):                                    # if apple is eaten, then we add to the score, length of our snake and we reset apple 
        global a, player3_score, length3
        if self.head_checking in apple_position:
            apple_position.remove(self.head_checking)
            player3_score += 1
            length3 += 1
            a = 0
            
    def eat_poison(self):                                   # if poison is eaten, then we remove poison and we kill our snake
        global r
        if self.head_checking in poison_position:
            poison_position.remove(self.head_checking)
            r = 0
    
    def collision_border(self):                             # collision with border or with snake itself kills our snake
        global r
        if self.head_checking[0] > 960 or self.head_checking[0] < 0:
            r = 0
        if self.head_checking[1] > 720 or self.head_checking[1] < 0:
            r = 0 
        if snake_position3.count(self.head) > 1:
            r = 0

    def collision_with_players(self):
        global r
        if self.head in snake_position1:
            r = 0
        if self.head in snake_position2:
            r = 0



"""
                                        -----
            START END CODE SECTION
                                        -----
"""

def controls_player1():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:          # movement with keyboard - arrows - for Player number 1                
            queue1.append("LEFT")
        if event.key == pygame.K_RIGHT:
            queue1.append("RIGHT")
        if event.key == pygame.K_UP:
            queue1.append("UP")
        if event.key == pygame.K_DOWN:
            queue1.append("DOWN")

def controls_player2():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:          # movement with keyboard - WSAD - for Player number 2                 
            queue2.append("LEFT")
        if event.key == pygame.K_d:
            queue2.append("RIGHT")
        if event.key == pygame.K_w:
            queue2.append("UP")
        if event.key == pygame.K_s:
            queue2.append("DOWN")

def controls_player3():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_j:          # movement with keyboard - IKJL - for Player number 3                 
            queue3.append("LEFT")
        if event.key == pygame.K_l:
            queue3.append("RIGHT")
        if event.key == pygame.K_i:
            queue3.append("UP")
        if event.key == pygame.K_k:
            queue3.append("DOWN")


"""
                        ----
        MAIN
                        ----
"""
player1_score = 0
player2_score = 0           # this will represent the results at the end
player3_score = 0

print("Zvolte si počet hráčů:  (1 = jeden hráč, 2 = 2 hráči, 3 = 3hráči)")      # decide how many players are playing; 1 up to 3
while True:
    no_players = int(input())
    if no_players == 1 or no_players == 2 or no_players == 3:
        break
    else:
        print("Znovu a lépe :)")

if no_players == 1:             # we set up the game for only one player
    q = 0
    r = 0
    pygame.init()
    pygame.display.set_caption("Snake Game - multiplayer - by DZ")
    width = 960
    height = 720
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    A = Apple()                             # init of Apple
    P = Poison()

    player1_coord_x = 200                   # starting coordinations of 1. snake
    player1_coord_y = 200   
    player1_movement_x = 40                 # starting speed and direction of 1. snake
    player1_movement_y = 0 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            controls_player1()

        screen.fill(pygame.Color(0, 0, 0))              # black screen, then our squares - board
        create_board()

        if p == 1:                                      # if our snake is alive, then we init him and his core functions
            S1 = Snake1(player1_coord_x, player1_coord_y)
            S1.draw()
            S1.movement()
            S1.eat_apple()
            S1.eat_poison()
            S1.collision_border()
        else:                                           # if the snake dies, his current position is set to none
            snake_position1.clear() 
        S1.collision_with_players()
        A.check_if_apple_eaten()                        # core functions of Apple and Poison classes
        A.draw()
        P.draw()
        player1_coord_x = player1_coord_x + player1_movement_x                  # OUR MAIN SOURCE OF MOVEMENT !!!
        player1_coord_y = player1_coord_y + player1_movement_y
        i += 1 
        if p == 0 and q == 0 and r == 0:
            break
        pygame.display.flip()
        clock.tick(5)                                                           # OUR MAIN SOURCE OF MOVEMENT !!! 

if no_players == 2:                 # we set the game for 2 players
    r = 0
    pygame.init()
    pygame.display.set_caption("Snake Game - multiplayer - by DZ")
    width = 960
    height = 720
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    A = Apple()                     # init of Apple
    P = Poison()

    player1_coord_x = 200                   # starting coordinations of 1. snake
    player1_coord_y = 200   
    player1_movement_x = 40                 # starting speed and direction of 1. snake
    player1_movement_y = 0

    player2_coord_x = 600
    player2_coord_y = 600                   # starting coordinations of 2. snake
    player2_movement_x = 0                  # starting speed and direction of 2. snake
    player2_movement_y = -40 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            controls_player1() 
            controls_player2() 
        screen.fill(pygame.Color(0, 0, 0))              # black screen, then our squares - board
        create_board()

        if p == 1:                                      # if 1. snake is alive, then we init him and his core functions
            S1 = Snake1(player1_coord_x, player1_coord_y)
            S1.draw()
            S1.movement()
            S1.eat_apple()
            S1.eat_poison()
            S1.collision_border()
        else:                                           # if the snake dies, his current position is set to none
            snake_position1.clear()
        if q == 1:                                      # if 2. snake is alive, then we init him and his core functions
            S2 = Snake2(player2_coord_x, player2_coord_y)
            S2.draw()
            S2.movement()
            S2.eat_apple()
            S2.eat_poison()
            S2.collision_border()
        else:                                           # if the snake dies, his current position is set to none
            snake_position2.clear()

        S1.collision_with_players()
        S2.collision_with_players()
        A.check_if_apple_eaten()                        # core functions of Apple and Poison classes
        A.draw()
        P.draw()
        player1_coord_x = player1_coord_x + player1_movement_x                  # OUR MAIN SOURCE OF MOVEMENT !!!
        player1_coord_y = player1_coord_y + player1_movement_y
        player2_coord_x = player2_coord_x + player2_movement_x
        player2_coord_y = player2_coord_y + player2_movement_y
        i += 1 
        if p == 0 and q == 0 and r == 0:
            break
        pygame.display.flip()
        clock.tick(5)

if no_players == 3:                     # we set the game for 3 players
    pygame.init()
    pygame.display.set_caption("Snake Game - multiplayer - by DZ")
    width = 960
    height = 720
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    A = Apple()                     # init of Apple
    P = Poison()

    player1_coord_x = 200                   # starting coordinations of 1. snake
    player1_coord_y = 200   
    player1_movement_x = 40                 # starting speed and direction of 1. snake
    player1_movement_y = 0

    player2_coord_x = 600                   # starting coordinations of 2. snake
    player2_coord_y = 600
    player2_movement_x = 0                  # starting speed and direction of 2. snake
    player2_movement_y = -40 

    player3_coord_x = 480                   # starting coordinations of 3. snake
    player3_coord_y = 80
    player3_movement_x = -40                # startin speed and direction of 3. snake
    player3_movement_y = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            controls_player1() 
            controls_player2()
            controls_player3() 
        screen.fill(pygame.Color(0, 0, 0))              # black screen, then we draw our board - squares
        create_board()

        if p == 1:                                      # if 1. snake is alive, then we init him and his core functions
            S1 = Snake1(player1_coord_x, player1_coord_y)
            S1.draw()
            S1.movement()
            S1.eat_apple()
            S1.eat_poison()
            S1.collision_border()
        else:                                           # if the snake dies, his current position is set to none
            snake_position1.clear()
        if q == 1:                                      # if 2. snake is alive, then we init him and his core functions
            S2 = Snake2(player2_coord_x, player2_coord_y)
            S2.draw()
            S2.movement()
            S2.eat_apple()
            S2.eat_poison()
            S2.collision_border()
        else:                                           # if the snake dies, his current position is set to none
            snake_position2.clear()
        if r == 1:                                      # if 3. snake is alive, then we init him and his core functions
            S3 = Snake3(player3_coord_x, player3_coord_y)
            S3.draw()
            S3.movement()
            S3.eat_apple()
            S3.eat_poison()
            S3.collision_border()
        else:                                           # if the snake dies, his current position is set to none
            snake_position3.clear()

        S1.collision_with_players()
        S2.collision_with_players()
        S3.collision_with_players()
        A.check_if_apple_eaten()                        # core functions of Apple and Poison classes
        A.draw()
        P.draw()
        player1_coord_x = player1_coord_x + player1_movement_x                  # OUR MAIN SOURCE OF MOVEMENT !!!
        player1_coord_y = player1_coord_y + player1_movement_y
        player2_coord_x = player2_coord_x + player2_movement_x
        player2_coord_y = player2_coord_y + player2_movement_y
        player3_coord_x = player3_coord_x + player3_movement_x                  # OUR MAIN SOURCE OF MOVEMENT !!!
        player3_coord_y = player3_coord_y + player3_movement_y
        i += 1 
        if p == 0 and q == 0 and r == 0:
            break
        pygame.display.flip()
        clock.tick(5)

if p == 0 and q == 0 and r == 0:                # when the game ends, i created custom fireworks to celebrate with results
    pygame.init()
    width = 960
    height = 720
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    coord_x = 160
    coord_y = 680
    i = 0
    def particles(k,l,m,n):   
        pygame.draw.polygon(screen, (255,0,0), [(k,l), (m,n)], width=3)
    
    player1_score = str(player1_score)
    player2_score = str(player2_score)          # preparations for printing results on the screen
    player3_score = str(player3_score)
    myfont = pygame.font.SysFont("Cosmic Sans MS", 32)
    textsurface1 = myfont.render("Player1: " + player1_score, False, (255,0,0))
    textsurface2 = myfont.render("Player2: " + player2_score, False, (255,0,0))
    textsurface3 = myfont.render("Player3: " + player3_score, False, (255,0,0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(pygame.Color(0, 0, 0))

        screen.blit(textsurface1, (520,440))
        screen.blit(textsurface2, (520,480))    # printing results on the screen
        screen.blit(textsurface3, (520,520))

        if i != 10:
            if coord_y != 260:
                particles(coord_x,coord_y, coord_x, coord_y-30)                     # fireworks itself, custom made
                coord_y -= 60
            else:
                particles(coord_x, coord_y-30, coord_x, coord_y-60)
                particles(coord_x-30, coord_y-90, coord_x-60, coord_y-120)
                particles(coord_x+30, coord_y-90, coord_x+60, coord_y-120)

                particles(coord_x-30, coord_y-30, coord_x-60, coord_y-60)
                particles(coord_x+30, coord_y-30, coord_x+60, coord_y-60)
                particles(coord_x-90, coord_y-80, coord_x-120, coord_y-80)
                particles(coord_x+90, coord_y-80, coord_x+120, coord_y-80)

                particles(coord_x-30, coord_y, coord_x-60, coord_y)
                particles(coord_x-90,coord_y,coord_x-120,coord_y+15)
                particles(coord_x+30,coord_y,coord_x+60,coord_y)
                particles(coord_x+90,coord_y,coord_x+120,coord_y+15)

                particles(coord_x-30, coord_y+30, coord_x-60, coord_y+60)
                particles(coord_x+30, coord_y+30, coord_x+60, coord_y+60)
                particles(coord_x-70, coord_y+90, coord_x-80, coord_y+120)
                particles(coord_x+70, coord_y+90, coord_x+80, coord_y+120)
        else:
            i = 0
            coord_x = 160
            coord_y = 680
        i += 1   
        pygame.display.flip()
        clock.tick(5)

"""
Hopefully you enjoyed playing my version of the snake game!
"""