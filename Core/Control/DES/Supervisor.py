from Core.Control.DES.Automaton import Automaton


class Supervisor(Automaton):
    def __init__(self, initial_state):
        super().__init__(initial_state)
        self.disablements = {}

    def disable(self, event):
        self.disablements[event] = True

    def enable(self, event):
        self.disablements[event] = False

    def is_disabled(self, event):
        return self.disablements.get(event, False)