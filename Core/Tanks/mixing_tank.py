from Instruments import Valve, LevelTransmitter, Mixer

class MixingTank:
    def __init__(self, inlet_valve: Valve, outlet_valve: Valve, level_transmitter: LevelTransmitter, mixer: Mixer):
        self.inlet_valve = inlet_valve
        self.outlet_valve = outlet_valve
        self.level_transmitter = level_transmitter
        self.mixer = mixer