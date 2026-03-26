import pygame as pg
import sys
from queue import PriorityQueue
import math
pg.init()
WIDTH = 700
screen = pg.display.set_mode((WIDTH,WIDTH))
pg.display.set_caption("A* Pathfinding")
clock = pg.time.Clock()

## gloabl vars
ROWS = 50
speed = 1 # make the number bigger for faster result (10 slow, 25 normal , 50 fast , 100 very fast , 1000 or bigger instatnt)
cellWidth = WIDTH//ROWS
WHITECOLOR = (255,255,255)
BLACKCOLOR = (0,0,0)
GRAYCOLOR = (100, 100, 100)
GREENCOLOR = (0, 255, 0) # Start
REDCOLOR = (255, 0, 0) # End
ORANGECOLOR = (255, 165, 0) # End
BLUECOLOR = (0, 0, 255) # Closed (Already checked)
YELLOWCOLOR = (255, 255, 0) # Open (In the queue to be checked)
PURPLECOLOR = (128, 0, 128) # The final path
start_node = None
end_node = None

def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
class Node:
    
    def __init__(self,row,col,width):
        self.row = row
        self.col = col 
        self.x =col*width
        self.y = row * width
        self.color = WHITECOLOR
        self.width=width
        self.neighbors = []
        self.isA = False
        self.cost = 1
        self.isSwamp = False
    def GetPos(self):
        return self.row,self.col
    def IsWall(self):
        return self.color == BLACKCOLOR
    def MakeWall(self): 
        self.isA = False
        self.color = BLACKCOLOR
    def MakeSwamp(self): 

        self.isA = False
        self.isSwamp = True
        self.color = ORANGECOLOR
        self.cost = 5
    def reset(self,color = WHITECOLOR): 
        self.isA = False
        self.color = color

    def MakeStart(self):
        self.isA = False
        self.color = GREENCOLOR

    def MakeEnd(self): 
        self.isA = False
        self.color = REDCOLOR
    def MakeClosed(self): 
        if not self.isSwamp:
            self.color = BLUECOLOR 
        self.isA = True

    def MakeOpen(self): 
        self.isA = True
        if not self.isSwamp:
            self.color = YELLOWCOLOR

    def MakePath(self): 
        self.isA = True
        if  self.isSwamp:
            self.color = (255,0,0)
        else:
            self.color = PURPLECOLOR
    def UpdateNeighbors(self, grid):
        self.neighbors = []
        # DOWN
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].IsWall():
            self.neighbors.append(grid[self.row + 1][self.col])
        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].IsWall():
            self.neighbors.append(grid[self.row - 1][self.col])
        # RIGHT
        if self.col < ROWS - 1 and not grid[self.row][self.col + 1].IsWall():
            self.neighbors.append(grid[self.row][self.col + 1])
        # LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].IsWall():
            self.neighbors.append(grid[self.row][self.col - 1])

    def Draw(self,surface):
        rect = (self.x,self.y,self.width,self.width)
        
        pg.draw.rect(surface,self.color,rect)
        pg.draw.rect(surface=screen,color=GRAYCOLOR,rect=rect,width=1)
    
    
Grid = [[Node(row,col,cellWidth) for col in range(ROWS)] for row in range(ROWS)]

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.MakePath()
        draw()

def algorithm(draw, grid, start, end):
    pq = PriorityQueue()
    count = 0
    cameFrom = {}
    pq.put((0,count,start))
    gScore = {node:float("inf") for row in grid for node in row}
    gScore[start] = 0

    fScore = {node:float("inf") for row in grid for node in row}

    fScore[start] = h(start.GetPos(),end.GetPos())

    open_set_hash = {start}
    steps = 0
    while not pq.empty():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
    
        current = pq.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(cameFrom,current,draw_wrapper)
            end.MakeEnd()
            start.MakeStart()
            return True
        
        for neighbor in current.neighbors:
            tempGscore = gScore[current]+neighbor.cost
            if tempGscore < gScore[neighbor]:
                cameFrom[neighbor]=current
                gScore[neighbor] = tempGscore
                fScore[neighbor]= tempGscore+ h(neighbor.GetPos(),end.GetPos())
                if neighbor not in open_set_hash:
                    count +=1
                    pq.put((fScore[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.MakeOpen()

        steps +=1
        if steps%speed==0:# make the number bigger for faster result
            draw()
        if current != start:
            current.MakeClosed()


def DrawGrid():
    for i in Grid:
        for node in i:
            node.Draw(screen)

def draw_wrapper():
    DrawGrid()
    pg.display.flip()
def AReset():
    for i in Grid:
        for node in i:
            if node.isA and node.isSwamp:
                node.reset(ORANGECOLOR)
            elif node.isA:
                node.reset()            

while True:
    
    for event in pg.event.get():
        keys = pg.key.get_pressed()
        

        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if keys[pg.K_c]:
            
            Grid = [[Node(row,col,cellWidth) for col in range(ROWS)] for row in range(ROWS)]
            start_node=None
            end_node = None
        if keys[pg.K_r]:
            AReset()
        if keys[pg.K_SPACE] and start_node and end_node:
            for row in Grid:
                for node in row:
                    node.UpdateNeighbors(Grid)
            AReset()
            algorithm(draw_wrapper, Grid, start_node, end_node)
        if pg.mouse.get_pressed()[0]:
            mouseX, mouseY = pg.mouse.get_pos()
            row = max(0, min(ROWS - 1, mouseY // cellWidth))
            col = max(0, min(ROWS - 1, mouseX // cellWidth))
            node = Grid[row][col]

            if not start_node and node != end_node:
                start_node = node
                start_node.MakeStart()
            elif not end_node and node != start_node:
                end_node = node
                end_node.MakeEnd()
            elif node != start_node and node != end_node and keys[pg.K_LSHIFT]:
                node.MakeSwamp()
            elif node != start_node and node != end_node:
                node.MakeWall()


        # Right Click (Erase)
        elif pg.mouse.get_pressed()[2]:
            mouseX, mouseY = pg.mouse.get_pos()
            row = max(0, min(ROWS - 1, mouseY // cellWidth))
            col = max(0, min(ROWS - 1, mouseX // cellWidth))
            node = Grid[row][col]

            
            node.reset()
            if node == start_node:
                start_node = None
            elif node == end_node:
                end_node = None
    ## logic
    
    ## Draw
    screen.fill((30, 30, 46))
    DrawGrid()
    # the end
    pg.display.flip()
    clock.tick(60)