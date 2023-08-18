from connection_manager import connect_wifi
from microdot import Microdot, Response, send_file

app = Microdot()
Response.default_content_type = 'text/html'

@app.route('/')
def index(request):
    response = send_file('index.html')
    return response

@app.route('/upload', methods=['POST'])
def fileUpload(request):
    print('request object', request.body)
    return 'Success!', 200


try:
    print('runing')
    ip = connect_wifi()
    app.run(host=ip, port=80, debug=True)
#     connection = open_socket(ip)
#     serve(connection)
except KeyboardInterrupt:
    print('broke')
#     # machine.reset()



