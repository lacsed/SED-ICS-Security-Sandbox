from opcua import Client


class OPCClient:
    def __init__(self, server_url="opc.tcp://localhost:4840/freeopcua/server/"):
        self.server_url = server_url
        self.client = Client(server_url)
        self.variables = {
            "temperature": None,
            "flow": None,
            "time": None,
            "level": None
        }

    def connect(self):
        try:
            self.client.connect()
            print("OPC UA client connected successfully.")
            self.root = self.client.get_root_node()
            for var_name in self.variables:
                self.variables[var_name] = self.root.get_child(["0:Objects", "2:Tags", f"2:{var_name.capitalize()}"])
        except Exception as e:
            print("Error connecting OPC UA client:", e)

    def disconnect(self):
        try:
            if self.client:
                self.client.disconnect()
                print("OPC UA client disconnected successfully.")
        except Exception as e:
            print("Error disconnecting OPC UA client:", e)

    def write_variable(self, var_type, value):
        if var_type in self.variables:
            self.variables[var_type].set_value(value)
            print(f"Variable '{var_type}' written successfully.")
        else:
            print(f"Variable type '{var_type}' not found.")

    def start_heating_process(self):
        try:
            self.heating_method.call_method()
            print("Heating process started.")
            return True
        except Exception as e:
            print("Error when starting the heating process:", e)
            return False

    def start_mixing_process(self):
        try:
            self.mixing_method.call_method()
            print("Mixing process started.")
            return True
        except Exception as e:
            print("Error when starting the mixing process:", e)
            return False

    def start_product_process(self):
        try:
            self.product_method.call_method()
            print("Product process started.")
            return True
        except Exception as e:
            print("Error when starting the product process:", e)
            return False
