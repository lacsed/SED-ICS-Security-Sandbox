from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.Supervisor import Supervisor


class DES:
    def __init__(self, controllable_events, num_c_events, uncontrollable_events, num_u_events):
        self.next_event = None
        self.list_size = None
        self.action_list = None
        self.mode = None
        self.plants = []
        self.supervisors = []
        self.num_plants = 0
        self.num_sups = 0
        self.controllable_events = controllable_events
        self.uncontrollable_events = uncontrollable_events
        self.num_c_events = num_c_events
        self.num_u_events = num_u_events
        self.enabled_events_status = [1] * num_c_events

    def add_plant(self, plant: Automaton):
        self.plants.append(plant)
        self.num_plants += 1

    def supervisor_states(self):
        for supervisor in self.supervisors:
            state = supervisor.current_state_num()

    def add_supervisor(self, sup: Supervisor):
        self.supervisors.append(sup)
        self.num_sups += 1

    def trigger_if_possible(self, event):
        if any(plant.is_defined(event) for plant in self.plants):
            if any(plant.is_feasible(event) for plant in self.plants):
                if any(supervisor.is_disabled(event) for supervisor in self.supervisors):
                    print(f"Event {event} is disabled by a supervisor and cannot be triggered.")
                    return False
                else:
                    # Trigger in all plants and supervisors
                    for plant in self.plants:
                        plant.trigger(event)

                    for supervisor in self.supervisors:
                        supervisor.trigger(event)

                    self.update_des()
        return True

    def trigger_supervisors(self, event):
        for supervisor in self.supervisors:
            if supervisor.is_feasible(event):
                supervisor.trigger(event)

    def enabled_events(self):
        for i in range(self.num_c_events):
            self.enabled_events_status[i] = 1

        for i, controllable_event in enumerate(self.controllable_events):
            not_defined = True
            for plant in self.plants:
                if plant.is_defined(controllable_event):
                    not_defined = False
                    if plant.is_feasible(controllable_event):
                        for supervisor in self.supervisors:
                            if supervisor.is_disabled(controllable_event):
                                self.enabled_events_status[i] = 0
                                break
                    else:
                        self.enabled_events_status[i] = 0
                        break
            if not_defined:
                self.enabled_events_status[i] = 0

    def update_des(self):
        self.enabled_events()

        if self.next_event is not None and self.enabled_events_status[self.next_event] == 1:
            for plant in self.plants:
                plant.trigger(self.action_list[self.next_event])

            for supervisor in self.supervisors:
                supervisor.trigger(self.action_list[self.next_event])

            self.next_event += 1
            if self.next_event >= self.list_size:
                self.next_event = 0
