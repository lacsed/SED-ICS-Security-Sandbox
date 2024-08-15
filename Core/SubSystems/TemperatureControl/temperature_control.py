import threading
import time

from Core.SubSystems.TemperatureControl.Automaton.temperature_control_automaton import TemperatureControlAutomaton
from OPCClient.opc_client import OPCClient


class TemperatureControl(threading.Thread):
    def __init__(self, semaphore, client: OPCClient):
        super().__init__()
        self.semaphore = semaphore
        self.client = client
        self.temperature_control_automaton = TemperatureControlAutomaton().initialize_automaton()
        self.location = "Temperature_Location"

    def run(self):
        heating_temperature = self.client.query_variable('Heating_Temperature')
        cooling_temperature = self.client.query_variable('Cooling_Temperature')

        while not self.client.read_control_temperature_on():
            self.temperature_control_automaton.trigger('Reset')
            time.sleep(1)

        if self.client.read_control_temperature_on():
            self.temperature_control_automaton.trigger('Control_Temperature_On')

        while self.client.read_control_temperature_on():
            self.semaphore.acquire()
            if self.client.query_variable('Temperature') >= heating_temperature:
                self.client.update_cooled(False)
                self.client.update_heated(True)
            if self.client.read_heated():
                if self.client.query_variable('Temperature') <= cooling_temperature:
                    self.client.update_cooled(True)
                    self.client.update_heated(False)
            self.semaphore.release()


        while not self.client.read_control_temperature_off():
            time.sleep(1)

        if self.client.read_control_temperature_off():
            self.temperature_control_automaton.trigger('Control_Temperature_Off')
