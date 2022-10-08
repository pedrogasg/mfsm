"""
Test Unitaires for FSM
Window Controller
"""
from enum import Enum

import pytest

from mfsm import FSM, State, When

class ControlState(State):
    """
    State of the Push Button  Machine
    """
    OPEN = 1
    CLOSE = 2

class ControlInput(Enum):
    """
    Button that control the window
    """
    PRESS = 1


class ControlOutput(Enum):
    """
    The output of the machine that control
    """
    CW = 1
    CCW = 2

class ControlWindow(FSM):
    """
    Push Botton Window Controller State Machine    
    """
    STATES = ControlState

    @When(ControlState.OPEN)
    def handle_open_window(self, inputs):
        """
        The button is pressed when we are in the open state
        """
        if inputs == ControlInput.PRESS:
            self.goto(ControlState.CLOSE)
            return ControlOutput.CCW

    @When(ControlState.CLOSE)
    def handle_close_window(self, inputs):
        """
        The button is pressed when we are in the close state
        """
        if inputs == ControlInput.PRESS:
            self.goto(ControlState.OPEN)
            return ControlOutput.CW

@pytest.fixture(name="control_machine")
def fixture_control_machine():
    """
    A control machine
    """
    return ControlWindow(ControlState.CLOSE)

def test_initial_control_machine(control_machine):
    """
    Test a new control machine
    """
    assert ControlState.CLOSE == control_machine.current_state()


def test_close_control_machine(control_machine):
    """
    Testing states of a closed window machine
    """
    assert ControlOutput.CW == control_machine(ControlInput.PRESS)


def test_open_control_machine(control_machine):
    """
    Testing states of a open window machine
    """
    control_machine(ControlInput.PRESS)
    assert ControlOutput.CCW == control_machine(ControlInput.PRESS)