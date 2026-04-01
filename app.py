import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Add a Pet")

col_a, col_b = st.columns(2)
with col_a:
    new_pet_name = st.text_input("New pet name", key="new_pet_name")
with col_b:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"], key="new_pet_species")

if st.button("Add Pet"):
    if new_pet_name.strip():
        new_pet = Pet(name=new_pet_name.strip(), pet_type=new_pet_species)
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Added {new_pet} to {st.session_state.owner.name}'s pets.")
    else:
        st.warning("Please enter a pet name.")

st.divider()

st.subheader("Session State Demo")
st.caption("Shows how st.session_state stores objects across reruns.")

# Guard: only create Owner once
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)

# Guard: only create Pet once
if "pet" not in st.session_state:
    st.session_state.pet = Pet(name=pet_name, pet_type=species)
    st.session_state.owner.add_pet(st.session_state.pet)

# Guard: only create Scheduler once
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)

# Display current vault contents
st.write("**Vault contents:**")
st.write(f"- owner: {st.session_state.owner.name}")
st.write(f"- owner's pets: {[str(p) for p in st.session_state.owner.get_pets()]}")

if st.button("Reset session"):
    del st.session_state["owner"]
    del st.session_state["pet"]
    del st.session_state["scheduler"]
    st.rerun()

st.divider()

st.subheader("Build Schedule")

pet_options = st.session_state.owner.get_pets()
pet_labels = [str(p) for p in pet_options]

if not pet_options:
    st.info("Add a pet above before scheduling tasks.")
else:
    # --- Schedule a Walk ---
    with st.expander("Schedule a Walk", expanded=True):
        walk_pet_label = st.selectbox("Pet", pet_labels, key="walk_pet")
        col_w1, col_w2 = st.columns(2)
        with col_w1:
            walk_start = st.text_input("Start time (HH:MM)", value="08:00", key="walk_start")
        with col_w2:
            walk_duration = st.number_input("Duration (minutes)", min_value=1, max_value=120, value=30, key="walk_duration")

        if st.button("Schedule a Walk"):
            walk_pet = pet_options[pet_labels.index(walk_pet_label)]
            task = Task(
                title="Walk",
                task_type="walk",
                duration_minutes=int(walk_duration),
                start_time=walk_start,
                pet=walk_pet,
            )
            st.session_state.scheduler.add_task(task)
            st.success(f"Scheduled a {int(walk_duration)}-min walk for {walk_pet.name} at {walk_start}.")

    # --- Schedule Grooming ---
    with st.expander("Schedule Grooming", expanded=True):
        groom_pet_label = st.selectbox("Pet", pet_labels, key="groom_pet")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            groom_start = st.text_input("Start time (HH:MM)", value="10:00", key="groom_start")
        with col_g2:
            groom_duration = st.number_input("Duration (minutes)", min_value=1, max_value=120, value=45, key="groom_duration")

        if st.button("Schedule Grooming"):
            groom_pet = pet_options[pet_labels.index(groom_pet_label)]
            task = Task(
                title="Grooming",
                task_type="grooming",
                duration_minutes=int(groom_duration),
                start_time=groom_start,
                pet=groom_pet,
            )
            st.session_state.scheduler.add_task(task)
            st.success(f"Scheduled grooming for {groom_pet.name} at {groom_start}.")

    st.divider()

    if st.button("Generate schedule"):
        schedule = st.session_state.scheduler.generate_schedule()
        if schedule:
            st.text(st.session_state.scheduler.explain_plan(schedule))
        else:
            st.info("No tasks scheduled yet. Use the buttons above to add some.")
