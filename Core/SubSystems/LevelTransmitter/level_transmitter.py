import threading
import time
from colorama import Fore, Style

from OPCClient.opc_client import OPCClient
from Configuration.set_points import TANK_CAPACITY


class LevelTransmitter(threading.Thread):
    def __init__(self, semaphore, client: OPCClient):
        super().__init__()
        self.semaphore = semaphore
        self.client = client

    def run(self):
        current_volume = 0

        while not self.client.read_open_input_valve():
            time.sleep(1)

        self.semaphore.acquire()
        print("Filling Tank.")
        while self.client.read_open_input_valve():
            current_volume += 10
            level = (current_volume / TANK_CAPACITY) * 100
            print(Fore.BLUE + f"Level in {level:.2f}% of capacity" + Style.RESET_ALL)

            if level == 100:
                self.client.update_level_low(False)
                self.client.update_level_high(True)
                break

            time.sleep(1)

        self.semaphore.release()

        while not self.client.read_open_output_valve():
            time.sleep(1)

        # pegar variavel do servodor no pump e decrementar

        self.semaphore.acquire()
        print("Emptying Tank.")
        while self.client.read_open_output_valve():
            current_volume -= 10
            level = (current_volume / TANK_CAPACITY) * 100
            print(Fore.BLUE + f"Level in {level:.2f}% of capacity" + Style.RESET_ALL)

            if level == 0:
                self.client.update_level_high(False)
                self.client.update_level_low(True)
                break

            time.sleep(1)

        self.semaphore.release()
