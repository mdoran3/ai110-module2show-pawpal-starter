# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

The `Scheduler` class includes several features beyond basic task management:

- **Sorting** — `sort_by_time()` orders tasks chronologically by `start_time` using a lambda key on zero-padded `"HH:MM"` strings.
- **Filtering** — `filter_tasks(completed, pet_name)` returns a subset of tasks by completion status, pet name, or both. All parameters are optional.
- **Recurring tasks** — `complete_task(task)` marks a task done and automatically schedules the next occurrence for `daily` (+1 day) and `weekly` (+7 days) tasks using Python's `timedelta`. One-time tasks return `None`.
- **Conflict detection** — `add_task()` warns whenever a new task's time window overlaps with an existing one on the same date. Overlap is detected with the interval check `a_start < b_end and b_start < a_end`, so partial overlaps are caught too. The program continues normally after printing the warning. `get_conflicts()` can also audit the full schedule for all conflicting pairs at once.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Testing PawPal+

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

The core scheduling logic — sorting, filtering, recurring tasks, and conflict detection — is thoroughly tested across normal cases, edge cases, and boundary conditions. The one-star gap reflects areas not yet covered by automated tests: the Streamlit UI layer, `generate_plan()` AI output, and multi-owner or multi-pet scenarios at scale.

---

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
