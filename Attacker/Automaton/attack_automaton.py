from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.State import State


class AttackAutomaton:
    @staticmethod
    def initialize_automaton(trigger_event):
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)

        automaton = Automaton('AttackAutomaton', state0)

        automaton.add_transition(state0, state0, 'Reset')

        automaton.add_transition(state0, state3, trigger_event)
        automaton.add_transition(state0, state1, 'Deny_Event')
        automaton.add_transition(state0, state2, 'Insert_Event')

        automaton.add_transition(state1, state3, 'Insert_Event')

        automaton.add_transition(state2, state3, 'Deny_Event')

        return automaton
