from colorama import init, Fore, Style

from Core.Instruments.level_trasmitter import LevelTransmitter
from Core.Instruments.mixer import Mixer
from Core.Instruments.pump import Pump
from Core.Instruments.temperature_transmitter import TemperatureTransmitter
from Core.Instruments.valve import Valve
from OPCClient.opc_client import OPCClient

init()


class Tank:
    def __init__(self, name: str, capacity: float, batch: float, inlet_valve: Valve, outlet_valve: Valve,
                 reagent_valve: Valve, mixer: Mixer, temperature_transmitter: TemperatureTransmitter,
                 level_transmitter: LevelTransmitter, pump: Pump, opc_client: OPCClient):
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
        self.reagent_valve = reagent_valve
        self.mixer = mixer
        self.temperature_transmitter = temperature_transmitter
        self.level_transmitter = level_transmitter
        self.pump = pump
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

    def heat_tank(self, initial_temperature: float, final_temperature: float, time_to_heat: int):
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

    def mix_tank(self, time_to_mix: int):
        print(f"Mixing tank '{self.name}'...")
        self.mixer.set_mixing_time(time_to_mix)
        self.mixer.start_mixing()
        #time.sleep(time_to_mix)

        if self.opc_client.start_mixing_process:
            print("Mixing process started on the server.")
        else:
            print("Failed to start mixing process on the server.")

        self.mixer.stop_mixing()
        print(f"Tank '{self.name}' mixed.")

    def pump_tank(self):
        print(f"Pumping tank '{self.name}'...")
        self.pump.start_pump()

        if self.opc_client.start_product_process:
            print("Product process started on the server.")
        else:
            print("Failed to start product process on the server.")

        time_to_pump = self.batch / self.pump.flow

        self.pump.set_pump_flow_rate()
        self.pump.set_pump_flow()

        self.pump.stop_pump()

        print(f"Tank '{self.name}' pumped.")

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
