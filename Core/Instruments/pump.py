class Pump:
    def __init__(self, id, flow, flow_rate):
        self.id = id
        self.flow = flow
        self.flow_rate = flow_rate

    def set_pump_flow_rate(self):
        self.flow_rate = self.flow_rate
        print(f"Pump flow rate set to {self.flow_rate}%")

    def set_pump_flow(self):
        self.flow *= self.flow_rate
        print(f"Pump flow set to {self.flow}l/s")

    def start_pump(self):
        print("Pump started")
    
    def stop_pump(self):
        print("Pump stopped")