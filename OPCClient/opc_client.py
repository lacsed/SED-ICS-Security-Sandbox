from opcua import Client
from opcua import ua
from colorama import init, Fore, Style

init()


class OPCClient:
    def __init__(self, server_url="opc.tcp://localhost:4840/freeopcua/server/"):
        self.root = None
        self.server_url = server_url
        self.client = Client(server_url)
        self.variables = {
            "Init": None,
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
            "Volume": None
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

    def write_variable(self, var_type, value):
        if var_type in self.variables:
            try:
                self.variables[var_type].set_value(ua.Variant(value, ua.VariantType.Boolean))
                print(Fore.YELLOW + f"Variable '{var_type}' written successfully." + Style.RESET_ALL)
            except Exception as e:
                print(Fore.LIGHTRED_EX + f"Error writing variable '{var_type}':", e, Style.RESET_ALL)
        else:
            print(Fore.LIGHTRED_EX + f"Variable type '{var_type}' not found." + Style.RESET_ALL)

    def read_variable(self, var_type):
        if var_type in self.variables:
            try:
                value = self.variables[var_type].get_value()
                text = "Enabled" if value is True else "Disabled"

                # print(Fore.YELLOW + f"Event '{var_type}' is currently {text}" + Style.RESET_ALL)
                return value
            except Exception as e:
                print(Fore.LIGHTRED_EX + f"Error reading variable '{var_type}':", e, Style.RESET_ALL)
        else:
            print(Fore.LIGHTRED_EX + f"Variable type '{var_type}' not found." + Style.RESET_ALL)

    def update_variable(self, var_name, value):
        self.write_variable(var_name, value)

    def query_variable(self, var_name):
        return self.read_variable(var_name)

    def update_init(self, value: bool):
        self.write_variable("Init", value)
    
    def update_start_process(self, value: bool):
        self.write_variable("Start_Process", value)

    def update_finish_process(self, value: bool):
        self.write_variable("Finish_Process", value)

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

    def read_init(self):
        return self.read_variable("Init")

    def read_start_process(self):
        return self.read_variable("Start_Process")

    def read_finish_process(self):
        return self.read_variable("Finish_Process")

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
