import ultrades.automata as ud
from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.Supervisor import Supervisor
from colorama import init, Fore, Style

init()


class Pump:
    def __init__(self, pump_device, reset, init, heated, cooled, pumped=False):
        self.reset = reset
        self.init = init
        self.heated = heated
        self.cooled = cooled
        self.pumped = pumped
        self.pump_device = pump_device

    # Events
    turn_on_pump = ud.event('15', True)
    turn_off_pump = ud.event('17', True)

    # States
    pump_0 = ud.state('0')
    pump_1 = ud.state('1')

    s7_0 = ud.state('0')
    s7_1 = ud.state('1')
    s7_2 = ud.state('2')
    s8_0 = ud.state('0')
    s8_1 = ud.state('1')
    s8_2 = ud.state('2')

    # Automatons
    pump = Automaton(pump_0)
    s7 = Supervisor(s7_0)
    s8 = Supervisor(s8_0)

    outcoming_msg = []

    def pump_0_action(self):
        self.pumped = False
        self.pump_device.stop_pump()

    def pump_1_action(self):
        self.pumped = True
        self.pump_device.start_pump()

    def pump_turn_on_action(self):
        self.outcoming_msg.append(self.turn_on_pump)

    def pump_turn_off_action(self):
        self.outcoming_msg.append(self.turn_off_pump)

    def s7_0_action(self):
        self.s7.disable(self.turn_on_pump)

    def s7_1_action(self):
        self.s7.enable(self.turn_on_pump)

    def s7_2_action(self):
        pass

    def s8_0_action(self):
        pass

    def s8_1_action(self):
        self.s8.enable(self.turn_off_pump)

    def s8_2_action(self):
        self.s8.disable(self.turn_off_pump)

    def create_automaton(self):
        self.s7.trigger(self.init)
        self.s8.trigger(self.init)

        print("PUMP")
        self.pump.add_transition(self.pump_0, self.pump_1, self.turn_on_pump, self.pump_1_action)
        self.pump.add_transition(self.pump_1, self.pump_0, self.turn_off_pump, self.pump_0_action)
        self.pump.add_transition(self.pump_1, self.pump_0, self.reset)
        self.pump.add_transition(self.pump_0, self.pump_0, self.reset)

        print("S7")
        self.s7.add_transition(self.s7_0, self.s7_0, self.init)
        self.s7.add_transition(self.s7_0, self.s7_1, self.heated)
        self.s7.add_transition(self.s7_1, self.s7_2, self.turn_on_pump)
        self.s7.add_transition(self.s7_2, self.s7_1, self.heated)
        self.s7.add_transition(self.s7_2, self.s7_0, self.turn_off_pump)
        self.s7.add_transition(self.s7_1, self.s7_0, self.reset)
        self.s7.add_transition(self.s7_2, self.s7_0, self.reset)
        self.s7.add_transition(self.s7_0, self.s7_0, self.reset)

        print("S8")
        self.s8.add_transition(self.s8_0, self.s8_0, self.init)
        self.s8.add_transition(self.s8_0, self.s8_1, self.cooled)
        self.s8.add_transition(self.s8_1, self.s8_0, self.turn_off_pump)
        self.s8.add_transition(self.s8_0, self.s8_2, self.turn_on_pump)
        self.s8.add_transition(self.s8_2, self.s8_1, self.cooled)
        self.s8.add_transition(self.s8_1, self.s8_0, self.reset)
        self.s8.add_transition(self.s8_2, self.s8_0, self.reset)
        self.s8.add_transition(self.s8_0, self.s8_0, self.reset)

    def trigger_event(self, event):
        print(Fore.YELLOW + f"Triggering event: {event}" + Style.RESET_ALL)
        self.pump.trigger(event)
        self.s7.trigger(event)
        self.s8.trigger(event)