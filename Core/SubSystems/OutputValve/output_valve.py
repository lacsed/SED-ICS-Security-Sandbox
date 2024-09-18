import threading
import time

from Core.SubSystems.OutputValve.Automaton.output_valve_automaton import OutputValveAutomaton
from OPCClient.opc_client import OPCClient


class OutputValve(threading.Thread):
    def __init__(self, client: OPCClient):
        super().__init__()
        self.client = client
        self.output_valve_automaton = OutputValveAutomaton().initialize_automaton_with_client(self.client)

    def stop_device_process(self):
        if self.client.read_stop_process():
            while not self.client.read_start_process():
                time.sleep(1)


    def run(self):
        while not self.client.read_open_output_valve():
            self.stop_device_process()
            self.output_valve_automaton.trigger('Reset')
            time.sleep(1)

        self.stop_device_process()

        if self.client.read_open_output_valve():
            self.output_valve_automaton.trigger('Open_Output_Valve')

        while self.client.read_level_low():
            self.stop_device_process()
            self.output_valve_automaton.trigger('Level_Low')

        if self.client.read_close_output_valve():
            self.output_valve_automaton.trigger('Close_Input_Valve')
            self.output_valve_automaton.trigger('Reset')

