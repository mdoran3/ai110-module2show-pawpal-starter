# PawPal+

**PawPal+** is a pet care scheduling app built with Python and Streamlit. It helps owners plan, track, and manage daily care tasks for one or more pets — with automatic conflict detection, recurring task support, and filtered schedule views.

---

## Features

### Multi-Pet Management
Each `Owner` maintains a list of `Pet` objects. Pets can be added or removed at any time through the UI. The scheduler validates that every task belongs to a pet owned by the active owner — tasks assigned to an unregistered pet raise a `ValueError`.

### Chronological Sorting
`Scheduler.sort_by_time()` sorts all scheduled tasks in ascending order by `start_time` using a lambda key on zero-padded `"HH:MM"` strings. Tasks added in any order are always displayed chronologically.

### Conflict Detection
Whenever a task is added, `add_task()` checks it against every existing task using the interval overlap formula:

```
a_start < b_end  and  b_start < a_end
```

Partial overlaps are caught, not just full ones. The app continues normally after warning the user. The full schedule can also be audited at any time with `get_conflicts()`, which returns every conflicting pair.

### Recurring Task Scheduling
`Scheduler.complete_task()` marks a task done and automatically schedules the next occurrence:

- **Daily** tasks roll forward **+1 day** via `timedelta(days=1)`
- **Weekly** tasks roll forward **+7 days** via `timedelta(days=7)`
- **One-time** tasks return `None` — no follow-up is created

All fields (title, type, duration, start time, description, pet) are preserved on the new occurrence.

### Filtered Schedule Views
`Scheduler.filter_tasks()` returns a subset of the schedule based on optional parameters:

| Parameter | Behavior |
|---|---|
| `completed=True` | Only completed tasks |
| `completed=False` | Only pending tasks |
| `pet_name="Name"` | Only tasks for that pet |
| Both combined | Intersection of both filters |
| No arguments | All tasks returned |

Filtering never mutates the internal task list.

### Schedule Generation
`Scheduler.generate_schedule()` returns the full task list sorted so **pending tasks always appear before completed ones**, with each group sorted by start time. This is the view used by the "Generate schedule" button in the UI.

### Plan Explanation
`Scheduler.explain_plan()` takes a task list and returns a formatted, human-readable summary — each task's status, pet name, title, start time, duration, and frequency — suitable for displaying to the user as a plain-text report.

### Task Completion with UI Feedback
Each task row in the schedule view includes a **Mark complete** button. Clicking it calls `complete_task()`, which marks the task done and (for recurring tasks) enqueues the next occurrence before refreshing the view.

---

## 📸 Demo

**Owner & Pet Setup** — Enter an owner name, pet name, and species. Additional pets can be added dynamically.

<a href="/course_images/ai110/demo1.png" target="_blank"><img src='/course_images/ai110/demo1.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

**Owner Information & Add a Task** — Registered owner and pets are displayed live. Use "Add a Task" to define custom task types that appear in the Schedule Builder.

<a href="/course_images/ai110/demo2.png" target="_blank"><img src='/course_images/ai110/demo2.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

**Build Schedule** — Expandable panels let you configure start time and duration for each task type (Walk, Grooming, or any custom task) before scheduling it.

<a href="/course_images/ai110/demo3.png" target="_blank"><img src='/course_images/ai110/demo3.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

**View Schedule** — Filter by pet and sort by time. Conflict detection runs automatically. Each task row shows status, duration, and frequency, with a "Mark complete" button for pending tasks. Summary metrics and a plain-text plan explanation are shown below.

<a href="/course_images/ai110/demo4.png" target="_blank"><img src='/course_images/ai110/demo4.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

---

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### Run from the command line (no UI)

```bash
python main.py
```

---

## Testing

Run the full test suite with:

```bash
python -m pytest
```

### What the tests cover

| Area | Tests |
|---|---|
| **Task status** | Marking a task complete flips its `completed` flag |
| **Sorting** | `sort_by_time()` orders tasks chronologically, handles empty schedules, and is stable for equal start times |
| **Recurring tasks** | Daily tasks roll forward +1 day; weekly tasks roll forward +7 days; one-time tasks return `None`; boundary dates (month/year crossings) work correctly; all task fields are preserved on recurrence |
| **Conflict detection** | Overlapping windows on the same date are caught; adjacent (non-overlapping) windows are not flagged; tasks on different dates with the same time don't conflict; empty and single-task schedules return no conflicts |
| **Filtering** | Filter by completion status, pet name, or no arguments (returns all); filtering never mutates the scheduler's task list; tasks without a pet are excluded when filtering by pet name |
| **Ownership validation** | Adding a task for a pet not owned by the scheduler's owner raises `ValueError`; tasks with no pet don't raise |
| **Remove task** | `remove_task()` removes the task from both the scheduler list and the pet's task list |
| **Schedule generation** | `generate_schedule()` places pending tasks before completed ones regardless of start time |

**25 / 25 tests passing.**

### Confidence Level

★★★★☆ (4/5)

The core scheduling logic — sorting, filtering, recurring tasks, and conflict detection — is thoroughly tested across normal cases, edge cases, and boundary conditions. The one-star gap reflects areas not yet covered by automated tests: the Streamlit UI layer and multi-owner or multi-pet scenarios at scale.

---

## Project Structure

```
pawpal_system.py   # Owner, Pet, Task, Scheduler classes
app.py             # Streamlit UI
main.py            # Command-line demo
test/
  test_pawpal.py   # Full automated test suite
```
