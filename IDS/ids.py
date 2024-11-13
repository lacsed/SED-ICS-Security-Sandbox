import threading
import time

from OPCClient.opc_client import OPCClient
from IDS.process_sequence import process_sequence

class IDS(threading.Thread):
    def __init__(self, client: OPCClient):
        super().__init__()
        self.client = client
        self.current_index = 0
        self.previous_event_count = 0

    def check_event_sequence(self, processed_events):
        while self.current_index < len(process_sequence):
            if len(processed_events) > self.current_index:
                if processed_events[self.current_index] == process_sequence[self.current_index]:
                    print(f"Event '{processed_events[self.current_index]}' is in correct order.")
                    self.current_index += 1
                else:
                    print("Attack detected!!!")
                    self.client.attack_detected(True)
                    break
            else:
                break

    def run(self):
        processed_events = []

        while not self.client.read_finish_process():
            processed_events = self.client.query_processed_events()
            current_event_count = len(processed_events)

            if current_event_count > self.previous_event_count:
                self.check_event_sequence(processed_events)
                self.previous_event_count = current_event_count

            time.sleep(1)

        print(processed_events)
