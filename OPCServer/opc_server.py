from opcua import Server, ua

from Configuration.set_points import INITIAL_TEMP, HEATING_TIME, COOLING_TIME, HEATING_TEMP, COOLING_TEMP


class OPCServer:
    def __init__(self):
        self.variables = None
        self.obj = None
        self.server = Server()
        self.uri = "http://industrialplant.com"
        self.idx = self.server.register_namespace(self.uri)
        self.message_log = []

    def start(self):
        try:
            print("Starting OPC UA server...")
            self.server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
            self.server.start()
            print("OPC UA server started successfully.")

            objects = self.server.nodes.objects
            self.obj = objects.add_object(self.idx, "Tags")

            self.variables = {
                "Start_Process": self.obj.add_variable(self.idx, "Start_Process", False),
                "Finish_Process": self.obj.add_variable(self.idx, "Finish_Process", False),
                "Level_High": self.obj.add_variable(self.idx, "Level_High", False),
                "Level_Low": self.obj.add_variable(self.idx, "Level_Low", False),
                "Open_Input_Valve": self.obj.add_variable(self.idx, "Open_Input_Valve", False),
                "Close_Input_Valve": self.obj.add_variable(self.idx, "Close_Input_Valve", False),
                "Open_Output_Valve": self.obj.add_variable(self.idx, "Open_Output_Valve", False),
                "Close_Output_Valve": self.obj.add_variable(self.idx, "Close_Output_Valve", False),
                "Heated": self.obj.add_variable(self.idx, "Heated", False),
                "Cooled": self.obj.add_variable(self.idx, "Cooled", False),
                "Control_Temperature_On": self.obj.add_variable(self.idx, "Control_Temperature_On", False),
                "Control_Temperature_Off": self.obj.add_variable(self.idx, "Control_Temperature_Off", False),
                "Mixer_On": self.obj.add_variable(self.idx, "Mixer_On", False),
                "Mixer_Off": self.obj.add_variable(self.idx, "Mixer_Off", False),
                "Pump_On": self.obj.add_variable(self.idx, "Pump_On", False),
                "Pump_Off": self.obj.add_variable(self.idx, "Pump_Off", False),
                "Reset": self.obj.add_variable(self.idx, "Reset", False),
                "Level": self.obj.add_variable(self.idx, "Level", 0),
                "Temperature": self.obj.add_variable(self.idx, "Temperature", INITIAL_TEMP),
                "Volume": self.obj.add_variable(self.idx, "Volume", 0),
                "Heating_Time": self.obj.add_variable(self.idx, "Heating_Time", HEATING_TIME),
                "Cooling_Time": self.obj.add_variable(self.idx, "Cooling_Time", COOLING_TIME),
                "Initial_Temperature": self.obj.add_variable(self.idx, "Initial_Temperature", INITIAL_TEMP),
                "Heating_Temperature": self.obj.add_variable(self.idx, "Heating_Temperature", HEATING_TEMP),
                "Cooling_Temperature": self.obj.add_variable(self.idx, "Cooling_Temperature", COOLING_TEMP),
                "Operation_Mode": self.obj.add_variable(self.idx, "Operation_Mode", 0),
                "Attack_Type": self.obj.add_variable(self.idx, "Attack_Type", 0),
                "Attack_Event": self.obj.add_variable(self.idx, "Attack_Event", 0),
                "Processed_Events": self.obj.add_variable(self.idx, "Processed_Events",
                                                          ua.Variant([], ua.VariantType.String)),
                "Unprocessed_Events": self.obj.add_variable(self.idx, "Unprocessed_Events",
                                                            ua.Variant([], ua.VariantType.String)),
                "Stop_Process": self.obj.add_variable(self.idx, "Stop_Process", False),
                "Reset_Process": self.obj.add_variable(self.idx, "Reset_Process", False),
                "Under_Attack": self.obj.add_variable(self.idx, "Under_Attack", False),
                "Release_Attack": self.obj.add_variable(self.idx, "Release_Attack", True)
            }

            for var in self.variables.values():
                var.set_writable()

        except Exception as e:
            print("Error when starting OPC UA server:", e)

    def stop(self):
        try:
            self.server.stop()
            print("OPC UA server stopped.")
        except Exception as e:
            print("Error when stopping OPC UA server:", e)

    def write_variable(self, var_name, value):
        try:
            variable = self.variables.get(var_name, None)
            if variable is not None:
                variable.set_value(value)
                print(f"Variable '{var_name}' written successfully.")
            else:
                print(f"Variable '{var_name}' not found.")
        except Exception as e:
            print("Error writing variable:", e)

    def add_to_list_variable(self, var_name, value):
        try:
            variable = self.variables.get(var_name, None)
            if variable is not None:
                current_value = variable.get_value()
                if isinstance(current_value, list):
                    current_value.append(value)
                    variable.set_value(current_value)
                else:
                    print(f"Variable '{var_name}' is not a list.")
            else:
                print(f"Variable '{var_name}' not found.")
        except Exception as e:
            print(f"Error adding value to list variable '{var_name}':", e)

    def remove_from_list_variable(self, var_name, value):
        try:
            variable = self.variables.get(var_name, None)
            if variable is not None:
                current_value = variable.get_value()
                if isinstance(current_value, list):
                    if value in current_value:
                        current_value.remove(value)
                        variable.set_value(current_value)
                    else:
                        print(f"Value '{value}' not found in '{var_name}'.")
                else:
                    print(f"Variable '{var_name}' is not a list.")
            else:
                print(f"Variable '{var_name}' not found.")
        except Exception as e:
            print(f"Error removing value from list variable '{var_name}':", e)

    def query_list_variable(self, var_name):
        try:
            variable = self.variables.get(var_name, None)
            if variable is not None:
                current_value = variable.get_value()
                if isinstance(current_value, list):
                    return current_value
                else:
                    print(f"Variable '{var_name}' is not a list.")
                    return None
            else:
                print(f"Variable '{var_name}' not found.")
                return None
        except Exception as e:
            print(f"Error querying list variable '{var_name}':", e)
            return None

    def reset_variables(self):
        if self.variables is None:
            print("Error: 'self.variables' is not initialized.")
            return

        initial_values = {
            "Start_Process": False,
            "Finish_Process": False,
            "Level_High": False,
            "Level_Low": False,
            "Open_Input_Valve": False,
            "Close_Input_Valve": False,
            "Open_Output_Valve": False,
            "Close_Output_Valve": False,
            "Heated": False,
            "Cooled": False,
            "Control_Temperature_On": False,
            "Control_Temperature_Off": False,
            "Mixer_On": False,
            "Mixer_Off": False,
            "Pump_On": False,
            "Pump_Off": False,
            "Reset": False,
            "Level": 0,
            "Temperature": INITIAL_TEMP,
            "Volume": 0,
            "Heating_Time": HEATING_TIME,
            "Cooling_Time": COOLING_TIME,
            "Initial_Temperature": INITIAL_TEMP,
            "Heating_Temperature": HEATING_TEMP,
            "Cooling_Temperature": COOLING_TEMP,
            "Operation_Mode": False,
            "Attack_Type": None,
            "Attack_Event": None,
            "Processed_Events": ua.Variant([], ua.VariantType.String),
            "Unprocessed_Events": ua.Variant([], ua.VariantType.String),
            "Stop_Process": False,
            "Reset_Process": False,
            "Under_Attack": False,
            "Release_Attack": True
        }

        for key, value in initial_values.items():
            if key in self.variables and self.variables[key] is not None:
                self.variables[key].set_value(value)
            else:
                print(f"Warning: Variable '{key}' is not initialized or is None.")

        print("All variables have been reset to their initial values.")

    def update_variable(self, var_name: str, value):
        self.write_variable(var_name, value)

    def query_variable(self, var_name: str):
        return self.variables[var_name].get_value()

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

    def start_process(self):
        return self.variables["Start_Process"].get_value()

    def finish_process(self):
        return self.variables["Finish_Process"].get_value()

    def stop_process(self):
        return self.variables["Stop_Process"].get_value()

    def reset_process(self):
        return self.variables["Reset_Process"].get_value()

    def under_attack(self):
        return self.variables["Under_Attack"].get_value()

    def get_attack_type(self):
        return self.variables["Attack_Type"].get_value()

    def deny_attack(self):
        return self.variables["Attack_Type"].get_value() == 0

    def host_and_watch_attack(self):
        return self.variables["Attack_Type"].get_value() == 1

    def insert_attack(self):
        return self.variables["Attack_Type"].get_value() == 2

    def intercept_attack(self):
        return self.variables["Attack_Type"].get_value() == 3

    def stealth_insert_attack(self):
        return self.variables["Attack_Type"].get_value() == 4

    def get_attack_event(self):
        return self.variables["Attack_Event"].get_value()

    def level_high(self):
        return self.variables["Level_High"].get_value()

    def level_low(self):
        return self.variables["Level_Low"].get_value()

    def open_input_valve(self):
        return self.variables["Open_Input_Valve"].get_value()

    def close_input_valve(self):
        return self.variables["Close_Input_Valve"].get_value()

    def open_output_valve(self):
        return self.variables["Open_Output_Valve"].get_value()

    def close_output_valve(self):
        return self.variables["Close_Output_Valve"].get_value()

    def heated(self):
        return self.variables["Heated"].get_value()

    def cooled(self):
        return self.variables["Cooled"].get_value()

    def control_temperature_on(self):
        return self.variables["Control_Temperature_On"].get_value()

    def control_temperature_off(self):
        return self.variables["Control_Temperature_Off"].get_value()

    def mixer_on(self):
        return self.variables["Mixer_On"].get_value()

    def mixer_off(self):
        return self.variables["Mixer_Off"].get_value()

    def pump_on(self):
        return self.variables["Pump_On"].get_value()

    def pump_off(self):
        return self.variables["Pump_Off"].get_value()

    def reset(self):
        return self.variables["Reset"].get_value()

    def update_start_process(self, value: bool):
        self.write_variable("Start_Process", value)

    def update_finish_process(self, value: bool):
        self.write_variable("Finish_Process", value)

    def update_stop_process(self, value: bool):
        self.write_variable("Stop_Process", value)

    def update_reset_process(self, value: bool):
        self.write_variable("Reset_Process", value)

    def update_under_attack(self, value: bool):
        self.write_variable("Release_Attack", not value)
        self.write_variable("Under_Attack", value)

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
