import random as rand
import time

from lib.esieatoy import EsieaToy, SCREEN_W, SCREEN_H

toy = EsieaToy()
#taille laby
COLUMN = 15
LINES = 6

SIZE = 5
SPEED = 4
longueur_screen = SCREEN_W
hauteur_screen = SCREEN_H
toy.beep(100, 100)

def init_seed(seed= 420):
    return rand.seed(seed)


# faire un tableau 2 dimensions. il faut que ses dimension soit impaire, on va les décider en regardant le sujet. longueur 13 hauteur 5
# les salle sont a 1line/2 et 1col/2
labrinthe = [[' ' if (i % 2 == 0 and j % 2 == 0) else 1 for j in range(14)] for i in range(6)]
init_seed()
#  Haut   bas  droite  gauche
allWay = [(0, 2), (0, -2), (2, 0), (-2, 0)]
possibleWay = [[]]
visited = [[0, 0]]
fildAriane = [[0, 0]]
currentPos = [0, 0]
xRef, yRef = 0, 0
x, y = 0, 0


def check_cul_de_sac():
    culdesac = 0
    for choice in allWay:
        arround = [currentPos[0] + choice[0], currentPos[1] + choice[1]]
        if arround not in visited and 0 <= arround[0] <= 4 and 0 <= arround[1] <= 12:  # si y'a un chemon possible
            return False
        else:
            culdesac += 1
    return True


while fildAriane:

    xRef, yRef = rand.choice(allWay)

    xWall, yWall = currentPos[0] + xRef // 2, currentPos[1] + yRef // 2
    if 0 <= currentPos[0] + xRef <= 4 and 0 <= currentPos[1] + yRef <= 12:  # -
        if [currentPos[0] + xRef, currentPos[1] + yRef] not in visited:
            currentPos = [currentPos[0] + xRef, currentPos[1] + yRef]  # x
            labrinthe[xWall][yWall] = ' '  ## casse le mur
              # se déplace de 2 case (derrière le mur en gros)
            visited.append(currentPos)  # ajoute la salle à la liste des salles visitées
            fildAriane.append(currentPos)
        else:
            if check_cul_de_sac():
                print("pile :", len(fildAriane), "position :", currentPos)
                fildAriane.pop()
                if fildAriane:
                    currentPos = fildAriane[-1]

toy.clear()
toy.rect(0, 0, 128, 64, 1)
for i in range(14):
    for j in range(6):

        toy.text(f"{labrinthe[j][i]}", 0 + i * 9, 10 + j * 8)
toy.line(SCREEN_W, SCREEN_H - 1, SCREEN_W - 7, SCREEN_H - 1, 0)
toy.text("AAAAA", SCREEN_H - 1, SCREEN_W - 7, 0)
toy.show()

time.sleep_ms(500)
