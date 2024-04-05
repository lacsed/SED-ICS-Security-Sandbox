import sys
from pathlib import Path

diretorio_pai = Path(__file__).resolve().parent.parent
sys.path.append(str(diretorio_pai))

from OPCClient.opc_client import OPCClient

class Client:
    def __init__(self):
        self.client = OPCClient("opc.tcp://localhost:4840/freeopcua/server/")

    def read_variable(self):
        self.client.connect()
        self.client.read_variable()
        self.client.disconnect()

    def write_variable(self, new_value):
        self.client.connect()
        self.client.write_variable(new_value)
        self.client.disconnect()