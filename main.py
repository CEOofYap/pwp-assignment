import os
from datetime import datetime
import json

# Helper function
def clear_menu():
    """
    Clear the terminal when called
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def menu(func):
    def wrapper(*args, **kwargs):
        clear_menu()

        global history, pg_idx

        history.append(func)
        pg_idx+=1

        return func(*args, **kwargs)
    
    return wrapper

def exit():
    print("Exiting program...")
    # print(f"{history=}")
    # print(f"{pg_idx=}")
    quit()

def show_options(options:tuple):
    """
    Print a list of options

    Args:
    options(list of tuples of display msg and function to call)
    """
    for index, option in enumerate(options):
        print(f"[{index}] {option[0]}")

def route_options(options:tuple):
    """
    Print a list of options, then ask for user input.
    It will call the function related to user option.

    Args:
        options(list of tuples of display msg and function to call)
    """
    options.append(("Exit", exit))
    print(" Options ".center(96, "="))
    show_options(options)
    print("="*96)
    user_input : int
    func : any
    while True:
        try: 
            user_input = int(input("Enter your option: "))
        except ValueError:
            print("Invalid input, please try again \n")
            continue
        if not -1 < user_input < len(options):
            print("Invalid input, please try again \n")
            continue

        print(f"You chose [{user_input}]")
        func = options[user_input][1]
        break
    func()

def load_json(filepath:str):
    """
    Loads a json file into python from a file path

    Args:
        filepath(str): Where the json file is located
    """
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        print("Something is wrong when loading the function!!!")
        print(e)

def create_doctors(name: str, age:int):
    global doctors
    id = max(d["doctor_id"] for d in doctors) + 1  if doctors else 0 # Get biggest id then + 1 for new id, use 0 if no doctors
    new_doctor = {
        "doctor_id": id,
        "name": name,
        "age": age,
    }
    doctors.append(new_doctor)

def save_json(filepath: str, data):
    """
    Saves a python dict into json file at target file path

    Args:
        filepath(str): Where the json file will be located
    """
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print("Please put a proper json object in the function!!! Here's the error msg: ")
        print(e)

def create_appointment(doctor_id: int, patient_id: int, status:str, diagnosis: str, treatment: str, datetime: str):
    global appointments
    id = max(a["appointment_id"] for a in appointments) + 1  if appointments else 0 # Get biggest id then + 1 for new id, use 0 if no item in the list
    new_appointment = {
        "appointment_id": id,
        "doctor_id": doctor_id,
        "patient_id": patient_id,
        "status": status,
        "diagnosis": diagnosis,
        "treatment": treatment,
        "datetime": datetime
    }
    appointments.append(new_appointment)

# Global variables here
history = []
pg_idx = 0
doctors: list[dict] = load_json("doctors.json")
appointments: list[dict] = load_json("appointments.json")

# Menus
@menu
def func1():
    print("This is func1")
    route_options([
        ("func 1 again", func1),
        ("func 2", func2),
        ("func 3", func3)
    ])

@menu 
def func2():
    print("This is func2")
    route_options([
        ("func 1", func1),
        ("func 2 again", func2),
        ("func 3", func3)
    ])

@menu
def func3():
    print("This is func3")
    route_options([
        ("func 1", func1),
        ("func 2", func2),
        ("func 3 again", func3)
    ])

@menu
def main_menu():
    print("="*96)
    print(r"""  /$$$$$$                                      /$$      /$$$$$$  /$$ /$$           /$$          
 /$$__  $$                                    | $$     /$$__  $$| $$|__/          |__/          
| $$  \__/ /$$$$$$/$$$$   /$$$$$$   /$$$$$$  /$$$$$$  | $$  \__/| $$ /$$ /$$$$$$$  /$$  /$$$$$$$
|  $$$$$$ | $$_  $$_  $$ |____  $$ /$$__  $$|_  $$_/  | $$      | $$| $$| $$__  $$| $$ /$$_____/
 \____  $$| $$ \ $$ \ $$  /$$$$$$$| $$  \__/  | $$    | $$      | $$| $$| $$  \ $$| $$| $$      
 /$$  \ $$| $$ | $$ | $$ /$$__  $$| $$        | $$ /$$| $$    $$| $$| $$| $$  | $$| $$| $$      
|  $$$$$$/| $$ | $$ | $$|  $$$$$$$| $$        |  $$$$/|  $$$$$$/| $$| $$| $$  | $$| $$|  $$$$$$$
 \______/ |__/ |__/ |__/ \_______/|__/         \___/   \______/ |__/|__/|__/  |__/|__/ \_______/
                                                                                                
""", end="")
    print("Welcome to SmartClinic - Appointment and Patient System")
    route_options([
        ("Administrator", func1),
        ("Receptionist", func2),
        ("Doctor", doctor_main),
        ("Finance officier", func1) # Replace these function with your main function
    ])

@menu
def doctor_main():
    print("="*96)
    print("Role: Doctor")
    print("What do you want to do?")
    route_options([
        ("View appointment", view_appointment),
        ("Record consultation", record_consultation),
        ("Mark appointment status", mark_appointment)
    ])
    
@menu
def view_appointment():
    pass

@menu
def record_consultation():
    pass

@menu
def mark_appointment():
    pass
        


test = [
    ("func1 option", func1),
    ("func2 option", func2),
    ("func3 option", func3),
]

if __name__ == "__main__":
    # create_appointment(1, 0, "Awaiting", "Ligma", "Balls", datetime.now().isoformat())
    # print(json.dumps(appointments, indent=4))
    # save_json("appointments.json", appointments)
    pass