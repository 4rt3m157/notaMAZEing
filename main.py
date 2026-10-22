import framebuf

from lib.esieatoy import *
from lib.labyrinthe import *
from lib.network import *

toy = EsieaToy()

brint_buf = bytearray(SCREEN_W * SCREEN_H // 8)  # 1 oct / pxl
laby_fb = framebuf.FrameBuffer(brint_buf, SCREEN_W, SCREEN_H, framebuf.MONO_VLSB)

joueur_buf = bytearray(9)  # nb pxl joueur
joueur_fb = framebuf.FrameBuffer(joueur_buf, JOUEUR, JOUEUR, framebuf.MONO_VLSB)
joueur_fb.fill(1)


def pos(k):
    # à quel pixel commencer à dessiner en x ou y (cf
    return (k // 2) * (CORIDOR + WALL) + (CORIDOR if k % 2 else 0)


def load_maze(buffer_image):
    buffer_image.fill(0)
    for i in range(LINES):
        for j in range(COLUMN):
            # Les Cases (=0)
            # Toutes sont sur ligne & colonne paires
            if labrinthe[i][j] == 1:
                # Wall (=1)
                # pair en ligne et impair en colonne, c'est un | 1px/5
                # impair en ligne et pair en colonne, c'est un - 5px/1
                # impair en ligne et impair en colonne, c'est forcément une intesection invincible, donc soir entre 2 Wall de 5 donc un trou de 1 px. Cf. mon carnet p41 si vous voulez voir un schema moche
                x, y = pos(j) + 5, pos(i) + 10  # adapation de l'affichage (au px prés !(?))
                if i % 2 == 1 and j % 2 == 0:
                    buffer_image.line(x, y, x + CORIDOR - 1, y, 1)
                elif i % 2 == 0 and j % 2 == 1:
                    buffer_image.line(x, y, x, y + CORIDOR - 1, 1)
                else:  # 1 px
                    buffer_image.line(x, y, x, y, 1)
    buffer_image.rect(4, 10, 121, 55, 1)
    buffer_image.text(f"J1 {seed}", 0, 0)
    buffer_image.line(SCREEN_W, SCREEN_H - 1, SCREEN_W - 10, SCREEN_H - 1, 0)


config = lire_config()
sta = connection(config["wifi_ssid"], config["wifi_password"])

## TODO SOCKET
## collision (mais bon, en vrais c'est trop hardcore faut enlever les collisions

load_maze(laby_fb)

# if a + b pressed, mode light
toy.screen.invert(0)
xPlayer, yPlayer = 6, 11
while True:
    xPlayer += int(toy.accel_x() * SPEED)
    yPlayer -= int(toy.accel_y() * SPEED)
    if xPlayer < -JOUEUR:
        xPlayer = SCREEN_W
    if xPlayer > SCREEN_W:
        xPlayer = -JOUEUR
    if yPlayer < -JOUEUR:
        yPlayer = SCREEN_H
    if yPlayer > SCREEN_H:
        yPlayer = -JOUEUR
    toy.blit(laby_fb, 0, 0)
    toy.blit(joueur_fb, xPlayer, yPlayer)

    toy.show()
