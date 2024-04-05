import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from OPCServer.opc_server import OPCServer

class Server:
    def __init__(self):
        self.server = OPCServer()

    def start_server(self):
        self.server.start()

    def stop_server(self):
        self.server.stop()