from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.State import State


class TemperatureControlAutomaton:
    @staticmethod
    def initialize_automaton():
        state0 = State(0)
        state1 = State(1)

        automaton = Automaton('TemperatureControl', state0)

        automaton.add_transition(state0, state0, 'Reset')
        automaton.add_transition(state0, state1, 'Control_Temperature_On')
        automaton.add_transition(state1, state0, 'Control_Temperature_Off')
        automaton.add_transition(state1, state0, 'Reset')

        return automaton
