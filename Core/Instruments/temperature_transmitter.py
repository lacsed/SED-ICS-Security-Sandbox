import math
from colorama import init, Fore, Style

from OPCClient.opc_client import OPCClient

init()


class TemperatureTransmitter:
    R = 500
    C = 0.02

    def __init__(self, id, initial_temperature, current_temperature, final_temperature, heating_time, opc_client: OPCClient):
        self.id = id
        self.initial_temperature = initial_temperature
        self.current_temperature = current_temperature
        self.final_temperature = final_temperature
        self.heating_time = heating_time
        self.opc_client = opc_client
    
    def set_initial_temperature(self, initial_temperature):
        self.initial_temperature = initial_temperature
        print(Fore.RED + f"[{self.id}] Initial temperature set to {self.initial_temperature:.2f} °C" + Style.RESET_ALL)
    
    def set_current_temperature(self, current_temperature):
        self.current_temperature = current_temperature
        print(Fore.RED + f"[{self.id}] Current temperature set to {self.current_temperature:.2f} °C" + Style.RESET_ALL)
    
    def set_final_temperature(self, final_temperature):
        self.final_temperature = final_temperature
        print(Fore.RED + f"[{self.id}] Final temperature set to {self.final_temperature:.2f} °C" + Style.RESET_ALL)
    
    def set_heating_time(self, heating_time):
        self.heating_time = heating_time
        print(Fore.RED + f"[{self.id}] Heating time set to {self.heating_time} minutes" + Style.RESET_ALL)

    def initialize_heating_circuit(self, time_elapsed):
        tau = TemperatureTransmitter.R * TemperatureTransmitter.C
        temperature = self.current_temperature

        temperature += (self.final_temperature - temperature) * (1 - math.exp(-(time_elapsed/60) / tau))
        self.set_current_temperature(temperature)

        return temperature

    def start_heating(self):
        print(Fore.RED + f"[{self.id}] Heating started" + Style.RESET_ALL)

    def stop_heating(self):
        print(Fore.RED + f"[{self.id}] Heating stopped" + Style.RESET_ALL)
