from math import sqrt

class print_controller:

    def __init__(self):
        self.height = 600
        self.width = 600
    
    def move_stepper(self, l1, l2):
        print('moving steppers to', l1, l2)
        pass

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
        self.move_stepper(l1, l2)

