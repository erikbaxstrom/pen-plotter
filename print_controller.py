from math import sqrt
from machine import Pin
from time import sleep

moves_per_mm = 1


L_pins = [
    Pin(5, Pin.OUT),
    Pin(4, Pin.OUT),
    Pin(3, Pin.OUT),
    Pin(2, Pin.OUT)]

R_pins = [
    Pin(9, Pin.OUT),
    Pin(8, Pin.OUT),
    Pin(7, Pin.OUT),
    Pin(6, Pin.OUT)]

motor_sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

# L_pins = [L1, L2, L3, L4]

class print_controller:

    def __init__(self):
        self.height = 600
        self.width = 600
    
    def move_steppers(self, l1, l2):
        print('moving steppers to', l1, l2)
        l1_moves = l1 * moves_per_mm
        l2_moves = l2 * moves_per_mm
        for move in range(l1_moves):
            for step in motor_sequence:
                for i in range(4):
                    L_pins[i].value(step[i])
                    sleep(0.001)
        for move in range(l2_moves):
            for step in motor_sequence:
                for i in range(4):
                    R_pins[i].value(step[i])
                    sleep(0.001)




    def print_line(self, code):
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
            self.paint(x, y)
            return
        

    def paint(self, x, y):
        l1 = sqrt((x**2 + (self.height - y)**2 ))
        l2 = sqrt(((self.width - x)**2 + (self.height - y)**2 ))
        self.move_steppers(l1, l2)

