class Mixer:
    def __init__(self, id, mixing_time):
        self.id = id
        self.mixing_time = mixing_time

    def set_mixing_time(self, mixing_time):
        self.mixing_time = mixing_time
        print(f"Mixing time set to {self.mixing_time} minutes")
    
    def start_mixing(self):
        print("Mixer started")
    
    def stop_mixing(self):
        print("Mixer stopped")