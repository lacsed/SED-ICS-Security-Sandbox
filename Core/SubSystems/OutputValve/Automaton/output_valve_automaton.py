from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.State import State
from OPCClient.opc_client import OPCClient


class OutputValveAutomaton:
    @staticmethod
    def initialize_automaton():
        state0 = State(0)
        state1 = State(1)

        automaton = Automaton('OutputValve', state0)
        
        automaton.add_transition(state0, state0, 'Reset')
        automaton.add_transition(state0, state1, 'Open_Output_Valve')
        automaton.add_transition(state1, state1, 'Level_Low')
        automaton.add_transition(state1, state0, 'Close_Output_Valve')
        automaton.add_transition(state1, state0, 'Reset')

        return automaton
