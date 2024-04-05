class Valve:
    def __init__(self, id, flow, flow_rate):
        self.id = id
        self.flow = flow
        self.flow_rate = flow_rate

    def set_valve_flow(self):
        self.flow *= self.flow_rate
        print(f"Valve flow set to {self.flow}l/s")