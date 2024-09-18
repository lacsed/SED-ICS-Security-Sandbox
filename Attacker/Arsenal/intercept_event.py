from OPCServer.opc_server import OPCServer
from Tools.mapper import get_event_name


def intercept_event(server: OPCServer):
    event = get_event_name(server.query_variable('Attack_Event'))

    if event in server.query_processed_events():
        print(f"Event '{event}' already processed, interception not possible.")
        return

    server.add_to_processed_events(event)
    server.update_under_attack(False)
    print(f"Event '{event}' was intercepted and executed.")
