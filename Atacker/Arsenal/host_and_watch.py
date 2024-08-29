import time

from OPCServer.opc_server import OPCServer


def host_and_watch(server: OPCServer):
    # Simulates event monitoring
    print(f"Monitoring System...")

    for event in server.variables:
        if str(event) == 'True':
            print(f"Event '{event}' has already been processed. Monitoring post-execution.")

    time.sleep(0.01)
