import os
from datetime import datetime, date
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

def get_data_path(filepath: str):
    """
    Returns the full path for data files stored beside main.py.
    """
    if os.path.isabs(filepath):
        return filepath
    return os.path.join(BASE_DIR, filepath)

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
        with open(get_data_path(filepath), "r") as f:
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

def create_doctors(name: str, age: int, specialization: str, fee: int, available_slots: list[str]):
    global doctors
    id = max(d["doctor_id"] for d in doctors) + 1  if doctors else 0 # Get biggest id then + 1 for new id, use 0 if no doctors
    new_doctor = {
        "doctor_id": id,
        "name": name,
        "age": age,
        "specialization": specialization,
        "fee": fee,
        "available_slots": available_slots
    }
    doctors.append(new_doctor)

def save_json(filepath: str, data):
    """
    Saves a python dict into json file at target file path

    Args:
        filepath(str): Where the json file will be located
    """
    try:
        with open(get_data_path(filepath), "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print("Please put a proper json object in the function!!! Here's the error msg: ")
        print(e)

def get_patient_by_ID(ID: str):
    """
    Return patient if their ID matched, else return None
    """
    id = ID.upper().strip()
    for p in patients:
        if id == p["patient_id"]:
            return p
    return None

def get_doctor_by_ID(ID: int):
    """
    Return patient if their ID matched, else return None
    """
    for d in doctors:
        if ID == d["doctor_id"]:
            return d
    return None

def get_next_patient_id():
    biggest_id = 0
    for patient in patients:
        patient_id = str(patient.get("patient_id", ""))
        if patient_id.startswith("P") and patient_id[1:].isdigit():
            biggest_id = max(biggest_id, int(patient_id[1:]))
    return f"P{biggest_id + 1:03d}"

def create_appointment(doctor_id: int, patient_id: str, status:str, diagnosis: str, treatment: str, datetime: str):
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
    save_json("appointments.json", appointments)


def create_patient(name: str, age: int, gender: str, phone: str, address: str):
    global patients
    patient_id = get_next_patient_id()
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
    print(f"Patient registered! ID: {patient_id}")

def print_doctors(doctors: list):
    print(f"\n  {'ID':<6} {'Name':<30} {'Age':<5} Specialization")
    print("  " + "-" * 70)
    for d in doctors:
        print(f"  {d["doctor_id"]:<6} {d["name"]:<30} {d["age"]:<5} {d["specialization"]}")

def is_future(appointment):
    return datetime.strptime(appointment["datetime"], '%Y-%m-%d %H:%M').date() > date.today()

def is_today(appointment):
    return datetime.strptime(appointment["datetime"], '%Y-%m-%d %H:%M').date() == date.today()

def save_bill_json(appointment_id):
    bills = load_json("bills.json")

    bill_data = {
        "appointment_id": appointment_id,
        "items": [
            {
                "name": bill_name[i],
                "price": bill[i]
            }
            for i in range(len(bill))
        ],
        "total": sum(bill),
        "outstanding": sum(bill)
    }

    bills.append(bill_data)
    save_json("bills.json", bills)

    print("Bill saved successfully!")

# Global variables here
history = []
pg_idx = 0
doctors: list[dict] = load_json("doctors.json")
appointments: list[dict] = load_json("appointments.json")
patients: list[dict] = load_json("patients.json")
bills: list[dict] = load_json("bills.json")
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
#receptionist menu
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

    patient_id = get_next_patient_id()

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

#Finance menu
@menu
def finance_main():
    def generate_bill():
        def create_bill():
            appointment_id = int(input("Enter appointment id: "))
            for existing_bill in bills:
                if existing_bill["appointment_id"] == appointment_id:
                    print("A bill already exists for this appointment.")
                    route_options([
                    ("Back", generate_bill),
                    ])

            while True:

                def add_consultation():
                    doctor_id = (appointments[appointment_id]["doctor_id"])
                    for i in doctors:
                        if i["doctor_id"] == doctor_id:
                            bill_name.append("Consultation fees")
                            bill.append(i["fee"])
                            print("Consultation fees added")

                def add_bill():
                    item = input("Enter item name: ")
                    bill_name.append(item)
                    price = int(input("Enter price: "))
                    bill.append(price)

                def save_bill():
                    save_bill_json(appointment_id)

                route_options([
                ("Add consultation fees", add_consultation),
                ("Add bill item", add_bill),
                ("Save bill", save_bill),
                ("Back", generate_bill)
                ])
        
        def print_bill():
            bills = load_json("bills.json")

            appointment_id = int(input("Enter appointment ID: "))

            for bill in bills:
                if bill["appointment_id"] == appointment_id:

                    filename = f"bill_{appointment_id}.txt"

                    content = []
                    content.append("=" * 60)
                    content.append(f"BILL FOR APPOINTMENT #{appointment_id}")
                    content.append("=" * 60)
                    content.append(f"{'No':<5}{'Item':<30}{'Price':>10}")
                    content.append("-" * 60)

                    for i, item in enumerate(bill["items"]):
                        content.append(f"{i+1:<5}{item['name']:<30}{item['price']:>10.2f}")

                    content.append("-" * 60)
                    content.append(f"{'TOTAL':<35}{bill['total']:>10.2f}")
                    content.append(f"{'OUTSTANDING':<35}{bill['outstanding']:>10.2f}")
                    content.append("=" * 60)

                    text_output = "\n".join(content)

                    print("\n" + text_output)

                    save_to_txt = input("Save to .txt file? y/N: ")
                    if save_to_txt.upper() == "Y":
                        with open(filename, "w") as f:
                            f.write(text_output)

                        print(f"\nBill exported to {filename}")
                    route_options([
                    ("Back", generate_bill),
                    ])

                print("Bill not found for that appointment ID.")
                route_options([
                ("Back", finance_main),
                ])

        route_options([
        ("Create bill", create_bill),
        ("Print bill", print_bill),
        ("Back", finance_main)
        ])


    def generate_reports():
        def date_revenue():
            revenue = 0
            appointment_id = []
            date = input("Enter date (YYYY/MM/DD) or \"today\" for today's date: ")
            date = parse_date(date)

            for i in appointments:
                if str(datetime.fromisoformat(i["datetime"]).date()) == date:
                    appointment_id.append(i["appointment_id"])

            for i in bills:
                if i["appointment_id"] in appointment_id:
                    revenue += i["total"]
                    
            print(f"Total for {date}: {revenue}")
            route_options([
            ("Home", main_menu),
            ])

        def doctor_revenue():
            print_doctors(doctors)

            doctor = int(input("\nEnter Doctor ID: "))

            appointment_id = []
            revenue = 0
            total_appointments = 0

            for i in appointments:
                if i["doctor_id"] == doctor:
                    appointment_id.append(i["appointment_id"])
                    total_appointments += 1

            for i in bills:
                if i["appointment_id"] in appointment_id:
                    revenue += i["total"]

            print("\n" + "-" * 40)
            print(f"Doctor ID          : {doctor}")
            print(f"Total Appointments : {total_appointments}")
            print(f"Total Revenue      : RM {revenue:,.2f}")
            print("-" * 40)
            route_options([
            ("Back", finance_main),
            ])
        
        route_options([
            ("Daily Revenue", date_revenue),
            ("Revenue by Doctor", doctor_revenue),
            ("Back", finance_main)
        ])
        
    def pay_bill():
        bills = load_json("bills.json")

        appointment_id = int(input("Enter appointment ID: "))

        for bill in bills:
            if bill["appointment_id"] == appointment_id:

                print(f"Total Bill      : RM {bill['total']:.2f}")
                print(f"Outstanding     : RM {bill['outstanding']:.2f}")

                payment = float(input("Payment Amount: "))

                if payment <= 0:
                    print("Invalid payment amount.")
                    return

                if payment > bill["outstanding"]:
                    print("Payment exceeds outstanding amount.")
                    return

                bill["outstanding"] -= payment

                save_json("bills.json", bills)

                print(f"Remaining Balance: RM {bill['outstanding']:.2f}")

                if bill["outstanding"] == 0:
                    print("Bill fully paid.")

                return

        print("Bill not found.")
        
    route_options([
        ("Generate Bill", generate_bill),
        ("Generate Reports", generate_reports),
        ("Pay Bills", pay_bill),
        ("Home", main_menu)
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

# Doctor menu
@menu
def doctor_main():
    print("="*96)
    print("Role: Doctor")
    print("What do you want to do?")
    route_options([
        ("View daily appointment schedule", view_doctor_appointment),
        ("View all future appointments", view_future_appointment),
        ("Record a consultation/Mark appointment status", record_consultation),
        ("Edit past consultation", edit_consultation),
        ("Back to main menu", main_menu)
    ])

def find_doctor():
    """
    Find doctor from user input of Doctor ID or Name.

    Returns: Doctor if found, else None
    """
    keyword = input("Enter Doctor ID or Name to check daily appointment: ").strip().lower()
    matches = [d for d in doctors if keyword in str(d["doctor_id"]) or keyword in d["name"].lower()]

    if not matches: 
        print("[!] No matching patient found.")
        wait = input('\nPress Enter to continue...')
        return None
    elif len(matches) > 1:
        print_doctors(matches)
        wait = input("\n There are more than one doctor with matching name/ID, please specify...")
        return None
    else:
        return matches[0]

def find_appointment_by(apts: list, *conditions) -> list:
    """Going through appoint from input and checking if it satisfy all the conditions

    Return the filtered list of appointment
    """
    matches = []
    # Going through each appointment
    for a in apts:
        # Going throgh each condition to satisfy
        if all(c(a) for c in conditions):
            matches.append(a)
    return matches

def print_appointments(appointments: list) -> None:
    """Given a list of appointments, print it all in a table
    """
    print(f"\nAPPOINTMENTS")
    print(f"  {'ID':<6} {"Patient ID":<10} {"Name":<30} {"Status":<10} {"Datetime"}")
    print("  " + "-" * 70)
    for a in appointments:
        p = get_patient_by_ID(a["patient_id"])
        print(f"  {a["appointment_id"]:<6} {p["patient_id"]:<10} {p["name"]:<30} {a["status"]:<10} {a["datetime"]}")

@menu
def view_doctor_appointment():
    # Insert doctor name or ID
    # Identify which doctor and display their daily appointment 
    # maybe show future appointment as well
    daily_a = []
    print("=" * 96)
    print("SEARCH DOCTOR")
    print_doctors(doctors)

     # Find doctor from user input
    d = find_doctor()
    
    if d:
        # Find appointment based on doctor
        print_doctors([d])
        daily_a = find_appointment_by(appointments, 
                            is_today, # Check if the date is in future
                            lambda a: a["doctor_id"] == d["doctor_id"] # Check if its the doctor's appointment
                            )
    else:
        # Run again to ask for doctor again
        view_doctor_appointment()

    # Check if there is any appoint today
    if not daily_a:
        print("\nThere is no appointment today")
    else:
        print_appointments(daily_a)
    wait = input("Press Enter to continue...")
    doctor_main()

@menu
def view_future_appointment():
    future_a = []
    print("=" * 96)
    print("SEARCH DOCTOR")
    print_doctors(doctors)
    
    # Find doctor from user input
    d = find_doctor()
    
    if d:
        # Find appointment based on doctor
        print_doctors([d])
        future_a = find_appointment_by(appointments, 
                            is_future, # Check if the date is in future
                            lambda a: a["doctor_id"] == d["doctor_id"] # Check if its the doctor's appointment
                            )
    else:
        # Run again to ask for doctor again
        view_future_appointment()


    # Check if there is any appoint today
    if not future_a:
        print("\nThere is no future appointment")
    else:
        print_appointments(future_a)
    wait = input("Press Enter to continue...")
    doctor_main()


@menu
def record_consultation():
    # Display recent appointment (within a month)
    # Select which appointment
    # Mark it status as Complete/Awaiting/Missed/Cancelled
    # Insert diagnosis and treatment

    matched_appointment = []
    # Find which doctor
    print("=" * 96)
    print("SEARCH DOCTOR")
    print_doctors(doctors)
    d = find_doctor()

    if d:
        print_doctors([d])
        matched_appointment = find_appointment_by(appointments, 
                                      lambda a: a["status"] == "Awaiting", # Find all appointments that is awaiting
                                      lambda a: a["doctor_id"] == d["doctor_id"] # Check if doctor id matches
                                      )
    else:
        # Run the function again to get the doctor
        record_consultation()
    
    # Check if there is any appointment
    if not matched_appointment:
        print("No appointment for this doctor to mark")
        wait = input("Press Enter to continue...")
        doctor_main()
    
    print_appointments(matched_appointment)

    # Keep asking for appointment ID until user gives a valid one
    while True:
        try:
            choose = int(input("Enter appointment ID to record: ").strip())
        except ValueError:
            print("Incorrect appointment ID, please try again...")
            continue

        # Find valid appointment where the appointment ID matched
        valid_apt = find_appointment_by(matched_appointment, 
                                    lambda a: a["appointment_id"] == choose
                                    )
        if valid_apt:
            break
        else:
            print("Incorrect appointment ID, please try again...")
            doctor_main()
    
    while True:
        try:
            print()
            print(" Options ".center(96, "="))
            print("""[0] Complete
[1] Cancelled
[2] Missed""")
            print("="*96)
            mark = int(input("Mark the status of the appointment: ").strip())
            if not -1 < mark < 3:
                print("Invalid option, please try again...")
            else: 
                break
        except ValueError:
            print("[!] Invalid input. Please enter a number.")

    a = valid_apt[0]
    if mark == 0:
        # Ask for diagnosis and treatment
        a["status"] = "Complete"
        p = get_patient_by_ID(a["patient_id"])
        diagnosis = input(f"Enter diagnosis for patient {p["patient_id"]} {p["name"]}: ").strip()
        treatment = input(f"Enter treatment for patient {p["patient_id"]} {p["name"]}: ").strip()
        a["diagnosis"] = diagnosis
        a["treatment"] = treatment
    elif mark == 1:
        a["status"] = "Cancelled"
    elif mark == 2:
        a["status"] = "Missed"

    save_json("appointments.json", appointments)
    wait = input("\nPress Enter to continue...")

    # Return to the doctor main menu
    doctor_main()


@menu
def edit_consultation():
    # Display all consultation
    # Select which to edit
    # Make changes
    
    matched_apt = []
    print("=" * 96)
    print("SEARCH DOCTOR")
    print_doctors(doctors)
    # Find doctor from user input
    d = find_doctor()
    
    if d:
        # Find appointment based on doctor
        print_doctors([d])
        matched_apt = find_appointment_by(appointments, 
                            lambda a: a["doctor_id"] == d["doctor_id"], # Check if its the doctor's appointment
                            lambda a: a["status"] != "Awaiting"
                            )
    else:
        # Run again to ask for doctor again
        edit_consultation()

    # Check if there is any appointment
    if not matched_apt:
        print("No appointment for this doctor to edit")
        wait = input("Press Enter to continue...")
        doctor_main()
    
    print_appointments(matched_apt)
    # Keep asking for appointment ID until user gives a valid one
    while True:
        try:
            choose = int(input("Enter appointment ID to edit: ").strip())
        except ValueError:
            print("Incorrect appointment ID, please try again...")
            continue

        # Find valid appointment where the appointment ID matched
        valid_apt = find_appointment_by(matched_apt, 
                                    lambda a: a["appointment_id"] == choose
                                    )
        if valid_apt:
            break
        else:
            print("Incorrect appointment ID, please try again...")
            doctor_main()

    a = valid_apt[0]
    p = get_patient_by_ID(a["patient_id"])
    d = get_doctor_by_ID(a["doctor_id"])
    print("\n    Consultation editing:")
    print(f"     Patient  : {p['name']} (ID: {p["patient_id"]})")
    print(f"     Doctor   : Dr. {d['name']} ({d.get('specialization', 'N/A')})")
    print(f"     Date     : {a["datetime"]}")
    print(f"     Status   : {a["status"]}")
    print(f"     Diagnosis: RM {a.get('diagnosis', 'N/A')}")
    print(f"     Treatment: RM {a.get('treatment', 'N/A')}")

    # Ask for a new status
    while True:
        try:
            print()
            print(" Options ".center(96, "="))
            print("""[0] Complete
[1] Cancelled
[2] Missed""")
            print("="*96)
            mark = int(input("Mark the status of the appointment: ").strip())
            if not -1 < mark < 3:
                print("Invalid option, please try again...")
            else: 
                break
        except ValueError:
            print("[!] Invalid input. Please enter a number.")

    new_diagnosis = ""
    new_treatment = ""
    if mark == 0:
        # Ask for diagnosis and treatment
        new_status = "Complete"
        p = get_patient_by_ID(a["patient_id"])
        new_diagnosis = input(f"Enter new diagnosis for patient {p["patient_id"]} {p["name"]}: ").strip()
        new_treatment = input(f"Enter new treatment for patient {p["patient_id"]} {p["name"]}: ").strip()
    elif mark == 1:
        new_status = "Cancelled"
    elif mark == 2:
        new_status = "Missed"

    print("\n    New Consultation edits")
    print(f"     Patient  : {p['name']} (ID: {p["patient_id"]})")
    print(f"     Doctor   : Dr. {d['name']} ({d.get('specialization', 'N/A')})")
    print(f"     Date     : {a["datetime"]}")
    print(f"     Status   : {new_status}")
    print(f"     Diagnosis: {new_diagnosis if new_diagnosis else "N/A"}")
    print(f"     Treatment: {new_treatment if new_treatment else "N/A"}")

    # Confirm cancellation
    confirm = input("\n  Are you sure you want to edit this consulation? (Y/N): ").strip().upper()
    if confirm == "Y":
        a["status"] = new_status
        a["treatment"] = new_treatment if new_treatment else ""
        a["diagnosis"] = new_diagnosis if new_diagnosis else ""
        save_json("appointments.json", appointments)
        print(f"\n  ✔ Consultation {a["appointment_id"]} has been edited.")
        print(f"     Patient : {p["name"]}")
        print(f"     Doctor  : {d["name"]}")
        print(f"     Date    : {a["datetime"]}")
        print(f"     Diagnosis: {new_diagnosis if new_diagnosis else "N/A"}")
        print(f"     Treatment: {new_treatment if new_treatment else "N/A"}")
    else:
        print("\n  Edits aborted. No changes made.")

    wait = input("Press Enter to continue...")
    doctor_main()
        

if __name__ == "__main__":
    # create_appointment(1, 0, "Awaiting", "Ligma", "Balls", datetime.now().isoformat())
    # print(json.dumps(appointments, indent=4))
    # save_json("appointments.json", appointments)
    main_menu()
    pass
