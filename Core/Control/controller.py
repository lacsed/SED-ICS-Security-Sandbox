import threading
import time
from collections import deque

from colorama import Fore, Style

from Atacker.attacker import Attacker
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
        self.location = "Controller_Location"

    def run(self):
        controlable_events = ['Open_Input_Valve', 'Close_Input_Valve',
                              'Open_Output_Valve', 'Close_Output_Valve',
                              'Control_Temperature_On', 'Control_Temperature_Off',
                              'Mixer_On', 'Mixer_Off', 'Pump_On', 'Pump_Off', 'Reset']

        uncontrolable_events = ['Level_High', 'Level_Low', 'Heated', 'Cooled',
                                'Start_Process', 'Finish_Process']

        control = DES(controlable_events, controlable_events.__len__(),
                      uncontrolable_events, uncontrolable_events.__len__())

        # Supervisors
        open_input_valve_supervisor = OpenInputValveSupervisor().initialize_supervisor()
        control.add_supervisor(open_input_valve_supervisor)

        close_input_valve_supervisor = CloseInputValveSupervisor().initialize_supervisor()
        control.add_supervisor(close_input_valve_supervisor)

        open_output_valve_supervisor = OpenOutputValveSupervisor().initialize_supervisor()
        control.add_supervisor(open_output_valve_supervisor)

        close_output_valve_supervisor = CloseOutputValveSupervisor().initialize_supervisor()
        control.add_supervisor(close_output_valve_supervisor)

        starting_mixer_supervisor = StartingMixerSupervisor().initialize_supervisor()
        control.add_supervisor(starting_mixer_supervisor)

        stopping_mixer_supervisor = StoppingMixerSupervisor().initialize_supervisor()
        control.add_supervisor(stopping_mixer_supervisor)

        starting_pump_supervisor = StartingPumpSupervisor().initialize_supervisor()
        control.add_supervisor(starting_pump_supervisor)

        stopping_pump_supervisor = StoppingPumpSupervisor().initialize_supervisor()
        control.add_supervisor(stopping_pump_supervisor)

        starting_control_temperature_supervisor = StartingTemperatureControlSupervisor().initialize_supervisor()
        control.add_supervisor(starting_control_temperature_supervisor)

        stopping_control_temperature_supervisor = StoppingTemperatureControlSupervisor().initialize_supervisor()
        control.add_supervisor(stopping_control_temperature_supervisor)

        # Automatons
        process_automaton = ProcessAutomaton().initialize_automaton()
        control.add_plant(process_automaton)

        input_valve_automaton = InputValveAutomaton().initialize_automaton()
        control.add_plant(input_valve_automaton)

        output_valve_automaton = OutputValveAutomaton().initialize_automaton()
        control.add_plant(output_valve_automaton)

        mixer_automaton = MixerAutomaton().initialize_automaton()
        control.add_plant(mixer_automaton)

        pump_automaton = PumpAutomaton().initialize_automaton()
        control.add_plant(pump_automaton)

        temperature_control_automaton = TemperatureControlAutomaton().initialize_automaton()
        control.add_plant(temperature_control_automaton)

        control.update_des()
        control.supervisor_states()

        while not self.server.start_process():
            time.sleep(1)

        def process_uncontrolable_events():
            for uncontrolable_event in uncontrolable_events:
                if self.server.query_variable(uncontrolable_event):
                    for sup in control.supervisors:
                        if sup.is_feasible(uncontrolable_event):
                            sup.trigger(uncontrolable_event)

        def process_event(current_event):
            processed_events = set(self.server.query_processed_events())

            if current_event in processed_events:
                return

            possible_plants = [plant for plant in control.plants if plant.is_defined(event)]
            time.sleep(0.01)

            event_processed = False
            for plant in possible_plants:
                if plant.is_feasible(current_event):
                    if any(sup.is_disabled(current_event) for sup in control.supervisors):
                        print(f"Event {event} is disabled by a supervisor and cannot be triggered.")
                    else:
                        plant.trigger(current_event)
                        control.trigger_supervisors(current_event)
                        control.update_des()
                        self.server.update_variable(current_event, True)
                        time.sleep(0.01)
                        print(Fore.LIGHTWHITE_EX + f"Event '{current_event}' executed successfully." + Style.RESET_ALL)
                        self.server.add_to_processed_events(current_event)
                        event_processed = True
                        break
                else:
                    print(Fore.LIGHTWHITE_EX + f"Event '{current_event}' is not feasible in the current state of the plant '{plant.name}'." + Style.RESET_ALL)

            if not event_processed:
                self.server.add_to_unprocessed_events(current_event)

            self.semaphore.acquire()
            process_uncontrolable_events()
            time.sleep(0.01)
            self.semaphore.release()

        while not self.server.finish_process():
            unprocessed_events = deque(self.server.query_unprocessed_events())
            while unprocessed_events:
                event = unprocessed_events.popleft()
                process_event(event)

            for event in controlable_events:
                process_event(event)

        print("Process Finished.")
