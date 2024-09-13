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

        while not self.client.read_mixer_on():
            self.mixer_automaton.trigger('Reset')
            time.sleep(1)

        self.mixer_automaton.trigger('Mixer_On')
        while self.client.read_mixer_on():
            if self.client.read_heated():
                break

            printer_count += 1
            if printer_count == 150:
                print(Fore.CYAN + f"Mixing tank." + Style.RESET_ALL)
                printer_count = 0

        self.client.update_mixer_on(False)
        self.mixer_automaton.trigger('Mixer_Off')
