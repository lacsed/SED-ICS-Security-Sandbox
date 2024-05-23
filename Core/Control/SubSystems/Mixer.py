import ultrades.automata as ud
from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.Supervisor import Supervisor
from colorama import init, Fore, Style

init()


class Mixer:
    def __init__(self, mixer_device, level_H1, reset, init, cooled, turn_off_tcontrol, turn_on_tcontrol, mixed=False):
        self.level_H1 = level_H1
        self.reset = reset
        self.init = init
        self.turn_off_tcontrol = turn_off_tcontrol
        self.turn_on_tcontrol = turn_on_tcontrol
        self.cooled = cooled
        self.mixed = mixed
        self.mixer_device = mixer_device

    # Events
    turn_on_mixer = ud.event('11', True)
    turn_off_mixer = ud.event('13', True)

    # States
    mixer_0 = ud.state('0')
    mixer_1 = ud.state('1')

    s5_0 = ud.state('0')
    s5_1 = ud.state('1')
    s5_2 = ud.state('2')
    s6_0 = ud.state('0')
    s6_1 = ud.state('1')
    s6_2 = ud.state('2')

    # Automatons
    mixer = Automaton(mixer_0)
    s5 = Supervisor(s5_0)
    s6 = Supervisor(s6_0)

    outcoming_msg = []

    def mixer_0_action(self):
        self.mixed = False
        self.mixer_device.stop_mixing()

    def mixer_1_action(self):
        self.mixed = True
        self.mixer_device.set_mixing_time(20)
        self.mixer_device.start_mixing()

    def mixer_turn_on_action(self):
        self.outcoming_msg.append(self.turn_on_mixer)

    def mixer_turn_off_action(self):
        self.outcoming_msg.append(self.turn_off_mixer)

    def s5_0_action(self):
        self.s5.disable(self.turn_on_mixer)

    def s5_1_action(self):
        self.s5.enable(self.turn_on_mixer)

    def s5_2_action(self):
        self.s5.enable(self.turn_on_mixer)

    def s6_0_action(self):
        self.s6.disable(self.turn_off_mixer)

    def s6_1_action(self):
        self.s6.enable(self.turn_off_mixer)

    def s6_2_action(self):
        self.s6.enable(self.turn_off_mixer)

    def create_automaton(self):
        self.s5.trigger(self.init)
        self.s6.trigger(self.init)

        print("MIXER")
        self.mixer.add_transition(self.mixer_0, self.mixer_1, self.turn_on_mixer, self.mixer_1_action)
        self.mixer.add_transition(self.mixer_1, self.mixer_0, self.turn_off_mixer, self.mixer_0_action)
        self.mixer.add_transition(self.mixer_1, self.mixer_0, self.reset)
        self.mixer.add_transition(self.mixer_0, self.mixer_0, self.reset)

        print("S5")
        self.s5.add_transition(self.s5_0, self.s5_0, self.init, self.s5_0_action)
        self.s5.add_transition(self.s5_0, self.s5_1, self.level_H1, self.s5_1_action)
        self.s5.add_transition(self.s5_1, self.s5_2, self.turn_on_mixer, self.s5_2_action)
        self.s5.add_transition(self.s5_2, self.s5_0, self.turn_off_mixer, self.s5_0_action)
        self.s5.add_transition(self.s5_2, self.s5_1, self.level_H1, self.s5_1_action)
        self.s5.add_transition(self.s5_1, self.s5_0, self.reset)
        self.s5.add_transition(self.s5_2, self.s5_0, self.reset)
        self.s5.add_transition(self.s5_0, self.s5_0, self.reset)

        print("S6")
        self.s6.add_transition(self.s6_0, self.s6_0, self.init, self.s6_0_action)
        self.s6.add_transition(self.s6_0, self.s6_1, self.cooled, self.s6_1_action)
        self.s6.add_transition(self.s6_1, self.s6_0, self.turn_off_mixer, self.s6_0_action)
        self.s6.add_transition(self.s6_2, self.s6_0, self.turn_off_mixer, self.s6_0_action)
        self.s6.add_transition(self.s6_1, self.s6_2, self.turn_off_tcontrol, self.s6_2_action)
        self.s6.add_transition(self.s6_2, self.s6_1, self.turn_on_tcontrol, self.s6_1_action)
        self.s6.add_transition(self.s6_1, self.s6_0, self.reset)
        self.s6.add_transition(self.s6_2, self.s6_0, self.reset)
        self.s6.add_transition(self.s6_0, self.s6_0, self.reset)

    def trigger_event(self, event):
        print(Fore.YELLOW + f"Triggering event: {event}" + Style.RESET_ALL)
        self.mixer.trigger(event)
        self.s5.trigger(event)
        self.s6.trigger(event)