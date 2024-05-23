import ultrades.automata as ud
from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.Supervisor import Supervisor
from colorama import init, Fore, Style


init()


class Temperature:
    def __init__(self, temperature_device, reset, init, cooled, heated, turn_off_tcontrol, turn_on_tcontrol, state_process=0):
        self.reset = reset
        self.init = init
        self.turn_off_tcontrol = turn_off_tcontrol
        self.turn_on_tcontrol = turn_on_tcontrol
        self.cooled = cooled
        self.heated = heated
        self.state_process = state_process
        self.temp_device = temperature_device

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
        print("Executing temp_0_action")
        self.temp_device.stop_heating()

    def temp_1_action(self):
        if self.temp_device.opc_client.start_heating_process:
            print("Heating process started on the server.")
        else:
            print("Failed to start the heating process on the server.")

        self.temp_device.start_heating()
        self.temp_device.set_initial_temperature(self.temp_device.initial_temperature)
        self.temp_device.set_final_temperature(self.temp_device.final_temperature)
        self.temp_device.set_heating_time(self.temp_device.heating_time)

        print(f"Activate device '{self.temp_device.id}'...")

        time_in_seconds = self.temp_device.heating_time * 60
        time_elapsed = 0

        for t in range(int(time_in_seconds)):
            time_elapsed += 1
            seconds = t % 60

            if time_elapsed == 10:
                current_temp = self.temp_device.initialize_heating_circuit(t)
                print(
                    Fore.RED + f"[{self.temp_device.id}] Time: {int(t / 60)}m {seconds}s, Temperature: {current_temp:.2f} °C" + Style.RESET_ALL)
                self.temp_device.opc_client.write_variable("temperature", self.temp_device.current_temperature)
                time_elapsed = 0

                if current_temp >= self.temp_device.final_temperature:
                    print(
                        Fore.RED + f"Desired temperature {self.temp_device.final_temperature:.2f} °C reached." + Style.RESET_ALL)
                    self.temp.trigger(self.turn_off_tcontrol)
                    break

        self.temp_device.stop_heating()
        print(f"Tank '{self.temp_device.id}' heated to {self.temp_device.current_temperature:.2f}°C.")

    def temp_turn_on_tcontrol_action(self):
        print("Executing temp_turn_on_tcontrol_action")
        self.outcoming_msg.append(self.turn_on_tcontrol)
        self.state_process = 2
        self.temp_device.start_heating()
        self.temp_1_action()

    def temp_turn_off_tcontrol_action(self):
        print("Executing temp_turn_off_tcontrol_action")
        self.outcoming_msg.append(self.turn_off_tcontrol)
        self.temp_device.stop_heating()
        self.temp_0_action()

    def temp_heated_action(self):
        print("Executing temp_heated_action")
        self.state_process = 3

    def temp_cooled_action(self):
        print("Executing temp_cooled_action")
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