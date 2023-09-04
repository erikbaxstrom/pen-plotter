from machine import Pin
from microdot import Microdot, Response, send_file
from rp2 import StateMachine
from time import sleep

from connectionmanager import connect_wifi
from filemanager import FileManager
from motorcontrol import MotorController
from piostep import pio_step
from printcontrol import PrintController, PrinterGeometry



STEPS_PER_MM = 51.2  # 2048 steps per revolution. 40 mm per revolution
CANVAS_WIDTH = 812  # units: mm (measured as 31 31/32")
CANVAS_HEIGHT = 889  # units: mm (measured as 35")

LEFT_SM_BASE_PIN = 6
RIGHT_SM_BASE_PIN = 2
LEFT_SM_NUMBER = 0
RIGHT_SM_NUMBER = 1
LEFT_MOTOR_DIRECTION = 1
RIGHT_MOTOR_DIRECTION = -1
LEFT_MOTOR_HOME_POSITION = RIGHT_MOTOR_HOME_POSITION = 50038   # center-bottom position is length * steps/mm. 


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
    side = request.args.getlist('motor')[0]
    mm = float(request.args.getlist('mm')[0])
    print_controller.nudge(side, mm)
    return 'woot', 200

@app.route('/api/v1/go-home')
def go_home(request):
    print_controller.go_to_home()
    return 'woohoo', 200

@app.route('/api/v1/motors-active')
def deactivate_motors(request):
    print('req arg', request.args.getlist('active')[0], bool(request.args.getlist('active')[0]))
    if request.args.getlist('active')[0] == "false":
        print_controller.hard_stop_motors()
    return 'woohoo', 200


left_sm = StateMachine(LEFT_SM_NUMBER, pio_step, freq=10000, set_base=Pin(LEFT_SM_BASE_PIN), out_base=Pin(LEFT_SM_BASE_PIN))
right_sm = StateMachine(RIGHT_SM_NUMBER, pio_step, freq=10000, set_base=Pin(RIGHT_SM_BASE_PIN), out_base=Pin(RIGHT_SM_BASE_PIN))

left_motor = MotorController(LEFT_MOTOR_DIRECTION, LEFT_MOTOR_HOME_POSITION, left_sm)
right_motor = MotorController(RIGHT_MOTOR_DIRECTION, RIGHT_MOTOR_HOME_POSITION, right_sm)

printer_geometry = PrinterGeometry(CANVAS_WIDTH, CANVAS_HEIGHT, STEPS_PER_MM)
print_controller = PrintController(left_motor, right_motor, printer_geometry)
file_manager = FileManager(print_controller)

try:

    print('running')
    ip = connect_wifi()
    app.run(host=ip, port=80, debug=True)
except KeyboardInterrupt:
    print('broke')
    # machine.reset()
