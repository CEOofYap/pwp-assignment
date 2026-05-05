import os

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
    print("Welcome to SmartClinic - Appointment and Patient System")
    route_options([
        ("Login", func1),
        ("Continue as guest", func2),
        ("Sign up", func3)
    ])

history = []
pg_idx = 0

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
    print("="*30)
    show_options(options)
    print("="*30)
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

test = [
    ("func1 option", func1),
    ("func2 option", func2),
    ("func3 option", func3),
]

if __name__ == "__main__":
    main_menu()
    pass