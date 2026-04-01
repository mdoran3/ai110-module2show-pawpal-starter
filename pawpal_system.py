from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's list of pets."""
        self.pets.remove(pet)

    def get_pets(self) -> list[Pet]:
        """Return the list of all pets belonging to this owner."""
        return self.pets

    def get_all_tasks(self) -> list[Task]:
        """Return a flat list of all tasks across every pet owned by this owner."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Pet:
    name: str
    pet_type: str
    owner: Optional[Owner] = None  # None-safe: always check before accessing owner attributes
    tasks: list[Task] = field(default_factory=list)

    def __str__(self) -> str:
        """Return a human-readable string with the pet's name and type."""
        return f"{self.name} ({self.pet_type})"


@dataclass
class Task:
    title: str
    task_type: str
    duration_minutes: int
    start_time: str
    description: str = ""
    frequency: str = "once"
    completed: bool = False
    pet: Optional[Pet] = None

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def __str__(self) -> str:
        """Return a formatted string showing the task's status, title, time, duration, and frequency."""
        status = "Done" if self.completed else "Pending"
        return f"[{status}] {self.title} at {self.start_time} ({self.duration_minutes} min, {self.frequency})"


@dataclass
class Scheduler:
    owner: Owner
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule, validating that the associated pet belongs to the owner."""
        if task.pet is not None and task.pet not in self.owner.pets:
            raise ValueError(f"{task.pet.name} does not belong to {self.owner.name}")
        self.tasks.append(task)
        if task.pet is not None and task not in task.pet.tasks:
            task.pet.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the schedule and from its associated pet's task list."""
        self.tasks.remove(task)
        if task.pet is not None and task in task.pet.tasks:
            task.pet.tasks.remove(task)

    def generate_schedule(self) -> list[Task]:
        """Return tasks sorted by completion status then start time, pending tasks first."""
        return sorted(self.tasks, key=lambda t: (t.completed, t.start_time))

    def explain_plan(self, schedule: list[Task]) -> str:
        """Return a formatted, human-readable summary of all scheduled tasks for the owner's pets."""
        if not schedule:
            return f"No tasks scheduled for {self.owner.name}'s pets."
        lines = [f"Schedule for {self.owner.name}'s pets:"]
        for task in schedule:
            pet_name = task.pet.name if task.pet else "Unknown"
            status = "Done" if task.completed else "Pending"
            lines.append(
                f"  [{status}] {pet_name} — {task.title} at {task.start_time} "
                f"({task.duration_minutes} min, {task.frequency})"
            )
        return "\n".join(lines)
