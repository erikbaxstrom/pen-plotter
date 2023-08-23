from machine import Pin
from rp2 import StateMachine
from time import sleep
from pio_stepper import pio_step


class motor_controller:

    def __init__(self, base_pin, sm_number):
        print('init state machine. base pin, sm #', base_pin, sm_number)
        # self.index = 0
        self.pattern = int(('1000' + '0100' + '0010' + '0001') * 2, 2) # The bit mask pattern. Four x 4-bit masks, but state machine takes 32bit word, so double the sequence. Use base 2.
        self.sm = StateMachine(sm_number, pio_step, freq=10000, set_base=Pin(base_pin), 
        out_base=Pin(base_pin))
        self.sm.irq(self.busy_handler)
        self.is_busy = False
        self.sm.active(1)
        # self.sm.restart()

    @property
    def is_busy(self):
        return self._is_busy
    
    @is_busy.setter
    def is_busy(self, value):
        self._is_busy = value

    @is_busy.getter
    def is_busy(self):
        return self._is_busy

    def busy_handler(self, sm):
        print('handler running with is_busy = ', self.is_busy)
        self.is_busy = False

    def step(self, steps):
        print('running this many steps:', steps)
        print('running this pattern:', self.pattern)
        self.is_busy = True
        self.sm.put(steps)
        print('done put steps')
        self.sm.put(self.pattern)
        print('done put pattern')


        # adjust index
        # adjust bitmask 
            # check sign
            # right or left shift according to sign
                # left: (pattern << bits)|(pattern >> (32 - bits))
                # right: (pattern >> bits)|(pattern << (32 - bits)) & 0xFFFFFFFF
            # forward or reverse pattern according to sign
        # call the state machine








# this should live in motor_controller 


# init the state machine 
LEFT_SM_BASE_PIN = 6
RIGHT_SM_BASE_PIN = 2
LEFT_SM_NUMBER = 0
RIGHT_SM_NUMBER = 1

left_motor = motor_controller(LEFT_SM_BASE_PIN, LEFT_SM_NUMBER)
right_motor = motor_controller(RIGHT_SM_BASE_PIN, RIGHT_SM_NUMBER)
# sleep(1)


# run a test sequence (run steps, wait, run more steps, wait, run negative steps)
steps = [(512, 128), (512, 0), (512, 128)]

for step in steps:
    while left_motor.is_busy or right_motor.is_busy:
        print('not ready: left, right', left_motor.is_busy, right_motor.is_busy)
        sleep(1)
    print('calling steps', step[0], step[1])
    left_motor.step(step[0])
    right_motor.step(step[1])
   