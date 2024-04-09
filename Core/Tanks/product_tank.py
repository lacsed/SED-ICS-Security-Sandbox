import time

from Core.Tanks.Base.tank import Tank
from Core.Instruments.level_trasmitter import LevelTransmitter
from Core.Instruments.pump import Pump
from Core.Instruments.valve import Valve

from OPCClient.opc_client import OPCClient


class ProductTank(Tank):
    def __init__(self, capacity: float, batch: float, inlet_valve: Valve, outlet_valve: Valve,
                 level_transmitter: LevelTransmitter, pump: Pump, opc_client: OPCClient):
        super().__init__("ProductTank", capacity, batch)
        self.inlet_valve = inlet_valve
        self.outlet_valve = outlet_valve
        self.level_transmitter = level_transmitter
        self.pump = pump
        self.opc_client = opc_client

    def pump_start(self):
        print(f"Pumping tank '{self.name}'...")
        self.pump.start_pump()

        time_to_pump = self.batch / self.pump.flow_rate
        #time.sleep(time_to_pump)

        self.pump.stop_pump()

        print(f"Tank '{self.name}' pumped.")

    def fill_and_empty(self):
        time_to_fill = self.batch / self.inlet_valve.flow_rate

        print(f"Filling tank '{self.name}'...")
        #time.sleep(time_to_fill)
        print(f"Tank '{self.name}' filled.")

        if self.opc_client.start_product_process:
            print("Product process started on the server.")
        else:
            print("Failed to start product process on the server.")

        time_to_empty = self.batch / self.outlet_valve.flow_rate

        print(f"Emptying tank '{self.name}'...")
        #time.sleep(time_to_empty)
        print(f"Tank '{self.name}' emptied.")

        self.pump_start()

        print("Processing completed.\n\n")