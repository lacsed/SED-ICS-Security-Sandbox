import random
import threading
import time

from Attacker.Arsenal.deny_event import deny_event
from Attacker.Arsenal.host_and_watch import host_and_watch
from Attacker.Arsenal.insert_event import insert_event
from Attacker.Arsenal.intercept_event import intercept_event
from Attacker.Arsenal.stealth_insert import stealth_insert
from Attacker.Automaton.input_valve_attack_automaton import InputValveAttackAutomaton
from OPCServer.opc_server import OPCServer


class Attacker(threading.Thread):
    def __init__(self, server: OPCServer):
        super().__init__()
        self.server = server
        self.input_valve_attack_automaton = InputValveAttackAutomaton().initialize_automaton()

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

    def run(self):
        while not self.server.open_input_valve():
            self.input_valve_attack_automaton.trigger('Reset')
            time.sleep(1)

        if self.server.open_input_valve():
            chance = random.randint(1, 100)
            print(f"Probability: {chance}")

            if chance <= 70:
                self.server.update_variable('Release_Attack', False)
                self.server.update_under_attack(True)
                self.server.update_variable('Attack_Type', 0)
                self.input_valve_attack_automaton.trigger('Insert_Event')
                insert_event(self.server, 'Open_Input_Valve')
                time.sleep(20)
                self.input_valve_attack_automaton.trigger('Deny_Event')
                deny_event(self.server, 'Open_Input_Valve')
            elif chance <= 90:
                self.input_valve_attack_automaton.trigger('Open_Input_Valve')
            else:
                self.server.update_variable('Release_Attack', False)
                self.server.update_under_attack(True)
                self.server.update_variable('Attack_Type', 0)
                self.input_valve_attack_automaton.trigger('Deny_Event')
                deny_event(self.server, 'Open_Input_Valve')
                time.sleep(20)
                self.input_valve_attack_automaton.trigger('Insert_Event')
                insert_event(self.server, 'Open_Input_Valve')
