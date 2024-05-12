from machines_cost_tracker import PricePlan, MachinesCostTracker


def list_machines(machines_cost_tracker: MachinesCostTracker):
    print(f"Machines: {machines_cost_tracker.get_machines_info()}")


def create_machine(machines_cost_tracker: MachinesCostTracker):
    name = input("Machine Name:\n>")

    if machines_cost_tracker.machine_exists(name=name):
        print(f"Machine with name '{name}' already exists!")
        return

    price_plan = input(
        "Price Plan:\n1. One Dollar Per Minute\n2. Two Dollars Per Minute\n>"
    )

    if price_plan == "1":
        price_plan = PricePlan.ONE_DOLLAR_PER_MINUTE
    elif price_plan == "2":
        price_plan = PricePlan.TWO_DOLLARS_PER_MINUTE
    else:
        print("Input not valid!")
        return

    machines_cost_tracker.create_machine(name=name, price_plan=price_plan)

    print(f"Machine Created: {machines_cost_tracker.get_machine_info(name=name)}")


def delete_machine(machines_cost_tracker: MachinesCostTracker):
    list_machines(machines_cost_tracker=machines_cost_tracker)
    name = input("Machine Name:\n>")
    if machines_cost_tracker.machine_exists(name=name):
        machine_info = machines_cost_tracker.get_machine_info(name=name)
        machines_cost_tracker.delete_machine(name=name)
        print(f"Machine Deleted: {machine_info}")
    else:
        print(f"Machine with name '{name}' does not exist!")


def start_machine(machines_cost_tracker: MachinesCostTracker):
    list_machines(machines_cost_tracker=machines_cost_tracker)
    name = input("Machine Name:\n>")
    if machines_cost_tracker.machine_exists(name=name):
        machines_cost_tracker.start_machine(name=name)
        print(f"Machine Started: {machines_cost_tracker.get_machine_info(name=name)}")
    else:
        print(f"Machine with name '{name}' does not exist!")


def stop_machine(machines_cost_tracker: MachinesCostTracker):
    list_machines(machines_cost_tracker=machines_cost_tracker)
    name = input("Machine Name:\n>")
    if machines_cost_tracker.machine_exists(name=name):
        machines_cost_tracker.stop_machine(name=name)
        print(f"Machine Stopped: {machines_cost_tracker.get_machine_info(name=name)}")
    else:
        print(f"Machine with name '{name}' does not exist!")


def start_all_machines(machines_cost_tracker: MachinesCostTracker):
    machines_cost_tracker.start_all_machines()
    list_machines(machines_cost_tracker=machines_cost_tracker)


def stop_all_machines(machines_cost_tracker: MachinesCostTracker):
    machines_cost_tracker.stop_all_machines()
    list_machines(machines_cost_tracker=machines_cost_tracker)


def get_machine_cost(machines_cost_tracker: MachinesCostTracker):
    list_machines(machines_cost_tracker=machines_cost_tracker)
    name = input("Machine Name:\n>")
    if machines_cost_tracker.machine_exists(name=name):
        print(f"Machine Cost: {machines_cost_tracker.get_machine_cost(name=name)}$")
    else:
        print(f"Machine with name '{name}' does not exist!")


def get_total_cost(machines_cost_tracker: MachinesCostTracker):
    print(f"Total Cost: {machines_cost_tracker.get_total_cost()}$")


def exit_program():
    # needed teardown should be added if project is extended
    exit()


actions = [
    {"id": "1", "title": "List Machines", "callback": list_machines},
    {"id": "2", "title": "Create Machine", "callback": create_machine},
    {"id": "3", "title": "Delete Machine", "callback": delete_machine},
    {"id": "4", "title": "Start Machine", "callback": start_machine},
    {"id": "5", "title": "Stop Machine", "callback": stop_machine},
    {"id": "6", "title": "Start All Machines", "callback": start_all_machines},
    {"id": "7", "title": "Stop All Machines", "callback": stop_all_machines},
    {"id": "8", "title": "Get Machine Cost", "callback": get_machine_cost},
    {"id": "9", "title": "Get Total Cost", "callback": get_total_cost},
]


if __name__ == "__main__":
    machines_cost_tracker = MachinesCostTracker()
    try:
        while True:
            print(
                "----------------------------------------------------------\n"
                + "\n".join(
                    [f"{action['id']}. {action['title']}" for action in actions]
                )
                + "\n----------------------------------------------------------"
            )

            is_valid_input = False
            while not is_valid_input:
                user_input = input(">")
                action = [action for action in actions if user_input == action["id"]]
                if action:
                    is_valid_input = True
                    print("----------------------------------------------------------")
                    action[0]["callback"](machines_cost_tracker)
                else:
                    print("Input not valid!")

    except Exception as e:
        print(f"Exception received: {e}")
    finally:
        exit_program()
