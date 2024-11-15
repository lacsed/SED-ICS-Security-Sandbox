from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.State import State


class InputValveAttackAutomaton:
    @staticmethod
    def initialize_automaton():
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)
        # state4 = State(4)
        # state5 = State(5)

        automaton = Automaton('InputValveAttack', state0)

        automaton.add_transition(state0, state0, 'Reset')

        automaton.add_transition(state0, state3, 'Open_Input_Valve')
        automaton.add_transition(state0, state1, 'Deny_Event')
        automaton.add_transition(state0, state2, 'Insert_Event')

        automaton.add_transition(state1, state3, 'Insert_Event')

        automaton.add_transition(state2, state3, 'Deny_Event')

        automaton.add_transition(state3, state3, 'Level_High')

        # automaton.add_transition(state3, state4, 'Close_Input_Valve')

        # automaton.add_transition(state4, state5, 'Finish_Process')

        # automaton.add_transition(state5, state0, 'Start_Process')

        return automaton
