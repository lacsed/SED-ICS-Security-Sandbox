class Tank:
    def __init__(self, name: str, capacity: float, batch: float):
        if not name:
            raise ValueError("The tank name must not be null or empty.")
        elif capacity <= 0:
            raise ValueError("The tank capacity must be greater than zero.")
        elif batch <= 0:
            raise ValueError("The tank batch must be greater than zero.")
        self.name = name
        self.capacity = capacity
        self.batch = batch
    
    def set_batch(self, batch: float):
        if batch <= 0:
            raise ValueError("The tank batch must be greater than zero.")
        self.batch = batch
        print(f"Production tank batch set to {self.batch}l")
