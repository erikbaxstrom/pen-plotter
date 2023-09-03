# tateMachine(LEFT_SM_NUMBER, pio_step, freq=10000, set_base=Pin(LEFT_SM_BASE_PIN), out_base=Pin(LEFT_SM_BASE_PIN))
from machine import Pin


class MockStateMachine:
    """mock of state machine"""


    def __init__(self, id, prog, freq, set_base=Pin(0), out_base=Pin(0)):
        self.id = id
        self.prog = prog
        self.freq = freq
        self.base = set_base
        self.out_base = out_base
        self.result = []

    def active(self, state):
        self.result.append(f"{self.id} active set {state}")
        # print('active called', self.result)
    
    def put(self, value):
        self.result.append(f"{self.id} put {value}")
    
    def irq(self, function):
        self.result.append(f"{self.id} irq handler set to {function.__name__}")

    def exec(self, command):
        self.result.append(f"{self.id} exec {command}")

    


def mock_pio_step():
    pass
