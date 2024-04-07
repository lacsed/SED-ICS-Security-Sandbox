from opcua import Client


class OPCClient:
    def __init__(self, server_url="opc.tcp://localhost:4840/freeopcua/server/"):
        self.server_url = server_url
        self.client = None
        self.root = None
        self.obj = None
        self.var = None
        self.heating_method = None
        self.mixing_method = None
        self.product_method = None

    def connect(self):
        try:
            self.client = Client(self.server_url)
            self.client.connect()
            self.root = self.client.get_root_node()
            self.obj = self.root.get_child(["0:Objects", "2:MyObject"])
            self.var = self.obj.get_child(["2:MyVariable"])
            self.heating_method = self.obj.get_method("2:start_heating_process")
            self.mixing_method = self.obj.get_method("2:start_mixing_process")
            self.product_method = self.obj.get_method("2:start_product_process")
            print("OPC UA client connected successfully.")
        except Exception as e:
            print("Error connecting OPC UA client:", e)

    def read_variable(self):
        try:
            value = self.var.get_value()
            print("Current variable value:", value)
            return value
        except Exception as e:
            print("Error reading variable:", e)
            return None

    def write_variable(self, new_value):
        try:
            print("Writing new value:", new_value)
            self.var.set_value(new_value)
            print("New variable value:", self.var.get_value())
        except Exception as e:
            print("Error writing variable:", e)

    def start_heating_process(self):
        try:
            self.heating_method()
            print("Heating process started.")
            if self.client.get_node("ns=2;i=1").get_value():
                return True
            else:
                return False
        except Exception as e:
            print("Error when starting the heating process:", e)

    def start_mixing_process(self):
        try:
            self.mixing_method()
            print("Mixing process started.")
            if self.client.get_node("ns=2;i=2").get_value():
                return True
            else:
                return False
        except Exception as e:
            print("Error when starting the mixing process:", e)

    def start_product_process(self):
        try:
            self.product_method()
            print("Product process started.")
            if self.client.get_node("ns=2;i=3").get_value():
                return True
            else:
                return False
        except Exception as e:
            print("Error when starting the product process:", e)

    def disconnect(self):
        try:
            if self.client:
                self.client.disconnect()
                print("OPC UA client disconnected successfully.")
        except Exception as e:
            print("Error when disconnecting OPC UA client:", e)