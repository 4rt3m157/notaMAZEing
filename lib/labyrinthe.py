import random as rand

from lib.config import *

global seed


def init_seed():
    seed = rand.randint(0, 10000)
    rand.seed(seed)
    return seed


labrinthe = [[0 if (i % 2 == 0 and j % 2 == 0) else 1 for j in range(COLUMN)] for i in range(LINES)]

seed = init_seed()
#  Haut   bas  droite  gauche
allWay = [(0, 2), (0, -2), (2, 0), (-2, 0)]
visited = [[0, 0]]
fildAriane = [[0, 0]]
currentPos = [0, 0]
xRef, yRef = 0, 0
x, y = 0, 0


def fitMaze(ligne, col):
    return 0 <= ligne < LINES and 0 <= col < COLUMN


def check_cul_de_sac():
    for xVecteur, yVecteur in allWay:
        voisin = [currentPos[0] + xVecteur, currentPos[1] + yVecteur]
        if fitMaze(voisin[0], voisin[1]) and voisin not in visited:
            return False  # y'a encore un chemin possible
    return True  # plus rien de possible


while fildAriane:
    xRef, yRef = rand.choice(allWay)
    x, y = currentPos[0] + xRef, currentPos[1] + yRef

    if fitMaze(x, y) and [x, y] not in visited:
        xWall, yWall = currentPos[0] + xRef // 2, currentPos[1] + yRef // 2
        labrinthe[xWall][yWall] = 0  # casse le mur
        currentPos = [x, y]  # se déplace de 2 case, derrière le mur
        visited.append(currentPos)
        fildAriane.append(currentPos)  # ajoute la salle au fil d'ariane

    elif check_cul_de_sac():
        fildAriane.pop()
        if fildAriane:
            currentPos = fildAriane[-1]
