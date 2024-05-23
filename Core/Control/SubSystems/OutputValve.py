import ultrades.automata as ud
from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.Supervisor import Supervisor
from colorama import init, Fore, Style

init()


class OutputValve:
    def __init__(self, valve_device, level_L1, reset, init, cooled, turn_off_tcontrol, turn_on_tcontrol,
                 valve_out=False, state_process=0):
        self.level_L1 = level_L1
        self.reset = reset
        self.init = init
        self.turn_off_tcontrol = turn_off_tcontrol
        self.turn_on_tcontrol = turn_on_tcontrol
        self.cooled = cooled
        self.valve_out = valve_out
        self.state_process = state_process
        self.valve_device = valve_device

    # Events
    open_vout = ud.event('5', True)
    close_vout = ud.event('7', True)

    # States
    vout_0 = ud.state('0')
    vout_1 = ud.state('1')

    s2_0 = ud.state('0')
    s2_1 = ud.state('1')
    s4_0 = ud.state('0')
    s4_1 = ud.state('1')
    s4_2 = ud.state('2')

    # Automatons
    vout = Automaton(vout_0)
    s2 = Supervisor(s2_0)
    s4 = Supervisor(s4_0)

    outcoming_msg = []

    def vout_0_action(self):
        self.valve_out = False
        self.valve_device.close_valve()

    def vout_1_action(self):
        self.valve_out = True
        self.state_process = 4
        self.valve_device.set_valve_flow_rate()
        self.valve_device.open_valve()

    def vout_open_vout_action(self):
        self.outcoming_msg.append(self.open_vout)

    def vout_close_vout_action(self):
        self.outcoming_msg.append(self.close_vout)

    def vout_level_l1_action(self):
        self.valve_device.set_valve_flow()

    def s2_0_action(self):
        self.s2.enable(self.close_vout)

    def s2_1_action(self):
        self.s2.disable(self.close_vout)

    def s4_0_action(self):
        self.s4.disable(self.open_vout)

    def s4_1_action(self):
        self.s4.enable(self.open_vout)

    def s4_2_action(self):
        self.s4.enable(self.open_vout)

    def create_automaton(self):
        self.s2.trigger(self.init)
        self.s4.trigger(self.init)

        print("VOUT")
        self.vout.add_transition(self.vout_0, self.vout_1, self.open_vout, self.vout_1_action)
        self.vout.add_transition(self.vout_1, self.vout_0, self.close_vout, self.vout_0_action)
        self.vout.add_transition(self.vout_1, self.vout_1, self.level_L1, self.vout_level_l1_action)
        self.vout.add_transition(self.vout_1, self.vout_0, self.reset)
        self.vout.add_transition(self.vout_0, self.vout_0, self.reset)

        print("S2")
        self.s2.add_transition(self.s2_0, self.s2_0, self.init, self.s2_0_action)
        self.s2.add_transition(self.s2_0, self.s2_1, self.open_vout, self.s2_1_action)
        self.s2.add_transition(self.s2_1, self.s2_0, self.level_L1, self.s2_0_action)
        self.s2.add_transition(self.s2_1, self.s2_0, self.reset)
        self.s2.add_transition(self.s2_0, self.s2_0, self.reset)

        print("S4")
        self.s4.add_transition(self.s4_0, self.s4_0, self.init, self.s4_0_action)
        self.s4.add_transition(self.s4_0, self.s4_1, self.cooled, self.s4_1_action)
        self.s4.add_transition(self.s4_1, self.s4_0, self.open_vout, self.s4_0_action)
        self.s4.add_transition(self.s4_1, self.s4_2, self.turn_off_tcontrol, self.s4_2_action)
        self.s4.add_transition(self.s4_2, self.s4_1, self.turn_on_tcontrol, self.s4_1_action)
        self.s4.add_transition(self.s4_2, self.s4_0, self.open_vout, self.s4_0_action)
        self.s4.add_transition(self.s4_1, self.s4_0, self.reset)
        self.s4.add_transition(self.s4_2, self.s4_0, self.reset)
        self.s4.add_transition(self.s4_0, self.s4_0, self.reset)

    def trigger_event(self, event):
        print(Fore.YELLOW + f"Triggering event: {event}" + Style.RESET_ALL)
        self.vout.trigger(event)
        self.s2.trigger(event)
        self.s4.trigger(event)