from Core.Control.DES.State import State
from Core.Control.DES.Supervisor import Supervisor

class CloseInputValveSupervisor:
    @staticmethod
    def initialize_supervisor():
        supervisor = Supervisor('InputValve')

        def on_enter_state_0():
            supervisor.enable('Close_Input_Valve')

        def on_enter_state_1():
            supervisor.disable('Close_Input_Valve')

        state0 = State(0, on_enter=on_enter_state_0)
        state1 = State(1, on_enter=on_enter_state_1)

        supervisor.set_initial_state(state0)

        supervisor.add_transition(state0, state0, 'Close_Input_Valve')
        supervisor.add_transition(state0, state0, 'Level_High')
        supervisor.add_transition(state0, state1, 'Open_Input_Valve')
        supervisor.add_transition(state1, state0, 'Level_High')

        return supervisor
