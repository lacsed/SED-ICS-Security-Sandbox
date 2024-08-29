import threading
import time
from colorama import Fore, Style

from Core.SubSystems.Mixer.Automaton.mixer_automaton import MixerAutomaton
from OPCClient.opc_client import OPCClient


class Mixer(threading.Thread):
    def __init__(self, client: OPCClient):
        super().__init__()
        self.client = client
        self.mixer_automaton = MixerAutomaton().initialize_automaton()
        self.location = "Mixer_Location"

    def run(self):
        printer_count = 0
        mixing_time = self.client.query_variable('Mixing_Time')

        while not self.client.read_mixer_on():
            self.mixer_automaton.trigger('Reset')
            time.sleep(1)

        self.mixer_automaton.trigger('Mixer_On')
        while self.client.read_mixer_on():
            start_time = time.time()
            time_elapsed = 0

            while time_elapsed <= mixing_time:
                if self.client.read_mixer_off():
                    break

                time_elapsed = time.time() - start_time
                printer_count += 1

                if printer_count == 150:
                    print(Fore.CYAN + f"Mixing tank." + Style.RESET_ALL)
                    printer_count = 0

            self.client.update_mixer_on(False)
            time.sleep(1)

        if self.client.read_mixer_off():
            self.mixer_automaton.trigger('Mixer_Off')
