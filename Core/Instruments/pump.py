from colorama import init, Fore, Style

from OPCClient.opc_client import OPCClient

init()

class Pump:
    def __init__(self, id, flow, flow_rate, opc_client: OPCClient):
        self.id = id
        self.flow = flow
        self.flow_rate = flow_rate
        self.opc_client = opc_client

    def set_pump_flow_rate(self):
        self.flow_rate = self.flow_rate
        print(Fore.CYAN + f"[{self.id}] Pump flow rate set to {self.flow_rate}%" + Style.RESET_ALL)

    def set_pump_flow(self):
        self.flow *= self.flow_rate
        print(Fore.CYAN + f"[{self.id}] Pump flow set to {self.flow}l/s" + Style.RESET_ALL)

    def start_pump(self):
        print(Fore.CYAN + f"[{self.id}] Pump started" + Style.RESET_ALL)
    
    def stop_pump(self):
        print(Fore.CYAN + f"[{self.id}] Pump stopped" + Style.RESET_ALL)