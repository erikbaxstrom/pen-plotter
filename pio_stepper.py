from rp2 import PIO, asm_pio
# from machine import Pin

@asm_pio(set_init=(PIO.OUT_LOW,) * 4,
        out_init=(PIO.OUT_LOW,) * 4,
        out_shiftdir=PIO.SHIFT_RIGHT
        # in_shiftdir=PIO.SHIFT_LEFT
        )
def pio_step():
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