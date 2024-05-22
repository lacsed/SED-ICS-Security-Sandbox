from threading import Thread

from Core.Control.controller import Controller
from Core.OPC.Server.server import OPCServer
from Core.OPC.Client.client import OPCClient

def run_server():
    opc_server = OPCServer()
    opc_server.start()

def run_client(uri, clients):
    opc_client = OPCClient(uri)
    opc_client.connect()
    clients.append(opc_client)

if __name__ == "__main__":
    uriServer = "opc.tcp://localhost:4840/freeopcua/server/"
    i = 0

    server_thread = Thread(target=run_server)
    server_thread.start()

    client_threads = []
    clients = []

    for _ in range(3):
        client_thread = Thread(target=run_client, args=(uriServer, clients))
        client_threads.append(client_thread)
        client_thread.start()

    for client_thread in client_threads:
        client_thread.join()

    '''heating_tank = HeatingTank(capacity=100,
                               batch=60,
                               inlet_valve=Valve("FV101", 20, 0.8),
                               outlet_valve=Valve("FV104", 20, 0.8),
                               temperature_transmitter=TemperatureTransmitter("TT102", 25, 25, 100, 2),
                               level_transmitter=LevelTransmitter("LT103", 0, 60, 100),
                               opc_client=clients[0])

    mixing_tank = MixingTank(capacity=150, batch=15,
                             inlet_valve=Valve("FV201", 20, 0.8),
                             outlet_valve=Valve("FV203", 20, 0.8),
                             level_transmitter=LevelTransmitter("LT204", 0, 60, 100),
                             mixer=Mixer("AG202", 20),
                             opc_client=clients[1])

    product_tank = ProductTank(capacity=200, batch=20,
                               inlet_valve=Valve("FV301", 20, 0.8),
                               outlet_valve=Valve("FV303", 20, 0.8),
                               level_transmitter=LevelTransmitter("LT302", 20, 60, 100),
                               pump=Pump("P303", 20, 0.8),
                               opc_client=clients[2])

    while i < 1:
        heating_tank.fill_and_heat(initial_temperature=25.0, final_temperature=100.0, time_to_heat=5)
        mixing_tank.fill_and_mix(time_to_mix=10)
        product_tank.fill_and_empty()

        i += 1'''

    controller = Controller()
    controller.setup()
    controller.loop(150)

    for client in clients:
        client.disconnect()

    server_thread.join()