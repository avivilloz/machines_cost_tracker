from datetime import datetime
from datetime import timedelta
from typing import List
from enum import Enum


class PricePlan(Enum):
    """
    Cloud Machine Price Plans
    """

    ONE_DOLLAR_PER_MINUTE = "One Dollar Per Minute"
    TWO_DOLLARS_PER_MINUTE = "Two Dollars Per Minute"


class Machine:
    """
    Responsible for starting, stoping and providing runtime related information for a single cloud machine.
    """

    def __init__(self, name) -> None:
        self.start_time = None
        self.name = name

    def start(self):
        self.start_time = datetime.now()

    def stop(self):
        self.start_time = None

    def get_uptime(self) -> timedelta:
        if not self.start_time:
            return timedelta(seconds=0)
        return datetime.now() - self.start_time


class MachineCostTracker(Machine):
    """
    Responsible for starting, stoping and tracking the cost for a single cloud machine.
    """

    def __init__(self, name: str, price_plan: PricePlan) -> None:
        super().__init__(name)
        self.price_plan = price_plan
        self.total_uptime = timedelta(seconds=0)
        self.is_running = False

    def start(self):
        if not self.is_running:
            super().start()
            self.is_running = True

    def stop(self):
        if self.is_running:
            self.total_uptime += self.get_uptime()
            super().stop()
            self.is_running = False

    def get_cost(self) -> float:
        if self.price_plan == PricePlan.ONE_DOLLAR_PER_MINUTE:
            return round(self._get_total_uptime_in_minutes(), 2)
        elif self.price_plan == PricePlan.TWO_DOLLARS_PER_MINUTE:
            return round(self._get_total_uptime_in_minutes() * 2, 2)

    def _get_total_uptime_in_minutes(self) -> float:
        return (self.total_uptime + self.get_uptime()).total_seconds() / 60

    def get_info(self):
        return dict(
            name=self.name,
            price_plan=self.price_plan.value,
            status="Running" if self.is_running else "Stopped",
            total_uptime_min=f"{round(self._get_total_uptime_in_minutes(), 2)} min",
        )


class MachinesCostTracker:
    """
    Responsible for creating, deleting, starting, stopping and tracking the cost for multiple cloud machines.
    """

    def __init__(self) -> None:
        self.machines: List[MachineCostTracker] = []
        self.total_cost: float = 0

    def create_machine(self, name: str, price_plan: PricePlan):
        self.machines.append(MachineCostTracker(name=name, price_plan=price_plan))

    def delete_machine(self, name: str):
        for machine in self.machines:
            if machine.name == name:
                machine.stop()
                self.total_cost += machine.get_cost()
                self.machines.remove(machine)
                break

    def start_machine(self, name: str):
        for machine in self.machines:
            if machine.name == name:
                machine.start()
                break

    def stop_machine(self, name: str):
        for machine in self.machines:
            if machine.name == name:
                machine.stop()
                break

    def start_all_machines(self):
        for machine in self.machines:
            machine.start()

    def stop_all_machines(self):
        for machine in self.machines:
            machine.stop()

    def get_machine_cost(self, name: str) -> float:
        for machine in self.machines:
            if machine.name == name:
                return machine.get_cost()

    def get_total_cost(self) -> float:
        cost = self.total_cost
        for machine in self.machines:
            cost += machine.get_cost()
        return round(cost, 2)

    def get_machines_names(self):
        return [machine.name for machine in self.machines]

    def get_machine_info(self, name: str) -> dict:
        for machine in self.machines:
            if machine.name == name:
                return machine.get_info()

    def get_machines_info(self):
        return [machine.get_info() for machine in self.machines]

    def machine_exists(self, name: str):
        return any(machine.name == name for machine in self.machines)
