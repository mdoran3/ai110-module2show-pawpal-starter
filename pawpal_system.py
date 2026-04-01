from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass

    def get_pets(self) -> list[Pet]:
        pass


@dataclass
class Pet:
    name: str
    pet_type: str
    owner: Optional[Owner] = None  # None-safe: always check before accessing owner attributes

    def __str__(self) -> str:
        pass


@dataclass
class Task:
    title: str
    task_type: str
    duration_minutes: int
    start_time: str
    pet: Optional[Pet] = None

    def __str__(self) -> str:
        pass


@dataclass
class Scheduler:
    owner: Owner
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        # Validate that task.pet belongs to self.owner before adding
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def generate_schedule(self) -> list[Task]:
        pass

    def explain_plan(self, schedule: list[Task]) -> str:
        pass
