import pygame
import random
import math
import sys
import time

error = pygame.init()
if error[1] > 0:
    print("Erro ao iniciar o PyGame!")
    format(error[1])
    sys.exit(-1)
else:
    print("Inicialializado com Sucesso!")


class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.previous = None
        self.wall = False

        if random.uniform(0, 1) <= 0.5:
            self.wall =  True

    def addNeighbors(self, grid):
        x = self.x
        y = self.y

        if x > 0:
            self.neighbors.append(grid[x - 1][y])
        if x < COLS - 1:
            self.neighbors.append(grid[x + 1][y])
        if y > 0:
            self.neighbors.append(grid[x][y - 1])
        if y < ROWS - 1:
            self.neighbors.append(grid[x][y + 1])
        if x > 0 and y > 0:
            self.neighbors.append(grid[x - 1][y - 1])
        if x > 0 and y < ROWS - 1:
            self.neighbors.append(grid[x - 1][y + 1])
        if x < COLS - 1 and y > 0:
            self.neighbors.append(grid[x + 1][y - 1])
        if x < COLS - 1 and y < ROWS - 1:
            self.neighbors.append(grid[x + 1][y + 1])


    def show(self, color):
        if self.wall:
            color = (0, 0, 0)
        pygame.draw.rect(window, color, (self.x * W, self.y * H, W - 1, H - 1))


COLS = 75
ROWS = 75

WIDTH = 600
HEIGHT = 600

W = WIDTH / COLS
H = HEIGHT / ROWS

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def main():

    grid = [[Spot(x, y) for y in range(ROWS)] for x in range(COLS)]
    for i in range(COLS):
        for f in range(ROWS):
            grid[i][f].addNeighbors(grid)

    path = []
    openSet = []
    closedSet = []

    start = grid[0][0]
    start.wall = False
    end = grid[COLS - 1][ROWS - 1]
    end.wall = False

    openSet.append(start)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
    
        window.fill((0, 0, 0))

        draw(grid, openSet, closedSet, end, path)
        
        pygame.display.flip()  
        clock.tick(30)

def draw(grid, openSet, closedSet, end, path):

    if len(openSet) > 0:
        winner = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[winner].f:
                winner = i

        current = openSet[winner]

        if current == end:
            print("Done!")
            openSet = []
            openSet.append(current)

        openSet.remove(current)
        closedSet.append(current)

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            if neighbor not in closedSet and not neighbor.wall:
                tempG = current.g + 1
                
                newPath = False
                if neighbor in openSet:
                    if tempG < neighbor.g:
                        newPath = True
                        neighbor.g = tempG
                else:
                    newPath = True
                    neighbor.g = tempG
                    openSet.append(neighbor)
                    
                if newPath:
                    neighbor.h = heuristic(neighbor, end)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.previous = current

    else:
        print("END")
        main()
        #pygame.quit()


    for i in grid:
        for f in i:
            f.show((255, 255, 255))

    for i in openSet:
        i.show((0, 255, 0))

    for i in closedSet:
        i.show((255, 0, 0))

    path = []
    temp = current
    path.append(temp)
    while temp.previous != None:
        path.append(temp.previous)
        temp = temp.previous

    for i in path:
        i.show((255, 0, 255))
    print(len(path))

def heuristic(neighbor, end):
    
    n = [neighbor.x, neighbor.y]
    e = [end.x, end.y]
    return math.dist(n, e)
    #return abs(neighbor.x - end.x) + abs(neighbor.y - end.y)

main()