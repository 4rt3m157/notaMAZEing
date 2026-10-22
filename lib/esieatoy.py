import time
import framebuf  # un framebuffer est une liste de nombres binaires (0b)
                  # représentant une matrice de pixels (l'image à l'écran).
from machine import Pin, I2C, PWM

from sh1106 import SH1106_I2C
from lis3dh import LIS3DH

# Hardware mapping — mirrors esieatoy-os/src/kernel/Hardware.h
PIN_SDA = 3
PIN_SCL = 10
PIN_LED_R = 20
PIN_LED_G = 8
PIN_LED_B = 7
PIN_BUZZER = 21
BUTTON_PINS = {
    "A": 5,
    "B": 6,
    "UP": 0,
    "DOWN": 1,
    "LEFT": 2,
    "RIGHT": 4,
}

SCREEN_W = 128
SCREEN_H = 64


class EsieaToy:
    def __init__(self) -> None:
        """
        Initialise la carte esieatoy : bus I2C, écran, accéléromètre,
        boutons, LED RGB et buzzer. Calibre l'accéléromètre au repos.
        """
        # I2C bus shared by OLED + accelerometer
        self._i2c = I2C(0, sda=Pin(PIN_SDA), scl=Pin(PIN_SCL), freq=400_000)

        # Screen — expose framebuf-style methods directly on the toy object
        self.screen = SH1106_I2C(SCREEN_W, SCREEN_H, self._i2c)
        self.width = SCREEN_W
        self.height = SCREEN_H

        # Accelerometer (with simple zero-bias calibration so a flat table = 0)
        try:
            self._accel = LIS3DH(self._i2c)
            self._bias_x, self._bias_y = self._calibrate()
            self._accel_ok = True
        except OSError:
            self._accel = None
            self._accel_ok = False
            self._bias_x = 0.0
            self._bias_y = 0.0

        # Buttons (pull-down, active HIGH)
        self._btn_pins = {
            name: Pin(gpio, Pin.IN, Pin.PULL_DOWN)
            for name, gpio in BUTTON_PINS.items()
        }
        self._btn_prev = {name: False for name in BUTTON_PINS}

        # RGB LED — common-anode (active LOW): duty 0 = full bright, 65535 = off.
        self._led_r = PWM(Pin(PIN_LED_R), freq=1000, duty_u16=65535)
        self._led_g = PWM(Pin(PIN_LED_G), freq=1000, duty_u16=65535)
        self._led_b = PWM(Pin(PIN_LED_B), freq=1000, duty_u16=65535)

        # Buzzer (passive) on PWM
        self._buzzer_pin = Pin(PIN_BUZZER)
        self._buzzer = None  # lazy: PWM only when we actually beep

    # ---------- calibration ----------
    def _calibrate(self) -> tuple[float, float]:
        """
        Mesure le biais de repos de l'accéléromètre en moyennant 20
        lectures, afin qu'une table plate corresponde à une inclinaison nulle.
        Renvoie le tuple (biais_x, biais_y).
        """
        sx = 0.0
        sy = 0.0
        for _ in range(20):
            x, y, _z = self._accel.read_g()
            sx += x
            sy += y
            time.sleep_ms(10)
        return sx / 20.0, sy / 20.0

    # ---------- buttons ----------
    def button(self, name: str) -> bool:
        """
        Renvoie True si le bouton nommé est actuellement maintenu enfoncé.
        Noms valides : "A", "B", "UP", "DOWN", "LEFT", "RIGHT".
        """
        return bool(self._btn_pins[name].value())

    def button_pressed(self, name: str) -> bool:
        """
        Renvoie True uniquement sur la première image où le bouton
        vient d'être pressé (et pas tant qu'il reste tenu).
        """
        cur = bool(self._btn_pins[name].value())
        prev = self._btn_prev[name]
        self._btn_prev[name] = cur
        return cur and not prev

    # ---------- accelerometer ----------
    def accel_x(self) -> float:
        """
        Inclinaison gauche/droite, entre -1.0 <> +1.0. Négatif = penché à gauche.
        Renvoie 0.0 si l'accéléromètre est défectueux ou autre erreur.
        """
        if not self._accel_ok:
            return 0.0
        x, _y, _z = self._accel.read_g()
        v = x - self._bias_x
        return _clamp(v, -1.0, 1.0)

    def accel_y(self) -> float:
        """
        Inclinaison arrière/avant, entre -1.0 <> +1.0.
        Renvoie 0.0 si l'accéléromètre est déféctueux ou autre erreur.
        """
        if not self._accel_ok:
            return 0.0
        _x, y, _z = self._accel.read_g()
        v = y - self._bias_y
        return _clamp(v, -1.0, 1.0)

    # ---------- buzzer ----------
    def beep(self, freq: float, ms: int) -> None:
        """
        Émet un bip (bloquant) : un son de fréquence `freq` Hz pendant `ms`
        millisecondes. Le PWM du buzzer est créé à la première utilisation.
        """
        if self._buzzer is None:
            self._buzzer = PWM(self._buzzer_pin)
        self._buzzer.freq(int(freq))
        self._buzzer.duty_u16(32768)
        time.sleep_ms(int(ms))
        self._buzzer.duty_u16(0)

    def silence(self) -> None:
        """
        Coupe immédiatement le son du buzzer s'il était en train de jouer.
        """
        if self._buzzer is not None:
            self._buzzer.duty_u16(0)

    # ---------- LED ----------
    def led(self, r: float, g: float, b: float) -> None:
        """
        Règle la couleur de la LED RGB. `r`, `g`, `b` valent chacun de 0.0
        (éteint) à 1.0 (pleine intensité). La LED est à anode commune (active
        à l'état bas), d'où l'inversion du rapport cyclique.
        """
        self._led_r.duty_u16(int(65535 - _clamp(r, 0, 1) * 65535))
        self._led_g.duty_u16(int(65535 - _clamp(g, 0, 1) * 65535))
        self._led_b.duty_u16(int(65535 - _clamp(b, 0, 1) * 65535))

    def led_off(self) -> None:
        """
        Éteint complètement la LED RGB.
        """
        self.led(0, 0, 0)

    # ---------- screen passthrough ----------
    def clear(self) -> None:
        """
        Efface le tampon de l'écran (tout en noir).
        L'affichage n'est mis à jour qu'après un appel de show().
        """
        self.screen.fill(0)

    def show(self) -> None:
        """
        Envoie le contenu du tampon vers l'écran (refresh).
        """
        self.screen.show()

    def pixel(self, x: int, y: int, c: int = 1) -> None:
        """
        Allume (c=1) ou éteint (c=0) le pixel aux coordonnées (x, y).
        """
        self.screen.pixel(x, y, c)

    def line(self, x1: int, y1: int, x2: int, y2: int, c: int = 1) -> None:
        """
        Trace une ligne du point (x1, y1) au point (x2, y2).
        """
        self.screen.line(x1, y1, x2, y2, c)

    def rect(self, x: int, y: int, w: int, h: int, c: int = 1) -> None:
        """
        Dessine le contour d'un rectangle (coin (x, y), largeur w, hauteur h).
        """
        self.screen.rect(x, y, w, h, c)

    def fill_rect(self, x: int, y: int, w: int, h: int, c: int = 1) -> None:
        """
        Dessine un rectangle plein (coin (x, y), largeur w, hauteur h).
        """
        self.screen.fill_rect(x, y, w, h, c)

    def text(self, s: str, x: int, y: int, c: int = 1) -> None:
        """
        Affiche la chaîne `s` à partir des coordonnées (x, y).
        """
        self.screen.text(s, x, y, c)

    def blit(self, fb: framebuf.FrameBuffer, x: int, y: int, key: int = -1) -> None:
        """
        Copie un autre framebuffer `fb` sur l'écran à la position (x, y).
        `key` définit la couleur transparente (-1 = aucune).
        """
        self.screen.blit(fb, x, y, key)


def _clamp(v: float, lo: float, hi: float) -> float:
    """
    Borne la valeur `v` dans l'intervalle [lo, hi] et la renvoie.
    """
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v
