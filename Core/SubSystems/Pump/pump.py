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

    def stop_device_process(self):
        if self.client.read_stop_process():
            while not self.client.read_start_process():
                time.sleep(1)

    def run(self):
        while not self.client.read_pump_on():
            self.stop_device_process()
            self.pump_automaton.trigger('Reset')
            time.sleep(1)

        self.stop_device_process()

        self.pump_automaton.trigger('Pump_On')
        print(Fore.MAGENTA + f"Pumping tank." + Style.RESET_ALL)
        while self.client.read_pump_on():
            self.stop_device_process()
            if self.client.read_cooled():
                break

        self.client.update_pump_on(False)
        self.pump_automaton.trigger('Pump_Off')
