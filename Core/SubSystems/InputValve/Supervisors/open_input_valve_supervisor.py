from Core.Control.DES.State import State
from Core.Control.DES.Supervisor import Supervisor

class OpenInputValveSupervisor:
    @staticmethod
    def initialize_supervisor():
        supervisor = Supervisor('InputValve')

        def on_enter_state_0():
            supervisor.disable('Open_Input_Valve')

        def on_enter_state_1():
            supervisor.enable('Open_Input_Valve')

        state0 = State(0, on_enter=on_enter_state_0)
        state1 = State(1, on_enter=on_enter_state_1)
        state2 = State(2)

        supervisor.set_initial_state(state0)

        supervisor.add_transition(state0, state0, 'Reset')
        supervisor.add_transition(state0, state0, 'Finish_Process')
        supervisor.add_transition(state0, state1, 'Start_Process')
        supervisor.add_transition(state1, state2, 'Finish_Process')
        supervisor.add_transition(state1, state0, 'Open_Input_Valve')
        supervisor.add_transition(state1, state0, 'Reset')
        supervisor.add_transition(state2, state0, 'Open_Input_Valve')
        supervisor.add_transition(state2, state0, 'Reset')

        return supervisor
