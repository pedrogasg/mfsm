"""
Test Unitaires for FSM
Turnstile
"""
from enum import Enum

import pytest

from mfsm import FSM, State, When


class TurnstileState(State):
    """
    State of the Turnstile Machine
    """
    LOCKED = 1
    UNLOCKED = 2


class TurnstileInput(Enum):
    """
    Inputs of the Turnstile Machine
    """
    COIN = 1
    PUSH = 2

class TurnstileOutput(Enum):
    """
    Outputs of the Turnstile Machine
    """
    LOCK = 1
    UNLOCK = 2
    THANKS = 3
    ALARM = 4


class TurnstileFSM(FSM):
    """
    Turnstile State Machine Definition
    """
    STATES = TurnstileState

    @When(TurnstileState.LOCKED)
    def handle_locked(self, inputs):
        """
        This function is called when we are in the LOCKET state
        """
        if inputs == TurnstileInput.COIN:
            self.goto(TurnstileState.UNLOCKED)
            return TurnstileOutput.UNLOCK
        elif inputs == TurnstileInput.PUSH:
            self.stay(inputs)
            return TurnstileOutput.ALARM

    @When(TurnstileState.UNLOCKED)
    def handle_unlocked(self, inputs):
        """
        This function is called when we are in the UNLOCKET state
        """
        if inputs == TurnstileInput.COIN:
            self.stay(inputs)
            return TurnstileOutput.THANKS
        elif inputs == TurnstileInput.PUSH:
            self.goto(TurnstileState.LOCKED)
            return TurnstileOutput.LOCK

@pytest.fixture(name="locked_machine")
def fixture_locked_machine():
    """
    A locked machine
    """
    return TurnstileFSM(TurnstileState.LOCKED)

def test_initial_turnstile(locked_machine):
    """
    Test a new turnstile
    """
    assert TurnstileState.LOCKED == locked_machine.current_state()

@pytest.mark.parametrize("_in, _out", [(TurnstileInput.COIN, TurnstileOutput.UNLOCK),
        (TurnstileInput.PUSH, TurnstileOutput.ALARM)])
def test_locked_turnstile(locked_machine,  _in, _out):
    """
    Testing states of a locked machine
    """
    assert _out == locked_machine(_in)

@pytest.mark.parametrize("_in, _out", [(TurnstileInput.COIN, TurnstileOutput.THANKS),
        (TurnstileInput.PUSH, TurnstileOutput.LOCK)])
def test_unlocked_turnstile(locked_machine,  _in, _out):
    """
    Testing states of a unlocked machine
    """
    _ = locked_machine(TurnstileInput.COIN)
    assert _out == locked_machine(_in)


