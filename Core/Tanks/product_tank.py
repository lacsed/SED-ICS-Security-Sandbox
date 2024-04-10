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

        time_to_pump = self.batch / self.pump.flow

        self.pump.set_pump_flow_rate()
        self.pump.set_pump_flow()

        self.pump.stop_pump()

        print(f"Tank '{self.name}' pumped.")

    def fill_and_empty(self):
        self.inlet_valve.set_valve_flow_rate()
        self.inlet_valve.set_valve_flow()

        time_to_fill = self.batch / self.inlet_valve.flow

        print(f"Filling tank '{self.name}'...")
        self.opc_client.write_variable("flow", self.inlet_valve.flow)
        time_in_seconds = time_to_fill * 60

        time_elapsed = 0
        for t in range(int(time_in_seconds)):
            time_elapsed += 1
            level = self.inlet_valve.flow * (t / 60)

            if time_elapsed == 10:
                self.level_transmitter.set_level(level, t)
                self.opc_client.write_variable("level", self.level_transmitter.current_level)
                time_elapsed = 0

        print(f"Tank '{self.name}' filled.")

        if self.opc_client.start_product_process:
            print("Product process started on the server.")
        else:
            print("Failed to start product process on the server.")

        time_to_empty = self.batch / self.outlet_valve.flow

        self.outlet_valve.set_valve_flow_rate()
        self.outlet_valve.set_valve_flow()
        print(f"Emptying tank '{self.name}'...")
        self.opc_client.write_variable("flow", self.outlet_valve.flow)
        time_in_seconds = time_to_empty * 60

        time_elapsed = 0
        for t in range(int(time_in_seconds)):
            time_elapsed += 1
            level = self.batch - self.outlet_valve.flow * (t / 60)

            if time_elapsed == 10:
                self.level_transmitter.set_level(level, t)
                self.opc_client.write_variable("level", self.level_transmitter.current_level)
                time_elapsed = 0

        print(f"Tank '{self.name}' emptied.")

        self.pump_start()

        print("Processing completed.\n\n")