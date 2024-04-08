import math


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
        print(f"Initial temperature set to {self.initial_temperature} °C")
    
    def set_current_temperature(self, current_temperature):
        self.current_temperature = current_temperature
        print(f"Current temperature set to {self.current_temperature} °C")
    
    def set_final_temperature(self, final_temperature):
        self.final_temperature = final_temperature
        print(f"Final temperature set to {self.final_temperature} °C")
    
    def set_heating_time(self, heating_time):
        self.heating_time = heating_time
        print(f"Heating time set to {self.heating_time} minutes")

    def initialize_heating_circuit(self):
        tau = TemperatureTransmitter.R * TemperatureTransmitter.C
        time_seconds = self.heating_time * 60
        temperature = self.current_temperature

        for t in range(int(time_seconds)):
            temperature += (self.final_temperature - temperature) * (1 - math.exp(-1 / tau))
            self.set_current_temperature(temperature)
            print(f"Time: {t / 60} minutes, Temperature: {temperature:.2f} °C")

        self.set_final_temperature(self.current_temperature)

        return temperature
    
    @staticmethod
    def start_heating():
        print("Heating started")
    
    @staticmethod
    def stop_heating():
        print("Heating stopped")