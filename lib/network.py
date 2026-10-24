import json
import time

import network


def scan():
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    for net in sta.scan():
        print(repr(net[0].decode()), "canal", net[2], "signal", net[3])


def connection(ssid, mdp, timeout=10):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    sta.disconnect()
    time.sleep_ms(100)

    print("tentative conn  ", ssid)
    try:
        sta.connect(ssid, mdp)
    except OSError as e:  # reset
        sta.active(False)
        time.sleep_ms(300)
        sta.active(True)
        time.sleep_ms(300)
        sta.connect(ssid, mdp)

    debut = time.ticks_ms()
    while not sta.isconnected():
        if time.ticks_diff(time.ticks_ms(), debut) > timeout * 1000:
            print("timeout")
            sta.disconnect()
            return None
        time.sleep_ms(200)

    print("IP ", sta.ifconfig()[0])
    return sta
