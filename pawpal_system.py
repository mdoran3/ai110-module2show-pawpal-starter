from dataclasses import dataclass, field


@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet) -> None:
        pass

    def remove_pet(self, pet) -> None:
        pass

    def get_pets(self) -> list:
        pass


@dataclass
class Pet:
    name: str
    type: str
    owner: Owner = None

    def __str__(self) -> str:
        pass


@dataclass
class Task:
    title: str
    task_type: str
    duration_minutes: int
    start_time: str
    pet: Pet = None

    def __str__(self) -> str:
        pass


@dataclass
class Scheduler:
    owner: Owner
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def generate_schedule(self) -> list:
        pass

    def explain_plan(self, schedule: list) -> str:
        pass
    