from Instruments import Valve, LevelTransmitter, Pump

class ProductTank:
    def __init__(self, inlet_valve: Valve, outlet_valve: Valve, level_transmitter: LevelTransmitter, pump: Pump):
        self.inlet_valve = inlet_valve
        self.outlet_valve = outlet_valve
        self.level_transmitter = level_transmitter
        self.pump = pump