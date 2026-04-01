from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta
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
    due_date: date = field(default_factory=date.today)
    pet: Optional[Pet] = None

    def _start_minutes(self) -> int:
        """Return start_time as total minutes since midnight for arithmetic comparisons."""
        h, m = map(int, self.start_time.split(":"))
        return h * 60 + m

    def conflicts_with(self, other: Task) -> bool:
        """Return True if this task's time window overlaps with another task on the same date."""
        if self.due_date != other.due_date:
            return False
        a_start, a_end = self._start_minutes(), self._start_minutes() + self.duration_minutes
        b_start, b_end = other._start_minutes(), other._start_minutes() + other.duration_minutes
        return a_start < b_end and b_start < a_end

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
        for existing in self.tasks:
            if task.conflicts_with(existing):
                print(f"Warning: '{task.title}' ({task.start_time}) overlaps with '{existing.title}' ({existing.start_time}) on {task.due_date}")
        self.tasks.append(task)
        if task.pet is not None and task not in task.pet.tasks:
            task.pet.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the schedule and from its associated pet's task list."""
        self.tasks.remove(task)
        if task.pet is not None and task in task.pet.tasks:
            task.pet.tasks.remove(task)

    def sort_by_time(self) -> None:
        """Sort tasks in-place by their start_time in ascending chronological order."""
        self.tasks = sorted(self.tasks, key=lambda task: task.start_time)

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task complete and, if daily/weekly, schedule the next occurrence."""
        task.mark_complete()
        if task.frequency not in ("daily", "weekly"):
            return None
        days_ahead = 1 if task.frequency == "daily" else 7
        next_task = Task(
            title=task.title,
            task_type=task.task_type,
            duration_minutes=task.duration_minutes,
            start_time=task.start_time,
            description=task.description,
            frequency=task.frequency,
            due_date=task.due_date + timedelta(days=days_ahead),
            pet=task.pet,
        )
        self.add_task(next_task)
        return next_task

    def get_conflicts(self) -> list[tuple[Task, Task]]:
        """Return all pairs of tasks whose time windows overlap on the same date."""
        conflicts = []
        for i, a in enumerate(self.tasks):
            for b in self.tasks[i + 1:]:
                if a.conflicts_with(b):
                    conflicts.append((a, b))
        return conflicts

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> list[Task]:
        """Return tasks filtered by completion status and/or pet name. Both filters are optional."""
        return [
            task for task in self.tasks
            if (completed is None or task.completed == completed)
            and (pet_name is None or (task.pet is not None and task.pet.name == pet_name))
        ]

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
