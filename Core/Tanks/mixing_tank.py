import time

from Core.Tanks.Base.tank import Tank
from Core.Instruments.level_trasmitter import LevelTransmitter
from Core.Instruments.mixer import Mixer
from Core.Instruments.valve import Valve

from OPCClient.opc_client import OPCClient


class MixingTank(Tank):
    def __init__(self, capacity: float, batch: float, inlet_valve: Valve, outlet_valve: Valve,
                 level_transmitter: LevelTransmitter, mixer: Mixer, opc_client: OPCClient):
        super().__init__("MixingTank", capacity, batch, inlet_valve, outlet_valve,
                         level_transmitter, opc_client)
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
        self.fill_tank()

        if self.opc_client.start_mixing_process:
            print("Mixing process started on the server.")
        else:
            print("Failed to start mixing process on the server.")

        self.mix(time_to_mix)

        self.empty_tank()

        print("Processing completed.\n\n")
