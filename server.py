import json
import select
import socket
import time
import pygame
from lib.labyrinthe import *

srv = socket.socket()
sockets = {}
conns = {}
update = {}
noms = {}
couleurs = {}
nbJoueur = 2
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", 5000))
srv.listen(nbJoueur)
print("enz attente...")
surv = select.poll()

for i in range(nbJoueur):
    conn, addr = srv.accept()
    fd = conn.fileno()
    infos = json.loads(conn.recv(200).decode('utf-8'))
    sockets[fd] = ""
    conns[fd] = conn
    update[fd] = (6, 11)
    noms[fd] = infos["name"]
    couleurs[fd] = tuple(c * 255 for c in infos["color"])
    surv.register(conn, select.POLLIN)
    print("connecté :", addr, noms[fd])
    conn.send(b"12341\n")

SCREEN_W, SCREEN_H = 128, 64
JOUEUR = 3
SCALE = 6
BLANC = (255, 255, 255)

seed = init_seed(12341)
labrinthe = dig_a_laby()


def pos(k):
    # à quel pixel commencer à dessiner (cf p40)
    # salle+Wall     #6                     #Wall ?
    return (k // 2) * (CORIDOR + WALL) + (CORIDOR if k % 2 else 0)


def draw_buff_laby(buffer_image):
    buffer_image.fill((0, 0, 0))
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
                    pygame.draw.line(buffer_image, BLANC, (x, y), (x + CORIDOR - 1, y))
                elif i % 2 == 0 and j % 2 == 1:
                    pygame.draw.line(buffer_image, BLANC, (x, y), (x, y + CORIDOR - 1))
                else:  # 1 px
                    buffer_image.set_at((x, y), BLANC)
    pygame.draw.rect(buffer_image, BLANC, (4, 10, 121, 55), 1)
    pygame.draw.rect(buffer_image, BLANC, (119, 60, 3, 5))


pygame.init()
fenetre = pygame.display.set_mode((SCREEN_W * SCALE, SCREEN_H * SCALE))
pygame.display.set_caption(" vs ".join(noms.values()))
laby_fb = pygame.Surface((SCREEN_W, SCREEN_H))
draw_buff_laby(laby_fb)

joueur_fb = pygame.Surface((JOUEUR, JOUEUR))  # nb pxl joueur
police = pygame.font.Font(None, 30)

temps = time.time()
gameing = True
while gameing:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            gameing = False

    listEv = surv.poll(0)
    if listEv:
        for entry in listEv:
            fd = entry[0]
            data = conns[fd].recv(100).decode('utf-8')
            if data != "":
                sockets[fd] += data
                if sockets[fd].find('\n') == -1:
                    continue
                else:
                    messages = sockets[fd].split('\n')
                    sockets[fd] = messages.pop(-1)
                    for message in messages:
                        if message == "WIN":
                            print(noms[fd], "a gagné en", round(time.time() - temps, 2), "s")
                            gameing = False
                        else:
                            posX, posY = message.split(" ")
                            update[fd] = (int(posX), int(posY))
            else:
                gameing = False

    frame = laby_fb.copy()
    for fd in update:
        joueur_fb.fill(couleurs[fd])
        frame.blit(joueur_fb, update[fd])
    fenetre.blit(pygame.transform.scale(frame, fenetre.get_size()), (0, 0))
    fenetre.blit(police.render(f"{time.time() - temps:.1f}", True, BLANC), (5, 5))
    pygame.display.flip()

pygame.quit()