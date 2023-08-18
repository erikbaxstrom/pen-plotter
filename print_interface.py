from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep


# Example code to run the stepper motor from https://github.com/tinkertechtrove/pico-pi-playing/blob/main/pio-steppers/test_motor1.py
@asm_pio(set_init=(PIO.OUT_LOW,) * 4)
def prog():
    wrap_target()
    set(pins, 8) [31] # 8
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
    set(pins, 2) [31] # 2
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    set(pins, 1) [31] # 1
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    wrap()
    


PIO(0).remove_program() # PIO does not automatically reset
sm = StateMachine(0, prog, freq=100000, set_base=Pin(2))

def run_stepper():
    sm.active(1)
    sleep(5)
    sm.active(0)
    sm.exec("set(pins,0)")
