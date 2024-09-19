import threading
import time
from collections import deque

from colorama import Fore, Style

from Attacker.attacker import Attacker
from Core.Control.DES.DES import DES
from Core.SubSystems.InputValve.Automaton.input_valve_automaton import InputValveAutomaton
from Core.SubSystems.InputValve.Supervisors.close_input_valve_supervisor import CloseInputValveSupervisor
from Core.SubSystems.InputValve.Supervisors.open_input_valve_supervisor import OpenInputValveSupervisor
from Core.SubSystems.Mixer.Automaton.mixer_automaton import MixerAutomaton
from Core.SubSystems.Mixer.Supervisors.starting_mixer_supervisor import StartingMixerSupervisor
from Core.SubSystems.Mixer.Supervisors.stopping_mixer_supervisor import StoppingMixerSupervisor
from Core.SubSystems.OutputValve.Automaton.output_valve_automaton import OutputValveAutomaton
from Core.SubSystems.OutputValve.Supervisors.close_output_valve_supervisor import CloseOutputValveSupervisor
from Core.SubSystems.OutputValve.Supervisors.open_output_valve_supervisor import OpenOutputValveSupervisor
from Core.Process.Automaton.process_automaton import ProcessAutomaton
from Core.SubSystems.Pump.Automaton.pump_automaton import PumpAutomaton
from Core.SubSystems.Pump.Supervisors.starting_pump_supervisor import StartingPumpSupervisor
from Core.SubSystems.Pump.Supervisors.stopping_pump_supervisor import StoppingPumpSupervisor
from Core.SubSystems.TemperatureControl.Automaton.temperature_control_automaton import TemperatureControlAutomaton
from Core.SubSystems.TemperatureControl.Supervisors.starting_temperature_control_supervisor import \
    StartingTemperatureControlSupervisor
from Core.SubSystems.TemperatureControl.Supervisors.stopping_temperature_control_supervisor import \
    StoppingTemperatureControlSupervisor
from OPCServer.opc_server import OPCServer


class Controller(threading.Thread):
    def __init__(self, semaphore, server: OPCServer):
        super().__init__()
        self.semaphore = semaphore
        self.server = server
        self.controlable_events = ['Open_Input_Valve', 'Close_Input_Valve',
                                   'Open_Output_Valve', 'Close_Output_Valve',
                                   'Control_Temperature_On', 'Control_Temperature_Off',
                                   'Mixer_On', 'Mixer_Off', 'Pump_On', 'Pump_Off', 'Reset']
        self.uncontrolable_events = ['Level_High', 'Level_Low', 'Heated', 'Cooled',
                                     'Start_Process', 'Finish_Process']
        self.control = DES(self.controlable_events, len(self.controlable_events),
                           self.uncontrolable_events, len(self.uncontrolable_events))
        self.attacker = Attacker(self.server)

    def initialize_supervisors(self):
        supervisors = [
            OpenInputValveSupervisor(), CloseInputValveSupervisor(),
            OpenOutputValveSupervisor(), CloseOutputValveSupervisor(),
            StartingMixerSupervisor(), StoppingMixerSupervisor(),
            StartingPumpSupervisor(), StoppingPumpSupervisor(),
            StartingTemperatureControlSupervisor(), StoppingTemperatureControlSupervisor()
        ]
        for supervisor in supervisors:
            self.control.add_supervisor(supervisor.initialize_supervisor())

    def initialize_automatons(self):
        automatons = [
            ProcessAutomaton(), InputValveAutomaton(),
            OutputValveAutomaton(), MixerAutomaton(),
            PumpAutomaton(), TemperatureControlAutomaton()
        ]
        for automaton in automatons:
            self.control.add_plant(automaton.initialize_automaton())

    def process_deny_event_attack(self):
        if self.server.under_attack():
            if self.server.deny_attack():
                self.attacker.attacker_handler()


    def process_attacks(self):
        if self.server.under_attack():
            if self.server.intercept_attack():
                self.attacker.attacker_handler()
            elif self.server.host_and_watch_attack():
                self.attacker.attacker_handler()

    def process_insert_event_attack(self):
        if self.server.under_attack():
            if self.server.insert_attack():
                self.attacker.attacker_handler()
                self.server.update_under_attack(False)

    def process_event(self, event):
        # Process Attacks
        self.process_attacks()
        processed_events = set(self.server.query_processed_events())
        if event in processed_events:
            return

        possible_plants = [plant for plant in self.control.plants if plant.is_defined(event)]
        time.sleep(0.01)
        event_processed = False

        for plant in possible_plants:
            if plant.is_feasible(event) and not any(sup.is_disabled(event) for sup in self.control.supervisors):
                plant.trigger(event)
                self.control.trigger_supervisors(event)
                self.control.update_des()
                self.server.update_variable(event, True)
                # Process Attacks
                self.process_deny_event_attack()
                time.sleep(0.01)
                print(Fore.LIGHTWHITE_EX + f"Event '{event}' executed successfully." + Style.RESET_ALL)
                self.server.add_to_processed_events(event)
                event_processed = True
                break
            else:
                print(Fore.LIGHTWHITE_EX + f"Event '{event}' is not feasible in the current state of the plant '{plant.name}'." + Style.RESET_ALL)

        if not event_processed:
            self.server.add_to_unprocessed_events(event)

        self.semaphore.acquire()
        self.process_uncontrolable_events()
        time.sleep(0.01)
        self.semaphore.release()

    def process_uncontrolable_events(self):
        for uncontrolable_event in self.uncontrolable_events:
            if self.server.query_variable(uncontrolable_event):
                for sup in self.control.supervisors:
                    if sup.is_feasible(uncontrolable_event):
                        sup.trigger(uncontrolable_event)

    def run(self):
        self.initialize_supervisors()
        self.initialize_automatons()

        self.control.update_des()
        self.control.supervisor_states()

        while not self.server.start_process():
            time.sleep(1)

        while not self.server.finish_process():
            unprocessed_events = deque(self.server.query_unprocessed_events())

            if self.server.stop_process():
                while not self.server.start_process():
                    time.sleep(1)

            while unprocessed_events:
                # Process attack
                self.process_insert_event_attack()
                event = unprocessed_events.popleft()
                self.process_event(event)

            for event in self.controlable_events:
                self.process_event(event)

        print("Finished batch.")
