import network
import socket
from secrets import WIFI_SSID, WIFI_KEY
from time import sleep
from print_interface import run_stepper



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

def handle_request(request):
    try:
        split = request.split()
        path = split[1]
    except IndexError:
        return 'error'
    if path == '/runmotor?':
        run_stepper()



def serve(connection):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request.split())
        handle_request(request)
        html = webpage()
        client.send(html)
        client.close()