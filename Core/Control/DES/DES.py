class DES:
    RANDOM = 1
    PRIORITY = 2
    LIST = 3

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
        self.enabled_events = [1] * num_c_events

    def add_plant(self, plant):
        self.plants.append(plant)
        self.num_plants += 1

    def supervisor_states(self):
        for supervisor in self.supervisors:
            print(supervisor.current_state_num())
        print()

    def add_supervisor(self, sup):
        self.supervisors.append(sup)
        self.num_sups += 1

    def trigger_if_possible(self, event):
        if any(supervisor.is_disabled(event) for supervisor in self.supervisors):
            return False

        for plant in self.plants:
            plant.trigger(event)

        for supervisor in self.supervisors:
            supervisor.trigger(event)

        self.update_des()
        return True

    def trigger_supervisors(self, event):
        for supervisor in self.supervisors:
            supervisor.trigger(event)

    def enabled_events(self):
        for i in range(self.num_c_events):
            self.enabled_events[i] = 1

        for i, controllable_event in enumerate(self.controllable_events):
            not_defined = True
            for plant in self.plants:
                if plant.is_defined(controllable_event):
                    not_defined = False
                    if plant.is_feasible(controllable_event):
                        for supervisor in self.supervisors:
                            if supervisor.is_disabled(controllable_event):
                                self.enabled_events[i] = 0
                                break
                    else:
                        self.enabled_events[i] = 0
                        break
            if not_defined:
                self.enabled_events[i] = 0

    def set_mode(self, mode, lst=None):
        self.mode = mode

        if mode == self.LIST and lst:
            self.action_list = lst
            self.list_size = len(lst)
            self.next_event = 0

    def update_des(self):
        self.enabled_events()

        if self.mode == self.LIST:
            if self.enabled_events[self.next_event] == 1:
                for plant in self.plants:
                    plant.trigger(self.action_list[self.next_event])

                for supervisor in self.supervisors:
                    supervisor.trigger(self.action_list[self.next_event])

                self.next_event += 1
                if self.next_event >= self.list_size:
                    self.next_event = 0
