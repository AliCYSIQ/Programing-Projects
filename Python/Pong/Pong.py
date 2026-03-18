import pygame as pg
import sys

pg.init()

screen = pg.display.set_mode((540, 650))  # x,y
pg.display.set_caption("Pong")
clock = pg.time.Clock()
oppentBaddel = pg.Rect(350, 10, 100, 10)
playerBaddel = pg.Rect(350, 630, 100, 10)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:  # If they click the 'X'
            pg.quit()
            sys.exit()

    screen.fill((30, 30, 46))  # Fill the screen with a dark color (RGB)

    pg.draw.rect(surface=screen, color=(255, 255, 255), rect=playerBaddel)
    pg.draw.rect(surface=screen, color=(255, 255, 255), rect=oppentBaddel)

    pg.display.flip()

    # Force the loop to run at exactly 60 Frames Per Second
    clock.tick(60)
