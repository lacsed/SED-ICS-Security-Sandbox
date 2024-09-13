from OPCServer.opc_server import OPCServer


def host_and_watch(server: OPCServer):
    # Simulates event monitoring
    print(f"Monitoring System...")

    for event in server.variables:
        if server.query_variable(event):
            print(f"Event '{event}' has already been processed. Monitoring post-execution.")
