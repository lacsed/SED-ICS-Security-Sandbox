from OPCServer.opc_server import OPCServer
from Tools.mapper import get_event_name


def deny_event(server: OPCServer):
    event = get_event_name(server.query_variable('Attack_Event'))

    if not server.query_variable(event):
        return

    if server.query_variable(event):
        server.update_variable(event, False)
        server.update_under_attack(False)
        print(f"Event '{event}' has been denied and will not be executed.")
