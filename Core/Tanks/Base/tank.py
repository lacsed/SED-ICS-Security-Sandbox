from Core.Instruments.level_trasmitter import LevelTransmitter
from Core.Instruments.valve import Valve
from OPCClient.opc_client import OPCClient


class Tank:
    def __init__(self, name: str, capacity: float, batch: float, inlet_valve: Valve,
                 outlet_valve: Valve, level_transmitter: LevelTransmitter, opc_client: OPCClient):
        if not name:
            raise ValueError("The tank name must not be null or empty.")
        elif capacity <= 0:
            raise ValueError("The tank capacity must be greater than zero.")
        elif batch <= 0:
            raise ValueError("The tank batch must be greater than zero.")
        self.name = name
        self.capacity = capacity
        self.batch = batch
        self.inlet_valve = inlet_valve
        self.outlet_valve = outlet_valve
        self.level_transmitter = level_transmitter
        self.opc_client = opc_client
    
    def set_batch(self, batch: float):
        if batch <= 0:
            raise ValueError("The tank batch must be greater than zero.")
        self.batch = batch
        print(f"Production tank batch set to {self.batch}l")

    def fill_tank(self):
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

    def empty_tank(self):
        self.outlet_valve.set_valve_flow_rate()
        self.outlet_valve.set_valve_flow()

        time_to_empty = self.batch / self.outlet_valve.flow

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
