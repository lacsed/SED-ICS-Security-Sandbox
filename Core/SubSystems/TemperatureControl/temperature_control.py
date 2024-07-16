import math
import threading
import time
from colorama import Fore, Style

from Configuration.set_points import HEATING_TEMP, INITIAL_TEMP, HEATING_TIME
from Core.SubSystems.TemperatureControl.Automaton.temperature_control_automaton import TemperatureControlAutomaton
from OPCClient.opc_client import OPCClient


class TemperatureControl(threading.Thread):
    R = 10
    C = 0.1

    def __init__(self, semaphore, client: OPCClient):
        super().__init__()
        self.semaphore = semaphore
        self.client = client
        self.temperature_control_automaton = TemperatureControlAutomaton().initialize_automaton()

    def run(self):
        current_temperature = INITIAL_TEMP

        while not self.client.read_control_temperature_on():
            self.temperature_control_automaton.trigger('Reset')
            time.sleep(1)

        if self.client.read_control_temperature_on():
            self.temperature_control_automaton.trigger('Control_Temperature_On')

        print(Fore.RED + "Heating Tank." + Style.RESET_ALL)

        while self.client.read_control_temperature_on():
            self.semaphore.acquire()
            tau = self.R * self.C

            start_time = time.time()
            time_elapsed = 0
            while time_elapsed <= HEATING_TIME:
                if self.client.read_control_temperature_off():
                    break

                time_elapsed = time.time() - start_time
                temperature = current_temperature
                temperature += (HEATING_TEMP - temperature) * (1 - math.exp(-(time_elapsed / 60) / tau))

                print(Fore.RED + f"Temperature set to {temperature:.2f}ºC." + Style.RESET_ALL)

            self.client.update_cooled(False)
            self.client.update_heated(True)

            self.semaphore.release()

            break

        while not self.client.read_control_temperature_off():
            time.sleep(1)

        if self.client.read_control_temperature_off():
            self.temperature_control_automaton.trigger('Control_Temperature_Off')

        while self.client.read_control_temperature_off():
            break
