from Core.Control.DES.State import State
from Core.Control.DES.Supervisor import Supervisor

class StoppingTemperatureControlSupervisor:
    @staticmethod
    def initialize_supervisor():
        supervisor = Supervisor('TemperatureControl')

        def on_enter_state_0():
            supervisor.enable('Control_Temperature_Off')

        def on_enter_state_1():
            supervisor.disable('Control_Temperature_Off')

        def on_enter_state_2():
            supervisor.disable('Control_Temperature_Off')

        state0 = State(0, on_enter=on_enter_state_0)
        state1 = State(1, on_enter=on_enter_state_1)
        state2 = State(2, on_enter=on_enter_state_2)

        supervisor.set_initial_state(state0)

        supervisor.add_transition(state0, state0, 'Reset')
        supervisor.add_transition(state0, state0, 'Control_Temperature_Off')
        supervisor.add_transition(state0, state0, 'Heated')
        supervisor.add_transition(state0, state0, 'Cooled')
        supervisor.add_transition(state0, state1, 'Control_Temperature_On')

        supervisor.add_transition(state1, state1, 'Cooled')
        supervisor.add_transition(state1, state2, 'Heated')
        supervisor.add_transition(state1, state0, 'Reset')

        supervisor.add_transition(state2, state2, 'Heated')
        supervisor.add_transition(state2, state0, 'Cooled')
        supervisor.add_transition(state2, state0, 'Reset')

        return supervisor
