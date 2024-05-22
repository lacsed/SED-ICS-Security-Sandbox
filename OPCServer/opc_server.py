from datetime import datetime
from opcua import Server


class OPCServer:
    def __init__(self):
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

            self.temperature_var = self.obj.add_variable(self.idx, "Temperature", 0)
            self.flow_var = self.obj.add_variable(self.idx, "Flow", 0)
            self.time_var = self.obj.add_variable(self.idx, "Time", 0)
            self.level_var = self.obj.add_variable(self.idx, "Level", 0)

            self.temperature_var.set_writable()
            self.flow_var.set_writable()
            self.time_var.set_writable()
            self.level_var.set_writable()
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
            variable = getattr(self, f"{var_name}_var", None)
            if variable is not None:
                variable.set_value(value)
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

    def start_heating_process(self, parent, *args):
        try:
            print("Heating process started on the server.")
            return True
        except Exception as e:
            print("Error starting heating process on the server:", e)
            return False

    def start_mixing_process(self, parent, *args):
        try:
            print("Mixing process started on the server.")
            return True
        except Exception as e:
            print("Error starting mixing process on the server:", e)
            return False

    def start_product_process(self, parent, *args):
        try:
            print("Product process started on the server.")
            return True
        except Exception as e:
            print("Error starting product process on the server:", e)

    def stop(self):
        try:
            self.server.stop()
            print("OPC UA server stopped.")
        except Exception as e:
            print("Error when shutting down OPC UA server:", e)
