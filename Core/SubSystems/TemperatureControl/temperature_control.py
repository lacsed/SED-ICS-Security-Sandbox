import math
import threading
import time
from colorama import Fore, Style

from Configuration.set_points import HEATING_TEMP, INITIAL_TEMP, HEATING_TIME, COOLING_TEMP, COOLING_TIME
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

        self.semaphore.acquire()
        time.sleep(1)
        print(Fore.RED + "Heating Tank." + Style.RESET_ALL)

        while self.client.read_control_temperature_on():
            tau = self.R * self.C

            start_time = time.time()

            while current_temperature <= HEATING_TEMP:
                if self.client.read_control_temperature_off():
                    break

                time_elapsed = time.time() - start_time
                current_temperature += (HEATING_TEMP - INITIAL_TEMP) * (1 - math.exp(-(time_elapsed / 60) / tau))
                # self.client.update_variable("Temperature", current_temperature)

                print(Fore.RED + f"Temperature set to {current_temperature:.2f}ºC." + Style.RESET_ALL)

            self.client.update_cooled(False)
            self.client.update_heated(True)

            self.semaphore.release()

            time.sleep(HEATING_TIME)
            break

        while not self.client.read_control_temperature_off():
            time.sleep(1)

        if self.client.read_control_temperature_off():
            self.temperature_control_automaton.trigger('Control_Temperature_Off')

        self.semaphore.acquire()
        time.sleep(1)
        print(Fore.RED + "Cooling Tank." + Style.RESET_ALL)

        while self.client.read_control_temperature_off():
            tau = self.R * self.C

            start_time = time.time()

            while current_temperature >= COOLING_TEMP:
                if self.client.read_control_temperature_on():
                    break

                time_elapsed = time.time() - start_time
                current_temperature -= (COOLING_TEMP - INITIAL_TEMP) * (1 - math.exp(-(time_elapsed / 60) / tau))
                self.client.update_variable("Temperature", current_temperature)

                print(Fore.RED + f"Temperature set to {current_temperature:.2f}ºC." + Style.RESET_ALL)

            self.client.update_cooled(False)
            self.client.update_heated(True)

            self.semaphore.release()

            time.sleep(COOLING_TIME)
            break
