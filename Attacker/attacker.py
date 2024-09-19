from Attacker.Arsenal.deny_event import deny_event
from Attacker.Arsenal.host_and_watch import host_and_watch
from Attacker.Arsenal.insert_event import insert_event
from Attacker.Arsenal.intercept_event import intercept_event
from Attacker.Arsenal.stealth_insert import stealth_insert
from OPCServer.opc_server import OPCServer


class Attacker:
    def __init__(self, server: OPCServer):
        super().__init__()
        self.server = server

    def attacker_handler(self):
        attack_handlers = {
            0: deny_event,
            1: host_and_watch,
            2: insert_event,
            3: intercept_event,
            4: stealth_insert
        }

        attack_type = self.server.get_attack_type()

        if attack_type in attack_handlers:
            attack_handlers[attack_type](self.server)
        else:
            raise ValueError("Invalid attack type specified.")
