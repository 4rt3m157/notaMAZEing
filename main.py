import random
import time


from lib.esieatoy import EsieaToy, SCREEN_W, SCREEN_H

def init_seed(seed = 42):
    return random.seed(seed)

toy = EsieaToy()
SIZE = 5
SPEED = 4
x = SCREEN_W
y = SCREEN_H
toy.beep(300, 100)
texts = ["Hello World", "Random Text", "Python Script"]
# faire un tableau 2 dimensions. il faut que ses dimension soit impaire, on va les décider en regardant le sujet. longueur 13 hauteur 5
# les salle sont a 1line/2 et 1col/2
labrinthe = [['#' if (i % 2 == 0 or j % 2 == 0) else 'O' for j in range(14)] for i in range(6)]

currentWay = [(0,0)]



init_seed()
while True:
    toy.clear()
    toy.rect(0,0,128,64,1)
    rand = random.choice(texts)
    for i in range(14):
        for j in range(6):
            toy.text(labrinthe[j][i], 0 + i*9, 0 + j*8)
    toy.line(SCREEN_W,SCREEN_H-1, SCREEN_W-7, SCREEN_H-1, 0)

    toy.show()

    time.sleep_ms(500)

