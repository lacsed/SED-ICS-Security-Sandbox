from opc_client import OPCClient

if __name__ == "__main__":
    opc_client = OPCClient()
    opc_client.connect()
    opc_client.disconnect()
