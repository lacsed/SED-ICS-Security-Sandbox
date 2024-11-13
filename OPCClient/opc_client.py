from opcua import Client
from opcua import ua
from colorama import Fore, Style

from Tools.mapper import get_attack_number, get_event_name


class OPCClient:
    def __init__(self, server_url="opc.tcp://localhost:4840/freeopcua/server/"):
        self.root = None
        self.server_url = server_url
        self.client = Client(server_url)
        self.variables = {
            "Start_Process": None,
            "Finish_Process": None,
            "Level_High": None,
            "Level_Low": None,
            "Open_Input_Valve": None,
            "Close_Input_Valve": None,
            "Open_Output_Valve": None,
            "Close_Output_Valve": None,
            "Heated": None,
            "Cooled": None,
            "Control_Temperature_On": None,
            "Control_Temperature_Off": None,
            "Mixer_On": None,
            "Mixer_Off": None,
            "Pump_On": None,
            "Pump_Off": None,
            "Reset": None,
            "Level": None,
            "Temperature": None,
            "Volume": None,
            "Heating_Time": None,
            "Cooling_Time": None,
            "Initial_Temperature": None,
            "Heating_Temperature": None,
            "Cooling_Temperature": None,
            "Attack_Type": "",
            "Attack_Event": "",
            "Processed_Events": None,
            "Unprocessed_Events": None,
            "Stop_Process": None,
            "Reset_Process": None,
            "Under_Attack": None,
            "Release_Attack": None,
            "Operation_Mode": None,
            "AttacksQueue": None,
            "Attack_Detected": None
        }

    def connect(self):
        try:
            self.client.connect()
            print(Fore.LIGHTGREEN_EX + "OPC UA client connected successfully." + Style.RESET_ALL)
            self.root = self.client.get_root_node()
            for var_name in self.variables:
                self.variables[var_name] = self.root.get_child(["0:Objects", "2:Tags", f"2:{var_name}"])
        except Exception as e:
            print(Fore.LIGHTRED_EX + "Error connecting OPC UA client:", e, Style.RESET_ALL)

    def disconnect(self):
        try:
            if self.client:
                self.client.disconnect()
                print(Fore.LIGHTGREEN_EX + "OPC UA client disconnected successfully." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.LIGHTRED_EX + "Error disconnecting OPC UA client:", e, Style.RESET_ALL)

    def write_variable(self, var_name, value):
        if var_name in self.variables:
            try:
                if isinstance(value, bool):
                    variant_type = ua.VariantType.Boolean
                elif isinstance(value, int):
                    variant_type = ua.VariantType.Int32
                elif isinstance(value, float):
                    variant_type = ua.VariantType.Float
                elif isinstance(value, str):
                    variant_type = ua.VariantType.String
                elif isinstance(value, list):
                    variant_type = ua.VariantType.String
                else:
                    raise ValueError(f"Unsupported variable type: {type(value)}")

                self.variables[var_name].set_value(ua.Variant(value, variant_type))
                print(Fore.YELLOW + f"Variable '{var_name}' written successfully." + Style.RESET_ALL)
            except Exception as e:
                print(Fore.LIGHTRED_EX + f"Error writing variable '{var_name}': {e}" + Style.RESET_ALL)
        else:
            print(Fore.LIGHTRED_EX + f"Variable '{var_name}' not found." + Style.RESET_ALL)

    def read_variable(self, var_type):
        if var_type in self.variables:
            try:
                value = self.variables[var_type].get_value()
                return value
            except Exception as e:
                print(Fore.LIGHTRED_EX + f"Error reading variable '{var_type}':", e, Style.RESET_ALL)
        else:
            print(Fore.LIGHTRED_EX + f"Variable type '{var_type}' not found." + Style.RESET_ALL)

    def add_to_list_variable(self, var_name, value):
        try:
            current_value = self.read_variable(var_name)
            if isinstance(current_value, list):
                current_value.append(value)
                self.write_variable(var_name, current_value)
            else:
                print(Fore.LIGHTRED_EX + f"Variable '{var_name}' is not a list." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.LIGHTRED_EX + f"Error adding value to list variable '{var_name}':", e, Style.RESET_ALL)

    def remove_from_list_variable(self, var_name, value):
        try:
            current_value = self.read_variable(var_name)
            if isinstance(current_value, list):
                if value in current_value:
                    current_value.remove(value)
                    self.write_variable(var_name, current_value)
                else:
                    print(Fore.LIGHTRED_EX + f"Value '{value}' not found in '{var_name}'." + Style.RESET_ALL)
            else:
                print(Fore.LIGHTRED_EX + f"Variable '{var_name}' is not a list." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.LIGHTRED_EX + f"Error removing value from list variable '{var_name}':", e, Style.RESET_ALL)

    def query_list_variable(self, var_name):
        try:
            current_value = self.read_variable(var_name)
            if isinstance(current_value, list):
                return current_value
            else:
                print(Fore.LIGHTRED_EX + f"Variable '{var_name}' is not a list." + Style.RESET_ALL)
                return None
        except Exception as e:
            print(Fore.LIGHTRED_EX + f"Error querying list variable '{var_name}':", e, Style.RESET_ALL)
            return None

    def update_variable(self, var_name, value):
        self.write_variable(var_name, value)

    def query_variable(self, var_name):
        return self.read_variable(var_name)

    def add_to_processed_events(self, event):
        self.add_to_list_variable("Processed_Events", event)

    def remove_from_processed_events(self, event):
        self.remove_from_list_variable("Processed_Events", event)

    def query_processed_events(self):
        return self.query_list_variable("Processed_Events")

    def add_to_unprocessed_events(self, event):
        self.add_to_list_variable("Unprocessed_Events", event)

    def remove_from_unprocessed_events(self, event):
        self.remove_from_list_variable("Unprocessed_Events", event)

    def query_unprocessed_events(self):
        return self.query_list_variable("Unprocessed_Events")

    def update_start_process(self, value: bool):
        self.write_variable("Start_Process", value)

    def update_finish_process(self, value: bool):
        self.write_variable("Finish_Process", value)

    def update_stop_process(self, value: bool):
        self.write_variable("Stop_Process", value)

    def update_reset_process(self, value: bool):
        self.write_variable("Reset_Process", value)

    def update_level_high(self, value: bool):
        self.write_variable("Level_High", value)

    def update_level_low(self, value: bool):
        self.write_variable("Level_Low", value)

    def update_open_input_valve(self, value: bool):
        self.write_variable("Open_Input_Valve", value)

    def update_close_input_valve(self, value: bool):
        self.write_variable("Close_Input_Valve", value)

    def update_open_output_valve(self, value: bool):
        self.write_variable("Open_Output_Valve", value)

    def update_close_output_valve(self, value: bool):
        self.write_variable("Close_Output_Valve", value)

    def update_heated(self, value: bool):
        self.write_variable("Heated", value)

    def update_cooled(self, value: bool):
        self.write_variable("Cooled", value)

    def update_control_temperature_on(self, value: bool):
        self.write_variable("Control_Temperature_On", value)

    def update_control_temperature_off(self, value: bool):
        self.write_variable("Control_Temperature_Off", value)

    def update_mixer_on(self, value: bool):
        self.write_variable("Mixer_On", value)

    def update_mixer_off(self, value: bool):
        self.write_variable("Mixer_Off", value)

    def update_pump_on(self, value: bool):
        self.write_variable("Pump_On", value)

    def update_pump_off(self, value: bool):
        self.write_variable("Pump_Off", value)

    def update_reset(self, value: bool):
        self.write_variable("Reset", value)

    def attack_detected(self, value: bool):
        self.write_variable("Attack_Detected", value)

    def read_start_process(self):
        return self.read_variable("Start_Process")

    def read_finish_process(self):
        return self.read_variable("Finish_Process")

    def read_stop_process(self):
        return self.read_variable("Stop_Process")

    def read_reset_process(self):
        return self.read_variable("Reset_Process")

    def read_under_attack(self):
        return self.read_variable("Under_Attack")

    def get_attack_type(self):
        return self.read_variable("Attack_Type")

    def get_attack_event(self):
        return get_event_name(self.read_variable("Attack_Event"))

    def deny_attack(self):
        return self.read_variable("Attack_Type") == 0

    def host_and_watch_attack(self):
        return self.read_variable("Attack_Type") == 1

    def insert_attack(self):
        return self.read_variable("Attack_Type") == 2

    def intercept_attack(self):
        return self.read_variable("Attack_Type") == 3

    def stealth_insert_attack(self):
        return self.read_variable("Attack_Type") == 4

    def read_level_high(self):
        return self.read_variable("Level_High")

    def read_level_low(self):
        return self.read_variable("Level_Low")

    def read_open_input_valve(self):
        return self.read_variable("Open_Input_Valve")

    def read_close_input_valve(self):
        return self.read_variable("Close_Input_Valve")

    def read_open_output_valve(self):
        return self.read_variable("Open_Output_Valve")

    def read_close_output_valve(self):
        return self.read_variable("Close_Output_Valve")

    def read_heated(self):
        return self.read_variable("Heated")

    def read_cooled(self):
        return self.read_variable("Cooled")

    def read_control_temperature_on(self):
        return self.read_variable("Control_Temperature_On")

    def read_control_temperature_off(self):
        return self.read_variable("Control_Temperature_Off")

    def read_mixer_on(self):
        return self.read_variable("Mixer_On")

    def read_mixer_off(self):
        return self.read_variable("Mixer_Off")

    def read_pump_on(self):
        return self.read_variable("Pump_On")

    def read_pump_off(self):
        return self.read_variable("Pump_Off")

    def read_reset(self):
        return self.read_variable("Reset")

    def released_by_attack(self, attack_type, attack_event):
        return (self.query_variable('Attack_Type') != attack_type
                or self.query_variable('Attack_Event') != get_attack_number(attack_event))

    def block_by_attack(self, attack_type, attack_event):
        return (self.query_variable('Attack_Type') == attack_type
                and self.query_variable('Attack_Event') == get_attack_number(attack_event))
