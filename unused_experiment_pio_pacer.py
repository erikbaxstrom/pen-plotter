from rp2 import PIO, asm_pio, StateMachine
from machine import Pin
from time import sleep



@asm_pio(set_init=(PIO.OUT_LOW,) * 4,
        out_init=(PIO.OUT_LOW,) * 4,
        out_shiftdir=PIO.SHIFT_RIGHT
        # in_shiftdir=PIO.SHIFT_LEFT
        )
def step():
    wrap_target()
    pull(block) # pull steps
    mov(x, osr) # move steps from osr to x
    pull() # pull pattern
    mov(y, osr)# move pattern from osr to y

    jmp(not_x, "end") # if step count is zero, we're done

    label("loop")
    jmp(not_osre, "step") # skip moving y into osr if osr isn't empty
    mov(osr, y) # put the pattern into the osr

    label("step")
    # irq(block, 1)
    out(pins, 4) [31] # output four bits from the osr to the pins
    jmp(x_dec, "loop") # decrement x and jump back to the beginning of the loop

    label("end") #CANNOT END WITH LABEL!!!! ADD NOP() IF NEEDED!!!!!!!!!!!!!
    irq(block, 0) # raise flag to handler that we're done
    # nop()
    wrap()


@asm_pio(set_init=(PIO.OUT_LOW,) * 4,
        out_init=(PIO.OUT_LOW,) * 4,
        out_shiftdir=PIO.SHIFT_RIGHT
        # in_shiftdir=PIO.SHIFT_LEFT
        )
def blink():
    wrap_target()
    irq(block, 1)
    set(pins, 1)
    nop() [31]
    set(pins, 0)
    wrap()



@asm_pio(set_init=PIO.OUT_HIGH, out_init=PIO.OUT_HIGH, out_shiftdir=PIO.SHIFT_RIGHT, pull_thresh=32)
def pio_pace():
    pull()
    pull()
    wrap()
    
# a broken attempt
    # wrap_target()
    # pull(block)
    # mov(x, osr) # move step count into x from osr
    # pull() # pull the pace
    # mov(y, osr)
    # mov(osr, x)
    # jmp(not_x, "end") # if step count is zero, we're done

    # label("startcount")
    # mov(x, osr) 

    # label("countdown")
    # jmp(x_dec, "countdown")

    # irq(clear, 1)
    # jmp(y_dec, "startcount")

    # label("end")
    # nop()
    # wrap()


# a different attempt
    # nop()
    # label('getnew')
    # # label('getnew')
    # pull(ifempty, noblock)
    # out(y, osr)
    # label("countagain")
    # mov(x, y)
    # label("countdown")
    # # jmp(not_osre, "getnew")
    # jmp(x_dec, "countdown")
    # irq(clear, 1)
    # # jmp("countagain")
    # nop()



# and another attempt
    # label("newpace")
    # out(y, 32)

    # wrap_target()
    # irq(clear, 1)
    # pull(ifempty, noblock)
    # jmp(not_osre, "newpace")

    # mov(x, y)

    # label("countdown")
    # jmp(x_dec, "countdown")

    # wrap()




proceed = False
def handler(sm):
    x = (PIO(0).irq().flags())
    print('PIO(0).irq(): {:5d}'.format(x))
    global proceed
    proceed = True
    print('handled', proceed, sm.irq().flags())

the_first_one = PIO(0)

pattern = int(('1000' + '0100' + '0010' + '0001') * 2, 2)

sm = StateMachine(0, step, freq=20000, set_base=Pin(2), out_base=Pin(2))
sm.irq(handler)
pacer = StateMachine(1, pio_pace, freq=20000, set_base=Pin(20))
# sm1 = StateMachine(0, blink, freq=2000, set_base=Pin(6))
# pacer1 = StateMachine(1, pio_pace, freq=2000, set_base=Pin(7))

pacer.active(1)
sm.active(1)
sm.put(512)
sm.put(pattern)
pacer.put(620)
pacer.put(100)
# sm1.active(1)
# pacer1.active(1)
while not proceed:
    print('not proceed')
    sleep(1)
pacer.put(512)
pacer.put(100)
sm.put(512)
sm.put(pattern)
sleep(5)
pacer.active(70)
sm.active(0)
# sm1.active(0)
# pacer1.active(0)