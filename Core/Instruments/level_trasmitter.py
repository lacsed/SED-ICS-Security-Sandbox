from colorama import init, Fore, Style

init()


class LevelTransmitter:
    def __init__(self, id, current_level, final_level, max_level):
        self.id = id
        self.current_level = current_level
        self.final_level = final_level
        self.max_level = max_level

    def set_level(self, level, time):
        self.current_level = level
        seconds = time % 60
        print(Fore.BLUE + f"[{self.id}] Time: {int(time/60)}m {seconds}s" + Style.RESET_ALL)
        print(Fore.BLUE + f"[{self.id}] Level in {self.current_level:.2f}% of capacity" + Style.RESET_ALL)
    
    def set_final_level(self, final_level):
        self.final_level = final_level
        print(Fore.BLUE + f"[{self.id}] Final level set to {self.final_level}%" + Style.RESET_ALL)
    
    def set_max_level(self, max_level):
        self.max_level = max_level
        print(Fore.BLUE + f"[{self.id}] Max level set to {self.max_level}%" + Style.RESET_ALL)