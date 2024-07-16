from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.State import State


class Supervisor(Automaton):
    def __init__(self, name, initial_state: State = None):
        super().__init__(name, initial_state)
        self.disablements = []

    def disable(self, event):
        if not self.is_disabled(event):
            self.disablements.append(event)

    def enable(self, event):
        if self.is_disabled(event):
            self.disablements.remove(event)

    def is_disabled(self, event):
        return event in self.disablements

    def trigger(self, event):
        if not self.is_disabled(event):
            super().trigger(event)
        else:
            print(f"Event {event} is disabled and cannot be triggered.")
