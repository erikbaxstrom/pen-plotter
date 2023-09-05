from math import sqrt
from time import sleep


class PrintController:
    """Controls the print head position and prints gcode strings.

    Args:
        canvas_width (float): Width of the canvas in mm.
        canvas_height (float): Height of the canvas in mm.
        steps_per_mm (float): Number of motor steps per millimeter of travel.

    Attributes:
        home_coords (tuple)(float, float): Coordinates for the home position.
        current_x (float): Current x-coordinate.
        current_y (float): Current y-coordinate.
        steps_per_mm (float): Number of motor steps per millimeter of travel.
    """

    def __init__(self, left_motor, right_motor, printer_geometry, steps_per_mm):
        self.geometry = printer_geometry
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.steps_per_mm = steps_per_mm
        self.set_new_home()
    


    def nudge(self, side, mm):
        """Nudge the print head position by changing the left or right belt lengths (mm) """
        steps = self.length_to_steps(mm)
        print(f"nudge {side} {mm} mm, {steps} steps")
        if side == 'left':
            self.left_motor.step(steps)
        if side == 'right':
            self.right_motor.step(steps)
        self.set_new_home()


    def set_new_home(self):
        """Set the current position as the home position for the print head."""
        self.current_x = self.geometry.home_x
        self.current_y = self.geometry.home_y
        self.left_motor.current_position = self.length_to_steps(self.geometry.home_length)
        self.right_motor.current_position = self.length_to_steps(self.geometry.home_length)

    def go_to_home(self):
        """Move print head to home position."""
        self.move_to_coord(self.geometry.home_x, self.geometry.home_y)
        while self.left_motor.is_busy or self.right_motor.is_busy:
            sleep(1)
        self.deactivate_motors()
        

    def print_gcode(self, string): 
        """Print a string of G-code commands separated by newline characters. """
        
        for code in string.split('\n'):
            self.execute_gcode(code)
        self.deactivate_motors()


    def execute_gcode(self, code):
        """Execute a single G-code command."""

        gcodelets = code.split(' ')
        command = gcodelets[0]
        if command == ';':
            return
        if command == 'G1':
            print('Printing', code)
            x = gcodelets[2][1:]
            y = gcodelets[3][1:]
            x = float(x)
            y = float(y)
            self.move_to_coord(x, y)
            return
        

    def move_to_coord(self, x, y):
        """Move the print head to the specified x, y coordinate."""

        # TODO: interpolate
        interpolated_coordinates = [(x,y)]
        for x, y in interpolated_coordinates:
            l, r = self.geometry.xy_to_lr(x, y)
            l_step_pos = self.length_to_steps(l)
            r_step_pos = self.length_to_steps(r)
            print("converted coordinates (mm)", x, y,  "to belt lengths (mm)", l, r, "to stepper positions", l_step_pos, r_step_pos)
            self.left_motor.step_to(l_step_pos)
            self.right_motor.step_to(r_step_pos)
            while self.left_motor.is_busy or self.right_motor.is_busy:
                sleep(0.1)
        self.current_x = x
        self.current_y = y

    def deactivate_motors(self):
        """Deactivate both left and right motors."""
        self.left_motor.enabled = False
        self.right_motor.enabled = False

    def hard_stop_motors(self):
        self.deactivate_motors()
        self.left_motor.reset()
        self.right_motor.reset()
        

    def length_to_steps(self, length):
        return int(length * self.steps_per_mm)

class PrinterGeometry:
    """Geometry for the printer"""

    def __init__(self, total_width, total_height, canvas_width):
        self.total_width = total_width
        self.total_height = total_height
        self.canvas_width = canvas_width
        self.home_x = 0.5 * canvas_width
        self.home_y = 0
        self.home_length = sqrt((self.total_width/2)**2 + self.total_height**2)
        self.left_margin = 0.5 * (self.total_width - self.canvas_width)
        print('home_x', self.home_x, 'home_y', self.home_y, 'homelength', self.home_length)

    def xy_to_lr(self, x, y):
        x_tot = x + self.left_margin
        depth = self.total_height - y
        l_length = sqrt( depth**2 + x_tot**2 )
        r_length = sqrt( depth**2 + (self.total_width - x_tot)**2 )
        return l_length, r_length
    

    

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
