from connection_manager import connect_wifi, open_socket, serve

try:
    print('runing')
    ip = connect_wifi()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    print('broke')
    # machine.reset()