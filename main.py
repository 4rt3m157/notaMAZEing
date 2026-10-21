import random as rand
import time

from lib.esieatoy import EsieaToy, SCREEN_W, SCREEN_H

toy = EsieaToy()
# taille laby
COLUMN = 21  # nombre de colonne, j'ai essayé de le changer... votre exemple est très bien.
LINES = 8  # pareil mais pour les lignes

CORIDOR = 5  # taille du CORIDOR
WALL = 1  # taille du mur

JOUEUR = 3  # taille du joueur
SPEED = 4
longueur_screen = SCREEN_W
hauteur_screen = SCREEN_H
toy.beep(100, 100)


def init_seed(seed=420):
    return rand.seed(seed)

# faire un tableau 2 dimensions. il faut que ses dimension soit impaire, on va les décider en regardant le sujet. longueur 13 hauteur 5
# les salle sont a 1line/2 et 1col/2
labrinthe = [[' ' if (i % 2 == 0 and j % 2 == 0) else 1 for j in range(COLUMN)] for i in range(LINES)]
init_seed()
#  Haut   bas  droite  gauche
allWay = [(0, 2), (0, -2), (2, 0), (-2, 0)]
possibleWay = [[]]
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
    return True # plus rien de possible


while fildAriane:
    xRef, yRef = rand.choice(allWay)
    x, y = currentPos[0] + xRef, currentPos[1] + yRef

    if fitMaze(x, y) and [x, y] not in visited:
        xWall, yWall = currentPos[0] + xRef // 2, currentPos[1] + yRef // 2
        labrinthe[xWall][yWall] = ' '  # casse le mur
        currentPos = [x, y]  # se déplace de 2 case, derrière le mur
        visited.append(currentPos)
        fildAriane.append(currentPos)  # ajoute la salle au fil d'ariane
    elif check_cul_de_sac():
        print("pile :", len(fildAriane), "position :", currentPos) # debug
        fildAriane.pop()
        if fildAriane:
            currentPos = fildAriane[-1]

toy.clear()
toy.rect(0, 0, 128, 64, 1)
for i in range(COLUMN):
    for j in range(LINES):
        toy.text(f"{labrinthe[j][i]}", 0 + i * 9, 10 + j * 8)
toy.line(SCREEN_W, SCREEN_H - 1, SCREEN_W - 7, SCREEN_H - 1, 0)
toy.text("AAAAA", SCREEN_H - 1, SCREEN_W - 7, 0)
toy.show()
time.sleep_ms(500)
