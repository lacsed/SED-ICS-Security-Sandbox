from datetime import datetime
from opcua import Server

from Configuration.set_points import INITIAL_TEMP, MIXING_TIME, HEATING_TIME, COOLING_TIME, PUMPING_TIME, HEATING_TEMP, \
    COOLING_TEMP


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
                "Mixing_Time": self.obj.add_variable(self.idx, "Mixing_Time", MIXING_TIME),
                "Heating_Time": self.obj.add_variable(self.idx, "Heating_Time", HEATING_TIME),
                "Cooling_Time": self.obj.add_variable(self.idx, "Cooling_Time", COOLING_TIME),
                "Pumping_Time": self.obj.add_variable(self.idx, "Pumping_Time", PUMPING_TIME),
                "Initial_Temperature": self.obj.add_variable(self.idx, "Initial_Temperature", INITIAL_TEMP),
                "Heating_Temperature": self.obj.add_variable(self.idx, "Heating_Temperature", HEATING_TEMP),
                "Cooling_Temperature": self.obj.add_variable(self.idx, "Cooling_Temperature", COOLING_TEMP),
                "Operation_Mode": self.obj.add_variable(self.idx, "Operation_Mode", False),
                "Controller_Location": self.obj.add_variable(self.idx, "Controller_Location", 0),
                "InputValve_Location": self.obj.add_variable(self.idx, "InputValve_Location", 0),
                "OutputValve_Location": self.obj.add_variable(self.idx, "OutputValve_Location", 0),
                "Mixer_Location": self.obj.add_variable(self.idx, "Mixer_Location", 0),
                "Temperature_Location": self.obj.add_variable(self.idx, "Temperature_Location", 0),
                "Pump_Location": self.obj.add_variable(self.idx, "Pump_Location", 0),
                "Level_Location": self.obj.add_variable(self.idx, "Level_Location", 0)
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
                self.log_message(var_name, value)
            else:
                print(f"Variable '{var_name}' not found.")
        except Exception as e:
            print("Error writing variable:", e)

    def log_message(self, name, value):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = {"name": name, "value": value, "timestamp": timestamp}
        self.message_log.append(message)

    def remove_messages(self, num_messages):
        if num_messages <= len(self.message_log):
            self.message_log = self.message_log[:-num_messages]
        else:
            print("There are not enough messages to remove.")

    def update_variable(self, var_name: str, value):
        self.write_variable(var_name, value)

    def query_variable(self, var_name: str):
        return self.variables[var_name].get_value()

    def start_process(self):
        return self.variables["Start_Process"].get_value()

    def finish_process(self):
        return self.variables["Finish_Process"].get_value()

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
