import threading
import time
from colorama import Fore, Style

from Configuration.set_points import PUMPING_TIME
from Core.SubSystems.Pump.Automaton.pump_automaton import PumpAutomaton
from OPCClient.opc_client import OPCClient


class Pump(threading.Thread):
    def __init__(self, semaphore, client: OPCClient):
        super().__init__()
        self.semaphore = semaphore
        self.client = client
        self.pump_automaton = PumpAutomaton().initialize_automaton()

    def run(self):
        while not self.client.read_pump_on():
            self.pump_automaton.trigger('Reset')
            time.sleep(1)

        self.pump_automaton.trigger('Pump_On')
        while self.client.read_pump_on():
            self.semaphore.acquire()

            start_time = time.time()
            time_elapsed = 0

            while time_elapsed <= PUMPING_TIME:
                if self.client.read_pump_off():
                    break

                time_elapsed = time.time() - start_time
                print(Fore.MAGENTA + f"Pumping tank." + Style.RESET_ALL)

            self.semaphore.release()

        if self.client.read_pump_off():
            self.pump_automaton.trigger('Pump_Off')
