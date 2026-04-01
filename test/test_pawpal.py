import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta
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


def make_scheduler():
    owner = Owner(name="Alex")
    pet = Pet(name="Buddy", pet_type="Dog", owner=owner)
    owner.add_pet(pet)
    return Scheduler(owner=owner), owner, pet


# --- Existing tests ---

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


# --- Sorting ---

def test_sort_by_time_chronological_order():
    scheduler, _, _ = make_scheduler()
    scheduler.add_task(make_task(title="Evening Walk", start_time="18:00"))
    scheduler.add_task(make_task(title="Lunch",        start_time="13:00"))
    scheduler.add_task(make_task(title="Breakfast",    start_time="07:30"))

    scheduler.sort_by_time()

    times = [t.start_time for t in scheduler.tasks]
    assert times == ["07:30", "13:00", "18:00"]


def test_sort_by_time_empty_scheduler():
    scheduler, _, _ = make_scheduler()
    scheduler.sort_by_time()  # must not raise
    assert scheduler.tasks == []


def test_sort_by_time_stable_for_equal_times():
    scheduler, _, _ = make_scheduler()
    t1 = make_task(title="A", start_time="09:00")
    t2 = make_task(title="B", start_time="09:00")
    scheduler.add_task(t1)
    scheduler.add_task(t2)
    scheduler.sort_by_time()
    # Both tasks present and start times unchanged
    assert all(t.start_time == "09:00" for t in scheduler.tasks)
    assert len(scheduler.tasks) == 2


# --- Recurring task logic ---

def test_complete_daily_task_creates_next_day_task():
    scheduler, _, _ = make_scheduler()
    today = date.today()
    task = make_task(title="Breakfast", frequency="daily", due_date=today)
    scheduler.add_task(task)

    next_task = scheduler.complete_task(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.frequency == "daily"
    assert next_task.title == "Breakfast"
    assert next_task.completed is False
    assert next_task in scheduler.tasks


def test_complete_weekly_task_creates_next_week_task():
    scheduler, _, _ = make_scheduler()
    today = date.today()
    task = make_task(title="Grooming", frequency="weekly", due_date=today)
    scheduler.add_task(task)

    next_task = scheduler.complete_task(task)

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=7)


def test_complete_once_task_returns_none():
    scheduler, _, _ = make_scheduler()
    task = make_task(title="Vet Visit", frequency="once")
    scheduler.add_task(task)

    result = scheduler.complete_task(task)

    assert result is None
    assert task.completed is True
    # No new task was added
    assert len(scheduler.tasks) == 1


def test_daily_recurrence_crosses_month_boundary():
    scheduler, _, _ = make_scheduler()
    last_day = date(2024, 1, 31)
    task = make_task(title="Walk", frequency="daily", due_date=last_day)
    scheduler.add_task(task)

    next_task = scheduler.complete_task(task)

    assert next_task.due_date == date(2024, 2, 1)


def test_weekly_recurrence_crosses_year_boundary():
    scheduler, _, _ = make_scheduler()
    last_week = date(2024, 12, 28)
    task = make_task(title="Bath", frequency="weekly", due_date=last_week)
    scheduler.add_task(task)

    next_task = scheduler.complete_task(task)

    assert next_task.due_date == date(2025, 1, 4)


def test_recurring_task_preserves_all_fields():
    scheduler, _, pet = make_scheduler()
    today = date.today()
    task = make_task(
        title="Evening Feed",
        task_type="feeding",
        duration_minutes=10,
        start_time="18:00",
        description="wet food",
        frequency="daily",
        due_date=today,
        pet=pet,
    )
    scheduler.add_task(task)

    next_task = scheduler.complete_task(task)

    assert next_task.title == task.title
    assert next_task.task_type == task.task_type
    assert next_task.duration_minutes == task.duration_minutes
    assert next_task.start_time == task.start_time
    assert next_task.description == task.description
    assert next_task.frequency == task.frequency
    assert next_task.pet is task.pet


# --- Conflict detection ---

def test_overlapping_tasks_detected_as_conflict():
    scheduler, _, _ = make_scheduler()
    today = date.today()
    # 07:00–07:30 overlaps 07:15–07:45
    t1 = make_task(title="Walk",     start_time="07:00", duration_minutes=30, due_date=today)
    t2 = make_task(title="Grooming", start_time="07:15", duration_minutes=30, due_date=today)
    scheduler.add_task(t1)
    scheduler.add_task(t2)

    conflicts = scheduler.get_conflicts()

    assert len(conflicts) == 1
    assert (t1, t2) in conflicts


def test_adjacent_tasks_not_a_conflict():
    scheduler, _, _ = make_scheduler()
    today = date.today()
    # 07:00–07:30 and 07:30–08:00 are adjacent, not overlapping
    t1 = make_task(title="Walk",      start_time="07:00", duration_minutes=30, due_date=today)
    t2 = make_task(title="Breakfast", start_time="07:30", duration_minutes=30, due_date=today)
    scheduler.add_task(t1)
    scheduler.add_task(t2)

    conflicts = scheduler.get_conflicts()

    assert conflicts == []


def test_same_time_different_dates_no_conflict():
    scheduler, _, _ = make_scheduler()
    today = date.today()
    t1 = make_task(title="Walk", start_time="08:00", duration_minutes=30, due_date=today)
    t2 = make_task(title="Walk", start_time="08:00", duration_minutes=30, due_date=today + timedelta(days=1))
    scheduler.add_task(t1)
    scheduler.add_task(t2)

    assert scheduler.get_conflicts() == []


def test_no_conflicts_in_single_task_schedule():
    scheduler, _, _ = make_scheduler()
    scheduler.add_task(make_task())
    assert scheduler.get_conflicts() == []


def test_no_conflicts_in_empty_schedule():
    scheduler, _, _ = make_scheduler()
    assert scheduler.get_conflicts() == []


# --- Filtering ---

def test_filter_by_completion_status():
    scheduler, _, _ = make_scheduler()
    t1 = make_task(title="Done Task")
    t2 = make_task(title="Pending Task")
    scheduler.add_task(t1)
    scheduler.add_task(t2)
    t1.mark_complete()

    pending = scheduler.filter_tasks(completed=False)
    done    = scheduler.filter_tasks(completed=True)

    assert t2 in pending and t1 not in pending
    assert t1 in done    and t2 not in done


def test_filter_by_pet_name():
    owner = Owner(name="Alex")
    buddy   = Pet(name="Buddy",   pet_type="Dog", owner=owner)
    whiskers = Pet(name="Whiskers", pet_type="Cat", owner=owner)
    owner.add_pet(buddy)
    owner.add_pet(whiskers)
    scheduler = Scheduler(owner=owner)

    t1 = make_task(title="Walk",  pet=buddy)
    t2 = make_task(title="Brush", pet=whiskers)
    scheduler.add_task(t1)
    scheduler.add_task(t2)

    buddy_tasks = scheduler.filter_tasks(pet_name="Buddy")

    assert t1 in buddy_tasks and t2 not in buddy_tasks


def test_filter_no_args_returns_all():
    scheduler, _, _ = make_scheduler()
    scheduler.add_task(make_task(title="A"))
    scheduler.add_task(make_task(title="B"))

    assert len(scheduler.filter_tasks()) == 2


def test_filter_does_not_mutate_scheduler():
    scheduler, _, _ = make_scheduler()
    scheduler.add_task(make_task())
    scheduler.add_task(make_task())

    scheduler.filter_tasks(completed=True)

    assert len(scheduler.tasks) == 2


def test_filter_task_with_no_pet_by_pet_name():
    scheduler, _, _ = make_scheduler()
    task = make_task(title="Generic", pet=None)
    scheduler.add_task(task)

    result = scheduler.filter_tasks(pet_name="Buddy")

    assert result == []


# --- Ownership validation ---

def test_add_task_for_unowned_pet_raises():
    owner = Owner(name="Alex")
    scheduler = Scheduler(owner=owner)

    stranger_owner = Owner(name="Bob")
    stranger_pet   = Pet(name="Rex", pet_type="Dog", owner=stranger_owner)
    stranger_owner.add_pet(stranger_pet)

    task = make_task(title="Walk Rex", pet=stranger_pet)

    try:
        scheduler.add_task(task)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_add_task_without_pet_does_not_raise():
    scheduler, _, _ = make_scheduler()
    task = make_task(pet=None)
    scheduler.add_task(task)  # must not raise
    assert task in scheduler.tasks


# --- Remove task ---

def test_remove_task_cleans_both_lists():
    scheduler, _, pet = make_scheduler()
    task = make_task(title="Walk", pet=pet)
    scheduler.add_task(task)

    scheduler.remove_task(task)

    assert task not in scheduler.tasks
    assert task not in pet.tasks


# --- generate_schedule ordering ---

def test_generate_schedule_pending_before_completed():
    scheduler, _, _ = make_scheduler()
    early_done    = make_task(title="Early Done",    start_time="06:00")
    late_pending  = make_task(title="Late Pending",  start_time="22:00")
    scheduler.add_task(early_done)
    scheduler.add_task(late_pending)
    early_done.mark_complete()

    schedule = scheduler.generate_schedule()

    pending_idx = schedule.index(late_pending)
    done_idx    = schedule.index(early_done)
    assert pending_idx < done_idx
