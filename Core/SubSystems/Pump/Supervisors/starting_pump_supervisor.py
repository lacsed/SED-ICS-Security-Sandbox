from Core.Control.DES.State import State
from Core.Control.DES.Supervisor import Supervisor

class StartingPumpSupervisor:
    @staticmethod
    def initialize_supervisor():
        supervisor = Supervisor('Pump')

        def on_enter_state_0():
            supervisor.disable('Pump_On')

        def on_enter_state_1():
            supervisor.enable('Pump_On')

        def on_enter_state_2():
            supervisor.disable('Pump_On')

        state0 = State(0, on_enter=on_enter_state_0)
        state1 = State(1, on_enter=on_enter_state_1)
        state2 = State(2, on_enter=on_enter_state_2)

        supervisor.set_initial_state(state0)

        supervisor.add_transition(state0, state0, 'Reset')
        supervisor.add_transition(state0, state1, 'Heated')

        supervisor.add_transition(state1, state1, 'Pump_Off')
        supervisor.add_transition(state1, state1, 'Heated')
        supervisor.add_transition(state1, state2, 'Pump_On')
        supervisor.add_transition(state1, state0, 'Reset')

        supervisor.add_transition(state2, state1, 'Heated')
        supervisor.add_transition(state2, state0, 'Pump_Off')
        supervisor.add_transition(state2, state0, 'Reset')

        return supervisor
