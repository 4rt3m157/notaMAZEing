# esieatoy-micropython

Lib MicroPython pour la carte **esieatoy** (ESP32-C3).

Inclus dans les projets élèves comme submodule Git, monté à `lib/`.

## Contenu

| Fichier | Rôle |
|---------|------|
| `esieatoy.py` | Façade pédagogique : boutons, accéléro, LED RGB, buzzer, écran OLED. |
| `sh1106.py`   | Driver générique OLED 128×64 (I2C), sous-classe `framebuf.FrameBuffer`. |
| `lis3dh.py`   | Driver générique accéléromètre 3 axes LIS3DH (I2C, ±2g, 100 Hz). |

## Utilisation rapide

Sur la carte (après upload via `mpremote cp` ou submodule + `tools/upload.py` du projet parent) :

```python
from esieatoy import EsieaToy

toy = EsieaToy()
while True:
    if toy.button_pressed("A"):
        toy.beep(440, 100)
    toy.clear()
    toy.text("Hello", 0, 0)
    toy.show()
```

Voir le docstring en haut de `esieatoy.py` pour l'API complète.

## Comme submodule dans un projet

```bash
git submodule add https://gitlab.esiea.fr/esieatoy/esieatoy-micropython.git lib
git submodule update --init
```

## Cible matérielle

ESP32-C3 (esp32-c3-devkitm-1) — voir le projet parent pour les détails de câblage et le flash de MicroPython.
