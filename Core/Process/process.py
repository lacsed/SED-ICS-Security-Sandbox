import threading
import time

from Core.Process.Automaton.process_automaton import ProcessAutomaton
from OPCClient.opc_client import OPCClient


class Process(threading.Thread):
    def __init__(self, semaphore, client: OPCClient):
        super().__init__()
        self.semaphore = semaphore
        self.client = client
        self.process_automaton = ProcessAutomaton()

    def run(self):
        while self.client.read_init() is not True:
            time.sleep(1)

        time.sleep(1)
        self.semaphore.acquire()
        self.client.update_start_process(True)
        self.semaphore.release()

        print("Process started.")
