from opcua import Server


class OPCServer:
    def __init__(self):
        self.server = Server()
        self.uri = "http://industrialplant.com"
        self.idx = self.server.register_namespace(self.uri)

    def start(self):
        try:
            print("Iniciando servidor OPC UA...")
            self.server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
            self.server.start()
            print("Servidor OPC UA iniciado com sucesso.")
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
            print("Erro ao iniciar servidor OPC UA:", e)

    def stop(self):
        try:
            self.server.stop()
            print("Servidor OPC UA interrompido.")
        except Exception as e:
            print("Erro ao interromper servidor OPC UA:", e)

    def write_variable(self, var_type, value):
        if var_type == "temperature":
            self.temperature_var.set_value(value)
        elif var_type == "flow":
            self.flow_var.set_value(value)
        elif var_type == "time":
            self.time_var.set_value(value)
        elif var_type == "level":
            self.level_var.set_value(value)

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
