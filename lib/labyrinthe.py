import random as rand

from lib.config import *


def init_seed():
    seed = rand.randint(0, 10000)
    rand.seed(seed)
    return seed


#  Haut   bas  droite  gauche
allWay = [(0, 2), (0, -2), (2, 0), (-2, 0)]


def fit_maze(ligne, col):
    return 0 <= ligne < LINES and 0 <= col < COLUMN


def check_cul_de_sac(current, visited):
    for xVecteur, yVecteur in allWay:
        voisin = [current[0] + xVecteur, current[1] + yVecteur]
        if fit_maze(voisin[0], voisin[1]) and voisin not in visited:
            return False  # il reste un chemin possible
    return True  # plus rien de possible


def dig_a_laby():
    # 1 = mur, 0 = case/couloir ; les cases sont sur lignes & colonnes paires
    labrinthe = [[0 if (i % 2 == 0 and j % 2 == 0) else 1 for j in range(COLUMN)] for i in range(LINES)]
    visited = [[0, 0]]
    fildAriane = [[0, 0]]

    while fildAriane:
        currentPos = fildAriane[-1]

        if check_cul_de_sac(currentPos, visited):
            fildAriane.pop()  # retour arrière
            continue

        xRef, yRef = rand.choice(allWay)
        x, y = currentPos[0] + xRef, currentPos[1] + yRef

        if fit_maze(x, y) and [x, y] not in visited:
            xWall, yWall = currentPos[0] + xRef // 2, currentPos[1] + yRef // 2
            labrinthe[xWall][yWall] = 0  # casse le mur
            visited.append([x, y])
            fildAriane.append([x, y])

    return labrinthe  # plus pratique pour généré a la volé des labyrinthe. Pourquoi faire ca ? debug °-°
