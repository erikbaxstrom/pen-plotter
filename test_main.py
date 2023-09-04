from machine import Pin
from rp2 import StateMachine
from time import sleep

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


left_sm = StateMachine(LEFT_SM_NUMBER, pio_step, freq=10000, set_base=Pin(LEFT_SM_BASE_PIN), out_base=Pin(LEFT_SM_BASE_PIN))
right_sm = StateMachine(RIGHT_SM_NUMBER, pio_step, freq=10000, set_base=Pin(RIGHT_SM_BASE_PIN), out_base=Pin(RIGHT_SM_BASE_PIN))

left_motor = MotorController(LEFT_MOTOR_DIRECTION, LEFT_MOTOR_HOME_POSITION, left_sm)
right_motor = MotorController(RIGHT_MOTOR_DIRECTION, RIGHT_MOTOR_HOME_POSITION, right_sm)

printer_geometry = PrinterGeometry(CANVAS_WIDTH, CANVAS_HEIGHT, STEPS_PER_MM)

print_controller = PrintController(left_motor, right_motor, printer_geometry)
file_manager = FileManager(print_controller)


try:
    print('----   Start of Tests   ----\n')


    print('\n--  File Manager Add File  --')
    test_print_file_string = """
; paint
G1 F2300.0 X350 Y0 Z-3.3
; paint
G1 F2300.0 X350 Y50 Z-3.3
; paint
G1 F2300.0 X400 Y50 Z-3.3
; paint
G1 F2300.0 X400 Y0 Z-3.3
; paint
G1 F2300.0 X350 Y0 Z-3.3
;
;End of Gcode
"""
    file_manager.add_to_print_file(test_print_file_string.encode('utf-8'))
    assert file_manager.print_string == test_print_file_string, f"failed assert file_manager.print_string == test_print_file_string"
    print('success!')

    
    print('\n--  File Manager Start Print  --')
    file_manager.start_print()
    print('success!')



    print('\n--  Print Controller Go Home  --')
    print_controller.go_to_home()
    print('success!')


    print('\n--  Print Controller Nudge Route --')
    print_controller.nudge(side='left', mm=-20)
    print_controller.nudge(side='right', mm=-30)
    sleep(5)
    print_controller.go_to_home()
    sleep(5)
    print('success!')

    print('\n--  Print Controller Deactivate Motors  --')
    print_controller.deactivate_motors()
    print('success!')

except:
    print('\n-------   broke   -------\n')
    raise


