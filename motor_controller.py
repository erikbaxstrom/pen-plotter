from machine import Pin
from rp2 import StateMachine, PIO
from time import sleep
from pio_stepper import pio_step
# , pio_pace


class motor_controller:

    def __init__(self, base_pin, sm_number, motor_direction):
        print('init state machine. base pin, sm #', base_pin, sm_number)
        self.pattern = ('1000', '0100', '0010', '0001') * 2
        self.motor_direction = motor_direction
        self.sm = StateMachine(sm_number, pio_step, freq=10000, set_base=Pin(base_pin), 
        out_base=Pin(base_pin))
        self.sm.irq(self.busy_handler)
        self.is_busy = False
        self.sm.active(1)

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
        self.is_busy = True
        steps *= self.motor_direction
        pattern = self.pattern
        if steps < 0:
            pattern = list(reversed(pattern))
            steps = -steps
        bitmask = int( ''.join(pattern) , 2)
        self.sm.put(steps)
        self.sm.put(bitmask)
        print('done put steps, bitmask', bitmask, steps)


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
LEFT_MOTOR_DIRECTION = -1
RIGHT_MOTOR_DIRECTION = 1

left_motor = motor_controller(LEFT_SM_BASE_PIN, LEFT_SM_NUMBER, LEFT_MOTOR_DIRECTION)
right_motor = motor_controller(RIGHT_SM_BASE_PIN, RIGHT_SM_NUMBER, RIGHT_MOTOR_DIRECTION)
# sleep(1)


# run a test sequence (run steps, wait, run more steps, wait, run negative steps)
steps = [(512, 128), (-512, 0), (512, 128)]

for step in steps:
    while left_motor.is_busy or right_motor.is_busy:
        print('not ready: left, right', left_motor.is_busy, right_motor.is_busy)
        sleep(1)
    print('calling steps', step)
    left_motor.step(step[0])
    right_motor.step(step[1])
   