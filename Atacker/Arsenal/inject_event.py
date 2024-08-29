from OPCServer.opc_server import OPCServer
from Tools.mapper import get_event_name


def inject_event(server: OPCServer):
    event = get_event_name(server.query_variable('Attack_Event'))
    server.update_variable(event, True)
