
class Tank:
    def __init__(self, name: str):
        if not name:
            raise ValueError("The tank name must not be null or empty.")
        
        self.name = name
        # self.opc_client = opc_client or OPCClient()
        # self.opc_client.value_changed += self._opc_client_data_changed

    """@property
    def data_changed(self):
        return self._data_changed

    @data_changed.setter
    def data_changed(self, handler):
        self._data_changed = handler

    def dispose(self):
        self.opc_client.value_changed -= self._opc_client_data_changed

    def _opc_client_data_changed(self, sender, e):
        print(f"Data changed for node {e.node_id}. Old Value: {e.old_value}, New Value: {e.new_value}")
        self.on_data_changed(e)

    def on_data_changed(self, e):
        if self.data_changed is not None:
            self.data_changed(self, e)"""