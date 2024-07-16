from Core.Control.DES.State import State


class Automaton:
    def __init__(self, name, initial_state: State = None):
        self.current_state = initial_state
        self.name = name
        self.events = []
        if initial_state:
            self.current_state.enter()

    def set_initial_state(self, initial_state: State):
        if not self.current_state:
            self.current_state = initial_state
            self.current_state.enter()

    @staticmethod
    def add_transition(state_from: State, state_to: State, event, on_transition=None):
        state_from.add_event(event, state_to, on_transition)

    def trigger(self, event):
        if event in self.current_state.events:
            next_state, on_transition = self.current_state.events[event]
            self.current_state.exit()
            if on_transition:
                on_transition()
            self.current_state = next_state
            self.current_state.enter()

    def is_defined(self, event):
        return event in self.current_state.events

    def is_feasible(self, event):
        return event in self.current_state.events

    def current_state_num(self):
        return self.current_state.num_state

    def possible_events(self):
        if self.current_state is None:
            raise ValueError("The initial state has not defined for the automaton.")
        return list(self.current_state.events.keys())
