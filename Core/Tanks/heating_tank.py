import time

from Core.Tanks.Base.tank import Tank
from Core.Instruments.level_trasmitter import LevelTransmitter
from Core.Instruments.temperature_transmitter import TemperatureTransmitter
from Core.Instruments.valve import Valve

from OPCClient.opc_client import OPCClient


class HeatingTank(Tank):
    def __init__(self, capacity: float, batch: float, inlet_valve: Valve,
                 temperature_transmitter: TemperatureTransmitter, level_transmitter:LevelTransmitter,
                 opc_client: OPCClient):
        super().__init__("HeatingTank", capacity, batch)
        self.inlet_valve = inlet_valve
        self.temperature_transmitter = temperature_transmitter
        self.level_transmitter = level_transmitter
        self.opc_client = opc_client

    def heat(self, initial_temperature: float, final_temperature: float, time_to_heat: int):
        print(f"Heating tank '{self.name}'...")
        self.temperature_transmitter.start_heating()
        self.temperature_transmitter.set_initial_temperature(initial_temperature)
        self.temperature_transmitter.set_final_temperature(final_temperature)

        if self.opc_client.start_heating_process():
            print("Heating process started on the server.")
            self.opc_client.write_variable(self.temperature_transmitter.current_temperature)
        else:
            print("Failed to start the heating process on the server.")

        self.temperature_transmitter.set_heating_time(time_to_heat)
        self.temperature_transmitter.initialize_heating_circuit()

        time.sleep(time_to_heat * 60)

        self.temperature_transmitter.stop_heating()

        print(f"Tank '{self.name}' heated to {self.temperature_transmitter.final_temperature}°C.")

    def fill_and_heat(self, initial_temperature: float, final_temperature: float, time_to_heat: int):
        time_to_fill = self.batch / self.inlet_valve.flow_rate

        print(f"Filling tank '{self.name}'...")
        time.sleep(time_to_fill)
        print(f"Tank '{self.name}' filled.")

        self.heat(initial_temperature, final_temperature, time_to_heat)

        print("Processing completed.")