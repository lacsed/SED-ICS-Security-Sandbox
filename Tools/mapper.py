attack_events = {
    0: "Open_Input_Valve",
    1: "Close_Input_Valve",
    2: "Open_Output_Valve",
    3: "Close_Output_Valve",
    4: "Control_Temperature_On",
    5: "Control_Temperature_Off",
    6: "Mixer_On",
    7: "Mixer_Off",
    8: "Pump_On",
    9: "Pump_Off"
}

attack_type = {
    0: "Deny Event",
    1: "Host and Watch",
    2: "Inject Event",
    3: "Intercept Event"
}

def get_event_name(event_number):
    return attack_events.get(event_number)

def get_attack_type(attack_number):
    return attack_type.get(attack_number)
