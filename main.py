# Example code to run the stepper motor from https://github.com/tinkertechtrove/pico-pi-playing/blob/main/pio-steppers/test_motor1.py

from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep
import sys
import network
import socket
from secrets import WIFI_SSID, WIFI_KEY


def connect():
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

def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection

def webpage():
    html = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pen Plotter</title>
    </head>
    <body>
        <form action="./runmotor">
            <input type="submit" value="Run Motor" />
        </form>
    </body>
    </html>"""
    return str(html)

def serve(connection):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request)
        html = webpage()
        client.send(html)
        client.close()

# @asm_pio(set_init=(PIO.OUT_LOW,) * 4)
# def prog():
#     wrap_target()
#     set(pins, 8) [31] # 8
#     nop() [31]
#     nop() [31]
#     nop() [31]
#     nop() [31]
#     nop() [31]
#     nop() [31]
#     set(pins, 4) [31] # 4
#     nop() [31]
#     nop() [31]
#     nop() [31]
#     nop() [31]
#     nop() [31]
#     nop() [31]
#     set(pins, 2) [31] # 2
#     nop() [31]
#     nop() [31]
#     nop() [31]
#     nop() [31]
#     nop() [31]
#     nop() [31]
#     set(pins, 1) [31] # 1
#     nop() [31]
#     nop() [31]
#     nop() [31]
#     nop() [31]
#     nop() [31]
#     nop() [31]
#     wrap()
    

# sm = StateMachine(0, prog, freq=100000, set_base=Pin(2))

# def run_stepper():
#     sm.active(1)
#     sleep(5)
#     sm.active(0)
#     sm.exec("set(pins,0)")

try:
    print('runing')
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    print('broke')
    # machine.reset()