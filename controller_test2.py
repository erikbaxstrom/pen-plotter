from machine import Pin
from rp2 import PIO, StateMachine, asm_pio

index = 0

@asm_pio(set_init=(PIO.OUT_LOW,) * 4,
         out_init=(PIO.OUT_LOW,) * 4,
         out_shiftdir=PIO.SHIFT_RIGHT,
         in_shiftdir=PIO.SHIFT_LEFT)
def run_stepper(steps):
    # adjust index
    # adjust bitmask 
        # check sign
        # right or left shift according to sign
            # left: (pattern << bits)|(pattern >> (32 - bits))
            # right: (pattern >> bits)|(pattern << (32 - bits)) & 0xFFFFFFFF
        # forward or reverse pattern according to sign
    # call the state machine
        # output mask to sm
        # output step count to sm

    pass


# init the state machine
# run a test sequence (run steps, wait, run more steps, wait, run negative steps)