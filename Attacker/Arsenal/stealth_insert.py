from OPCServer.opc_server import OPCServer
from Tools.mapper import get_event_name


def stealth_insert(server: OPCServer):
    event = get_event_name(server.query_variable('Attack_Event'))

    if event in server.query_processed_events() or server.query_variable(event):
        return

    server.update_variable(event, True)
    print(f"Event '{event}' was insert in network.")
