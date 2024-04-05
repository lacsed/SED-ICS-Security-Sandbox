from opc_client import OPCClient

if __name__ == "__main__":
    opc_client = OPCClient()
    opc_client.connect()
    opc_client.read_variable()
    opc_client.write_variable(10.0)
    opc_client.disconnect()