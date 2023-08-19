from connection_manager import connect_wifi
from microdot import Microdot, Response, send_file
from print_manager import print_manager
from print_controller import print_controller

app = Microdot()
Response.default_content_type = 'text/html'
print_controller = print_controller()
print_manager = print_manager(print_controller)

@app.route('/')
def index(request):
    response = send_file('index.html')
    return response

@app.route('/upload', methods=['POST'])
def fileUpload(request):
    # print('Content-Range, Disposition', request.headers['Content-Range'], request.headers['Content-Disposition'])
    print_manager.add_to_print_file(request.body)
    blah = request.body
    return 'Success!', 200


@app.route('/print')
def startPrint(request):
    print('print route called')
    print_manager.start_print()
    return 'Success!', 200

try:
    print('runing')
    ip = connect_wifi()
    app.run(host=ip, port=80, debug=True)
except KeyboardInterrupt:
    print('broke')
    # machine.reset()



