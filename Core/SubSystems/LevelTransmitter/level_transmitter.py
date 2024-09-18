import threading
import time

from OPCClient.opc_client import OPCClient


class LevelTransmitter(threading.Thread):
    def __init__(self, client: OPCClient):
        super().__init__()
        self.client = client

    def stop_device_process(self):
        if self.client.read_stop_process():
            while not self.client.read_start_process():
                time.sleep(1)

    def run(self):
        while self.client.query_variable('Level') < 100:
            self.stop_device_process()
            time.sleep(1)

        self.stop_device_process()

        while self.client.read_open_input_valve():
            self.stop_device_process()
            if self.client.query_variable('Level') >= 100:
                self.client.update_level_low(False)
                self.client.update_level_high(True)
            self.client.update_open_input_valve(False)

        while self.client.query_variable('Level') > 0:
            self.stop_device_process()
            time.sleep(1)

        while self.client.read_open_output_valve():
            self.stop_device_process()
            if self.client.query_variable('Level') <= 0:
                self.client.update_level_high(False)
                self.client.update_level_low(True)
            self.client.update_open_output_valve(False)
            self.client.update_finish_process(True)
