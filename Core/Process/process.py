import threading
import time

from Core.Process.Automaton.process_automaton import ProcessAutomaton
from OPCClient.opc_client import OPCClient


class Process(threading.Thread):
    def __init__(self, semaphore, client: OPCClient):
        super().__init__()
        self.semaphore = semaphore
        self.client = client
        self.process_automaton = ProcessAutomaton().initialize_automaton()

    def run(self):
        while not self.client.read_start_process():
            self.process_automaton.trigger('Reset')
            time.sleep(1)

        if self.client.read_start_process():
            time.sleep(1)
            self.semaphore.acquire()
            self.process_automaton.trigger('Start_Process')
            print("Process started.")
            self.semaphore.release()

        if self.client.read_finish_process():
            self.process_automaton.trigger('Finish_Process')
            self.process_automaton.trigger('Reset')
