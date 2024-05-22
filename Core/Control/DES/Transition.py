import ultrades.automata as ud


class Transition:
    def __init__(self, state_from, state_to, event, on_transition=None):
        self.state_from = state_from
        self.state_to = state_to
        self.event = event
        self.on_transition = on_transition

    def make_transition(self):
        if self.on_transition is not None:
            self.on_transition()
        return self.state_to
