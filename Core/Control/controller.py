import ultrades.automata as ud
from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.DES import DES
from Core.Control.SubSystems.InputValve import InputValve
from Core.Control.SubSystems.OutputValve import OutputValve
from Core.Control.SubSystems.Mixer import Mixer
from Core.Control.SubSystems.Pump import Pump
from Core.Control.SubSystems.Temperature import Temperature
from Core.Instruments.temperature_transmitter import TemperatureTransmitter
from Core.Instruments.valve import Valve
from Core.Instruments.mixer import Mixer as MixerDevice
from Core.Instruments.pump import Pump as PumpDevice


class Controller:
    tempH1 = 50
    tempH2 = 100
    tempH3 = 200

    def __init__(self, input_valve_device: Valve,
                 output_valve_device: Valve,
                 mixer_device: MixerDevice,
                 pump_device: PumpDevice,
                 temperature_control_device: TemperatureTransmitter):
        self.input_valve_device = input_valve_device
        self.output_valve_device = output_valve_device
        self.mixer_device = mixer_device
        self.pump_device = pump_device
        self.temperature_control_device = temperature_control_device

        self.valve_in = False
        self.valve_out = False
        self.state_process = 0

        # Events
        self.init = ud.event('9', True)
        self.turn_on_tcontrol = ud.event('19', True)
        self.turn_off_tcontrol = ud.event('21', True)
        self.level_H1 = ud.event('2', False)
        self.level_L1 = ud.event('4', False)
        self.reset = ud.event('6', False)
        self.heated = ud.event('8', False)
        self.cooled = ud.event('10', False)
        self.empty = ud.event('12', False)
        self.process_start = ud.event('14', False)
        self.finish = ud.event('16', False)

        # States
        self.process_idle = ud.state('0')
        self.process_producing = ud.state('1')

        # Automatons
        self.process_system = Automaton(self.process_idle)

        self.controllable_events = {9, 19, 21}
        self.uncontrollable_events = {6, 8, 10}

        self.plant = DES(self.controllable_events, len(self.controllable_events),
                         self.uncontrollable_events, len(self.uncontrollable_events))

        self.setup()

    def process_idle_action(self):
        pass

    def process_producing_action(self):
        pass

    def setup(self):
        self.input_valve = InputValve(self.input_valve_device, self.level_H1, self.reset, self.process_start, self.finish, self.init,
                                      self.turn_on_tcontrol, self.valve_in, self.state_process)

        self.output_valve = OutputValve(self.output_valve_device, self.level_L1, self.reset, self.init, self.cooled,
                                        self.turn_off_tcontrol, self.turn_on_tcontrol, self.valve_out, self.state_process)

        self.mixer = Mixer(self.mixer_device, self.level_H1, self.reset, self.init, self.cooled, self.turn_off_tcontrol,
                           self.turn_on_tcontrol)

        self.pump = Pump(self.pump_device, self.reset, self.init, self.heated, self.cooled)

        self.temperature = Temperature(self.temperature_control_device, self.reset, self.init, self.cooled, self.heated,
                                       self.turn_off_tcontrol, self.turn_on_tcontrol)

        self.input_valve.create_automaton()
        self.input_valve.trigger_event(self.input_valve.init)
        self.input_valve.trigger_event(self.input_valve.open_vin)
        self.input_valve.trigger_event(self.input_valve.close_vin)
        self.input_valve.trigger_event(self.input_valve.reset)

        self.temperature.create_automaton()
        self.temperature.trigger_event(self.temperature.init)
        self.temperature.trigger_event(self.temperature.turn_on_tcontrol)
        self.temperature.trigger_event(self.temperature.heated)
        self.temperature.trigger_event(self.temperature.cooled)
        self.temperature.trigger_event(self.temperature.turn_off_tcontrol)
        self.temperature.trigger_event(self.temperature.reset)

        self.mixer.create_automaton()
        self.mixer.trigger_event(self.mixer.init)
        self.mixer.trigger_event(self.mixer.turn_on_mixer)
        self.mixer.trigger_event(self.mixer.turn_off_mixer)
        self.mixer.trigger_event(self.mixer.reset)

        self.output_valve.create_automaton()
        self.output_valve.trigger_event(self.output_valve.init)
        self.output_valve.trigger_event(self.output_valve.open_vout)
        self.output_valve.trigger_event(self.output_valve.close_vout)
        self.output_valve.trigger_event(self.output_valve.reset)

        self.pump.create_automaton()
        self.pump.trigger_event(self.pump.init)
        self.pump.trigger_event(self.pump.turn_on_pump)
        self.pump.trigger_event(self.pump.turn_off_pump)
        self.pump.trigger_event(self.pump.heated)
        self.pump.trigger_event(self.pump.cooled)
        self.pump.trigger_event(self.pump.reset)

        print("Process System")
        self.process_system.add_transition(self.process_idle, self.process_producing, self.turn_on_tcontrol)
        self.process_system.add_transition(self.process_producing, self.process_idle, self.turn_off_tcontrol)
        self.process_system.add_transition(self.process_producing, self.process_idle, self.reset)
        self.process_system.add_transition(self.process_idle, self.process_idle, self.reset)
