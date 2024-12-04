import random
import threading
import time

from Attacker.Arsenal.deny_event import deny_event
from Attacker.Arsenal.host_and_watch import host_and_watch
from Attacker.Arsenal.insert_event import insert_event
from Attacker.Arsenal.intercept_event import intercept_event
from Attacker.Arsenal.stealth_insert import stealth_insert
from Attacker.Automaton.attack_automaton import AttackAutomaton
from Attacker.Automaton.control_temperature_attack_automaton import ControlTemperatureAttackAutomaton
from Attacker.Automaton.input_valve_attack_automaton import InputValveAttackAutomaton
from Attacker.Automaton.mixer_attack_automaton import MixerAttackAutomaton
from Attacker.Automaton.pump_attack_automaton import PumpAttackAutomaton
from Core.Control.DES.Automaton import Automaton
from OPCServer.opc_server import OPCServer


class Attacker(threading.Thread):
    def __init__(self, server: OPCServer):
        super().__init__()
        self.server = server
        self.input_valve_attack_automaton = AttackAutomaton().initialize_automaton('Open_Input_Valve')
        self.control_temperature_attack_automaton = AttackAutomaton().initialize_automaton('Control_Temperature_On')
        self.mixer_attack_automaton = AttackAutomaton().initialize_automaton('Mixer_On')
        self.pump_attack_automaton = AttackAutomaton().initialize_automaton('Pump_On')
        self.output_valve_attack_automaton = AttackAutomaton().initialize_automaton('Open_Output_Valve')
        self.automatons = {
            "Open_Input_Valve": self.input_valve_attack_automaton,
            "Control_Temperature_On": self.control_temperature_attack_automaton,
            "Mixer_On": self.mixer_attack_automaton,
            "Pump_On": self.pump_attack_automaton,
            "Open_Output_Valve": self.output_valve_attack_automaton
        }
        self.previous_event_count = 1

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

    @staticmethod
    def random_sleep(min_time=5, max_time=30):
        time.sleep(random.uniform(min_time, max_time))

    def execute_attack(self, automaton: Automaton, attack_event):
        if self.server.query_variable(attack_event):
            chance = random.randint(1, 100)
            print(f"Probability: {chance}")

            if chance <= 50:
                automaton.trigger(attack_event)
            elif chance <= 80:
                self.server.update_variable('Release_Attack', False)
                self.server.update_under_attack(True)
                self.server.update_variable('Attack_Type', 0)
                automaton.trigger('Insert_Event')
                insert_event(self.server, attack_event)
                if random.choice([True, False]):
                    self.random_sleep()
                automaton.trigger('Deny_Event')
                deny_event(self.server, attack_event)
            else:
                self.server.update_variable('Release_Attack', False)
                self.server.update_under_attack(True)
                self.server.update_variable('Attack_Type', 0)
                automaton.trigger('Deny_Event')
                deny_event(self.server, attack_event)
                if random.choice([True, False]):
                    self.random_sleep()
                automaton.trigger('Insert_Event')
                insert_event(self.server, attack_event)

    def execute_attack_stealth(self, automaton: Automaton, attack_event):
        if self.server.query_variable(attack_event):
            chance = random.randint(1, 100)
            print(f"Probability: {chance}")

            if chance <= 70:
                automaton.trigger(attack_event)
            elif chance <= 90:
                self.server.update_variable('Release_Attack', False)
                self.server.update_under_attack(True)
                self.server.update_variable('Attack_Type', 0)
                automaton.trigger('Insert_Event')
                insert_event(self.server, attack_event)
                time.sleep(20)
                automaton.trigger('Deny_Event')
                deny_event(self.server, attack_event)
            else:
                self.server.update_variable('Release_Attack', False)
                self.server.update_under_attack(True)
                self.server.update_variable('Attack_Type', 0)
                automaton.trigger('Deny_Event')
                deny_event(self.server, attack_event)
                time.sleep(20)
                automaton.trigger('Insert_Event')
                insert_event(self.server, attack_event)

    def run(self):
        attack_mode = random.choice([0, 1])
        print(f"Attack Mode: {attack_mode}")

        while not self.server.finish_process():
            processed_events = self.server.query_processed_events()
            current_event_count = len(processed_events)

            if current_event_count > self.previous_event_count:
                self.previous_event_count = current_event_count
                last_event = processed_events[-1]
                get_automaton = self.automatons.get(last_event)
                if get_automaton is not None:
                    if attack_mode == 0:
                        self.execute_attack_stealth(get_automaton, last_event)
                    else:
                        self.execute_attack(get_automaton, last_event)
