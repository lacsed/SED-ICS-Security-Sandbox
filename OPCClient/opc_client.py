from opcua import Client

class OPCClient:
    def __init__(self, server_url="opc.tcp://localhost:4840/freeopcua/server/"):
        self.server_url = server_url
        self.client = None
        self.root = None
        self.obj = None
        self.var = None

    def connect(self):
        try:
            self.client = Client(self.server_url)
            self.client.connect()
            self.root = self.client.get_root_node()
            self.obj = self.root.get_child(["0:Objects", "2:MyObject"])
            self.var = self.obj.get_child(["2:MyVariable"])
            print("Cliente OPC UA conectado com sucesso.")
        except Exception as e:
            print("Erro ao conectar cliente OPC UA:", e)

    def read_variable(self):
        try:
            value = self.var.get_value()
            print("Valor atual da variável:", value)
            return value
        except Exception as e:
            print("Erro ao ler variável:", e)
            return None

    def write_variable(self, new_value):
        try:
            print("Escrevendo novo valor:", new_value)
            self.var.set_value(new_value)
            print("Novo valor da variável:", self.var.get_value())
        except Exception as e:
            print("Erro ao escrever variável:", e)

    def disconnect(self):
        try:
            if self.client:
                self.client.disconnect()
                print("Cliente OPC UA desconectado com sucesso.")
        except Exception as e:
            print("Erro ao desconectar cliente OPC UA:", e)