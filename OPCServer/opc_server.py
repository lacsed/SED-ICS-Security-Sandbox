from opcua import Server

class OPCServer:
    def __init__(self):
        self.server = Server()
        self.uri = "http://industrialplant.com"
        self.idx = None
        self.objects = None
        self.obj = None
        self.var = None
        self.method_ids = {}

    def start(self):
        try:
            print("Starting OPC UA server...")
            self.server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
            self.server.start()
            print("OPC UA server started successfully.")
            self.idx = self.server.register_namespace(self.uri)
            self.objects = self.server.get_objects_node()
            if self.objects is not None:
                self.obj = self.objects.add_object(self.idx, "MyObject")
                if self.obj is not None:
                    self.var = self.obj.add_variable(self.idx, "Temperature", 0.0)
                    if self.var is not None:
                        self.var.set_writable()
                        print("Temperature variable added to OPC UA server.")
                    else:
                        print("Failed to add temperature variable to OPC UA server.")
                else:
                    print("Failed to add object to OPC UA server.")
            else:
                print("Failed to get objects node from OPC UA server.")

            self.method_ids["start_heating_process"] = self.obj.add_method(self.idx, "start_heating_process", self.start_heating_process)
            self.method_ids["start_mixing_process"] = self.obj.add_method(self.idx, "start_mixing_process", self.start_mixing_process)
            self.method_ids["start_product_process"] = self.obj.add_method(self.idx, "start_product_process", self.start_product_process)

        except Exception as e:
            print("Error starting OPC UA server:", e)

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
