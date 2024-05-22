import ultrades.automata as ud
from Core.Control.DES.Automaton import Automaton
from Core.Control.DES.DES import DES
from Core.Control.SubSystems.InputValve import InputValve
from Core.Control.SubSystems.OutputValve import OutputValve
from Core.Control.SubSystems.Mixer import Mixer
from Core.Control.SubSystems.Pump import Pump
from Core.Control.SubSystems.Temperature import Temperature

class Controller:
    MAX_TEMP = 300
    MIN_TEMP = 10
    MAX_LEVEL = 100
    MIN_LEVEL = 10
    MAX_TIMER = 30
    MIN_TIMER = 2

    tempH1 = 50
    tempH2 = 100
    tempH3 = 200

    timerMixer = 10

    def __init__(self):
        self.start_process = False
        self.stop_process = False
        self.valve_in = False
        self.valve_out = False

        # Events
        self.init = ud.event('9', True)
        self.turn_on_tcontrol = ud.event('19', True)
        self.turn_off_tcontrol = ud.event('21', True)

        self.level_H1 = ud.event('2', False)
        self.level_L1 = ud.event('4', False)
        self.reset = ud.event('6', False)
        self.heated = ud.event('8', False)
        self.cooled = ud.event('10', False)
        self.empty = ud.event('12', False)
        self.process_start = ud.event('14', False)
        self.finish = ud.event('16', False)

        # States
        self.idle = 0
        self.filling = 1
        self.heating = 2
        self.cooling = 3
        self.draining = 4

        self.process_idle = ud.state('0')
        self.process_producing = ud.state('1')

        # Automatons
        self.process_system = Automaton(self.process_idle)

        self.controllable_events = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21}
        self.uncontrollable_events = {2, 4, 6, 8, 10, 12, 14, 16}

        self.plant = DES(self.controllable_events, len(self.controllable_events),
                         self.uncontrollable_events, len(self.uncontrollable_events))

        self.drain_out = False
        self.cool = False
        self.state_process = 0

        self.setup()

    def process_idle_action(self):
        self.drain_out = False
        self.cool = False
        self.state_process = 0

    def process_producing_action(self):
        pass

    def setup(self):
        self.input_valve = InputValve("FV101", 20, 0.8, self.level_H1, self.reset, self.process_start, self.finish, self.init,
                                      self.turn_on_tcontrol, self.valve_in, self.state_process)

        self.output_valve = OutputValve("FV107", 20, 0.8, self.level_L1, self.reset, self.init, self.cooled, self.turn_off_tcontrol,
                                        self.turn_on_tcontrol, self.valve_out, self.state_process)

        self.mixer = Mixer("AC103", 15, self.level_H1, self.reset, self.init, self.cooled, self.turn_off_tcontrol, self.turn_on_tcontrol)

        self.pump = Pump("P106", 20, 0.8, self.reset, self.init, self.heated, self.cooled)

        self.temperature = Temperature("TT104", 25, 25, 100, 2,
                                       self.reset, self.init, self.cooled, self.heated, self.turn_off_tcontrol, self.turn_on_tcontrol)

        self.input_valve.create_automaton()

        self.input_valve.trigger_event(self.input_valve.init)                # Inicializar os supervisores
        self.input_valve.trigger_event(self.input_valve.open_vin)            # Abrir válvula de entrada
        self.input_valve.trigger_event(self.input_valve.close_vin)           # Fechar válvula de entrada
        self.input_valve.trigger_event(self.input_valve.level_H1)            # Ajustar fluxo da válvula
        self.input_valve.trigger_event(self.input_valve.reset)               # Resetar

        self.temperature.create_automaton()

        self.temperature.trigger_event(self.temperature.init)               # Inicializar o supervisor
        self.temperature.trigger_event(self.temperature.turn_on_tcontrol)   # Ligar o controle de temperatura
        self.temperature.trigger_event(self.temperature.heated)             # Ação de aquecimento
        self.temperature.trigger_event(self.temperature.cooled)             # Ação de resfriamento
        self.temperature.trigger_event(self.temperature.turn_off_tcontrol)  # Desligar o controle de temperatura
        self.temperature.trigger_event(self.temperature.reset)              # Resetar

        self.mixer.create_automaton()

        self.mixer.trigger_event(self.mixer.init)                           # Inicializar os supervisores
        self.mixer.trigger_event(self.mixer.turn_on_mixer)                  # Ligar o misturador
        self.mixer.trigger_event(self.mixer.turn_off_mixer)                 # Desligar o misturador
        self.mixer.trigger_event(self.mixer.level_H1)                       # Ação de nível
        self.mixer.trigger_event(self.mixer.reset)                          # Resetar

        self.output_valve.create_automaton()

        self.output_valve.trigger_event(self.output_valve.init)             # Inicializar os supervisores
        self.output_valve.trigger_event(self.output_valve.open_vout)        # Abrir válvula de saída
        self.output_valve.trigger_event(self.output_valve.close_vout)       # Fechar válvula de saída
        self.output_valve.trigger_event(self.output_valve.level_L1)         # Ajustar fluxo da válvula
        self.output_valve.trigger_event(self.output_valve.reset)            # Resetar

        self.pump.create_automaton()

        self.pump.trigger_event(self.pump.init)                             # Inicializar os supervisores
        self.pump.trigger_event(self.pump.turn_on_pump)                     # Ligar a bomba
        self.pump.trigger_event(self.pump.turn_off_pump)                    # Desligar a bomba
        self.pump.trigger_event(self.pump.heated)                           # Ação de aquecimento
        self.pump.trigger_event(self.pump.cooled)                           # Ação de resfriamento
        self.pump.trigger_event(self.pump.reset)                            # Resetar

        print("Process System")
        self.process_system.add_transition(self.process_idle, self.process_producing, self.process_start)
        self.process_system.add_transition(self.process_producing, self.process_idle, self.finish)
        self.process_system.add_transition(self.process_producing, self.process_idle, self.reset)
        self.process_system.add_transition(self.process_idle, self.process_idle, self.reset)

    def loop(self, input):
        # Temperature
        if input <= self.tempH1:
            temp_state = 0
        elif self.tempH1 < input <= self.tempH2:
            temp_state = 1
        elif self.tempH2 < input <= self.tempH3:
            temp_state = 2
        elif input > self.tempH3:
            temp_state = 3
