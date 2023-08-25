from rp2 import PIO, asm_pio, StateMachine
from machine import Pin
from time import sleep

# @asm_pio(set_init=(PIO.OUT_LOW,) * 4,
#         out_init=(PIO.OUT_LOW,) * 4,
#         out_shiftdir=PIO.SHIFT_RIGHT
#         # in_shiftdir=PIO.SHIFT_LEFT
#         )
# def pio_step():
#     pull(block) # pull steps
#     mov(x, osr) # move steps from osr to x

#     jmp(not_x, "end") # if step count is zero, we're done


#     label("step")
#     out(pins, 4) [31] # output four bits from the osr to the pins
#     jmp(x_dec, "loop") # decrement x and jump back to the beginning of the loop
#     wait(0, irq, rel(2)) # wait on irq from counter

#     label("end")
#     irq(block, rel(0)) # raise flag to handler that we're done
# #     nop()


# @asm_pio()
# def pio_pace():
# #     pull(block)
# #     wrap_target()
#     irq(clear, rel(2))
# #     mov(x, osr)
# #     wait(1, irq, rel(4))
# #     label("countdown")
# #     jmp(x_dec, "countdown")
# #     irq(clear, rel(4))
#     # wait(1, irq, rel(4))





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
    irq(block, 0)
    out(pins, 4) [31] # output four bits from the osr to the pins
    jmp(x_dec, "loop") # decrement x and jump back to the beginning of the loop

    label("end") #CANNOT END WITH LABEL!!!! ADD NOP() IF NEEDED!!!!!!!!!!!!!
    # irq(block, rel(0)) # raise flag to handler that we're done
    nop()
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



@asm_pio(set_init=PIO.OUT_HIGH, out_init=PIO.OUT_HIGH, out_shiftdir=PIO.SHIFT_RIGHT)
def pio_pace():
    pull()
    wrap_target()
    mov(x, osr)
    irq(clear, 0)
    # set(pins, 1)
    label("countdown")
    jmp(x_dec, "countdown")
    # set(pins, 0)
    # nop() [31]
    # wait(1, irq, 0)
    wrap()



#     irq(clear, rel(2))
# #     mov(x, osr)
# #     wait(1, irq, rel(4))
# #     label("countdown")
# #     jmp(x_dec, "countdown")
# #     irq(clear, rel(4))
#     # wait(1, irq, rel(4))


the_first_one = PIO(0)

pattern = int(('1000' + '0100' + '0010' + '0001') * 2, 2)

sm = StateMachine(0, step, freq=10000, set_base=Pin(2), out_base=Pin(2))
pacer = StateMachine(1, pio_pace, freq=10000, set_base=Pin(20))
# sm1 = StateMachine(0, blink, freq=2000, set_base=Pin(6))
# pacer1 = StateMachine(1, pio_pace, freq=2000, set_base=Pin(7))

pacer.active(1)
pacer.put(10)
sm.active(1)
sm.put(512)
sm.put(pattern)
# sm1.active(1)
# pacer1.active(1)
sleep(5)
pacer.active(0)
sm.active(0)
# sm1.active(0)
# pacer1.active(0)