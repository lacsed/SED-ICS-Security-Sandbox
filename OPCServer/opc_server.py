from opcua import Server

class OPCServer:
    def __init__(self):
        self.server = Server()
        self.uri = "http://industrialplant.com"
        self.idx = None
        self.objects = None
        self.obj = None
        self.var = None

    def start(self):
        try:
            print("Iniciando servidor OPC UA...")
            self.server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
            self.server.start()
            print("Servidor OPC UA iniciado com sucesso.")
            self.idx = self.server.register_namespace(self.uri)
            self.objects = self.server.get_objects_node()
            if self.objects is not None:
                self.obj = self.objects.add_object(self.idx, "MyObject")
                if self.obj is not None:
                    self.var = self.obj.add_variable(self.idx, "MyVariable", 6.7)
                    if self.var is not None:
                        self.var.set_writable()
                        print("Variável adicionada ao servidor OPC UA.")
                    else:
                        print("Falha ao adicionar a variável ao servidor OPC UA.")
                else:
                    print("Falha ao adicionar o objeto ao servidor OPC UA.")
            else:
                print("Falha ao obter o nó de objetos do servidor OPC UA.")
        except Exception as e:
            print("Erro ao iniciar servidor OPC UA:", e)

    def stop(self):
        try:
            self.server.stop()
            print("Servidor OPC UA desligado.")
        except Exception as e:
            print("Erro ao desligar servidor OPC UA:", e)