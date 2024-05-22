import ultrades.automata as ud
from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.Supervisor import Supervisor
from Core.Instruments.valve import Valve
from colorama import init, Fore, Style

init()


class InputValve:
    def __init__(self, valve_id, flow, flow_rate, level_H1, reset, process_start, finish, init, turn_on_tcontrol,
                 valve_in=False, state_process=0):
        self.valve_in = valve_in
        self.state_process = state_process
        self.level_H1 = level_H1
        self.reset = reset
        self.process_start = process_start
        self.finish = finish
        self.init = init
        self.turn_on_tcontrol = turn_on_tcontrol
        self.valve = Valve(valve_id, flow, flow_rate)

    # Events
    open_vin = ud.event('1', True)
    close_vin = ud.event('3', True)

    # States
    vin_0 = ud.state('0')
    vin_1 = ud.state('1')

    s1_0 = ud.state('0')
    s1_1 = ud.state('1')
    s3_0 = ud.state('0')
    s3_1 = ud.state('1')
    s3_2 = ud.state('2')
    s9_0 = ud.state('0')
    s9_1 = ud.state('1')
    s9_2 = ud.state('2')

    # Automatons
    vin = Automaton(vin_0)
    s1 = Supervisor(s1_0)
    s3 = Supervisor(s3_0)
    s9 = Supervisor(s9_0)

    outcoming_msg = []

    def vin_0_action(self):
        self.valve_in = False
        self.valve.close_valve()

    def vin_1_action(self):
        self.valve_in = True
        self.state_process = 1
        self.valve.set_valve_flow_rate()
        self.valve.open_valve()

    def vin_level_h1_action(self):
        self.valve.set_valve_flow()

    def vin_open_vin_action(self):
        self.outcoming_msg.append(self.open_vin)

    def vin_close_vin_action(self):
        self.outcoming_msg.append(self.close_vin)

    def s1_0_action(self):
        self.s1.enable(self.close_vin)

    def s1_1_action(self):
        self.s1.disable(self.close_vin)

    def s3_0_action(self):
        self.s3.disable(self.open_vin)

    def s3_1_action(self):
        self.s3.enable(self.open_vin)

    def s3_2_action(self):
        self.s3.enable(self.open_vin)

    def s9_0_action(self):
        self.s9.disable(self.turn_on_tcontrol)

    def s9_1_action(self):
        self.s9.enable(self.turn_on_tcontrol)

    def s9_2_action(self):
        pass

    def create_automaton(self):
        self.s1.trigger(self.init)
        self.s3.trigger(self.init)
        self.s9.trigger(self.init)

        print("VIN")
        self.vin.add_transition(self.vin_0, self.vin_1, self.open_vin, self.vin_1_action)
        self.vin.add_transition(self.vin_1, self.vin_0, self.close_vin, self.vin_0_action)
        self.vin.add_transition(self.vin_1, self.vin_1, self.level_H1, self.vin_level_h1_action)
        self.vin.add_transition(self.vin_1, self.vin_0, self.reset)
        self.vin.add_transition(self.vin_0, self.vin_0, self.reset)

        print("S1")
        self.s1.add_transition(self.s1_0, self.s1_0, self.init, self.s1_0_action)
        self.s1.add_transition(self.s1_0, self.s1_1, self.open_vin, self.s1_1_action)
        self.s1.add_transition(self.s1_1, self.s1_0, self.level_H1, self.s1_0_action)
        self.s1.add_transition(self.s1_1, self.s1_0, self.reset)
        self.s1.add_transition(self.s1_0, self.s1_0, self.reset)

        print("S3")
        self.s3.add_transition(self.s3_0, self.s3_0, self.init, self.s3_0_action)
        self.s3.add_transition(self.s3_0, self.s3_1, self.process_start, self.s3_1_action)
        self.s3.add_transition(self.s3_1, self.s3_0, self.open_vin, self.s3_0_action)
        self.s3.add_transition(self.s3_1, self.s3_2, self.finish, self.s3_2_action)
        self.s3.add_transition(self.s3_2, self.s3_0, self.open_vin, self.s3_0_action)
        self.s3.add_transition(self.s3_1, self.s3_0, self.reset)
        self.s3.add_transition(self.s3_2, self.s3_0, self.reset)
        self.s3.add_transition(self.s3_0, self.s3_0, self.reset)

        print("S9")
        self.s9.add_transition(self.s9_0, self.s9_0, self.init, self.s9_0_action)
        self.s9.add_transition(self.s9_0, self.s9_1, self.level_H1, self.s9_1_action)
        self.s9.add_transition(self.s9_1, self.s9_0, self.turn_on_tcontrol, self.s9_0_action)
        self.s9.add_transition(self.s9_1, self.s9_2, self.close_vin, self.s9_2_action)
        self.s9.add_transition(self.s9_2, self.s9_1, self.open_vin, self.s9_1_action)
        self.s9.add_transition(self.s9_2, self.s9_0, self.turn_on_tcontrol, self.s9_0_action)
        self.s9.add_transition(self.s9_1, self.s9_0, self.reset)
        self.s9.add_transition(self.s9_2, self.s9_0, self.reset)
        self.s9.add_transition(self.s9_0, self.s9_0, self.reset)

    def trigger_event(self, event):
        print(Fore.YELLOW + f"Triggering event: {event}" + Style.RESET_ALL)
        self.vin.trigger(event)
        self.s1.trigger(event)
        self.s3.trigger(event)
        self.s9.trigger(event)