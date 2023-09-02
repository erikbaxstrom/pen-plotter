from machine import Pin
from rp2 import StateMachine

from filemanager import FileManager
from motorcontrol import MotorController
from piostep import pio_step
from printcontrol import PrintController



STEPS_PER_MM = 2048 / 40  # 2048 steps per revolution. 40 mm per revolution
CANVAS_WIDTH = 812  # units: mm (measured as 31 31/32")
CANVAS_HEIGHT = 889  # units: mm (measured as 35")

LEFT_SM_BASE_PIN = 6
RIGHT_SM_BASE_PIN = 2
LEFT_SM_NUMBER = 0
RIGHT_SM_NUMBER = 1
LEFT_MOTOR_DIRECTION = 1
RIGHT_MOTOR_DIRECTION = -1
LEFT_MOTOR_HOME_POSITION = RIGHT_MOTOR_HOME_POSITION = 50038   # center-bottom position is length * steps/mm. 

    # file_manager.add_to_print_file(request.body)

    # file_manager.start_print()


    # print_controller.go_to_home()

    # print('req arg', request.args.getlist('active')[0], bool(request.args.getlist('active')[0]))
    # if request.args.getlist('active')[0] == "false":
    #     print_controller.deactivate_motors()


left_sm = StateMachine(LEFT_SM_NUMBER, pio_step, freq=10000, set_base=Pin(LEFT_SM_BASE_PIN), out_base=Pin(LEFT_SM_BASE_PIN))
right_sm = StateMachine(RIGHT_SM_NUMBER, pio_step, freq=10000, set_base=Pin(RIGHT_SM_BASE_PIN), out_base=Pin(RIGHT_SM_BASE_PIN))

left_motor = MotorController(LEFT_MOTOR_DIRECTION, LEFT_MOTOR_HOME_POSITION, left_sm)
right_motor = MotorController(RIGHT_MOTOR_DIRECTION, RIGHT_MOTOR_HOME_POSITION, right_sm)

print_controller = PrintController(CANVAS_WIDTH, CANVAS_HEIGHT, STEPS_PER_MM, left_motor, right_motor)
file_manager = FileManager(print_controller)

try:
    print('tests start here')
    # print_controller.nudge(side=request.args.getlist('motor')[0], mm=request.args.getlist('mm')[0])
    print_controller.nudge(side='left', mm=20)
    print_controller.nudge(side='right', mm=20)

except:
    print('broke')
