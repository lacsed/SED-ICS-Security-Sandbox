from colorama import init, Fore, Style

from OPCClient.opc_client import OPCClient

init()

class Mixer:
    def __init__(self, id, mixing_time, opc_client: OPCClient):
        self.id = id
        self.mixing_time = mixing_time
        self.opc_client = opc_client

    def set_mixing_time(self, mixing_time):
        self.mixing_time = mixing_time
        print(Fore.GREEN + f"[{self.id}] Mixing time set to {self.mixing_time} minutes" + Style.RESET_ALL)
    
    def start_mixing(self):
        print(Fore.GREEN + f"[{self.id}] Mixer started" + Style.RESET_ALL)
    
    def stop_mixing(self):
        print(Fore.GREEN + f"[{self.id}] Mixer stopped" + Style.RESET_ALL)
