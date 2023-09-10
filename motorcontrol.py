class MotorController:
    """Controls a stepper motor

    This class provides control over a stepper motor by interfacing with a state machine
    and managing motor direction, position, and enabled/disabled states.

    Args:
        base_pin (int): Base GPIO pin number for the state machine output. Corresponds to ULN2003 controller Input 1.
        sm_number (int): State machine number.
        motor_direction (int): Motor direction (1 for clockwise, -1 for counterclockwise).

    Attributes:
        current_position (int): Current motor position.
        is_busy (bool): Indicates if the motor is currently busy.
        enabled (bool): Indicates whether the state machine controlling the motor is enabled. Setting to False will disable the state machine. 

    """

    def __init__(self, motor_direction, state_machine):
        # self.base_pattern = ('0001', '0010', '0100', '1000') * 2    # Wave Mode
        self.base_pattern = ('0011', '0110', '1100', '1001') * 2    # Full Step Mode
        # self.base_pattern = ('0001', '0011', '0010', '0110', '0100', '1100', '1000', '1001')    # Half Step Mode
        self.motor_direction = motor_direction
        self.current_position = 0
        self.pattern_index = 0
        self.sm = state_machine
        self.sm.irq(self.busy_handler)
        self.is_busy = False
        self.enabled = False

    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, value):
        try:
            if not self._enabled and value is True:
                self.sm.active(1)
                self._enabled = value
            if self._enabled and value is False:
                self.sm.exec("set(pins,0)")
                self.sm.active(0)
                self._enabled = value
        except AttributeError:  # when first called, it's not yet set
            self._enabled = value

    @enabled.getter
    def enabled(self):
        return self._enabled

    def reset(self):
        self.sm.restart()


    def busy_handler(self, sm):
        """Handler for PIO interrupts indicating completion of state machine output"""
        # print('handler running with is_busy = ', self.is_busy)
        self.is_busy = False
        self.sm.restart()

    def step(self, steps):
        """
        Move the motor by a specified number of steps.

        Args:
            steps (int): Number of steps to move.
        """
        
        self.is_busy = True
        self.enabled = True
        steps *= self.motor_direction

        pattern = []
        for i in range(0, 8):
            idx = (i + self.pattern_index) % 8
            if steps < 0:
                idx *= -1
            pattern.append( self.base_pattern[idx] )
        self.pattern_index = (steps + self.pattern_index )% 8
        bitmask = int( ''.join(pattern) , 2)

        if steps < 0:
            steps = -steps
        # print('pattern is ', pattern)
        self.sm.put(steps)
        self.sm.put(bitmask)
        # print('put steps, bitmask, pattern', steps, bitmask, pattern)


    def step_to(self, position):
        """
        Move the motor to a specific position.

        Args:
            position (int): Target position.
        """
        
        rel_steps = position - self.current_position
        self.step(rel_steps)
        self.current_position = position


 













# # TEST CODE

# from time import sleep

# from machine import Pin
# from rp2 import StateMachine, PIO

# from piostep import pio_step

# # init the state machine 
# LEFT_SM_BASE_PIN = 6
# RIGHT_SM_BASE_PIN = 2
# LEFT_SM_NUMBER = 0
# RIGHT_SM_NUMBER = 1
# LEFT_MOTOR_DIRECTION = 1
# RIGHT_MOTOR_DIRECTION = -1

# left_sm = StateMachine(LEFT_SM_NUMBER, pio_step, freq=10000, set_base=Pin(LEFT_SM_BASE_PIN), out_base=Pin(LEFT_SM_BASE_PIN))

# left_motor = MotorController(LEFT_MOTOR_DIRECTION, left_sm)


# # run a test sequence
# steps = [-5000, 3000, -3000, 5000]

# for step in steps:
#     while left_motor.is_busy:
#         # print('not ready: left, right', left_motor.is_busy, right_motor.is_busy)
#         sleep(0.1)
#     print('calling steps', step)
#     left_motor.step(step)
# while left_motor.is_busy:
#     sleep(1)
# left_motor.enabled = False





# # TEST CODE

# from time import sleep

# from machine import Pin
# from rp2 import StateMachine, PIO

# from piostep import pio_step

# # init the state machine 
# LEFT_SM_BASE_PIN = 6
# RIGHT_SM_BASE_PIN = 2
# LEFT_SM_NUMBER = 0
# RIGHT_SM_NUMBER = 1
# LEFT_MOTOR_DIRECTION = 1
# RIGHT_MOTOR_DIRECTION = -1

# left_sm = StateMachine(LEFT_SM_NUMBER, pio_step, freq=10000, set_base=Pin(LEFT_SM_BASE_PIN), out_base=Pin(LEFT_SM_BASE_PIN))
# right_sm = StateMachine(RIGHT_SM_NUMBER, pio_step, freq=10000, set_base=Pin(RIGHT_SM_BASE_PIN), out_base=Pin(RIGHT_SM_BASE_PIN))

# left_motor = MotorController(LEFT_MOTOR_DIRECTION, left_sm)
# right_motor = MotorController(RIGHT_MOTOR_DIRECTION, right_sm)
# # sleep(1)


# # run a test sequence (run steps, wait, run more steps, wait, run negative steps)
# # steps = [(2048, 0), (0, 0), (0, 0)]
# blah = 3
# steps = [(blah, blah), (-blah, -blah)]

# for step in steps:
#     while left_motor.is_busy or right_motor.is_busy:
#         # print('not ready: left, right', left_motor.is_busy, right_motor.is_busy)
#         sleep(0.1)
#     print('calling steps', step[0], step[1])
#     left_motor.step(step[0])
#     right_motor.step(step[1])
# while left_motor.is_busy or right_motor.is_busy:
#     sleep(1)
# left_motor.enabled = False
# right_motor.enabled = False
