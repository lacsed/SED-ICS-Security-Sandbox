from opcua import Client


class OPCClient:
    def __init__(self, server_url="opc.tcp://localhost:4840/freeopcua/server/"):
        self.server_url = server_url
        self.client = None
        self.obj = None
        self.heating_method = None
        self.mixing_method = None
        self.product_method = None

    def connect(self):
        try:
            self.client = Client(self.server_url)
            self.client.connect()
            print("OPC UA client connected successfully.")

            self.obj = self.client.get_objects_node().get_child(["2:MyObject"])

            self.heating_method = self.obj.get_child(["2:start_heating_process"])
            self.mixing_method = self.obj.get_child(["2:start_mixing_process"])
            self.product_method = self.obj.get_child(["2:start_product_process"])

        except Exception as e:
            print("Error connecting OPC UA client:", e)

    def disconnect(self):
        try:
            if self.client:
                self.client.disconnect()
                print("OPC UA client disconnected successfully.")
        except Exception as e:
            print("Error when disconnecting OPC UA client:", e)

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