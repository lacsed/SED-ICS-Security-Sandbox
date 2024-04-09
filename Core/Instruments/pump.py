from colorama import init, Fore, Style

init()

class Pump:
    def __init__(self, id, flow, flow_rate):
        self.id = id
        self.flow = flow
        self.flow_rate = flow_rate

    def set_pump_flow_rate(self):
        self.flow_rate = self.flow_rate
        print(Fore.YELLOW + f"[{self.id}] Pump flow rate set to {self.flow_rate}%" + Style.RESET_ALL)

    def set_pump_flow(self):
        self.flow *= self.flow_rate
        print(Fore.YELLOW + f"[{self.id}] Pump flow set to {self.flow}l/s" + Style.RESET_ALL)

    def start_pump(self):
        print(Fore.YELLOW + f"[{self.id}] Pump started" + Style.RESET_ALL)
    
    def stop_pump(self):
        print(Fore.YELLOW + f"[{self.id}] Pump stopped" + Style.RESET_ALL)