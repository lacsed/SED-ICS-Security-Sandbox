from opcua import Server


class OPCServer:
    def __init__(self):
        self.server = Server()
        self.uri = "http://industrialplant.com"
        self.idx = None
        self.objects = None
        self.obj = None
        self.var = None
        self.heating_process_started = False
        self.mixing_process_started = False
        self.product_process_started = False

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
                    self.var = self.obj.add_variable(self.idx, "MyVariable", 6.7)
                    if self.var is not None:
                        self.var.set_writable()
                        print("Variable added to OPC UA server.")
                    else:
                        print("Failed to add variable to OPC UA server.")
                else:
                    print("Failed to add object to OPC UA server.")
            else:
                print("Failed to get objects node from OPC UA server.")
        except Exception as e:
            print("Error starting OPC UA server:", e)
    
    def start_heating_process(self):
        try:
            self.heating_process_started = True
            print("Heating process started on the server.")
        except Exception as e:
            print("Error starting heating process on the server:", e)
    
    def start_mixing_process(self):
        try:
            self.mixing_process_started = True
            print("Mixing process started on the server.")
        except Exception as e:
            print("Error starting mixing process on the server:", e)

    def start_product_process(self):
        try:
            self.product_process_started = True
            print("Product process started on the server.")
        except Exception as e:
            print("Error starting product process on the server:", e)

    def stop(self):
        try:
            self.server.stop()
            print("OPC UA server stopped.")
        except Exception as e:
            print("Error when shutting down OPC UA server:", e)
