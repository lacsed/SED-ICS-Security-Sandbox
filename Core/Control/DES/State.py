class State:
    def __init__(self, num_state=0, on_enter=None, on_exit=None):
        self.num_state = num_state
        self.on_enter = on_enter
        self.on_exit = on_exit
        self.events = {}

    def enter(self):
        if self.on_enter:
            self.on_enter()

    def exit(self):
        if self.on_exit:
            self.on_exit(self)

    def add_event(self, event, next_state, on_transition=None):
        self.events[event] = (next_state, on_transition)
