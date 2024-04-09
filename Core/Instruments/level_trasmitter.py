from colorama import init, Fore, Style

init()

class LevelTransmitter:
    def __init__(self, id, current_level, final_level, max_level):
        self.id = id
        self.current_level = current_level
        self.final_level = final_level
        self.max_level = max_level

    def set_level(self):
        self.current_level = self.final_level
        print(Fore.RED + f"[{self.id}] Level set to {self.current_level}%" + Style.RESET_ALL)
    
    def set_final_level(self, final_level):
        self.final_level = final_level
        print(Fore.RED + f"[{self.id}] Final level set to {self.final_level}%" + Style.RESET_ALL)
    
    def set_max_level(self, max_level):
        self.max_level = max_level
        print(Fore.RED + f"[{self.id}] Max level set to {self.max_level}%" + Style.RESET_ALL)