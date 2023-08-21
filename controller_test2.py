from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep

index = 0
four_phase_pattern = int(('1000' + '0100' + '0010' + '0001') * 2, 2) # bitmask pattern. Four x 4-bit masks, but state machine takes 32bit word, so double the sequence. Use base 2.


def step(steps):
    print('steps', steps)
    left_sm.active(1)
    # sleep(5)
    # left_sm.active(0)
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
    set(pins, 1)
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    set(pins,2)
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    nop()[31]
    # output mask to sm
    # output step count to sm



# init the state machine
left_sm = StateMachine(0, run_stepper, freq=10000, set_base=Pin(2), out_base=Pin(2))
# run a test sequence (run steps, wait, run more steps, wait, run negative steps)
step(5)
sleep(1)
step(10)
sleep(1)
step(15)