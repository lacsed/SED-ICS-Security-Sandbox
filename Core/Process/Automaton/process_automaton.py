from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.State import State


class ProcessAutomaton:
    @staticmethod
    def initialize_automaton():
        state0 = State(0)
        state1 = State(1)

        automaton = Automaton('Process', state0)

        automaton.add_transition(state0, state0, 'Reset')
        automaton.add_transition(state0, state1, 'Start_Process')
        automaton.add_transition(state1, state0, 'Finish_Process')
        automaton.add_transition(state1, state0, 'Reset')

        return automaton
