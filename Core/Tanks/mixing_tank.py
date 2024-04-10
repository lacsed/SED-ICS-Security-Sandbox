import time

from Core.Tanks.Base.tank import Tank
from Core.Instruments.level_trasmitter import LevelTransmitter
from Core.Instruments.mixer import Mixer
from Core.Instruments.valve import Valve

from OPCClient.opc_client import OPCClient


class MixingTank(Tank):
    def __init__(self, capacity: float, batch: float, inlet_valve: Valve, outlet_valve: Valve,
                 level_transmitter: LevelTransmitter, mixer: Mixer, opc_client: OPCClient):
        super().__init__("MixingTank", capacity, batch)
        self.inlet_valve = inlet_valve
        self.outlet_valve = outlet_valve
        self.level_transmitter = level_transmitter
        self.mixer = mixer
        self.opc_client = opc_client

    def mix(self, time_to_mix: int):
        print(f"Mixing tank '{self.name}'...")

        self.mixer.set_mixing_time(time_to_mix)
        self.mixer.start_mixing()
        #time.sleep(time_to_mix)

        self.mixer.stop_mixing()
        print(f"Tank '{self.name}' mixed.")

    def fill_and_mix(self, time_to_mix: int):
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

        if self.opc_client.start_mixing_process:
            print("Mixing process started on the server.")
        else:
            print("Failed to start mixing process on the server.")

        self.mix(time_to_mix)

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

        print("Processing completed.\n\n")