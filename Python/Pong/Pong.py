import pygame as pg
import random
import sys

pg.init()
Xscreen = 540
Yscreen = 650
screen = pg.display.set_mode((Xscreen, Yscreen))  # x,y
pg.display.set_caption("Pong")
clock = pg.time.Clock()
oppentBaddel = pg.Rect(230, 10, 100, 10)
playerBaddel = pg.Rect(230, 630, 100, 10)
ball = pg.Rect(Xscreen / 2, Yscreen / 2, 10, 10)
ball_speed_x = 5 + random.randint(-1, 1)
ball_speed_y = 5 + random.randint(-1, 1)

baseXspeed = ball_speed_x
baseYspeed = ball_speed_y


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


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:  # If they click the 'X'
            pg.quit()
            sys.exit()

    screen.fill((30, 30, 46))  # Fill the screen with a dark color (RGB)

    ## draw
    pg.draw.ellipse(surface=screen, color=(255, 0, 0), rect=ball)
    pg.draw.rect(surface=screen, color=(255, 255, 255), rect=playerBaddel)
    pg.draw.rect(surface=screen, color=(255, 255, 255), rect=oppentBaddel)

    ## move

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top < 0 or ball.bottom > Yscreen:
        ball_speed_y *= -1.1
    if ball.left <= 0 or ball.right > Xscreen:
        ball_speed_x *= -1.1
    if ball.colliderect(playerBaddel) or ball.colliderect(oppentBaddel):
        ball_speed_y *= -1

    if ball_speed_x > 0:
        ball_speed_x = baseXspeed
    if ball_speed_y > 0:
        ball_speed_y = baseYspeed
    PlayerBaddelMovemnt()

    pg.display.flip()

    # Force the loop to run at exactly 60 Frames Per Second
    clock.tick(60)
