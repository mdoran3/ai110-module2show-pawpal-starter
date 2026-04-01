import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown("Plan and track pet care tasks — sorted, filtered, and conflict-checked automatically.")

st.divider()

st.subheader("Owner & Pet Setup")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

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

st.subheader("Owner Information")

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

pets = st.session_state.owner.get_pets()
pets_display = ", ".join(str(p) for p in pets) if pets else "None"
st.markdown(f'**Name:** <span style="font-size:0.85em; font-weight:normal;">{st.session_state.owner.name}</span>', unsafe_allow_html=True)
st.markdown(f'**Pets:** <span style="font-size:0.85em; font-weight:normal;">{pets_display}</span>', unsafe_allow_html=True)

if st.button("Reset session"):
    del st.session_state["owner"]
    del st.session_state["pet"]
    del st.session_state["scheduler"]
    st.rerun()

st.divider()

# --- Add a Task (defines a new task type for the Schedule Builder) ---
st.subheader("Add a Task")

if "custom_task_types" not in st.session_state:
    st.session_state.custom_task_types = []

col_at1, col_at2 = st.columns(2)
with col_at1:
    new_task_title = st.text_input("Task name", value="", placeholder="e.g. Feeding", key="new_task_title")
with col_at2:
    new_task_type = st.selectbox("Task type", ["walk", "grooming", "feeding", "vet", "play", "other"], key="new_task_type")

if st.button("Add Task"):
    if new_task_title.strip():
        st.session_state.custom_task_types.append(
            {"title": new_task_title.strip(), "task_type": new_task_type}
        )
        st.success(f"'{new_task_title.strip()}' added to the Schedule Builder.")
    else:
        st.warning("Please enter a task name.")

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

    # --- Dynamic custom task expanders ---
    for i, ct in enumerate(st.session_state.custom_task_types):
        with st.expander(f"Schedule {ct['title']}", expanded=True):
            ct_pet_label = st.selectbox("Pet", pet_labels, key=f"ct_{i}_pet")
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                ct_start = st.text_input("Start time (HH:MM)", value="12:00", key=f"ct_{i}_start")
            with col_c2:
                ct_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=15, key=f"ct_{i}_duration")
            with col_c3:
                ct_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], key=f"ct_{i}_frequency")

            if st.button(f"Schedule {ct['title']}", key=f"ct_{i}_btn"):
                ct_pet = pet_options[pet_labels.index(ct_pet_label)]
                task = Task(
                    title=ct["title"],
                    task_type=ct["task_type"],
                    duration_minutes=int(ct_duration),
                    start_time=ct_start,
                    frequency=ct_frequency,
                    pet=ct_pet,
                )
                st.session_state.scheduler.add_task(task)
                st.success(f"Scheduled {ct['title']} for {ct_pet.name} at {ct_start}.")

    st.divider()

    # --- Filter controls ---
    st.subheader("View Schedule")
    scheduler = st.session_state.scheduler
    pet_filter_options = ["All pets"] + [p.name for p in st.session_state.owner.get_pets()]
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        selected_pet_filter = st.selectbox("Filter by pet", pet_filter_options, key="filter_pet")
    with col_f2:
        sort_order = st.selectbox("Sort by time", ["Earliest first", "Latest first"], key="sort_order")

    if st.button("Generate schedule"):
        pet_name_filter = None if selected_pet_filter == "All pets" else selected_pet_filter

        scheduler.sort_by_time()
        schedule = scheduler.generate_schedule()
        filtered = scheduler.filter_tasks(pet_name=pet_name_filter)
        if sort_order == "Latest first":
            filtered = list(reversed(filtered))

        st.session_state.schedule_generated = True
        st.session_state.schedule_filtered = filtered
        st.session_state.schedule_full = schedule
        st.session_state.schedule_pet_label = selected_pet_filter
        st.session_state.schedule_sort_label = sort_order

    if st.session_state.get("schedule_generated"):
        schedule = st.session_state.schedule_full
        filtered = st.session_state.schedule_filtered

        if not schedule:
            st.info("No tasks scheduled yet. Use the expanders above to add some.")
        else:
            # --- Conflict warnings ---
            conflicts = scheduler.get_conflicts()
            if conflicts:
                st.warning(f"⚠️ {len(conflicts)} scheduling conflict(s) detected:")
                for a, b in conflicts:
                    a_pet = a.pet.name if a.pet else "Unknown"
                    b_pet = b.pet.name if b.pet else "Unknown"
                    st.warning(
                        f"**{a_pet} — {a.title}** ({a.start_time}, {a.duration_minutes} min) "
                        f"overlaps with **{b_pet} — {b.title}** ({b.start_time}, {b.duration_minutes} min)"
                    )
            else:
                st.success("No scheduling conflicts detected.")

            # --- Schedule rows with Mark Complete ---
            if filtered:
                pet_label = st.session_state.schedule_pet_label
                sort_label = st.session_state.schedule_sort_label
                st.markdown(f"#### Schedule — {pet_label} · {sort_label}")

                st.markdown(
                    "<div style='display:grid; grid-template-columns: 80px 80px 1fr 70px 110px 80px 130px; "
                    "font-weight:bold; padding:4px 0; border-bottom:1px solid #ddd;'>"
                    "<span>Status</span><span>Pet</span><span>Task</span><span>Start</span>"
                    "<span>Duration</span><span>Freq</span><span></span></div>",
                    unsafe_allow_html=True,
                )
                for i, task in enumerate(filtered):
                    c1, c2, c3, c4, c5, c6, c7 = st.columns([1, 1, 2, 1, 1.4, 1, 1.6])
                    c1.write("✅ Done" if task.completed else "🕐 Pending")
                    c2.write(task.pet.name if task.pet else "—")
                    c3.write(task.title)
                    c4.write(task.start_time)
                    c5.write(f"{task.duration_minutes} min")
                    c6.write(task.frequency)
                    if not task.completed:
                        if c7.button("Mark complete", key=f"complete_{i}"):
                            scheduler.complete_task(task)
                            # Refresh filtered list in session state
                            st.session_state.schedule_filtered = [
                                t for t in st.session_state.schedule_filtered
                            ]
                            st.rerun()
                    else:
                        c7.write("")

                # Summary counts
                total = len(filtered)
                done = sum(1 for t in filtered if t.completed)
                pending = total - done
                mc1, mc2, mc3 = st.columns(3)
                mc1.metric("Total tasks", total)
                mc2.metric("Pending", pending)
                mc3.metric("Completed", done)

                with st.expander("Plan explanation"):
                    st.text(scheduler.explain_plan(filtered))
            else:
                st.info(f"No tasks found for {st.session_state.schedule_pet_label}.")
