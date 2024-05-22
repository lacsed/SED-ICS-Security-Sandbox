import ultrades.automata as ud
from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.Supervisor import Supervisor
from Core.Instruments.temperature_transmitter import TemperatureTransmitter
from colorama import init, Fore, Style

init()


class Temperature:
    def __init__(self, temp_id, initial_temperature, current_temperature, final_temperature, heating_time, reset, init, cooled, heated, turn_off_tcontrol, turn_on_tcontrol, state_process=0):
        self.reset = reset
        self.init = init
        self.turn_off_tcontrol = turn_off_tcontrol
        self.turn_on_tcontrol = turn_on_tcontrol
        self.cooled = cooled
        self.heated = heated
        self.state_process = state_process
        self.temp_device = TemperatureTransmitter(temp_id, initial_temperature, current_temperature, final_temperature, heating_time)

    # Events
    turn_on_tcontrol = ud.event('19', True)
    turn_off_tcontrol = ud.event('21', True)

    # States
    temp_0 = ud.state('0')
    temp_1 = ud.state('1')

    s10_0 = ud.state('0')
    s10_1 = ud.state('1')
    s10_2 = ud.state('2')

    # Automatons
    temp = Automaton(temp_0)
    s10 = Supervisor(s10_0)

    outcoming_msg = []

    def temp_0_action(self):
        self.temp_device.stop_heating()

    def temp_1_action(self):
        self.temp_device.start_heating()
        temperature = self.temp_device.initialize_heating_circuit(5)
        print(Fore.RED + f"[{self.temp_device.id}] Temperature after heating: {temperature:.2f} °C" + Style.RESET_ALL)

    def temp_turn_on_tcontrol_action(self):
        self.outcoming_msg.append(self.turn_on_tcontrol)
        self.state_process = 2
        self.temp_device.start_heating()
        self.temp_device.set_initial_temperature(self.temp_device.initial_temperature)
        self.temp_device.set_final_temperature(self.temp_device.final_temperature)
        self.temp_device.set_heating_time(self.temp_device.heating_time)

    def temp_turn_off_tcontrol_action(self):
        self.outcoming_msg.append(self.turn_off_tcontrol)
        self.temp_device.stop_heating()

    def temp_heated_action(self):
        self.state_process = 3

    def temp_cooled_action(self):
        self.temp_device.set_current_temperature(self.temp_device.initial_temperature)

    def s10_0_action(self):
        self.s10.enable(self.turn_off_tcontrol)

    def s10_1_action(self):
        self.s10.disable(self.turn_off_tcontrol)

    def s10_2_action(self):
        self.s10.disable(self.turn_off_tcontrol)

    def create_automaton(self):
        self.s10.trigger(self.init)

        print("TEMP")
        self.temp.add_transition(self.temp_0, self.temp_1, self.turn_on_tcontrol, self.temp_turn_on_tcontrol_action)
        self.temp.add_transition(self.temp_1, self.temp_1, self.heated, self.temp_heated_action)
        self.temp.add_transition(self.temp_1, self.temp_1, self.cooled, self.temp_cooled_action)
        self.temp.add_transition(self.temp_1, self.temp_0, self.turn_off_tcontrol, self.temp_turn_off_tcontrol_action)
        self.temp.add_transition(self.temp_1, self.temp_0, self.reset)
        self.temp.add_transition(self.temp_0, self.temp_0, self.reset)

        print("S10")
        self.s10.add_transition(self.s10_0, self.s10_0, self.init)
        self.s10.add_transition(self.s10_0, self.s10_1, self.turn_on_tcontrol)
        self.s10.add_transition(self.s10_1, self.s10_2, self.heated)
        self.s10.add_transition(self.s10_2, self.s10_0, self.cooled)
        self.s10.add_transition(self.s10_1, self.s10_0, self.reset)
        self.s10.add_transition(self.s10_2, self.s10_0, self.reset)
        self.s10.add_transition(self.s10_0, self.s10_0, self.reset)

    def trigger_event(self, event):
        print(Fore.YELLOW + f"Triggering event: {event}" + Style.RESET_ALL)
        self.temp.trigger(event)
        self.s10.trigger(event)