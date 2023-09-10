from math import sqrt, ceil
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
        self.g0_to_coord(self.geometry.home_x, self.geometry.home_y)
        while self.left_motor.is_busy or self.right_motor.is_busy:
            sleep(0)
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
            self.g1_to_coord(x, y)
            return
        if command == 'G0':
            print('G0 to', code)
        
    def g1_to_coord(self, x, y):
        self.move_to_coord(x, y, 1)
    
    def g0_to_coord(self, x, y):
        self.move_to_coord(x, y, 0)


    def move_to_coord(self, x, y, interp_dist):
        """Move the print head to the specified x, y coordinate."""
        interpolated_coordinates = self.interpolate(x,y, interp_dist)
        for (x, y) in interpolated_coordinates:
            l, r = self.geometry.xy_to_lr(x, y)
            l_step_pos = self.length_to_steps(l)
            r_step_pos = self.length_to_steps(r)
            print("converted coordinates (mm)", x, y,  "to belt lengths (mm)", l, r, "to stepper positions", l_step_pos, r_step_pos)
            self.left_motor.step_to(l_step_pos)
            self.right_motor.step_to(r_step_pos)
            while self.left_motor.is_busy or self.right_motor.is_busy:
                sleep(0)
        self.current_x = x
        self.current_y = y

    def interpolate(self, x, y, max_distance):
        if max_distance == 0:  #don't interpolate
            return [(x, y)]
        start_x = self.current_x
        start_y = self.current_y
        end_x = x
        end_y = y
        interp_steps = []
        distance = sqrt( (end_x - start_x)**2 + (end_y - start_y)**2)
        interp_step_count = int(ceil(distance / max_distance))
        for i in range(1, (interp_step_count + 1)):
            incr_x = start_x + i * (end_x - start_x) / interp_step_count
            incr_y = start_y + i * (end_y - start_y) / interp_step_count
            interp_steps.append((round(incr_x, 2), round(incr_y, 2)))
        print('interp steps', interp_steps)
        return interp_steps

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
        # print('home_x', self.home_x, 'home_y', self.home_y, 'homelength', self.home_length)

    def xy_to_lr(self, x, y):
        x_tot = x + self.left_margin
        depth = self.total_height - y
        l_length = sqrt( depth**2 + x_tot**2 )
        r_length = sqrt( depth**2 + (self.total_width - x_tot)**2 )
        # print('xy_to_lr:', 'x', x, 'y', y,  'xtot', x_tot, 'depth', depth, 'l_length', l_length, 'r_length', r_length)
        return l_length, r_length

