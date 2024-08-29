import threading
import time

from Atacker.Arsenal.deny_event import deny_event
from Atacker.Arsenal.host_and_watch import host_and_watch
from Atacker.Arsenal.inject_event import inject_event
from Atacker.Arsenal.intercept_event import intercept_event
from OPCServer.opc_server import OPCServer


class Attacker(threading.Thread):
    def __init__(self, semaphore, server: OPCServer):
        super().__init__()
        self.server = server
        self.semaphore = semaphore

    def run(self):
        attack_handlers = {
            0: deny_event,
            1: host_and_watch,
            2: inject_event,
            3: intercept_event
        }

        while self.server.query_variable('Attack_Type') is not None:
            attack_type = self.server.query_variable('Attack_Type')

            if attack_type in attack_handlers:
                attack_handlers[attack_type](self.server)
            else:
                raise ValueError("Invalid attack type specified.")
