import random as rand
import time

from lib.esieatoy import EsieaToy, SCREEN_W, SCREEN_H

toy = EsieaToy()
# taille laby
COLUMN = 40  # nevermind, j'étais avec un tableau, pas des murs. c'est le nombre de colonnes a mon tableau, pas au maze
LINES = 18  # pareil mais pour les lignes

CORIDOR = 5  # taille du CORIDOR
WALL = 1  # taille du mur

JOUEUR = 3  # taille du joueur
SPEED = 4 # VITESSSSS du gyro
global seed

def init_seed():
    seed = rand.randint(0,10000)
    rand.seed(seed)
    return seed



def pos(k):
    # à quel pixel commencer à dessiner en x ou y (cf
    return (k // 2) * (CORIDOR + WALL) + (CORIDOR if k % 2 else 0)


def draw_maze():
    toy.clear()
    for i in range(LINES):
        for j in range(COLUMN):
            # Les Cases (=0)
            # Toutes sont sur ligne & colonne paires
            if labrinthe[i][j] == 1:
                # Wall (=1)
                # pair en ligne et impair en colonne, c'est un | 1px/5
                # impair en ligne et pair en colonne, c'est un - 5px/1
                # impair en ligne et impair en colonne, c'est forcément une intesection invincible, donc soir entre 2 Wall de 5 donc un trou de 1 px. Cf. mon carnet p41 si vous voulez voir un schema moche
                x, y = pos(j), pos(i)
                x += 5 # gesiton de l'affichage
                y += 10 #  précis hehe
                if i % 2 == 1 and j % 2 == 0:
                    toy.line(x, y, x + CORIDOR - 1, y, 1)
                elif i % 2 == 0 and j % 2 == 1:
                    toy.line(x, y, x, y + CORIDOR - 1, 1)
                else:  # 1 px
                    toy.line(x, y, x, y, 1)
    toy.rect(4, 10, 121, 55, 1)
    toy.text(f"J1 {seed}",0,0)
    toy.show()


# faire un tableau 2 dimensions. il faut que ses dimension soit impaire, on va les décider en regardant le sujet. longueur 13 hauteur 5
# les salle sont a 1line/2 et 1col/2
labrinthe = [[' ' if (i % 2 == 0 and j % 2 == 0) else 1 for j in range(COLUMN)] for i in range(LINES)]

seed = init_seed()
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
    return True  # plus rien de possible


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
        print("pile :", len(fildAriane), "position :", currentPos)  # debug
        fildAriane.pop()
        if fildAriane:
            currentPos = fildAriane[-1]

toy.clear()
toy.rect(0, 0, 128, 64, 1)
for i in range(LINES):
    for j in range(COLUMN):
        print(labrinthe[i][j], end='')
    print()
print()

for ligne in labrinthe:
    print(ligne)

toy.line(SCREEN_W, SCREEN_H - 1, SCREEN_W - 7, SCREEN_H - 1, 0)
toy.show()
draw_maze()
#if a + b pressed, mode light
toy.screen.invert(0)
time.sleep_ms(500)
