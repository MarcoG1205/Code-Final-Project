
import os
import pygame
import random
import math
# initialize pygame 
pygame.init ()

screen = pygame.display.set_mode ((800,600))

#os.chdir("Code-Final-Project")
pygame.display.set_caption ("Space Raiders")
icon = pygame.image.load ('space-ship.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load ('screen.png')

# player (creates the space ship)
playerImg = pygame.image.load ('player.png')
playerX = 370
playerY = 480
playerX_change = 0


# Enemy (creates the enemy)
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range (num_of_enemies):
    enemyImg.append(pygame.image.load ('enemy.png'))
    enemyX.append(random.randint (0,735))
    enemyY.append(random.randint (50,150))
    enemyX_change.append(2.5)
    enemyY_change.append(40)

# ready means you can't see the laser on the screen
# fire = the laser is currently moving 
# laser (creates the lazer)
laserImg = pygame.image.load ('laser.png')
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 7
laser_state = "ready"

# score
# font
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10 
textY = 10

#game over text 
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score (x,y):
    score = font.render("Score :" + str(score_value) , True, (255,255,255))
    screen.blit (score, ( x, y ))

def game_over_text():
    over_text = font.render ("GAME OVER", True, (255,255,255))
    screen.blit (over_text, ( 200, 250))

def player (x,y):
    screen.blit (playerImg, ( x, y ))

def enemy (x,y,i):
    screen.blit (enemyImg[i], ( x, y ))

def fire_laser (x,y) :
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x+16,y+10))

def isCollision (enemyX,enemyY,laserX,laserY) :
    distance = math.sqrt ((math.pow(enemyX - laserX,2)) +  (math.pow(enemyY - laserY,2)))
    if distance <27:
        return True
    else:
        return False
# game loop
running = True 
while running: 
    
     # RGB
    screen.fill ((0,0,0))
    # background image
    screen.blit(background, (0,0))

    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            running = False 

        # if key pressed check whether its right of left 
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_a :
               playerX_change = -3
            if event.key == pygame.K_d :
                 playerX_change = 3
            if event.key == pygame.K_SPACE :
                if laser_state is "ready":
                    laserX = playerX
                    fire_laser(laserX,laserY)
        
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_a or event.key == pygame.K_d :
                playerX_change = 0

                
            
    # checking for boundaries 
    playerX += playerX_change   

    if playerX <=0 :
        playerX = 0
    elif playerX >=736 :
        playerX = 736

    # laser movement 
    if laserY <=0:
        laserY = 480
        laser_state == "ready"
    
    if laser_state == "fire":
        fire_laser(laserX,laserY)
        laserY -= laserY_change
    

    # enemy movement
    for i in range (num_of_enemies):
        
        # game over 
        if enemyY[i] > 440: 
            for j in range (num_of_enemies):
                enemyY [j] = 2000
            game_over_text ()
            break
        
        enemyX[i] += enemyX_change[i]   
        if enemyX[i] <=0 :
                enemyX_change[i] = 2.5
                enemyY[i] += enemyY_change[i] 
        elif enemyX[i] >=736 :
                enemyX_change[i] = -2.5
                enemyY[i] += enemyY_change[i]
   
    #collision 
        collision = isCollision (enemyX[i], enemyY[i], laserX,laserY)
        if collision: 
            laserY = 480
            laser_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint (0,735)
            enemyY[i] = random.randint (50,150)

        enemy( enemyX[i], enemyY[i], i)


    player( playerX, playerY)
    show_score (textX, textY)
    pygame.display.update()