from Core.Control.DES.State import State
from Core.Control.DES.Supervisor import Supervisor

class StartingMixerSupervisor:
    @staticmethod
    def initialize_supervisor():
        supervisor = Supervisor('Mixer')

        def on_enter_state_0():
            supervisor.disable('Mixer_On')

        def on_enter_state_1():
            supervisor.enable('Mixer_On')

        state0 = State(0, on_enter=on_enter_state_0)
        state1 = State(1, on_enter=on_enter_state_1)
        state2 = State(2)

        supervisor.set_initial_state(state0)

        supervisor.add_transition(state0, state0, 'Reset')
        supervisor.add_transition(state0, state1, 'Level_High')

        supervisor.add_transition(state1, state1, 'Level_High')
        supervisor.add_transition(state1, state1, 'Mixer_Off')
        supervisor.add_transition(state1, state2, 'Mixer_On')
        supervisor.add_transition(state1, state0, 'Reset')

        supervisor.add_transition(state2, state1, 'Level_High')
        supervisor.add_transition(state2, state0, 'Mixer_Off')
        supervisor.add_transition(state2, state0, 'Reset')

        return supervisor
