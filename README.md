# Industrial Plant Simulation

This project represents a real industrial process consisting of the following production steps:

1. **Open the Input Valve**
   - The input valve opens, allowing fluid to flow into the tank.
   - The system monitors the fluid level, waiting until the level high event is triggered, indicating that the tank is full
2. **Close the Input Valve**
   - Once the level high event is detected, the input valve is closed to stop the inflow of fluid.
3. **Heat the Fluid**
   - The temperature control system is activated to heat the fluid in the tank.
   - Simultaneously, the mixer is turned on to ensure even heating of the fluid.
   - The mixer remains on until the heated event is triggered, indicating the fluid has reached the desired temperature.
4. **Cool the Tank:**
   - After heating, the cooling phase begins. 
   - The pump is turned on to assist in cooling the fluid. 
   - The system continues cooling until the cooled event is triggered, confirming that the fluid has reached the required low temperature.
5. **Open the Output Valve**
   -  The output valve opens to release the fluid from the tank. 
   - The system waits until the level low event is triggered, indicating the tank has emptied to the desired level.
6. **Close the Output Valve**
   - Once the tank is emptied, the output valve is closed to complete the outflow process. 
7. **Finish the Process**
   - After the output valve is closed, the system concludes the current process cycle. 

## Project Structure

The project is organized as follows:
```
IndustrialPlantSimulation/
│
├── .venv/                        # Virtual environment
│
├── App/
│   └── app.py                    # Main application entry point
│
├── Attacker/
│   ├── Arsenal/
│   │   ├── deny_event.py         # Logic for denying events
│   │   ├── host_and_watch.py     # Host and watch attacker logic
│   │   ├── insert_event.py       # Logic for inserting events
│   │   ├── intercept_event.py    # Logic for intercepting events
│   │   └── stealth_insert.py     # Logic for stealth event insertion
│   ├── Automaton/
│   │   └── attack_automaton.py   # Automaton for attack control
│   └── attacker.py               # Main attacker thread module
│
├── Configuration/
│   └── set_points.py             # Configuration settings for the application
│
├── Core/
│   ├── Control/
│   │   └── DES/
│   │   │   ├── Automaton.py      # Implementation of a automaton logic
│   │   │   ├── DES.py            # Main control logic of a DES service manager
│   │   │   ├── State.py          # State DES definition
│   │   │   └── Supervisor.py     # Implementation of a supervisor logic
│   │   └── controller.py         # Control system for the application
│   │
│   ├── Process/
│   │   ├── Automaton/
│   │   │   └── process_automaton.py  # Automaton for process control
│   │   ├── Tank/
│   │   │   └── tank.py               # Tank system control
│   │   └── process.py                # Process logic
│   │
│   └── SubSystems/
│       ├── InputValve/
│       │   ├── Automaton/
│       │   │   └── input_valve_automaton.py         # Automaton for input valve control
│       │   ├── Supervisors/
│       │   │   ├── close_input_valve_supervisor.py  # Supervisor to close input valve
│       │   │   └── open_input_valve_supervisor.py   # Supervisor to open input valve
│       │   └── input_valve.py                       # Input valve system
│       │
│       ├── LevelTransmitter/        # Level transmitter subsystem
│       ├── Mixer/                   # Mixer subsystem
│       ├── OutputValve/             # Output valve subsystem
│       ├── Pump/                    # Pump subsystem
│       └── TemperatureControl/      # Temperature control subsystem
│
├── IDS/
│   ├── ids.py                     # Implementation of IDS thread monitoring
│   └── process_sequence.py        # Expected event sequence of the system
│
├── OPCClient/                     # OPC client for communication
├── OPCServer/                     # OPC server for communication
├── SCADA/                         # SCADA system integration
│
├── Tools/
│   └── mapper.py                  # Tool for mapping data
│
├── requirements.txt               # List of required Python packages
└── README.md                      # Project documentation
```

## Installation

### Requirements

- Python 3.x
- InduSoft Web Studio Educational
- Required packages listed in `requirements.txt`

### Installation Steps

#### Install Python

1. **Download Python:**
   - Go to the [Python downloads page](https://www.python.org/downloads/).
   - Select the version suitable for your operating system and download it.

2. **Install Python:**
   - Run the downloaded installer.
   - Make sure to check the box that says "Add Python to PATH."
   - Follow the installation instructions.

3. **Verify Python Installation:**
   - Open a terminal or command prompt.
   - Type `python --version` and press Enter.
   - You should see the installed Python version.

#### Install InduSoft Web Studio Educational

1. **Download InduSoft Web Studio Educational:**
   - Go to the [InduSoft Web Studio download page (only for UFMG members)](https://ufmgbr-my.sharepoint.com/:u:/g/personal/hugomichel_ufmg_br/EaMcR4JxMh1Fv4o6hcDO3O8B_YHsXh1dgMilNt2FRcPKFw?e=u5ooTI).

2. **Install InduSoft Web Studio Educational:**
   - Unzip the folder (IWSEduXX.Y.Y.zip) containing the installation file. 
   - Run the “Setup.exe” file with Administrator privileges (Right Click -> Run as Administrator) located in the “...\IWSEduXX.Y.Y\DISK1\” folder.
   - Obtaining a Site Code:
     - Close all modules from InduSoft Web Studio Educational. 
     - Run the “Register” module with elevated privileges ([Windows Start Menu] > All Programs > Wonderware InduSoft Web Studio Educational vX.Y > Register > Run as administrator):
     - Select “Softkey” Protection Type and click “Check...”
     - “Change License...”
     - Choose the Network Adapter in order to generate your Site Code. Copie it using the button located on the right hand side of the field
     - Obtaining the Site Key:
       - Access [AVEVA Edge Educational(formerly InduSoft Web Studio Educational)](https://om.aveva.com/InduSoftActivation/Home/Education)
       - Paste the Site Code from the Register module (Step 1) on “Site Code” field.
       - Generate License.
       - Copy and paste the generated Site Key on the Register module and click “Authorize”
       - The updated Softkey Settings is displayed. Click on “Close” and start using InduSoft Web Studio Educational.


#### Set Up the Project Environment

1. Clone the repository:
    ```sh
    git clone https://github.com/marconefaria/IndustrialPlantSimulation.git
    ```

2. Navigate to the project directory:
    ```sh
    cd App
    ```

3. Create a virtual environment:
    ```sh
    python3 -m venv venv
    ```

4. Activate the virtual environment:

    On Windows:
    ```sh
    venv\Scripts\activate
    ```

    On macOS and Linux:
    ```sh
    source venv/bin/activate
    ```

5. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To run this project, execute the script shown below:

```sh
python app.py
```

And run the executable IndustrialPlantSimulation localized in the directory:

```sh
    cd SCADA\IndustrialPlantSimulation
```