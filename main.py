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
            if not f.read().strip():
                return []
            f.seek(0)
            return json.load(f)
    except Exception as e:
        print("Something is wrong when loading the function!!!")
        print(e)
        return []

def parse_date(date_text: str):
    """
    Converts user date input into YYYY-MM-DD format.
    Accepts YYYY-MM-DD, YYYY/MM/DD, or today.
    """
    date_text = date_text.strip()

    if date_text.upper() == "TODAY":
        return datetime.now().date().isoformat()

    for date_format in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(date_text, date_format).date().isoformat()
        except ValueError:
            continue

    print("[!] Invalid date format. Please use YYYY-MM-DD.")
    return None

def call_menu(function_name: str):
    return lambda: globals()[function_name]()

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
def create_patient(name: str, age: int, gender: str, phone: str, address: str):
    global patients
    id = max(p["patient_id"] for p in patients) + 1 if patients else 0
    new_patient = {
        "patient_id": id,
        "name": name,
        "age": age,
        "gender": gender,
        "phone": phone,
        "address": address
    }
    patients.append(new_patient)
    save_json("patients.json", patients)
    print(f"Patient registered! ID: {id}")
# Global variables here
history = []
pg_idx = 0
doctors: list[dict] = load_json("doctors.json")
appointments: list[dict] = load_json("appointments.json")
patients: list[dict] = load_json("patients.json")
CONSULTATION_FEE = 50
bill_name = []
bill = []

# Menus
@menu
def func1():
    print("This is func1")
    route_options([
        ("func 1 again", func1),
        ("func 2", call_menu("receptionist_main")),
        ("func 3", func3)
    ])
#receptionist
@menu
def receptionist_main():
    print("=" * 96)
    print("Role: Receptionist")
    print("What do you want to do?")
    route_options([
        ("Register new patient",      register_patient),
        ("Search patient",            search_patient),
        ("View all patients",         view_all_patients),
        ("Book appointment",          book_appointment),
        ("Reschedule appointment",    reschedule_appointment),
        ("Cancel appointment",        cancel_appointment),
        ("View appointments",         view_appointments),
        ("Check doctor availability", check_availability),
        ("Back to main menu",         main_menu),
    ])

@menu
def register_patient():
    print("=" * 96)
    print("REGISTER NEW PATIENT")

    # Change this line - generate P001 format
    num = max((int(p["patient_id"][1:]) for p in patients), default=0) + 1
    patient_id = f"P{num:03d}"

    name    = input("Full name   : ").strip()
    age     = int(input("Age         : ").strip())
    gender  = input("Gender (M/F): ").strip().upper()
    phone   = input("Phone       : ").strip()
    address = input("Address     : ").strip()

    new_patient = {
        "patient_id": patient_id,
        "name": name,
        "age": age,
        "gender": gender,
        "phone": phone,
        "address": address
    }
    patients.append(new_patient)
    save_json("patients.json", patients)
    print(f"\n  ✔ Patient registered! ID: {patient_id}")
    input("\nPress ENTER to continue...")
    receptionist_main()

@menu
def search_patient():
    print("=" * 96)
    print("SEARCH PATIENT")

    keyword = input("Enter Patient ID or Name to search: ").strip().lower()
    matches = [p for p in patients if keyword in str(p["patient_id"]) or keyword in p["name"].lower()]

    if not matches:
        print("[!] No matching patient found.")
    else:
        print(f"\n  {'ID':<6} {'Name':<25} {'Age':<5} {'Gender':<8} {'Phone':<14} Address")
        print("  " + "-" * 70)
        for p in matches:
            print(f"  {p['patient_id']:<6} {p['name']:<25} {p['age']:<5} {p['gender']:<8} {p['phone']:<14} {p['address']}")

    input("\nPress ENTER to continue...")
    receptionist_main()

@menu
def view_all_patients():
    print("=" * 96)
    print("ALL REGISTERED PATIENTS")

    if not patients:
        print("[!] No patients registered yet.")
    else:
        print(f"\n  {'ID':<6} {'Name':<25} {'Age':<5} {'Gender':<8} {'Phone':<14} Address")
        print("  " + "-" * 70)
        for p in patients:
            print(f"  {p['patient_id']:<6} {p['name']:<25} {p['age']:<5} {p['gender']:<8} {p['phone']:<14} {p['address']}")

    input("\nPress ENTER to continue...")
    receptionist_main()

@menu
def book_appointment():
    print("=" * 96)
    print("BOOK APPOINTMENT")

    # Check patients exist
    if not patients:
        print("[!] No patients registered yet.")
        input("Press ENTER to continue...")
        receptionist_main()
        return

    # Show all patients
    print(f"\n  {'Patient ID':<12} {'Name':<25} {'Age':<6} {'Gender':<8} Phone")
    print("  " + "-" * 60)
    for p in patients:
        print(f"  {p['patient_id']:<12} {p['name']:<25} {p['age']:<6} {p['gender']:<8} {p['phone']}")

    patient_id = input("\nEnter Patient ID: ").strip()
    patient = next((p for p in patients if str(p["patient_id"]) == patient_id), None)
    if not patient:
        print("[!] Patient not found.")
        input("Press ENTER to continue...")
        receptionist_main()
        return

    # Show all doctors
    if not doctors:
        print("[!] No doctors available.")
        input("Press ENTER to continue...")
        receptionist_main()
        return

    print(f"\n  {'Doctor ID':<12} {'Name':<25} {'Specialization':<20} Fee")
    print("  " + "-" * 65)
    for d in doctors:
        spec = d.get("specialization", "N/A")
        fee  = d.get("fee", "N/A")
        print(f"  {d['doctor_id']:<12} {d['name']:<25} {spec:<20} RM {fee}")

    doctor_id = input("\nEnter Doctor ID: ").strip()
    doctor = next((d for d in doctors if str(d["doctor_id"]) == doctor_id), None)
    if not doctor:
        print("[!] Doctor not found.")
        input("Press ENTER to continue...")
        receptionist_main()
        return

    # Ask for date
    while True:
        date_str = parse_date(input("Enter appointment date (YYYY-MM-DD): ").strip())
        if date_str:
            break

    # Get doctor's slots and cross-check with bookings
    available_slots = doctor.get("available_slots", [])
    if not available_slots:
        print("[!] This doctor has no available slots configured.")
        input("Press ENTER to continue...")
        receptionist_main()
        return

    booked_slots = [
        a["datetime"].split(" ")[1][:5] if " " in a["datetime"]
        else a["datetime"].split("T")[1][:5] if "T" in a["datetime"]
        else ""
        for a in appointments
        if a["doctor_id"] == int(doctor_id)
        and a["datetime"].startswith(date_str)
        and a["status"] != "Cancelled"
    ]

    free_slots = [s for s in available_slots if s not in booked_slots]

    if not free_slots:
        print(f"\n  [!] Dr. {doctor['name']} is fully booked on {date_str}.")
        input("Press ENTER to continue...")
        receptionist_main()
        return

    # Show available slots
    print(f"\n  Available slots for Dr. {doctor['name']} on {date_str}:")
    print("  " + "-" * 30)
    for i, slot in enumerate(free_slots, 1):
        print(f"  [{i}] {slot}")

    # Pick a slot
    while True:
        try:
            slot_choice = int(input("\n  Select slot number: "))
            if 1 <= slot_choice <= len(free_slots):
                chosen_slot = free_slots[slot_choice - 1]
                break
            else:
                print(f"  [!] Please enter a number between 1 and {len(free_slots)}.")
        except ValueError:
            print("  [!] Invalid input. Please enter a number.")

    datetime_str = f"{date_str} {chosen_slot}"

    create_appointment(int(doctor_id), patient_id, "Awaiting", "", "", datetime_str)
    save_json("appointments.json", appointments)

    print("\n  ✔ Appointment booked successfully!")
    print(f"     Patient : {patient['name']} (ID: {patient_id})")
    print(f"     Doctor  : Dr. {doctor['name']} ({doctor.get('specialization', 'N/A')})")
    print(f"     Date    : {datetime_str}")
    print(f"     Fee     : RM {doctor.get('fee', 'N/A')}")

    input("\nPress ENTER to continue...")
    receptionist_main()

@menu
def reschedule_appointment():
    print("=" * 96)
    print("RESCHEDULE APPOINTMENT")

    if not appointments:
        print("[!] No appointments found.")
        input("Press ENTER to continue...")
        receptionist_main()
        return

    # Show only awaiting appointments
    scheduled = [a for a in appointments if a["status"] == "Awaiting"]
    if not scheduled:
        print("[!] No scheduled appointments to reschedule.")
        input("Press ENTER to continue...")
        receptionist_main()
        return

    # Show appointments with patient and doctor name
    print(f"\n  {'Appt ID':<10} {'Patient':<20} {'Doctor':<20} {'Date & Time':<22} Status")
    print("  " + "-" * 85)
    for a in scheduled:
        patient = next((p for p in patients if p["patient_id"] == a["patient_id"]), None)
        doctor  = next((d for d in doctors  if d["doctor_id"]  == a["doctor_id"]),  None)
        p_name  = patient["name"] if patient else f"ID {a['patient_id']}"
        d_name  = f"Dr. {doctor['name']}" if doctor else f"ID {a['doctor_id']}"

        raw_dt   = a["datetime"]
        clean_dt = raw_dt.replace("T", " ").split(".")[0].split("+")[0]

        print(f"  {a['appointment_id']:<10} {p_name:<20} {d_name:<20} {clean_dt:<22} {a['status']}")

    # Pick appointment
    while True:
        try:
            appt_id = int(input("\nEnter Appointment ID to reschedule: ").strip())
            appt = next((a for a in appointments if a["appointment_id"] == appt_id), None)
            if not appt:
                print("[!] Appointment ID not found. Try again.")
                continue
            if appt["status"] != "Awaiting":
                print(f"[!] Cannot reschedule — status is '{appt['status']}'.")
                input("Press ENTER to continue...")
                receptionist_main()
                return
            break
        except ValueError:
            print("[!] Invalid input. Please enter a number.")

    # Get the doctor for this appointment
    doctor = next((d for d in doctors if d["doctor_id"] == appt["doctor_id"]), None)
    if not doctor:
        print("[!] Doctor not found.")
        input("Press ENTER to continue...")
        receptionist_main()
        return

    # Ask for new date
    while True:
        new_date = parse_date(input("Enter appointment date (YYYY-MM-DD): ").strip())
        if new_date:
            break

    # Get doctor slots and cross-check bookings on new date (exclude current appointment)
    available_slots = doctor.get("available_slots", [])
    if not available_slots:
        print("[!] This doctor has no available slots configured.")
        input("Press ENTER to continue...")
        receptionist_main()
        return

    booked_slots = [
        a["datetime"].split(" ")[1][:5] if " " in a["datetime"]
        else a["datetime"].split("T")[1][:5] if "T" in a["datetime"]
        else ""
        for a in appointments
        if a["doctor_id"]       == appt["doctor_id"]
        and a["datetime"].startswith(new_date)
        and a["status"]         != "Cancelled"
        and a["appointment_id"] != appt_id       # exclude current appointment
    ]

    free_slots = [s for s in available_slots if s not in booked_slots]

    if not free_slots:
        print(f"\n  [!] Dr. {doctor['name']} is fully booked on {new_date}.")
        input("Press ENTER to continue...")
        receptionist_main()
        return

    # Show available slots
    print(f"\n  Available slots for Dr. {doctor['name']} on {new_date}:")
    print("  " + "-" * 30)
    for i, slot in enumerate(free_slots, 1):
        print(f"  [{i}] {slot}")

    # Pick a slot
    while True:
        try:
            slot_choice = int(input("\n  Select slot number: "))
            if 1 <= slot_choice <= len(free_slots):
                chosen_slot = free_slots[slot_choice - 1]
                break
            else:
                print(f"  [!] Please enter a number between 1 and {len(free_slots)}.")
        except ValueError:
            print("  [!] Invalid input. Please enter a number.")

    # Update the appointment
    old_datetime     = appt["datetime"]
    appt["datetime"] = f"{new_date} {chosen_slot}"
    save_json("appointments.json", appointments)

    print(f"\n  ✔ Appointment {appt_id} rescheduled successfully!")
    print(f"     Patient  : {next((p['name'] for p in patients if p['patient_id'] == appt['patient_id']), 'N/A')}")
    print(f"     Doctor   : Dr. {doctor['name']} ({doctor.get('specialization', 'N/A')})")
    print(f"     Old time : {old_datetime.replace('T', ' ').split('.')[0].split('+')[0]}")
    print(f"     New time : {appt['datetime']}")

    input("\nPress ENTER to continue...")
    receptionist_main()

@menu
def cancel_appointment():
    print("=" * 96)
    print("CANCEL APPOINTMENT")

    # Filter only active appointments
    active = [a for a in appointments if a["status"] not in ("Cancelled", "Completed")]
    if not active:
        print("[!] No active appointments to cancel.")
        input("Press ENTER to continue...")
        receptionist_main()
        return

    # Show active appointments with patient and doctor name
    print(f"\n  {'Appt ID':<10} {'Patient':<20} {'Doctor':<20} {'Date & Time':<22} Status")
    print("  " + "-" * 85)
    for a in active:
        patient  = next((p for p in patients if p["patient_id"] == a["patient_id"]), None)
        doctor   = next((d for d in doctors  if d["doctor_id"]  == a["doctor_id"]),  None)
        p_name   = patient["name"] if patient else f"ID {a['patient_id']}"
        d_name   = f"Dr. {doctor['name']}" if doctor else f"ID {a['doctor_id']}"

        raw_dt   = a["datetime"]
        clean_dt = raw_dt.replace("T", " ").split(".")[0].split("+")[0]

        print(f"  {a['appointment_id']:<10} {p_name:<20} {d_name:<20} {clean_dt:<22} {a['status']}")

    # Pick appointment
    while True:
        try:
            appt_id = int(input("\nEnter Appointment ID to cancel: ").strip())
            appt = next((a for a in appointments if a["appointment_id"] == appt_id), None)
            if not appt:
                print("[!] Appointment ID not found. Try again.")
                continue
            if appt["status"] in ("Cancelled", "Completed"):
                print(f"[!] Cannot cancel — status is already '{appt['status']}'.")
                input("Press ENTER to continue...")
                receptionist_main()
                return
            break
        except ValueError:
            print("[!] Invalid input. Please enter a number.")

    # Show appointment details before confirming
    patient  = next((p for p in patients if p["patient_id"] == appt["patient_id"]), None)
    doctor   = next((d for d in doctors  if d["doctor_id"]  == appt["doctor_id"]),  None)
    p_name   = patient["name"] if patient else f"ID {appt['patient_id']}"
    d_name   = f"Dr. {doctor['name']} ({doctor.get('specialization', 'N/A')})" if doctor else f"ID {appt['doctor_id']}"
    clean_dt = appt["datetime"].replace("T", " ").split(".")[0].split("+")[0]

    print(f"\n  Appointment details:")
    print(f"     Appt ID  : {appt_id}")
    print(f"     Patient  : {p_name}")
    print(f"     Doctor   : {d_name}")
    print(f"     Date     : {clean_dt}")
    print(f"     Status   : {appt['status']}")

    # Confirm cancellation
    confirm = input("\n  Are you sure you want to cancel this appointment? (Y/N): ").strip().upper()
    if confirm == "Y":
        appt["status"] = "Cancelled"
        save_json("appointments.json", appointments)
        print(f"\n  ✔ Appointment {appt_id} has been cancelled.")
        print(f"     Patient : {p_name}")
        print(f"     Doctor  : {d_name}")
        print(f"     Date    : {clean_dt}")
    else:
        print("\n  Cancellation aborted. No changes made.")

    input("\nPress ENTER to continue...")
    receptionist_main()

@menu
def view_appointments():
    print("=" * 96)
    print("VIEW APPOINTMENTS")

    if not appointments:
        print("[!] No appointments found.")
        input("\nPress ENTER to continue...")
        receptionist_main()
        return

    print(f"\n  {'Appt ID':<10} {'Patient':<20} {'Doctor':<20} {'Date & Time':<22} {'Status':<12} {'Diagnosis':<20} Treatment")
    print("  " + "-" * 115)

    for a in appointments:
        # Get patient name
        patient = next((p for p in patients if p["patient_id"] == a["patient_id"]), None)
        p_name = patient["name"] if patient else f"ID {a['patient_id']}"

        # Get doctor name
        doctor = next((d for d in doctors if d["doctor_id"] == a["doctor_id"]), None)
        d_name = f"Dr. {doctor['name']}" if doctor else f"ID {a['doctor_id']}"

        # Clean up datetime
        raw_dt = a["datetime"]
        clean_dt = raw_dt.replace("T", " ").split(".")[0].split("+")[0]

        # Handle empty fields
        diagnosis = a["diagnosis"] if a["diagnosis"] else "N/A"
        treatment = a["treatment"] if a["treatment"] else "N/A"

        print(f"  {a['appointment_id']:<10} {p_name:<20} {d_name:<20} {clean_dt:<22} {a['status']:<12} {diagnosis:<20} {treatment}")

    input("\nPress ENTER to continue...")
    receptionist_main()

@menu
def check_availability():
    print("=" * 96)
    print("CHECK DOCTOR AVAILABILITY")

    if not doctors:
        print("[!] No doctors available.")
        input("Press ENTER to continue...")
        receptionist_main()
        return

    while True:
        date_str = parse_date(input("Enter appointment date (YYYY-MM-DD): ").strip())
        if date_str:
            break

    print()
    for d in doctors:
        available_slots = d.get("available_slots", [])

        # Get booked slots for this doctor on this date
        booked_slots = [
            a["datetime"].split(" ")[1][:5] if " " in a["datetime"]
            else a["datetime"].split("T")[1][:5] if "T" in a["datetime"]
            else ""
            for a in appointments
            if a["doctor_id"] == d["doctor_id"]
            and a["datetime"].startswith(date_str)
            and a["status"] != "Cancelled"
        ]

        print(f"  Dr. {d['name']} ({d.get('specialization', 'N/A')}) — Fee: RM {d.get('fee', 'N/A')}")
        print(f"  {'Slot':<10} Availability")
        print("  " + "-" * 25)

        if not available_slots:
            print("  No slots configured for this doctor.")
        else:
            for slot in available_slots:
                if slot in booked_slots:
                    print(f"  {slot:<10} ✗ Booked")
                else:
                    print(f"  {slot:<10} ✔ Available")
        print()

    input("Press ENTER to continue...")
    receptionist_main()
@menu
def func3():
    print("This is func3")
    route_options([
        ("func 1", func1),
        ("func 2", receptionist_main),
        ("func 3 again", func3)
    ])

@menu
def finance_main():
    print("This is func3")

    def generate_bill():

        bill_name.clear
        bill.clear
            
        def create_bill():

            while True:

                def add_consultation():
                    bill_name.append("Consultation fees")
                    bill.append(CONSULTATION_FEE)
                    print("Consultation fees added")
                
                def add_bill():
                    item = input("Enter item name: ")
                    bill_name.append(item)
                    price = int(input("Enter price: "))
                    bill.append(price)
                
                route_options([
                ("Add consultation fees", add_consultation),
                ("Add bill item", add_bill),
                ("Back", generate_bill)
                ])

            
        def print_bill():
            def save_bill():
                total = sum(bill)
                appointmend_id =  int(input("Enter appointment ID: "))
                appointments = load_json("appointments.json")
                valid = 0
                for i in appointments:
                    if i["appointment_id"] == appointmend_id:
                        i["fees"] = total
                        save_json("appointments.json", appointments)
                        print("Added")
                        valid = 1
                        break

                if valid == 0:
                    print("Error")

            print("\n===== BILL =====")
            print(f"{'No':<5}{'Item':<25}{'Price':>10}")
            print("-" * 40)

            for i in range(len(bill)):
                print(f"{i+1:<5}{bill_name[i]:<25}{bill[i]:>10.2f}")

            print("-" * 40)
            print(f"{'Total':<30}{sum(bill):>10.2f}")
            
            route_options([
                ("Save bill", save_bill)
            ])

        route_options([
        ("Create bill", create_bill),
        ("Print bill", print_bill)
        ])

    def generate_reports():
        appointments = load_json("appointments.json")
        date_total = 0
        date = input("Enter date (YYYY/MM/DD) or \"today\" for today's date: ")
        if date.upper() == "TODAY":
            date = datetime.now().date()

        for i in appointments:
            if str(datetime.fromisoformat(i["datetime"]).date()) == date:
                date_total += (i["fees"])


        print(f"Total for {date}: {date_total}")

    route_options([
        ("func 1", func1),
        ("func 2", receptionist_main),
        ("func 3 again", func3),
        ("finance_main", finance_main),
        ("Generate Bill", generate_bill),
        ("Generate Reports", generate_reports)
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
        ("Receptionist", receptionist_main),
        ("Doctor", doctor_main),
        ("Finance officer", finance_main) # Replace these function with your main function
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
    ("func2 option", receptionist_main),
    ("func3 option", func3),
]



if __name__ == "__main__":
    # create_appointment(1, 0, "Awaiting", "Ligma", "Balls", datetime.now().isoformat())
    # print(json.dumps(appointments, indent=4))
    # save_json("appointments.json", appointments)
    main_menu()
    pass
