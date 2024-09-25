import threading
import time

from Core.SubSystems.TemperatureControl.Automaton.temperature_control_automaton import TemperatureControlAutomaton
from OPCClient.opc_client import OPCClient


class TemperatureControl(threading.Thread):
    def __init__(self, client: OPCClient):
        super().__init__()
        self.client = client
        self.temperature_control_automaton = TemperatureControlAutomaton().initialize_automaton()

    def stop_device_process(self):
        if self.client.read_stop_process():
            while not self.client.read_start_process():
                time.sleep(1)

    def run(self):
        heating_temperature = self.client.query_variable('Heating_Temperature')
        cooling_temperature = self.client.query_variable('Cooling_Temperature')

        while not self.client.read_control_temperature_on():
            self.stop_device_process()
            self.temperature_control_automaton.trigger('Reset')
            time.sleep(1)

        self.stop_device_process()

        if self.client.read_control_temperature_on():
            self.temperature_control_automaton.trigger('Control_Temperature_On')

        while not self.client.read_control_temperature_off():
            self.stop_device_process()
            if self.client.query_variable('Temperature') >= (heating_temperature - 15):
                self.client.update_cooled(False)
                self.client.update_heated(True)
            if self.client.read_heated():
                if self.client.query_variable('Temperature') <= cooling_temperature:
                    self.client.update_cooled(True)
                    self.client.update_heated(False)

        if self.client.read_control_temperature_off():
            self.client.update_control_temperature_on(False)
            self.temperature_control_automaton.trigger('Control_Temperature_Off')
