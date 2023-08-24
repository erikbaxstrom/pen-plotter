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
#     irq(block, rel(4))
    jmp(not_osre, "step") # skip moving y into osr if osr isn't empty
    mov(osr, y) # put the pattern into the osr

    label("step")
    out(pins, 4) [31] # output four bits from the osr to the pins
    jmp(x_dec, "loop") # decrement x and jump back to the beginning of the loop
    wait(0, irq, rel(2)) # wait on irq from counter

    label("end")
    irq(block, rel(0)) # raise flag to handler that we're done
#     nop()


@asm_pio()
def pio_pace():
#     pull(block)
#     wrap_target()
    irq(clear, rel(2))
#     mov(x, osr)
#     wait(1, irq, rel(4))
#     label("countdown")
#     jmp(x_dec, "countdown")
#     irq(clear, rel(4))
    # wait(1, irq, rel(4))
