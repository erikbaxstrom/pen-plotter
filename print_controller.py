from math import sqrt
from machine import Pin
from time import sleep
from motor_controller import motor_controller


LEFT_SM_BASE_PIN = 6
RIGHT_SM_BASE_PIN = 2
LEFT_SM_NUMBER = 0
RIGHT_SM_NUMBER = 1
LEFT_MOTOR_DIRECTION = 1
RIGHT_MOTOR_DIRECTION = -1
LEFT_MOTOR_HOME_POSITION = RIGHT_MOTOR_HOME_POSITION = 50038   # center-bottom position is length * steps/mm. 



class print_controller:


    def __init__(self, canvas_width, canvas_height, steps_per_mm):
        self.MAX_INTERP_DIST = 5  # units: mm
        self.width = canvas_width
        self.height = canvas_height
        self.current_x = 0.5 * canvas_width
        self.current_y = 0
        self.steps_per_mm = steps_per_mm

        self.left_motor = motor_controller(LEFT_SM_BASE_PIN, LEFT_SM_NUMBER, LEFT_MOTOR_DIRECTION, LEFT_MOTOR_HOME_POSITION)
        self.right_motor = motor_controller(RIGHT_SM_BASE_PIN, RIGHT_SM_NUMBER, RIGHT_MOTOR_DIRECTION, RIGHT_MOTOR_HOME_POSITION)
    

    def nudge(self, side, mm):
        print('nudging nudge', side, mm)
        steps = int(float(mm) * self.steps_per_mm)
        print('steps', steps)
        if side == 'left':
            self.left_motor.step(steps)
        if side == 'right':
            self.right_motor.step(steps)
        # set current position as home
        self.current_x = 0.5 * self.width
        self.current_y = 0
        self.left_motor.current_position = LEFT_MOTOR_HOME_POSITION
        self.right_motor.current_position = RIGHT_MOTOR_HOME_POSITION


    def go_to_home(self):
        self.move_to_coord(0.5 * self.width, 0)


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




# # # TEST CODE


# STEPS_PER_MM = 2048 / 40  # 2048 steps per revolution. 40 mm per revolution
# CANVAS_WIDTH = 812  # units: mm (measured as 31 31/32")
# CANVAS_HEIGHT = 889  # units: mm (measured as 35")

# center = CANVAS_WIDTH/2
# test_coords = [(center,0), (center + 100, 0), (center + 100, 200), (center - 100, 200), (center - 100, 0), (center, 0)]
# controller = print_controller(CANVAS_WIDTH, CANVAS_HEIGHT, STEPS_PER_MM)


# for coord in test_coords:
#     print("calling controller.move_to_coord()", coord)
#     controller.move_to_coord(coord[0], coord[1])

# controller.finish_print()
        

