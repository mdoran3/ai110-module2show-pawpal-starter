import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Owner, Pet, Task, Scheduler


def make_task(**kwargs) -> Task:
    defaults = dict(
        title="Feed",
        task_type="feeding",
        duration_minutes=5,
        start_time="08:00",
    )
    defaults.update(kwargs)
    return Task(**defaults)


def test_mark_complete_changes_status():
    task = make_task(title="Walk Buddy")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    owner = Owner(name="Alex")
    pet = Pet(name="Buddy", pet_type="Dog", owner=owner)
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    assert len(pet.tasks) == 0

    task = make_task(title="Morning Walk", pet=pet)
    scheduler.add_task(task)

    assert len(pet.tasks) == 1
