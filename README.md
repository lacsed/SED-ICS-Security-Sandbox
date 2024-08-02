# Industrial Plant Simulation

This project represents a real industrial process consisting of the following production steps:

1. **Open the Input Valve**
   1. Wait for the event indicating the level has reached the highest value
2. **Close the Input Valve**
3. **Turn on the Temperature Control**
   1. Wait for the event indicating the tank is heated
   2. Wait for the event indicating the tank is cooled
4. **Turn on the Mixer**
5. **Turn off the Mixer**
6. **Turn on the Pump**
7. **Turn off the Pump**
8. **Open the Output Valve**
   1. Wait for the event indicating the level has reached the lowest value
9. **Turn off the Temperature Control**
10. **Close the Output Valve**
11. **Finish the process**

## Project Structure

The project is organized as follows:
```
IndustrialPlantSimulation/
│
├── .venv/                       # Virtual environment
│
├── App/
│   └── app.py                   # Main application entry point
│
├── Configuration/
│   └── set_points.py            # Configuration settings for the application
│
├── Core/
│   ├── Control/
│   │   └── DES/
│   │       └── controller.py    # Control system for the application
│   │
│   ├── Process/
│   │   └── SubSystems/
│   │       └── InputValve/ # Each of all of one the subsystems have a similar structure shown below in the Input Valve subsystem
│   │           ├── Automaton/
│   │           │   └── input_valve_automaton.py     # Automaton for input valve control
│   │           │
│   │           ├── Supervisors/
│   │           │   ├── close_input_valve_supervisor.py  # Supervisor to close input valve
│   │           │   └── open_input_valve_supervisor.py   # Supervisor to open input valve
│   │           │
│   │           └── input_valve.py                     # Input valve system
│   │
│   │       ├── LevelTransmitter/       # Level transmitter subsystem
│   │       ├── Mixer/                  # Mixer subsystem
│   │       ├── OutputValve/            # Output valve subsystem
│   │       ├── Pump/                   # Pump subsystem
│   │       └── TemperatureControl/     # Temperature control subsystem
│
├── OPCClient/                 # OPC client for communication
├── OPCServer/                 # OPC server for communication
├── SCADA/                     # SCADA system integration
│
├── requirements.txt           # List of required Python packages
└── README.md                  # Project documentation
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