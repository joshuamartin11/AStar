import pygame,math as mt
from pygame.constants import K_RETURN, KEYDOWN, MOUSEBUTTONDOWN
pygame.init()
screen = pygame.display.set_mode((1000,1000))

pygame.display.set_caption('A* Test Program')

background = (255,255,255)

screen.fill(background)

openLst = list()

start = None
target = None

class Square:
    def __init__(self,rec,coords):
        self.rec = rec
        self.gCost = 0
        self.hCost = None
        self.fCost = None
        self.wall = False
        self.target = False
        self.start = False
        self.coords = coords
        self.parent = None
        self.closed = False
        self.open = False
        self.path = False

running = True

gridSize = 80
squareSize = 10
grid = [[0 for _ in range(gridSize)] for _ in range(gridSize)]

for y in range(gridSize):
    for x in range(gridSize):
        # print("test")
        grid[y][x] = Square(pygame.Rect(squareSize*x,squareSize*y,squareSize,squareSize),(x,y))


def redraw():
    for row in grid:
        for square in row:
            if(square.wall):
                pygame.draw.rect(screen,(0,0,255),square.rec)
            elif(square.start):
                pygame.draw.rect(screen,(0,200,0),square.rec)
            elif(square.target):
                pygame.draw.rect(screen,(255,0,0),square.rec)
            elif(square.closed):
                pygame.draw.rect(screen,(0,200,0),square.rec)
            elif(square.open):
                pygame.draw.rect(screen,(0,255,0),square.rec)
            else:
                pygame.draw.rect(screen,(0,0,0),square.rec)

            if(square.path):
                pygame.draw.rect(screen,(255,0,0),square.rec)


def calcH(square,tar):
    return (mt.sqrt((square.coords[0] - tar.coords[0])**2 + (square.coords[1] - tar.coords[1])**2))

def runAlg(cur,tar):
    j = 0
    found = False
    cur.fCost = calcH(cur,tar)
    openLst.append(cur)
    while(not found):
        current = openLst.pop(0)
        current.closed = True
        current.open = False
        redraw()
        pygame.display.update()
        if current.target:
            found = True
            print("Found!")
            return current

        neighbours = []
        if (current.coords[0] - 1 >= 0):
            neighbours.append(grid[current.coords[1]][current.coords[0] - 1])
        if (current.coords[0] + 1 < gridSize):
            neighbours.append(grid[current.coords[1]][current.coords[0] + 1])
        if (current.coords[1] - 1 >= 0):
            neighbours.append(grid[current.coords[1] - 1][current.coords[0]])
        if (current.coords[1] + 1 < gridSize):
            neighbours.append(grid[current.coords[1] + 1][current.coords[0]])

        print(len(openLst))
        for neighbour in neighbours:
            if(neighbour.closed == False and neighbour.wall == False):
                neighbour.hCost = calcH(neighbour,tar)
                f = neighbour.hCost + current.gCost + 1

                if(neighbour.fCost == None):
                    neighbour.fCost = f
                
                if(f < neighbour.fCost or neighbour.open == False):
                    neighbour.fCost = f
                    neighbour.parent = current
                    
                    if neighbour.open == False:
                        neighbour.open = True
                        i = 0
                        # j += 1
                        # print(j)
                        if len(openLst) != 0:
                            for s in openLst:
                                if(neighbour.fCost < s.fCost):
                                    openLst.insert(i,neighbour)
                                    break

                                i += 1
                        else:
                            openLst.append(neighbour)
                        
                        if i == len(openLst):
                            openLst.append(neighbour)

def drawPath(start, tar):
    current = tar
    while(start.coords != current.coords):
        current.path = True
        current = current.parent
        # print("ran")
    redraw()
    pygame.display.update()


while(running):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                runAlg(start,target)
                drawPath(start,target)
                


    if(pygame.mouse.get_pressed()[0] == True):
        # print("test")
        mouseX, mouseY = tuple(int(mousePos/squareSize) for mousePos in pygame.mouse.get_pos())
        grid[mouseY][mouseX].wall = True
    
    if(pygame.mouse.get_pressed()[2] == True):
        mouseX, mouseY = tuple(int(mousePos/squareSize) for mousePos in pygame.mouse.get_pos())
        grid[mouseY][mouseX].wall = False

    if(pygame.mouse.get_pressed()[1] == True):
        mouseX, mouseY = tuple(int(mousePos/squareSize) for mousePos in pygame.mouse.get_pos())
        grid[mouseY][mouseX].start = True
        if start != None and start != grid[mouseY][mouseX]:
            start.start = False
        start = grid[mouseY][mouseX]

    if(pygame.mouse.get_pressed(5)[4] == True):
        mouseX, mouseY = tuple(int(mousePos/squareSize) for mousePos in pygame.mouse.get_pos())
        grid[mouseY][mouseX].target = True
        if target != None and target != grid[mouseY][mouseX]:
            target.target = False
        target = grid[mouseY][mouseX]

    redraw()
    pygame.display.update()
