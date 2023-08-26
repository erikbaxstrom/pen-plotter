from math import sqrt
from machine import Pin
from time import sleep
from motor_controller import motor_controller


LEFT_SM_BASE_PIN = 6
RIGHT_SM_BASE_PIN = 2
LEFT_SM_NUMBER = 0
RIGHT_SM_NUMBER = 1
LEFT_MOTOR_DIRECTION = -1
RIGHT_MOTOR_DIRECTION = 1


class print_controller:


    def __init__(self, canvas_width, canvas_height, steps_per_mm):
        self.MAX_INTERP_DIST = 5  # units: mm
        self.width = canvas_width
        self.height = canvas_height
        self.current_x = 0
        self.current_y = 0.5 * canvas_width
        self.steps_per_mm = steps_per_mm
        self.left_motor = motor_controller(LEFT_SM_BASE_PIN, LEFT_SM_NUMBER, LEFT_MOTOR_DIRECTION)
        self.right_motor = motor_controller(RIGHT_SM_BASE_PIN, RIGHT_SM_NUMBER, RIGHT_MOTOR_DIRECTION)
    

    def execute_gcode(self, code):
        gcodelets = code.split(' ')
        command = gcodelets[0]
        if command == 'G1':
            print('found a g1 code, will print now', code)
            x = gcodelets[2][1:]
            y = gcodelets[3][1:]
            print('converting strings', x, y)
            x = float(x)
            y = float(y)
            print('as floats', x, y)
            self.move_to_coord(x, y)
            return
        

    def move_to_coord(self, x, y):
        # interpolate
        interpolated_coordinates = [(x,y)]
        # iterate through interpolated points 
        for x, y in interpolated_coordinates:
            # convert interpolated coordinates (mm) to belt lengths (mm)
            l_length = sqrt((x**2 + (self.height - y)**2 ))
            r_length = sqrt(((self.width - x)**2 + (self.height - y)**2 ))
            # convert belt lengths (mm) to stepper positions (steps)
            l_step_pos = int(l_length * self.steps_per_mm)
            r_step_pos = int(r_length * self.steps_per_mm)
            print("interpolated coordinates (mm)", x, y,  "to belt lengths (mm)", l_length, r_length, "to stepper positions", l_step_pos, r_step_pos)
            # output stepper positions to the stepper motors
            self.left_motor.step_to(l_step_pos)
            self.right_motor.step_to(r_step_pos)

            while self.left_motor.is_busy or self.right_motor.is_busy:
                print('not ready: left, right', self.left_motor.is_busy, self.right_motor.is_busy)
                sleep(1)

        self.current_x = x
        self.current_y = y


    def finish_print(self):
        self.left_motor.deactivate()
        self.right_motor.deactivate()




# # TEST CODE


# STEPS_PER_MM = 2048 / 40  # 2048 steps per revolution. 40 mm per revolution
# CANVAS_WIDTH = 600  # units: mm
# CANVAS_HEIGHT = 600  # units: mm

# test_coords = [(300,0), (300,100), (200, 100), (200, 0), (300, 0)]
# controller = print_controller(CANVAS_WIDTH, CANVAS_HEIGHT, STEPS_PER_MM)


# for coord in test_coords:
#     print("calling controller.move_to_coord()", coord)
#     controller.move_to_coord(coord[0], coord[1])

# controller.finish_print()
        

