import threading
import time
from colorama import Fore, Style

from Core.Control.controller import Controller
from Core.Process.Tank.tank import Tank
from Core.SubSystems.InputValve.input_valve import InputValve
from Core.SubSystems.LevelTransmitter.level_transmitter import LevelTransmitter
from Core.SubSystems.Mixer.mixer import Mixer
from Core.SubSystems.OutputValve.output_valve import OutputValve
from Core.Process.process import Process
from Core.SubSystems.Pump.pump import Pump
from Core.SubSystems.TemperatureControl.temperature_control import TemperatureControl
from OPCClient.opc_client import OPCClient
from OPCServer.opc_server import OPCServer

class SystemSetup:
    def __init__(self):
        self.server = OPCServer()
        self.process_client = OPCClient()
        self.tank_client = OPCClient()
        self.client_input = OPCClient()
        self.client_output = OPCClient()
        self.client_level_transmitter = OPCClient()
        self.client_mixer = OPCClient()
        self.client_pump = OPCClient()
        self.client_temperature_control = OPCClient()

        self.semaphore = threading.Semaphore(1)
        self.system_initialized = False

        # Create subsystems
        self.process = Process(self.semaphore, self.process_client)
        self.tank = Tank(self.process_client)
        self.input_valve = InputValve(self.client_input)
        self.output_valve = OutputValve(self.client_output)
        self.level_transmitter = LevelTransmitter(self.client_level_transmitter)
        self.mixer = Mixer(self.client_mixer)
        self.pump = Pump(self.client_pump)
        self.temperature_control = TemperatureControl(self.client_temperature_control)
        self.controller = Controller(self.semaphore, self.server)

    def create_threads(self):
        # Recreates and starts all subsystem threads
        self.process = Process(self.semaphore, self.process_client)
        self.tank = Tank(self.process_client)
        self.input_valve = InputValve(self.client_input)
        self.output_valve = OutputValve(self.client_output)
        self.level_transmitter = LevelTransmitter(self.client_level_transmitter)
        self.mixer = Mixer(self.client_mixer)
        self.pump = Pump(self.client_pump)
        self.temperature_control = TemperatureControl(self.client_temperature_control)
        self.controller = Controller(self.semaphore, self.server)

        # Start threads
        self.process.start()
        self.tank.start_threads()
        self.input_valve.start()
        self.output_valve.start()
        self.mixer.start()
        self.pump.start()
        self.temperature_control.start()
        self.level_transmitter.start()
        self.controller.start()

        print(Fore.LIGHTGREEN_EX + "System initialized." + Style.RESET_ALL)
        self.system_initialized = True
        self.server.update_stop_process(False)
        self.server.update_reset_process(False)
        self.server.update_finish_process(False)

    def stop_threads(self):
        # Stop all subsystem threads
        if self.server.stop_process():
            print(Fore.LIGHTRED_EX + "Stopping system..." + Style.RESET_ALL)

        self.system_initialized = False

        self.process.join()
        self.tank.join_threads()
        self.input_valve.join()
        self.output_valve.join()
        self.mixer.join()
        self.pump.join()
        self.temperature_control.join()
        self.level_transmitter.join()
        self.controller.join()

        if self.server.stop_process():
            print(Fore.LIGHTRED_EX + "System stopped." + Style.RESET_ALL)

    def reset_system(self):
        # Reset all subsystems and restart them
        print(Fore.LIGHTYELLOW_EX + "Resetting system..." + Style.RESET_ALL)
        self.server.reset_variables()

        # Stop current threads
        self.stop_threads()

        # Wait a moment for reset to process
        time.sleep(1)

        self.server.update_reset_process(False)
        print(Fore.LIGHTYELLOW_EX + "System reset." + Style.RESET_ALL)


if __name__ == "__main__":
    system_setup = SystemSetup()

    # Start server
    system_setup.server.start()

    # Connect all OPC clients
    system_setup.process_client.connect()
    system_setup.tank_client.connect()
    system_setup.client_input.connect()
    system_setup.client_output.connect()
    system_setup.client_level_transmitter.connect()
    system_setup.client_mixer.connect()
    system_setup.client_pump.connect()
    system_setup.client_temperature_control.connect()

    # Main control loop
    while True:
        if system_setup.server.start_process() and not system_setup.system_initialized:
            system_setup.create_threads()
        if system_setup.server.stop_process():
            system_setup.stop_threads()
            while not system_setup.server.start_process():
                time.sleep(1)
            continue
        if system_setup.server.reset_process():
            system_setup.reset_system()
