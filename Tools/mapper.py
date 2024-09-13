attack_events = {
    0: "Open_Input_Valve",
    1: "Level_High",
    2: "Close_Input_Valve",
    3: "Open_Output_Valve",
    4: "Level_Low",
    5: "Close_Output_Valve",
    6: "Control_Temperature_On",
    7: "Heated",
    8: "Cooled",
    9: "Control_Temperature_Off",
    10: "Mixer_On",
    11: "Mixer_Off",
    12: "Pump_On",
    13: "Pump_Off"
}

attack_type = {
    0: "Deny Event",
    1: "Host and Watch",
    2: "Insert Event",
    3: "Intercept Event",
    4: "Stealth Insert"
}

def get_event_name(event_number):
    return attack_events.get(event_number)

def get_attack_type(attack_number):
    return attack_type.get(attack_number)

def get_event_number(event_name):
    for number, name in attack_events.items():
        if name == event_name:
            return number
    return None

def get_attack_number(attack_name):
    for number, name in attack_type.items():
        if name == attack_name:
            return number
    return None
