class Pump:
    def __init__(self, id, flow, flow_rate):
        self.id = id
        self.flow = flow
        self.flow_rate = flow_rate

    def set_pump_flow(self):
        self.flow *= self.flow_rate
        print(f"Pump flow set to {self.flow}l/s")