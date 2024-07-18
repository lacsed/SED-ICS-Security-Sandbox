import threading
import time
from colorama import Fore, Style

from Configuration.set_points import MIXING_TIME
from Core.SubSystems.Mixer.Automaton.mixer_automaton import MixerAutomaton
from OPCClient.opc_client import OPCClient


class Mixer(threading.Thread):
    def __init__(self, semaphore, client: OPCClient):
        super().__init__()
        self.semaphore = semaphore
        self.client = client
        self.mixer_automaton = MixerAutomaton().initialize_automaton()

    def run(self):
        printer_count = 0

        while not self.client.read_mixer_on():
            self.mixer_automaton.trigger('Reset')
            time.sleep(1)

        self.mixer_automaton.trigger('Mixer_On')
        while self.client.read_mixer_on():
            self.semaphore.acquire()

            start_time = time.time()
            time_elapsed = 0

            while time_elapsed <= MIXING_TIME:
                if self.client.read_mixer_off():
                    break

                time_elapsed = time.time() - start_time
                printer_count += 1

                if printer_count == 150:
                    print(Fore.CYAN + f"Mixing tank." + Style.RESET_ALL)
                    printer_count = 0

            self.semaphore.release()

        if self.client.read_mixer_off():
            self.mixer_automaton.trigger('Mixer_Off')
