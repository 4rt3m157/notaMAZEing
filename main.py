import framebuf

from lib.esieatoy import *
from lib.labyrinthe import *
from lib.network import *

toy = EsieaToy()
thruttle = 0
penalite = 0
def pos(k):
    # à quel pixel commencer à dessiner (cf p40)
    # salle+Wall     #6                     #Wall ?
    return (k // 2) * (CORIDOR + WALL) + (CORIDOR if k % 2 else 0)


def draw_buff_laby(buffer_image):
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
    buffer_image.text(f"{config['name']} {seed}", 0, 0)
    buffer_image.rect(119, 60, 121, 64, 1, True)


brint_buf = bytearray(SCREEN_W * SCREEN_H // 8)  # 1 oct / pxl
laby_fb = framebuf.FrameBuffer(brint_buf, SCREEN_W, SCREEN_H, framebuf.MONO_VLSB)

joueur_buf = bytearray(9)  # nb pxl joueur
joueur_fb = framebuf.FrameBuffer(joueur_buf, JOUEUR, JOUEUR, framebuf.MONO_VLSB)
joueur_fb.fill(1)

config = lire_config()
toy.led(config["color"][1],config["color"][2],config["color"][3])
sta = connection(config["wifi_ssid"], config["wifi_password"])
seedRcv = 0
print(seedRcv)
import socket
s = socket.socket()
conOk = False
while conOk != True:
    try:
        s.connect(("192.168.1.178", 5000))
        conOk = True
    except ConnectionError as e:
        print("ConnectionError")
        continue
s.send((json.dumps({"name": config["name"], "color": config["color"]}) + "\n").encode())
seedRcv = s.recv(100).decode('utf-8')  ## take seed, il faudrait aussi take la clé pour la comparer
seed = int(seedRcv)
print("seed :", seed)

seed = init_seed(seed)
labrinthe = dig_a_laby()
draw_buff_laby(laby_fb)

xPlayer, yPlayer = 6, 11

# if a + b pressed, mode light
toy.clear()
toy.text("A+B mode", 0, 0)
toy.text("light", 10, 0)
toy.show()
time.sleep(300)

if toy.button_pressed("A") and toy.button_pressed("B"):
    toy.screen.invert(1)
    xPlayer, yPlayer = 6, 11
temps = time.time()
while True:
    if toy.button_pressed("A"):
        s.close()
    tmpX = int(toy.accel_x() * SPEED)
    tmpY = int(toy.accel_y() * SPEED)
    xPlayer += tmpX
    yPlayer -= tmpY
    if (laby_fb.pixel(xPlayer + 1,
                      yPlayer + 1) == 0):  # je check avec le milieu du joueur, parce que 2px de marge de manoeuvre c'est vraiment sadique comme jeux...
        if ((xPlayer > 119) and (60 > yPlayer)):
            toy.clear()
            toy.text("WINNEUUUR", 0, 0)
            s.send(b"WIN\n")
            toy.show()
            break
    else:  ## LE MUUUUR
        xPlayer -= tmpX
        yPlayer += tmpY
        toy.beep(300, 30)
        penalite += 1
        
    s.send(f"{xPlayer} {yPlayer}\n".encode())
    toy.blit(laby_fb, 0, 0)
    toy.blit(joueur_fb, xPlayer, yPlayer)
    thruttle += 1
    toy.text(str(temps), 800, 0)
    if thruttle > 10:
        temps = time.time() - temps
        thruttle = 0
    toy.show()
