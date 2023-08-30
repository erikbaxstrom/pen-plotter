from connection_manager import connect_wifi
from microdot import Microdot, Response, send_file

from filemanager import FileManager
from printcontrol import PrintController


STEPS_PER_MM = 2048 / 40  # 2048 steps per revolution. 40 mm per revolution
CANVAS_WIDTH = 812  # units: mm (measured as 31 31/32")
CANVAS_HEIGHT = 889  # units: mm (measured as 35")


app = Microdot()
Response.default_content_type = 'text/html'

@app.route('/')
def index(request):
    response = send_file('index.html')
    return response


@app.route('/api/v1/upload', methods=['POST'])
def fileUpload(request):
    # print('Content-Range, Disposition', request.headers['Content-Range'], request.headers['Content-Disposition'])
    file_manager.add_to_print_file(request.body)
    blah = request.body
    return 'Success!', 200

@app.route('/api/v1/print')
def startPrint(request):
    print('print route called')
    file_manager.start_print()
    return 'Success!', 200

@app.route('/api/v1/nudge')
def nudge(request):
    # print(request.args.getlist('motor')[0])
    print_controller.nudge(side=request.args.getlist('motor')[0], mm=request.args.getlist('mm')[0])
    return 'woot', 200

@app.route('/api/v1/go-home')
def go_home(request):
    print_controller.go_to_home()
    return 'woohoo', 200

@app.route('/api/v1/motors-active')
def deactivate_motors(request):
    print('req arg', request.args.getlist('active')[0], bool(request.args.getlist('active')[0]))
    if request.args.getlist('active')[0] == "false":
        print_controller.deactivate_motors()
    return 'woohoo', 200


try:
    print_controller = PrintController(CANVAS_WIDTH, CANVAS_HEIGHT, STEPS_PER_MM)
    file_manager = FileManager(print_controller)
    print('running')
    ip = connect_wifi()
    app.run(host=ip, port=80, debug=True)
except KeyboardInterrupt:
    print('broke')
    # machine.reset()
