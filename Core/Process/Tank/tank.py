import math
import threading
import time
from colorama import Fore, Style

from Configuration.set_points import TANK_CAPACITY
from OPCClient.opc_client import OPCClient


class Tank:
    R = 10
    C = 0.1

    def __init__(self, client: OPCClient):
        self.client = client

        self.fill_tank_thread = self.FillTankThread(self)
        self.empty_tank_thread = self.EmptyTankThread(self)
        self.heating_thread = self.HeatingThread(self)
        self.cooling_thread = self.CoolingThread(self)

    class FillTankThread(threading.Thread):
        def __init__(self, control):
            super().__init__()
            self.control = control

        def stop_tank_process(self):
            if self.control.client.read_stop_process():
                while not self.control.client.read_start_process():
                    time.sleep(1)

        def run(self):
            control = self.control
            current_volume = control.client.query_variable('Volume')

            while not control.client.read_open_input_valve():
                time.sleep(1)

            time.sleep(1)
            print("Filling Tank.")

            self.stop_tank_process()

            while control.client.read_open_input_valve():
                self.stop_tank_process()

                current_volume += 10
                level = (current_volume / TANK_CAPACITY) * 100
                control.client.update_variable("Level", level)
                control.client.update_variable("Volume", current_volume)
                print(Fore.BLUE + f"Level in {level:.2f}% of capacity" + Style.RESET_ALL)
                time.sleep(0.5)

                if level == 100:
                    break

                time.sleep(1)

    class EmptyTankThread(threading.Thread):
        def __init__(self, control):
            super().__init__()
            self.control = control

        def stop_tank_process(self):
            if self.control.client.read_stop_process():
                while not self.control.client.read_start_process():
                    time.sleep(1)

        def run(self):
            control = self.control

            while not control.client.read_open_output_valve():
                time.sleep(1)

            time.sleep(1)
            print("Emptying Tank.")
            current_volume = control.client.query_variable('Volume')

            self.stop_tank_process()

            while control.client.read_open_output_valve():
                self.stop_tank_process()

                current_volume -= 10
                level = (current_volume / TANK_CAPACITY) * 100
                control.client.update_variable("Level", level)
                control.client.update_variable("Volume", current_volume)
                print(Fore.BLUE + f"Level in {level:.2f}% of capacity" + Style.RESET_ALL)
                time.sleep(0.5)

                if level == 0:
                    break

                time.sleep(1)

    class HeatingThread(threading.Thread):
        def __init__(self, control):
            super().__init__()
            self.control = control

        def stop_tank_process(self):
            if self.control.client.read_stop_process():
                while not self.control.client.read_start_process():
                    time.sleep(1)

        def get_tau_value(self):
            R = 5
            C = 0.05
            if self.control.read_mixer_on():
                R = 10
                C = 0.1

            return R * C

        def run(self):
            control = self.control
            heating_temperature = control.client.query_variable('Heating_Temperature')
            initial_temperature = control.client.query_variable('Initial_Temperature')
            heating_time = control.client.query_variable('Heating_Time')

            while not control.client.read_control_temperature_on():
                time.sleep(1)

            print(Fore.RED + "Heating Tank." + Style.RESET_ALL)
            time.sleep(1)

            self.stop_tank_process()

            while control.client.read_control_temperature_on():
                self.stop_tank_process()

                start_time = time.time()
                time_elapsed = 0
                current_temperature = control.client.query_variable('Temperature')

                while (time_elapsed/100000) < heating_time:
                    self.stop_tank_process()

                    if control.client.read_control_temperature_off():
                        break
                    if current_temperature < heating_temperature:
                        time_elapsed = time.time() - start_time
                        current_temperature += (heating_temperature - initial_temperature) * (1 - math.exp(-(time_elapsed / 60) / (control.R * control.C)))
                        control.client.update_variable("Temperature", current_temperature)

                break


    class CoolingThread(threading.Thread):
        def __init__(self, control):
            super().__init__()
            self.control = control

        def stop_tank_process(self):
            if self.control.client.read_stop_process():
                while not self.control.client.read_start_process():
                    time.sleep(1)

        def get_tau_value(self):
            if self.control.read_pump_on():
                R = 1
                C = 0.01
            else:
                R = 1
                C = 0.1

            return R * C

        def run(self):
            control = self.control
            heating_temperature = control.client.query_variable('Heating_Temperature')
            cooling_temperature = control.client.query_variable('Cooling_Temperature')
            cooling_time = control.client.query_variable('Cooling_Time')

            while control.client.query_variable('Temperature') < heating_temperature:
                time.sleep(1)

            print(Fore.RED + "Cooling Tank." + Style.RESET_ALL)
            time.sleep(1)

            self.stop_tank_process()

            while control.client.read_control_temperature_on():
                self.stop_tank_process()

                start_time = time.time()
                time_elapsed = 0
                current_temperature = control.client.query_variable('Temperature')

                tau = 2 * 0.02

                while (time_elapsed/100000) < cooling_time:
                    self.stop_tank_process()

                    if control.client.read_control_temperature_off():
                        break
                    if current_temperature > cooling_temperature:
                        time_elapsed = time.time() - start_time
                        current_temperature = cooling_temperature + (current_temperature - cooling_temperature) * math.exp(-time_elapsed / (60 * tau))
                        control.client.update_variable("Temperature", current_temperature)

                break

    def start_threads(self):
        self.fill_tank_thread.start()
        self.empty_tank_thread.start()
        self.heating_thread.start()
        self.cooling_thread.start()

    def join_threads(self):
        self.fill_tank_thread.join()
        self.empty_tank_thread.join()
        self.heating_thread.join()
        self.cooling_thread.join()
