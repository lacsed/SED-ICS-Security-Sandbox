import time

from colorama import Fore, Style

from OPCServer.opc_server import OPCServer
from Tools.mapper import get_event_name


def stealth_insert(server: OPCServer):
    event = get_event_name(server.query_variable('Attack_Event'))

    if server.query_variable(event):
        return

    time.sleep(1)
    server.add_to_processed_events(event)
    server.update_under_attack(False)
    print(Fore.YELLOW + f"Event '{event}' was secretly insert in network." + Style.RESET_ALL)

    # atacante insere um evento e só o controlador vê (sensor)
