import threading
import time

from Core.Control.controller import Controller
from Core.SubSystems.InputValve.input_valve import InputValve
from Core.SubSystems.LevelTransmitter.level_transmitter import LevelTransmitter
from Core.SubSystems.Mixer.mixer import Mixer
from Core.SubSystems.OutputValve.output_valve import OutputValve
from Core.Process.process import Process
from Core.SubSystems.Pump.pump import Pump
from Core.SubSystems.TemperatureControl.temperature_control import TemperatureControl
from OPCClient.opc_client import OPCClient
from OPCServer.opc_server import OPCServer

if __name__ == "__main__":
    class TerminateProgramException(Exception):
        pass

    system_initialized = False
    semaphore = threading.Semaphore(1)

    # Iniciar o servidor
    server = OPCServer()
    server.start()

    # Conectar o cliente para o processo da planta
    process_client = OPCClient()
    process_client.connect()
    process = Process(semaphore, process_client)

    # Conectar o cliente para a válvula de entrada
    client_input = OPCClient()
    client_input.connect()
    input_valve = InputValve(client_input)

    # Conectar o cliente para a válvula de saída
    client_output = OPCClient()
    client_output.connect()
    output_valve = OutputValve(client_output)

    # Conectar o cliente para a o trasmissor de nível
    client_level_transmitter = OPCClient()
    client_level_transmitter.connect()
    level_transmitter = LevelTransmitter(semaphore, client_level_transmitter)

    # Conectar o cliente para o mixer
    client_mixer = OPCClient()
    client_mixer.connect()
    mixer = Mixer(semaphore, client_mixer)

    # Conectar o cliente para a bomba
    client_pump = OPCClient()
    client_pump.connect()
    pump = Pump(semaphore, client_pump)

    # Conectar o cliente para o controlador de temperatura
    client_temperature_control = OPCClient()
    client_temperature_control.connect()
    temperature_control = TemperatureControl(semaphore, client_temperature_control)

    # Iniciar o controlador
    controller = Controller(semaphore, server)

    def initialize_system():
        global system_initialized
        if not system_initialized:
            system_initialized = True
            process.start()
            input_valve.start()
            output_valve.start()
            mixer.start()
            pump.start()
            temperature_control.start()
            level_transmitter.start()
            controller.start()

            print("System initialized.")
            controller.server.update_init(True)
        else:
            print("System restarted.")
            controller.server.update_init(True)

    def check_response(command):
        if command == 'y':
            initialize_system()
            return True
        elif command == 'n':
            raise TerminateProgramException("Terminating the program.")
        else:
            print("Invalid response. Please enter 'y' for yes or 'n' for no.")
            return False

    # Manter a execução do programa até uma interrupção ser detectada
    while True:
        try:
            response = input("\nInitialize system? (y/n): ").strip().lower()
            if check_response(response):
                time.sleep(100)
        except TerminateProgramException as e:
            print("Stopping all threads and server...")
            controller.join()
            process.join()
            input_valve.join()
            output_valve.join()
            mixer.join()
            pump.join()
            temperature_control.join()
            level_transmitter.join()
            client_input.disconnect()
            client_output.disconnect()
            server.stop()
            break
