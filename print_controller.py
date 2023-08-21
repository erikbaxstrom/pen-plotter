from math import sqrt
from machine import Pin
from time import sleep
from motor_controller import motor_controller

steps_per_mm = 1

class print_controller:

    def __init__(self):
        self.height = 600
        self.width = 600
        # self.left_motor = motor_controller()
    

    def execute_gcode(self, code):
        codelets = code.split(' ')
        command = codelets[0]
        if command == 'G1':
            print('found a g1 code, will print now', code)
            x = codelets[2][1:]
            y = codelets[3][1:]
            print('converting strings', x, y)
            x = float(x)
            y = float(y)
            print('as floats', x, y)
            self.move_to(x, y)
            return


    def move_to(self, x, y):
        l1 = sqrt((x**2 + (self.height - y)**2 ))
        l2 = sqrt(((self.width - x)**2 + (self.height - y)**2 ))
        self.move_steppers(l1, l2)


    def move_steppers(self, l1, l2):
        print('moving steppers to', l1, l2)
        l1_steps = l1 * steps_per_mm
        l2_steps = l2 * steps_per_mm





        

