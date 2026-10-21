import time
import random

from lib.esieatoy import EsieaToy, SCREEN_W, SCREEN_H

toy = EsieaToy()

SIZE = 5
SPEED = 4
x = SCREEN_W // 2
y = SCREEN_H // 2
while True:
    if toy.button("LEFT"):
        x -= SPEED
    if toy.button("RIGHT"):
        x += SPEED
    if toy.button("UP"):
        y -= SPEED
    if toy.button("DOWN"):
        y += SPEED

    if x < -SIZE:
        x = SCREEN_W
    if x > SCREEN_W:
        x = -SIZE
    if y < -SIZE:
        y = SCREEN_H
    if y > SCREEN_H:
        y = -SIZE
    toy.clear()
    for dx in range(SIZE):
        for dy in range(SIZE):
            toy.pixel(int(x) + dx, int(y) + dy, 1)

    toy.show()
    time.sleep_ms(30)
