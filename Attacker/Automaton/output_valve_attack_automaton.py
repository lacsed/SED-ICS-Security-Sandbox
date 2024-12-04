from Attacker.Automaton.attack_automaton import AttackAutomaton
from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.State import State


class OutputValveAttackAutomaton(AttackAutomaton):
    @staticmethod
    def initialize_automaton(trigger_event="Open_Output_Valve"):
        return AttackAutomaton.initialize_automaton(trigger_event)

        '''state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)
        state4 = State(4)
        state5 = State(5)
        state6 = State(6)

        automaton = Automaton('OutputValveAttack', state0)

        automaton.add_transition(state0, state1, 'Control_Temperature_On')

        automaton.add_transition(state1, state1, 'Heated')
        automaton.add_transition(state1, state2, 'Cooled')

        automaton.add_transition(state2, state2, 'Cooled')
        automaton.add_transition(state2, state2, 'Heated')
        automaton.add_transition(state2, state3, 'Control_Temperature_Off')

        automaton.add_transition(state3, state6, 'Open_Output_Valve')
        automaton.add_transition(state3, state4, 'Insert_Event')
        automaton.add_transition(state3, state5, 'Deny_Event')

        automaton.add_transition(state4, state6, 'Deny_Event')

        automaton.add_transition(state5, state6, 'Insert_Event')

        automaton.add_transition(state6, state0, 'Close_Output_Valve')
        automaton.add_transition(state6, state6, 'Level_Low')

        return automaton'''
