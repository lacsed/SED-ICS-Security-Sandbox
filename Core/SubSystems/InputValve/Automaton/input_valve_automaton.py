from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.State import State


class InputValveAutomaton:
    @staticmethod
    def initialize_automaton():
        state0 = State(0)
        state1 = State(1)

        automaton = Automaton('InputValve', state0)
        
        automaton.add_transition(state0, state0, 'Reset')
        automaton.add_transition(state0, state1, 'Open_Input_Valve')
        automaton.add_transition(state1, state1, 'Level_High')
        automaton.add_transition(state1, state0, 'Close_Input_Valve')
        automaton.add_transition(state1, state0, 'Reset')

        return automaton
