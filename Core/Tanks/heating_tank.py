from Instruments import Valve, TemperatureTransmitter, LevelTransmitter

class HeatingTank:
    def __init__(self, inlet_valve: Valve, temperature_transmitter: TemperatureTransmitter,
                 level_transmitter: LevelTransmitter):
        self.inlet_valve = inlet_valve
        self.temperature_transmitter = temperature_transmitter
        self.level_transmitter = level_transmitter