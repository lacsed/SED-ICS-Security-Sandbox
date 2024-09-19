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
        self.running = True
        self.stopped = False

    def stop_device_process(self):
        if self.client.read_stop_process():
            while not self.client.read_start_process():
                time.sleep(1)

    def run(self):
        while not self.client.read_start_process():
            self.stop_device_process()
            self.process_automaton.trigger('Reset')
            time.sleep(1)

        while self.running:
            self.stop_device_process()

            if self.client.read_start_process() and not self.stopped:
                time.sleep(1)
                self.semaphore.acquire()
                self.process_automaton.trigger('Start_Process')
                self.client.update_start_process(False)
                self.semaphore.release()

            if self.client.read_finish_process():
                self.semaphore.acquire()
                self.process_automaton.trigger('Finish_Process')
                self.process_automaton.trigger('Reset')
                self.semaphore.release()
                break

            if self.client.read_stop_process():
                if not self.stopped:
                    self.semaphore.acquire()
                    self.stopped = True
                    self.semaphore.release()
                continue

            if self.client.read_reset():
                self.semaphore.acquire()
                self.stopped = False
                self.semaphore.release()
