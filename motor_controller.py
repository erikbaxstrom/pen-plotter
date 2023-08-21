from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep


class motor_controller:

    def __init__(self, base_pin, sm_number):
        self.index = 0
        self.four_step_pattern = int(('1000' + '0100' + '0010' + '0001') * 2, 2) # The bit mask pattern. Four x 4-bit masks, but state machine takes 32bit word, so double the sequence. Use base 2.
        self.sm = StateMachine(sm_number, self.run_stepper, freq=10000, set_base=Pin(base_pin), out_base=Pin(base_pin))



    def step(self, steps):
        self.sm.active(1)
        return


        # adjust index
        # adjust bitmask 
            # check sign
            # right or left shift according to sign
                # left: (pattern << bits)|(pattern >> (32 - bits))
                # right: (pattern >> bits)|(pattern << (32 - bits)) & 0xFFFFFFFF
            # forward or reverse pattern according to sign
        # call the state machine

    @asm_pio(set_init=(PIO.OUT_LOW,) * 4,
            out_init=(PIO.OUT_LOW,) * 4,
            out_shiftdir=PIO.SHIFT_RIGHT,
            in_shiftdir=PIO.SHIFT_LEFT)
    def run_stepper():
        set(pins, 8) [31] # 8
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]
        set(pins, 4) [31] # 4
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [31]


    # pull pattern
    # move osr to x
    # pull step count
    # move osr to y
    # start loop
    # 








# this should live in motor_controller init
# init the state machine 
LEFT_SM_BASE_PIN = 6
RIGHT_SM_BASE_PIN = 2

left_motor = motor_controller(LEFT_SM_BASE_PIN, 0)
right_motor = motor_controller(RIGHT_SM_BASE_PIN, 1)

# run a test sequence (run steps, wait, run more steps, wait, run negative steps)
left_motor.step(5)
sleep(2)
right_motor.step(10)
sleep(2)
left_motor.step(15)