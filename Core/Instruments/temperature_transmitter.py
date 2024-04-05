import math

class TemperatureTransmitter:
    R = 10
    C = 0.1

    def __init__(self, id, initial_temperature, current_temperature, final_temperature):
        self.id = id
        self.initial_temperature = initial_temperature
        self.current_temperature = current_temperature
        self.final_temperature = final_temperature

    def heating_circuit(self, heating_time):
        tau = TemperatureTransmitter.R * TemperatureTransmitter.C
        time_seconds = heating_time * 60
        temperature = 0.0

        for t in range(int(time_seconds)):
            temperature = (self.final_temperature + self.current_temperature - self.final_temperature) * \
                          math.exp(-t / tau)
            print(f"Time: {t / 60} minutes, Temperature: {temperature:.2f} °C")

        return temperature