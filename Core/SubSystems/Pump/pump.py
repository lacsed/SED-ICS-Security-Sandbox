import threading
import time
from colorama import Fore, Style

from Core.SubSystems.Pump.Automaton.pump_automaton import PumpAutomaton
from OPCClient.opc_client import OPCClient


class Pump(threading.Thread):
    def __init__(self, client: OPCClient):
        super().__init__()
        self.client = client
        self.pump_automaton = PumpAutomaton().initialize_automaton()
        self.location = "Pump_Location"

    def run(self):
        printer_count = 0

        while not self.client.read_pump_on():
            self.pump_automaton.trigger('Reset')
            time.sleep(1)

        self.pump_automaton.trigger('Pump_On')
        while self.client.read_pump_on():
            if self.client.read_cooled():
                break

            printer_count += 1
            if printer_count == 100:
                print(Fore.MAGENTA + f"Pumping tank." + Style.RESET_ALL)
                printer_count = 0

        self.client.update_pump_on(False)
        self.pump_automaton.trigger('Pump_Off')
