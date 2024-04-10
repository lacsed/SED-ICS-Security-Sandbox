from colorama import init, Fore, Style

from Core.Tanks.Base.tank import Tank
from Core.Instruments.level_trasmitter import LevelTransmitter
from Core.Instruments.temperature_transmitter import TemperatureTransmitter
from Core.Instruments.valve import Valve

from OPCClient.opc_client import OPCClient

init()


class HeatingTank(Tank):
    def __init__(self, capacity: float, batch: float, inlet_valve: Valve,
                 temperature_transmitter: TemperatureTransmitter, level_transmitter: LevelTransmitter,
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

        if self.opc_client.start_heating_process:
            print("Heating process started on the server.")
        else:
            print("Failed to start the heating process on the server.")

        self.temperature_transmitter.set_heating_time(time_to_heat)
        time_in_seconds = self.temperature_transmitter.heating_time * 60

        time_elapsed = 0
        for t in range(int(time_in_seconds)):
            time_elapsed += 1
            seconds = t % 60

            if time_elapsed == 10:
                print(Fore.RED + f"[{self.temperature_transmitter.id}] Time: {int(t/60)}m {seconds}s, Temperature: "
                                  f"{self.temperature_transmitter.initialize_heating_circuit(t):.2f} °C" + Style.RESET_ALL)
                self.opc_client.write_variable("temperature", self.temperature_transmitter.current_temperature)
                time_elapsed = 0

        #time.sleep(time_to_heat)

        self.temperature_transmitter.stop_heating()

        print(f"Tank '{self.name}' heated to {self.temperature_transmitter.final_temperature}°C.")

    def fill_and_heat(self, initial_temperature: float, final_temperature: float, time_to_heat: int):
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

        if self.opc_client.start_heating_process:
            print("Heating process started on the server.")
        else:
            print("Failed to start heating process on the server.")

        self.heat(initial_temperature, final_temperature, time_to_heat)

        print("Processing completed.\n\n")