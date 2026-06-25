import streamlit as st
from pawpal_system import Owner, Pet, Task

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
owner_name     = st.text_input("Owner name", value="Jordan")
time_available = st.number_input("Time available today (minutes)", min_value=10, max_value=480, value=120)
pet_name       = st.text_input("Pet name", value="Mochi")

st.markdown("### Tasks")
st.caption("Add tasks for your pet. These will feed into the scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

PRIORITY_MAP = {"low": 1, "medium": 2, "high": 3}

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    task = Task(
        title=task_title,
        description="",
        priority=PRIORITY_MAP[priority],
        duration=int(duration),
    )
    st.session_state.tasks.append(task)

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table([
        {"title": t.title, "duration (min)": t.duration, "priority": t.priority}
        for t in st.session_state.tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        owner = Owner(name=owner_name, time_available_minutes=int(time_available))
        pet   = Pet(name=pet_name)
        for task in st.session_state.tasks:
            pet.add_task(task)
        owner.add_pet(pet)

        schedule = owner.get_schedule(pet)

        if not schedule:
            st.warning("No tasks could fit within the available time.")
        else:
            st.success(f"Today's schedule for {pet_name}:")
            for entry in schedule:
                st.write(
                    f"**{entry.start_time.strftime('%H:%M')}** — "
                    f"{entry.task.title} ({entry.task.duration} min) "
                    f"[priority: {entry.task.priority}]"
                )
