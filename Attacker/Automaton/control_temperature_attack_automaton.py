from Attacker.Automaton.attack_automaton import AttackAutomaton
from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.State import State


class ControlTemperatureAttackAutomaton(AttackAutomaton):
    @staticmethod
    def initialize_automaton(trigger_event="Control_Temperature_On"):
        return AttackAutomaton.initialize_automaton(trigger_event)

        '''state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)
        state4 = State(4)
        state5 = State(5)
        state6 = State(6)

        automaton = Automaton('ControlTemperatureAttack', state0)

        automaton.add_transition(state0, state1, 'Open_Output_Valve')

        automaton.add_transition(state1, state2, 'Level_High')

        automaton.add_transition(state2, state2, 'Level_High')
        automaton.add_transition(state2, state3, 'Close_Output_Valve')

        automaton.add_transition(state3, state6, 'Control_Temperature_On')
        automaton.add_transition(state3, state4, 'Insert_Event')
        automaton.add_transition(state3, state5, 'Deny_Event')

        automaton.add_transition(state4, state6, 'Deny_Event')

        automaton.add_transition(state5, state6, 'Insert_Event')

        automaton.add_transition(state6, state0, 'Control_Temperature_On')
        automaton.add_transition(state6, state6, 'Heated')
        automaton.add_transition(state6, state6, 'Cooled')

        return automaton'''
