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

class Node:
    def __init__(self,row,col,width):
        self.row = row
        self.col = col 
        self.x =col*width
        self.y = row * width
        self.color = WHITECOLOR
        self.width=width
    def GetPos(self):
        return self.row,self.col
    def IsWall(self):
        return self.color == BLACKCOLOR
    def make_wall(self): 
        self.color = BLACKCOLOR
    def Draw(self,surface):
        rect = (self.x,self.y,self.width,self.width)
        
        return pg.draw.rect(surface,self.color,rect),pg.draw.rect(surface=screen,color=GRAYCOLOR,rect=rect,width=1)
    
Grid = [[Node(row,col,cellWidth) for col in range(ROWS)] for row in range(ROWS)]

    
        
def DrawGrid():
   for i in Grid:
       for node in i:
           node.Draw(screen)
        
    

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
                mouseX = max(0, min(ROWS - 1, mouseX))
                mouseY = max(0, min(ROWS - 1, mouseY))
                Grid[mouseY][mouseX].make_wall()
            except IndexError:
                print(mouseX, mouseY)
    ## logic
    
    ## Draw
    screen.fill((30, 30, 46))
    DrawGrid()
    # the end
    pg.display.flip()
    clock.tick(60)