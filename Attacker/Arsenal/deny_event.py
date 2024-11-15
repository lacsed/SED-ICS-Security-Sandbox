from OPCServer.opc_server import OPCServer
from Tools.mapper import get_event_name
from colorama import Fore, Style


def deny_event(server: OPCServer, event_send = None):
    event = event_send if event_send else get_event_name(server.query_variable('Attack_Event'))

    if not server.query_variable(event):
        return

    if server.query_variable(event):
        server.update_variable(event, False)
        if event in server.query_processed_events():
            server.remove_from_unprocessed_events(event)
        server.update_under_attack(False)
        print(Fore.YELLOW + f"Event '{event}' has been denied and will not be executed." + Style.RESET_ALL)
