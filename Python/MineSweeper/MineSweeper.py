import pygame as pg
import sys
import random as rand

## gloabl vars
WIDTH = 700
pg.init()
pg.font.init()
screen = pg.display.set_mode((WIDTH,WIDTH))
pg.display.set_caption("MineSweeper")
clock = pg.time.Clock()
ROWS = 20
TOTAL_MINES = int((ROWS+ROWS/2)+20)
cellWidth = WIDTH//ROWS
WHITECOLOR = (255,255,255)
BLACKCOLOR = (0,0,0)
GRAYCOLOR = (100, 100, 100)
GREENCOLOR = (0, 255, 0) # Start
REDCOLOR = (255, 0, 0) # End
ORANGECOLOR = (255, 165, 0) # End
BLUECOLOR = (0, 0, 255) 
YELLOWCOLOR = (255, 255, 0) # Open (In the queue to be checked)
PURPLECOLOR = (128, 0, 128) # The final path

fontSize = ROWS+15
try:
    font = pg.font.SysFont('arial', fontSize)
except:
    # Fallback if 'arial' is not available
    font = pg.font.Font(None, fontSize) 
class Cell:
    def __init__(self,row,col,width):
        self.row =row
        self.col = col
        self.x = col*width
        self.y = row*width
        self.width=width
        self.isMine = False
        self.is_revealed = False
        self.isFlagged = False
        self.color = GREENCOLOR
    def GetPos(self):
        return self.row,self.col
    def MakeMine(self):
        self.isMine = True
        self.color = REDCOLOR
    def CellDraw(self,color = GREENCOLOR):
        rect = (self.x,self.y,self.width,self.width)
        pg.draw.rect(screen,color,rect)
        pg.draw.rect(screen,GRAYCOLOR,rect,width=1)
    def NeighborMines(self):
        if self.isMine:
            return -1
             
        
        counter = 0
        # Loop through the 3x3 area around the cell
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                # Skip the center cell itself
                if dr == 0 and dc == 0:
                    continue
                
                r = self.row + dr
                c = self.col + dc
                
                # Use ROWS to check boundaries
                if 0 <= r < ROWS and 0 <= c < ROWS:
                    if GRID[r][c].isMine:
                        counter += 1
                        
        return int(counter)
    def EmptyCells(self):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue

                r = self.row + dr
                c = self.col + dc

                if 0 <= r < ROWS and 0 <= c < ROWS:
                    neighbor_cell = GRID[r][c]

                    if not neighbor_cell.is_revealed and not neighbor_cell.isMine: 
                        neighbor_cell.is_revealed = True
                        if -1 < neighbor_cell.NeighborMines()< 1 and not neighbor_cell.isFlagged:
                            neighbor_cell.CellDraw(WHITECOLOR)
                            neighbor_cell.EmptyCells()
                              
                        else:
                            neighbor_cell.EntityDraw()
                            
    def FlagCell(self):
        if self.is_revealed:
            return
        if self.isFlagged:
            self.isFlagged = False
            self.CellDraw()
            return
        self.isFlagged = True
        
        pg.draw.ellipse(screen,REDCOLOR,rect=(self.x+5/2,self.y+5/2,self.width-5,self.width-5))
    def EntityDraw(self):
        if(self.isFlagged):
            return
        n = self.NeighborMines()
        rect = pg.Rect(self.x,self.y,self.width,self.width)
        
        if n ==-1:
            self.CellDraw(REDCOLOR)
            self.is_revealed = True

            return      
        elif n ==0:
            self.CellDraw(WHITECOLOR)
            self.is_revealed = True
            self.EmptyCells()   
        else:
            self.is_revealed = True
            self.CellDraw(WHITECOLOR)
            textSurface = font.render(str(n),True,BLACKCOLOR)

            textRect = textSurface.get_rect(center=rect.center)
            screen.blit(textSurface,textRect)
            
GRID = [[Cell(row,col,cellWidth) for col in range(ROWS)]  for row in range(ROWS)]
def DrawGrid():
    for rows in GRID:
        for cell in rows:
            cell.isMine = False
            cell.is_revealed = False
            cell.isFlagged = False
            cell.CellDraw()
def RanMines(mines = TOTAL_MINES):
    placed = 0
    while placed < mines:
        y = rand.randint(0, ROWS-1)
        x = rand.randint(0, ROWS-1)
        if not GRID[y][x].isMine:
            GRID[y][x].MakeMine()
            placed += 1
    

            
start = True
while True:   
    for event in pg.event.get():
        keys = pg.key.get_pressed()
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if keys[pg.K_r]:
            start = True
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            Xcell = max(0, min(ROWS-1, x//cellWidth))
            Ycell = max(0, min(ROWS-1, y//cellWidth))
            
            if event.button == 1: # Left Click
                GRID[Ycell][Xcell].EntityDraw()
            elif event.button == 3: # Right Click
                GRID[Ycell][Xcell].FlagCell()
            

    
    if(start):
        screen.fill(BLACKCOLOR)
        DrawGrid()
        RanMines()

        start = False


    pg.display.flip()
    clock.tick(60)
    
