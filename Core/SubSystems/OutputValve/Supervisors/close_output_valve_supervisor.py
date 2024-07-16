from Core.Control.DES.State import State
from Core.Control.DES.Supervisor import Supervisor

class CloseOutputValveSupervisor:
    @staticmethod
    def initialize_supervisor():
        supervisor = Supervisor('OutputValve')

        def on_enter_state_0():
            supervisor.enable('Close_Output_Valve')

        def on_enter_state_1():
            supervisor.disable('Close_Output_Valve')

        state0 = State(0, on_enter=on_enter_state_0)
        state1 = State(1, on_enter=on_enter_state_1)

        supervisor.set_initial_state(state0)
        
        supervisor.add_transition(state0, state0, 'Reset')
        supervisor.add_transition(state0, state0, 'Close_Output_Valve')
        supervisor.add_transition(state0, state0, 'Level_Low')

        supervisor.add_transition(state0, state1, 'Open_Output_Valve')

        supervisor.add_transition(state1, state0, 'Level_Low')
        supervisor.add_transition(state1, state0, 'Reset')

        return supervisor
