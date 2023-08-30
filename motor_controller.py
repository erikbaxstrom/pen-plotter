from machine import Pin
from rp2 import StateMachine, PIO
from time import sleep
from pio_stepper import pio_step


class motor_controller:

    def __init__(self, base_pin, sm_number, motor_direction, home_position):
        print('init state machine. base pin, sm #', base_pin, sm_number)
        self.pattern = ('0001', '0010', '0100', '1000') * 2
        self.motor_direction = motor_direction
        self.current_position = home_position
        self.sm = StateMachine(sm_number, pio_step, freq=10000, set_base=Pin(base_pin), 
        out_base=Pin(base_pin))
        self.sm.irq(self.busy_handler)
        self.is_busy = False
        self.enabled = False

    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, value):
        try:
            if not self._enabled and value is True:
                self.sm.active(1)
                self._enabled = value
            if self._enabled and value is False:
                self.sm.exec("set(pins,0)")
                self.sm.active(0)
                self._enabled = value
        except AttributeError:  # when first called, it's not yet set
            self._enabled = value

    @enabled.getter
    def enabled(self):
        return self._enabled


    def busy_handler(self, sm):
        print('handler running with is_busy = ', self.is_busy)
        self.is_busy = False


    def step(self, steps):
        self.is_busy = True
        self.enabled = True
        steps *= self.motor_direction
        pattern = self.pattern
        if steps < 0:
            pattern = list(reversed(pattern))
            steps = -steps
        bitmask = int( ''.join(pattern) , 2)
        self.sm.put(steps)
        self.sm.put(bitmask)
        print('done put steps, bitmask', bitmask, steps)
    

    def step_to(self, position):
        print('step_to position', position)
        rel_steps = position - self.current_position
        self.step(rel_steps)
        self.current_position = position


 



        # adjust index
        # adjust bitmask 
            # check sign
            # right or left shift according to sign
                # left: (pattern << bits)|(pattern >> (32 - bits))
                # right: (pattern >> bits)|(pattern << (32 - bits)) & 0xFFFFFFFF
            # forward or reverse pattern according to sign
        # call the state machine








# this should live in motor_controller 


# # init the state machine 
# LEFT_SM_BASE_PIN = 6
# RIGHT_SM_BASE_PIN = 2
# LEFT_SM_NUMBER = 0
# RIGHT_SM_NUMBER = 1
# LEFT_MOTOR_DIRECTION = -1
# RIGHT_MOTOR_DIRECTION = 1

# left_motor = motor_controller(LEFT_SM_BASE_PIN, LEFT_SM_NUMBER, LEFT_MOTOR_DIRECTION)
# right_motor = motor_controller(RIGHT_SM_BASE_PIN, RIGHT_SM_NUMBER, RIGHT_MOTOR_DIRECTION)
# # sleep(1)


# # run a test sequence (run steps, wait, run more steps, wait, run negative steps)
# # steps = [(2048, 0), (0, 0), (0, 0)]
# blah = 2048 * 5
# steps = [(blah, 0), (0,0)]

# for step in steps:
#     while left_motor.is_busy or right_motor.is_busy:
#         print('not ready: left, right', left_motor.is_busy, right_motor.is_busy)
#         sleep(30)
#     print('calling steps', step[0], step[1])
#     left_motor.step_to(step[0])
#     right_motor.step_to(step[1])
# while left_motor.is_busy or right_motor.is_busy:
#     sleep(1)
# left_motor.deactivate()
# right_motor.deactivate()
   