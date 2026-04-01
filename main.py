from pawpal_system import Owner, Pet, Task, Scheduler

# 1) Create an Owner and two Pets
owner = Owner(name="Alex")
buddy = Pet(name="Buddy", pet_type="Dog", owner=owner)
whiskers = Pet(name="Whiskers", pet_type="Cat", owner=owner)
owner.add_pet(buddy)
owner.add_pet(whiskers)

# 2) Create a Scheduler and add tasks OUT OF ORDER intentionally
scheduler = Scheduler(owner=owner)

scheduler.add_task(Task(
    title="Vet Checkup",
    task_type="medical",
    duration_minutes=60,
    start_time="14:30",
    description="Annual wellness exam",
    frequency="once",
    pet=buddy,
))

scheduler.add_task(Task(
    title="Breakfast",
    task_type="feeding",
    duration_minutes=10,
    start_time="08:00",
    description="Half cup dry food",
    frequency="daily",
    pet=whiskers,
))

scheduler.add_task(Task(
    title="Evening Feed",
    task_type="feeding",
    duration_minutes=10,
    start_time="18:00",
    description="Half cup dry food",
    frequency="daily",
    completed=True,
    pet=whiskers,
))

scheduler.add_task(Task(
    title="Morning Walk",
    task_type="exercise",
    duration_minutes=30,
    start_time="07:00",
    description="Walk around the block",
    frequency="daily",
    pet=buddy,
))

# Intentional conflict: Grooming starts at 07:15, overlapping the 07:00-07:30 Morning Walk
scheduler.add_task(Task(
    title="Grooming",
    task_type="grooming",
    duration_minutes=20,
    start_time="07:15",
    description="Brush and trim",
    frequency="weekly",
    pet=buddy,
))

# 3) Print unsorted order to show tasks were added out of order
print("=== Added Order (unsorted) ===")
for task in scheduler.tasks:
    print(f"  {task}")

# 4) Sort and print
scheduler.sort_by_time()
print("\n=== After sort_by_time() ===")
for task in scheduler.tasks:
    print(f"  {task}")

# 5) Filter: pending tasks only
print("\n=== filter_tasks(completed=False) ===")
for task in scheduler.filter_tasks(completed=False):
    print(f"  {task}")

# 6) Filter: completed tasks only
print("\n=== filter_tasks(completed=True) ===")
for task in scheduler.filter_tasks(completed=True):
    print(f"  {task}")

# 7) Filter: Buddy's tasks only
print("\n=== filter_tasks(pet_name='Buddy') ===")
for task in scheduler.filter_tasks(pet_name="Buddy"):
    print(f"  {task}")

# 8) Filter: Whiskers' pending tasks
print("\n=== filter_tasks(completed=False, pet_name='Whiskers') ===")
for task in scheduler.filter_tasks(completed=False, pet_name="Whiskers"):
    print(f"  {task}")
