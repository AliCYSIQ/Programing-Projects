import pygame as pg
import random
import sys
import math

pg.init()
pg.font.init()
Xscreen = 540
Yscreen = 650
screen = pg.display.set_mode((Xscreen, Yscreen))  # x,y
pg.display.set_caption("Pong")
clock = pg.time.Clock()
oppentBaddel = pg.Rect(230, 10, 100, 10)
playerBaddel = pg.Rect(230, 630, 100, 10)
ball = pg.Rect(Xscreen / 2, Yscreen / 2, 10, 10)
ball_speed_x = 0
ball_speed_y = 0
playerPoint = 0
oppentPoint = 0
scoreTime = 0
isBallActive = False
ballStopTime = 500
ball_speed_x = 0
ball_speed_y = 0

def PlayerBaddelMovemnt():
    keys = pg.key.get_pressed()
    speed = 5
    if keys[pg.K_LSHIFT]:
        speed = 10
    else:
        speed = 5
    if keys[pg.K_a]:
        playerBaddel.x -= speed
    elif keys[pg.K_d]:
        playerBaddel.x += speed

    if playerBaddel.left < 0:
        playerBaddel.left = 0
    elif playerBaddel.right > Xscreen:
        playerBaddel.right = Xscreen


def MoveBall():
    global ball_speed_x, ball_speed_y, oppentPoint, playerPoint,scoreTime,isBallActive
    
    if not isBallActive:
        currentTime = pg.time.get_ticks()
       
        if currentTime - scoreTime >= ballStopTime:
            isBallActive = True
            ball_speed_x = 5 + random.randint(-2, 2)
            ball_speed_y = 5 + random.randint(-1, 1)
        return
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top < 0:
        ball.x = Xscreen / 2
        ball.y = Yscreen / 2
        playerPoint += 1
        isBallActive = False
        scoreTime = pg.time.get_ticks()
        ball_speed_y *= -1
        
    elif ball.bottom > Yscreen:
        ball.x = Xscreen / 2
        ball.y = Yscreen / 2
        oppentPoint += 1
        ball_speed_y *= -1
        isBallActive = False
        scoreTime = pg.time.get_ticks()

    if ball.left <= 0 or ball.right > Xscreen:
        ball_speed_x *= -1
    if ball.colliderect(playerBaddel) or ball.colliderect(oppentBaddel):
        ball_speed_y *= -1

    # (text string, antialias, text color, optional background color)
    text_surface = SPEED_FONT.render(
        f"{math.hypot(ball_speed_x, ball_speed_y):.1f} cm/s", True, (255, 255, 0)
    )  # White text

    screen.blit(text_surface, (ball.x + 3, ball.y + 3))

def OpponentMovement():
    freeOffsit =5
    aiSpeed = 4
    if(ball.y > (Yscreen/2)+freeOffsit):
        aiSpeed = 2 # to make it easier and more fair to the player 
    else:
        aiSpeed = 4
    if ball.centerx > oppentBaddel.centerx+freeOffsit:
        oppentBaddel.x +=aiSpeed
    elif ball.centerx < oppentBaddel.centerx+freeOffsit:
        oppentBaddel.x -=aiSpeed
# Pass None for the font file argument
SPEED_FONT = pg.font.Font(None, 25)
POINT_FONT = pg.font.Font(None, 30)


while True:
    # 1. INPUT
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # 2. Movement
    PlayerBaddelMovemnt()
    OpponentMovement() 
    MoveBall()

    # 3. DRAW
    screen.fill((30, 30, 46))
    pg.draw.ellipse(surface=screen, color=(255, 0, 0), rect=ball)
    pg.draw.rect(surface=screen, color=(255, 255, 255), rect=playerBaddel)
    pg.draw.rect(surface=screen, color=(255, 255, 255), rect=oppentBaddel)
    
    point_text = POINT_FONT.render(f"{playerPoint}:{oppentPoint}", True, (255, 255, 0))
    screen.blit(point_text, (Xscreen - 50, Yscreen / 2))

    speed_text = SPEED_FONT.render(
        f"{math.hypot(ball_speed_x, ball_speed_y):.1f} cm/s", True, (255, 255, 0)
    )  # White text
    screen.blit(speed_text, (ball.x + 3, ball.y + 3))

    # 4. FLIP & CLOCK
    pg.display.flip()
    clock.tick(60)