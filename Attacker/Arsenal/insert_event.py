import time

from OPCServer.opc_server import OPCServer
from Tools.mapper import get_event_name
from colorama import Fore, Style


def insert_event(server: OPCServer):
    event = get_event_name(server.query_variable('Attack_Event'))

    if server.query_variable(event):
        return

    server.update_variable(event, True)
    server.add_to_processed_events(event)
    time.sleep(1)
    server.update_under_attack(False)
    print(Fore.YELLOW + f"Event '{event}' was insert in network." + Style.RESET_ALL)
