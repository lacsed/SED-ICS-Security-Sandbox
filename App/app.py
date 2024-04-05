import sys
from pathlib import Path

diretorio_pai = Path(__file__).resolve().parent.parent
sys.path.append(str(diretorio_pai))

from Core.OPC.Server.server import OPCServer
from Core.OPC.Client.client import OPCClient

if __name__ == "__main__":
    opc_server = OPCServer()
    opc_server.start()

    opc_client = OPCClient("opc.tcp://localhost:4840/freeopcua/server/")
    opc_client.connect()
    opc_client.read_variable()
    opc_client.write_variable(10.0)
    opc_client.disconnect()

    opc_server.stop()