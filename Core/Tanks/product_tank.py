import time

from Core.Tanks.Base.tank import Tank
from Core.Instruments.level_trasmitter import LevelTransmitter
from Core.Instruments.pump import Pump
from Core.Instruments.valve import Valve

from OPCClient.opc_client import OPCClient


class ProductTank(Tank):
    def __init__(self, capacity: float, batch: float, inlet_valve: Valve, outlet_valve: Valve,
                 level_transmitter: LevelTransmitter, pump: Pump, opc_client: OPCClient):
        super().__init__("ProductTank", capacity, batch, inlet_valve, outlet_valve, level_transmitter,
                         opc_client)
        self.pump = pump

    def pump_start(self):
        print(f"Pumping tank '{self.name}'...")
        self.pump.start_pump()

        time_to_pump = self.batch / self.pump.flow

        self.pump.set_pump_flow_rate()
        self.pump.set_pump_flow()

        self.pump.stop_pump()

        print(f"Tank '{self.name}' pumped.")

    def fill_and_empty(self):
        self.fill_tank()

        if self.opc_client.start_product_process:
            print("Product process started on the server.")
        else:
            print("Failed to start product process on the server.")

        self.pump_start()

        self.empty_tank()

        print("Processing completed.\n\n")
