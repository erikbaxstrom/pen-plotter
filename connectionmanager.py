from time import sleep

import network

from secrets import WIFI_SSID, WIFI_KEY


def connect_wifi():
    """Connect to a WiFi network.

        Uses WIFI_SSID and WIFI_KEY from secrets.py

        Returns:
            ip (str): The IP address acquired from the network.
    """

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print('using', WIFI_KEY, WIFI_SSID)
    wlan.connect(WIFI_SSID, WIFI_KEY)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(5)
    print(wlan.ifconfig())
    ip = wlan.ifconfig()[0]
    return ip