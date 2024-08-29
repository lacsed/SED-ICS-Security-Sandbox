import threading
import time

from OPCClient.opc_client import OPCClient


class LevelTransmitter(threading.Thread):
    def __init__(self, client: OPCClient):
        super().__init__()
        self.client = client
        self.location = "Level_Location"

    def run(self):
        while self.client.query_variable('Level') < 100:
            time.sleep(1)

        while self.client.read_open_input_valve():
            if self.client.query_variable('Level') >= 100:
                self.client.update_level_low(False)
                self.client.update_level_high(True)
            self.client.update_open_input_valve(False)

        while self.client.query_variable('Level') > 0:
            time.sleep(1)

        while self.client.read_open_output_valve():
            if self.client.query_variable('Level') <= 0:
                self.client.update_level_high(False)
                self.client.update_level_low(True)
            self.client.update_open_output_valve(False)
            self.client.update_finish_process(True)
