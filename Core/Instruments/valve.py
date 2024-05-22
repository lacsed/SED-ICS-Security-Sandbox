from colorama import init, Fore, Style

init()


class Valve:
    def __init__(self, id, flow, flow_rate):
        self.id = id
        self.flow = flow
        self.flow_rate = flow_rate

    def set_valve_flow_rate(self):
        self.flow_rate = self.flow_rate
        print(Fore.MAGENTA + f"[{self.id}] Valve flow rate set to {self.flow_rate}%" + Style.RESET_ALL)

    def set_valve_flow(self):
        self.flow *= self.flow_rate
        print(Fore.MAGENTA + f"[{self.id}] Valve flow set to {self.flow}l/s" + Style.RESET_ALL)

    def open_valve(self):
        print(Fore.MAGENTA + f"[{self.id}] Valve opened" + Style.RESET_ALL)

    def close_valve(self):
        print(Fore.MAGENTA + f"[{self.id}] Valve closed" + Style.RESET_ALL)