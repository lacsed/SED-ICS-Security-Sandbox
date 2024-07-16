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

    @staticmethod
    def initialize_automaton_with_client(client: OPCClient):
        def on_enter_state_0():
            # client.update_open_output_valve(False)
            # client.update_close_output_valve(True)
            pass

        def on_enter_state_1():
            # client.update_open_output_valve(True)
            # client.update_close_output_valve(False)
            pass

        state0 = State(0, on_enter=on_enter_state_0)
        state1 = State(1, on_enter=on_enter_state_1)

        automaton = Automaton('OutputValve', state0)

        automaton.add_transition(state0, state0, 'Reset')
        automaton.add_transition(state0, state1, 'Open_Output_Valve')
        automaton.add_transition(state1, state1, 'Level_Low')
        automaton.add_transition(state1, state0, 'Close_Output_Valve')
        automaton.add_transition(state1, state0, 'Reset')

        return automaton
