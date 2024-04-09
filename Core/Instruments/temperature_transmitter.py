import math
from colorama import init, Fore, Style

init()


class TemperatureTransmitter:
    R = 10
    C = 0.1

    def __init__(self, id, initial_temperature, current_temperature, final_temperature, heating_time):
        self.id = id
        self.initial_temperature = initial_temperature
        self.current_temperature = current_temperature
        self.final_temperature = final_temperature
        self.heating_time = heating_time
    
    def set_initial_temperature(self, initial_temperature):
        self.initial_temperature = initial_temperature
        print(Fore.BLUE + f"[{self.id}] Initial temperature set to {self.initial_temperature} °C" + Style.RESET_ALL)
    
    def set_current_temperature(self, current_temperature):
        self.current_temperature = current_temperature
        print(Fore.BLUE + f"[{self.id}] Current temperature set to {self.current_temperature} °C" + Style.RESET_ALL)
    
    def set_final_temperature(self, final_temperature):
        self.final_temperature = final_temperature
        print(Fore.BLUE + f"[{self.id}] Final temperature set to {self.final_temperature} °C" + Style.RESET_ALL)
    
    def set_heating_time(self, heating_time):
        self.heating_time = heating_time
        print(Fore.BLUE + f"[{self.id}] Heating time set to {self.heating_time} minutes" + Style.RESET_ALL)

    def initialize_heating_circuit(self):
        tau = TemperatureTransmitter.R * TemperatureTransmitter.C
        time_seconds = self.heating_time * 60
        temperature = self.current_temperature

        for t in range(int(time_seconds)):
            temperature += (self.final_temperature - temperature) * (1 - math.exp(-1 / tau))
            self.set_current_temperature(temperature)
            print(Fore.BLUE + f"[{self.id}] Time: {t / 60} minutes, Temperature: {temperature:.2f} °C" + Style.RESET_ALL)

        self.set_final_temperature(self.current_temperature)

        return temperature

    def start_heating(self):
        print(Fore.BLUE + f"[{self.id}] Heating started" + Style.RESET_ALL)

    def stop_heating(self):
        print(Fore.BLUE + f"[{self.id}] Heating stopped" + Style.RESET_ALL)
