import threading
import time

from Core.SubSystems.InputValve.Automaton.input_valve_automaton import InputValveAutomaton
from OPCClient.opc_client import OPCClient


class InputValve(threading.Thread):
    def __init__(self, client: OPCClient):
        super().__init__()
        self.client = client
        self.input_valve_automaton = InputValveAutomaton().initialize_automaton()

    def run(self):
        while not self.client.read_open_input_valve():
            self.input_valve_automaton.trigger('Reset')
            time.sleep(1)

        if self.client.read_open_input_valve():
            self.input_valve_automaton.trigger('Open_Input_Valve')

        while self.client.read_level_high():
            self.input_valve_automaton.trigger('Level_High')

        if self.client.read_close_input_valve():
            self.input_valve_automaton.trigger('Close_Input_Valve')
            self.input_valve_automaton.trigger('Reset')
