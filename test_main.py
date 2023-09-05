from machine import Pin
from rp2 import StateMachine
from time import sleep

from filemanager import FileManager
from motorcontrol import MotorController
from piostep import pio_step
from printcontrol import PrintController, PrinterGeometry



STEPS_PER_MM = 51.2  # 2048 steps per revolution. 40 mm per revolution
PRINTER_TOTAL_WIDTH = 812  # units: mm. Total width, pulley center to pulley center. (measured as 31 31/32")
PRINTER_TOTAL_HEIGHT = 914  # units: mm. height from pulley center to home position (measured as 36")
CANVAS_WIDTH = 215  # 8.5" = 215 mm


LEFT_SM_BASE_PIN = 6
RIGHT_SM_BASE_PIN = 2
LEFT_SM_NUMBER = 0
RIGHT_SM_NUMBER = 1
LEFT_MOTOR_DIRECTION = 1
RIGHT_MOTOR_DIRECTION = -1



left_sm = StateMachine(LEFT_SM_NUMBER, pio_step, freq=10000, set_base=Pin(LEFT_SM_BASE_PIN), out_base=Pin(LEFT_SM_BASE_PIN))
right_sm = StateMachine(RIGHT_SM_NUMBER, pio_step, freq=10000, set_base=Pin(RIGHT_SM_BASE_PIN), out_base=Pin(RIGHT_SM_BASE_PIN))

left_motor = MotorController(LEFT_MOTOR_DIRECTION, left_sm)
right_motor = MotorController(RIGHT_MOTOR_DIRECTION, right_sm)

printer_geometry = PrinterGeometry(PRINTER_TOTAL_WIDTH, PRINTER_TOTAL_HEIGHT, CANVAS_WIDTH)
print_controller = PrintController(left_motor, right_motor, printer_geometry, STEPS_PER_MM)
file_manager = FileManager(print_controller)


try:
    print('----   Start of Tests   ----\n')


    print('\n--  File Manager Add File  --')
    test_print_file_string = """
; paint
G1 F2300.0 X0 Y0 Z-3.3
; paint
G1 F2300.0 X0 Y100 Z-3.3
; paint
G1 F2300.0 X100 Y100 Z-3.3
; paint
G1 F2300.0 X100 Y0 Z-3.3
; paint
G1 F2300.0 X50 Y0 Z-3.3
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
    print_controller.nudge(side='right', mm=-20)
    sleep(5)
    print_controller.go_to_home()
    sleep(5)
    print_controller.nudge(side='left', mm=20)
    print_controller.nudge(side='right', mm=20)
    sleep(5)
    print('success!')

    print('\n--  Print Controller Deactivate Motors  --')
    print_controller.deactivate_motors()
    print('success!')

except:
    print('\n-------   broke   -------\n')
    raise


