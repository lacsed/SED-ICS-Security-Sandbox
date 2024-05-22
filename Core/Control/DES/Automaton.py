import ultrades.automata as ud

from Core.Control.DES.Transition import Transition


class Automaton:
    def __init__(self, initial_state: ud.state):
        self.current_state = initial_state
        self.transitions = []
        self.num_transitions = 0

    def add_transition(self, state_from, state_to, event, on_transition=None):
        if state_from is None or state_to is None:
            return

        transition = Transition(state_from, state_to, event, on_transition)
        self.transitions.append(transition)
        self.num_transitions += 1

    def trigger(self, event):
        for transition in self.transitions:
            if transition.state_from == self.current_state and transition.event == event:
                self.current_state = transition.make_transition()
                return

    def is_defined(self, event):
        return any(event == transition.event for transition in self.transitions)

    def is_feasible(self, event):
        return any(
            event == transition.event and transition.state_from == self.current_state
            for transition in self.transitions
        )

    def current_state_num(self):
        return self.current_state
