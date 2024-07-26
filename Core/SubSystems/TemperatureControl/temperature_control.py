import threading
import time

from Configuration.set_points import HEATING_TEMP, INITIAL_TEMP, HEATING_TIME, COOLING_TEMP, COOLING_TIME
from Core.SubSystems.TemperatureControl.Automaton.temperature_control_automaton import TemperatureControlAutomaton
from OPCClient.opc_client import OPCClient


class TemperatureControl(threading.Thread):
    def __init__(self, semaphore, client: OPCClient):
        super().__init__()
        self.semaphore = semaphore
        self.client = client
        self.temperature_control_automaton = TemperatureControlAutomaton().initialize_automaton()

    def run(self):
        while not self.client.read_control_temperature_on():
            self.temperature_control_automaton.trigger('Reset')
            time.sleep(1)

        if self.client.read_control_temperature_on():
            self.temperature_control_automaton.trigger('Control_Temperature_On')

        while self.client.read_control_temperature_on():
            self.semaphore.acquire()
            if self.client.query_variable('Temperature') >= HEATING_TEMP:
                self.client.update_cooled(False)
                self.client.update_heated(True)
            if self.client.read_heated():
                if self.client.query_variable('Temperature') <= COOLING_TEMP:
                    self.client.update_cooled(True)
                    self.client.update_heated(False)
            self.semaphore.release()


        while not self.client.read_control_temperature_off():
            time.sleep(1)

        if self.client.read_control_temperature_off():
            self.temperature_control_automaton.trigger('Control_Temperature_Off')
