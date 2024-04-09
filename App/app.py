from Core.OPC.Server.server import OPCServer
from Core.OPC.Client.client import OPCClient
from Core.Tanks.heating_tank import HeatingTank
from Core.Tanks.mixing_tank import MixingTank
from Core.Tanks.product_tank import ProductTank
from Core.Instruments.valve import Valve
from Core.Instruments.temperature_transmitter import TemperatureTransmitter
from Core.Instruments.level_trasmitter import LevelTransmitter
from Core.Instruments.mixer import Mixer
from Core.Instruments.pump import Pump

if __name__ == "__main__":
    uriServer = "opc.tcp://localhost:4840/freeopcua/server/"
    i = 0

    opc_server = OPCServer()
    opc_server.start()

    opc_client1 = OPCClient(uriServer)
    opc_client1.connect()

    opc_client2 = OPCClient(uriServer)
    opc_client2.connect()

    opc_client3 = OPCClient(uriServer)
    opc_client3.connect()

    heating_tank = HeatingTank(capacity=100,
                               batch=60,
                               inlet_valve=Valve("FV101", 20, 0.8),
                               temperature_transmitter=TemperatureTransmitter("TT102", 25, 25, 100, 30),
                               level_transmitter=LevelTransmitter("LT103", 0, 60, 100),
                               opc_client=opc_client1)

    mixing_tank = MixingTank(capacity=150, batch=15,
                             inlet_valve=Valve("FV201", 20, 0.8),
                             outlet_valve=Valve("FV203", 20, 0.8),
                             level_transmitter=LevelTransmitter("LT204", 0, 60, 100),
                             mixer=Mixer("AG202", 20),
                             opc_client=opc_client2)

    product_tank = ProductTank(capacity=200, batch=20,
                               inlet_valve=Valve("FV301", 20, 0.8),
                               outlet_valve=Valve("FV303", 20, 0.8),
                               level_transmitter=LevelTransmitter("LT302", 20, 60, 100),
                               pump=Pump("P303", 20, 0.8),
                               opc_client=opc_client3)

    while i < 1:
        heating_tank.fill_and_heat(initial_temperature=25.0, final_temperature=50.0, time_to_heat=5)
        mixing_tank.fill_and_mix(time_to_mix=10)
        product_tank.fill_and_empty()

        i += 1

    opc_client1.disconnect()
    opc_client2.disconnect()
    opc_client3.disconnect()

    opc_server.stop()