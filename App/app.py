from threading import Thread, Lock, Event
import time

from Core.Control.controller import Controller
from Core.Instruments.pump import Pump
from Core.Instruments.temperature_transmitter import TemperatureTransmitter
from Core.Instruments.valve import Valve
from Core.Instruments.mixer import Mixer
from Core.OPC.Server.server import OPCServer
from Core.OPC.Client.client import OPCClient

clients = []
clients_lock = Lock()
clients_ready = Event()

def run_server():
    opc_server = OPCServer()
    opc_server.start()

def run_client(uri):
    opc_client = OPCClient(uri)
    opc_client.connect()
    with clients_lock:
        clients.append(opc_client)
        if len(clients) == 5:
            clients_ready.set()


if __name__ == "__main__":
    uriServer = "opc.tcp://localhost:4840/freeopcua/server/"

    server_thread = Thread(target=run_server)
    server_thread.start()

    time.sleep(2)

    client_threads = []

    for _ in range(5):
        client_thread = Thread(target=run_client, args=(uriServer,))
        client_threads.append(client_thread)
        client_thread.start()

    clients_ready.wait()

    for client_thread in client_threads:
        client_thread.join()

    if len(clients) < 4:
        raise RuntimeError("Unable to connect all OPC clients.")

    input_valve_device = Valve("FV101", 20, 0.8, clients[0])
    output_valve_device = Valve("FV107", 20, 0.8, clients[1])
    mixer_device = Mixer("AC103", 15, clients[2])
    pump_device = Pump("P106", 20, 0.8, clients[3])
    temperature_control_device = TemperatureTransmitter("TT104", 25, 25, 100, 1, clients[4])

    controller = Controller(input_valve_device,
                            output_valve_device,
                            mixer_device,
                            pump_device,
                            temperature_control_device)

    for client in clients:
        client.disconnect()


    server_thread.join()
