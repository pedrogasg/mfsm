# MIT License
#
# Copyright (c) 2022 Pedro Fillastre

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ===============================================================================

"""All the code is init for now"""
from enum import Enum
from typing import Any, List, Union


class State(Enum):
    """" Empty enum as root of states """


class UnhandleState(Exception):
    """ Unhandle _state send to the machine"""

class UnknowState(Exception):
    """ Unknow _state store to the machine"""


class When:
    """
    Create a decorator that attach the _state to the function to be able to call the right _state
    """

    def __init__(self, states: Union[State, List[State]]):
        self._states = states if isinstance(states, list) else [states]

    def __call__(self, func):
        func._states = self._states
        return func


class FSM(object):
    """
    Minimal backbone for a deterministic finite _state machine
    """
    STATES = State

    def __init__(self, start_with: State) -> None:
        self._state = start_with
        self._set_handlers()
        self.transitions = {}

    def _set_handlers(self):
        """
        Set all the handler and the custom handler attached by When
        """
        cls = self.__class__
        self.states = {s: self.when_unhandle for s in cls.STATES}
        for attribute in dir(self):
            attribute_value = getattr(self, attribute)
            if callable(attribute_value):
                if hasattr(attribute_value, "_states"):
                    for state in getattr(attribute_value, "_states"):
                        if state in cls.STATES:
                            self.states[state] = attribute_value
                        else:
                            raise UnknowState(f'Unknow State {state} was registred in the machine')

    def current_state(self):
        """Return the current state of the machine"""
        return self._state

    def when_unhandle(self, *args):
        """
        Default function that is call when a _state is reach
        this can be override if you do not want to raise the UnhandleState exception
        """
        raise UnhandleState(
            f'Not function was assing to handle the {self._state} _state')

    def stay(self, inputs):
        """
        This function can be override to do something in a hold state
        """

    def goto(self, new_state: State):
        """
        Function used to transistion of one _state to another
        """
        self._state = new_state

    def __call__(self, inputs: Any):
        """
        Send next input to a handler function
        """
        return self.states[self._state](inputs)
