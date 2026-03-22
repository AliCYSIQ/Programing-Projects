import pygame as pg
import sys
pg.init()
WIDTH = 600
screen = pg.display.set_mode((WIDTH,WIDTH))
pg.display.set_caption("A* Pathfinding")
clock = pg.time.Clock()

## gloabl vars
ROWS = 20
cellWidth = WIDTH//ROWS
WHITECOLOR = (255,255,255)
BLACKCOLOR = (0,0,0)
GRAYCOLOR = (100, 100, 100)
Grid = [[0 for _ in range(ROWS)] for _ in range(ROWS)]
Grid[0][1] = 1
Grid[2][10] = 1
def DrawGrid():
    for y, row in enumerate(Grid):
        for x, gridvalue in enumerate(row):
            
            # 2. Create the Rect object using a capital 'R'
            rect = pg.Rect(x * cellWidth, y * cellWidth, cellWidth, cellWidth)

            # 3. Draw it based on the grid value
            if gridvalue == 0:
                pg.draw.rect(surface=screen, color=WHITECOLOR, rect=rect)
            else:
                pg.draw.rect(surface=screen, color=BLACKCOLOR, rect=rect)
            pg.draw.rect(surface=screen,color=GRAYCOLOR,rect=rect,width=1)

while True:
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if pg.mouse.get_pressed()[0]:
            mouseX,mouseY = pg.mouse.get_pos()
            try:
                mouseX //= cellWidth
                mouseY //= cellWidth
                mouseX = min(mouseX,len(Grid)-1)
                mouseY = min(mouseY,len(Grid)-1)
                Grid[mouseY][mouseX] =1
            except IndexError:
                print(mouseX, mouseY)
    ## logic
    
    ## Draw
    screen.fill((30, 30, 46))
    DrawGrid()
    # the end
    pg.display.flip()
    clock.tick(60)