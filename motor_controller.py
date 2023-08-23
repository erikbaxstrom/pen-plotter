from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep


@asm_pio(set_init=(PIO.OUT_LOW,) * 4,
        out_init=(PIO.OUT_LOW,) * 4,
        out_shiftdir=PIO.SHIFT_RIGHT
        # in_shiftdir=PIO.SHIFT_LEFT
        )
def run_stepper():
    pull(block) # pull steps
    mov(x, osr) # move steps from osr to x
    pull() # pull step count
    mov(y, osr)# move pattern from osr to y

    jmp(not_x, "end") # if step count is zero, we're done

    label("loop")
    jmp(not_osre, "step") # skip moving y into osr if osr isn't empty
    mov(osr, y) # put the pattern into the osr

    label("step")
    out(pins, 4) [31] # output four bits from the osr to the pins
    # nop() [31] # delay 32 cycles x4
    # nop() [31]
    # nop() [31]
    # nop() [31]

    jmp(x_dec, "loop") # decrement x and jump back to the beginning of the loop

    label("end")
    irq(rel(0))
    nop()


class motor_controller:

    def __init__(self, base_pin, sm_number):
        print('init state machine. base pin, sm #', base_pin, sm_number)
        # self.index = 0
        self.pattern = int(('1000' + '0100' + '0010' + '0001') * 2, 2) # The bit mask pattern. Four x 4-bit masks, but state machine takes 32bit word, so double the sequence. Use base 2.
        self.sm = StateMachine(sm_number, run_stepper, freq=10000, set_base=Pin(base_pin), 
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
        # print(self.sm.tx_fifo())
        # sleep(1)
        self.sm.put(steps)
        print('done put steps')
        self.sm.put(self.pattern)
        print('done put pattern')
        # sleep(5)
        # self.sm.active(0)
        # self.sm.exec("set(pins,0)")
        # return


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
    
# print('calling step 400')
# left_motor.step(400)
# # sleep(2)
# right_motor.step(400)
# sleep(2)
# print('calling step 100')
# left_motor.step(101)