import network
import socket
from secrets import WIFI_SSID, WIFI_KEY
from time import sleep


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # print(wlan.scan())
    print('using', WIFI_KEY, WIFI_SSID)
    wlan.connect(WIFI_SSID, WIFI_KEY)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(5)
    print(wlan.ifconfig())
    ip = wlan.ifconfig()[0]
    return ip
