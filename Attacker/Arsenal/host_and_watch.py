from OPCServer.opc_server import OPCServer
from colorama import Fore, Style


def host_and_watch(server: OPCServer):
    # Simulates event monitoring
    print(Fore.YELLOW + f"Monitoring System...")

    for event in server.variables:
        if server.query_variable(event):
            print(Fore.YELLOW + f"Event '{event}' has already been processed. Monitoring post-execution." + Style.RESET_ALL)
