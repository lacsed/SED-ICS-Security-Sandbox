class Valve:
    def __init__(self, id, flow, flow_rate):
        self.id = id
        self.flow = flow
        self.flow_rate = flow_rate

    def set_valve_flow_rate(self):
        self.flow_rate = self.flow_rate
        print(f"Valve flow rate set to {self.flow_rate}%")

    def set_valve_flow(self):
        self.flow *= self.flow_rate
        print(f"Valve flow rate set to {self.flow}l/s")

    def open_valve(self):
        print("Valve opened")