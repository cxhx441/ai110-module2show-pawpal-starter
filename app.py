import streamlit as st
from datetime import date
from pawpal_system import Frequency, Owner, Pet, Scheduler, Task
from scenarios import ALL_TASK_SCENARIOS, make_conflict_schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")
st.title("🐾 PawPal+")

# st.markdown(
#     """
# Welcome to the PawPal+ starter app.
#
# This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
# but **it does not implement the project logic**. Your job is to design the system and build it.
#
# Use this app as your interactive demo once your backend classes/functions exist.
# """
# )

# with st.expander("Scenario", expanded=True):
#     st.markdown(
#         """
# **PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
# for their pet(s) based on constraints like time, priority, and preferences.
#
# You will design and implement the scheduling logic and connect it to this Streamlit UI.
# """
#     )

# with st.expander("What you need to build", expanded=True):
#     st.markdown(
#         """
# At minimum, your system should:
# - Represent pet care tasks (what needs to happen, how long it takes, priority)
# - Represent the pet and the owner (basic info and preferences)
# - Build a plan/schedule for a day that chooses and orders tasks based on constraints
# - Explain the plan (why each task was chosen and when it happens)
# """
#     )

st.divider()

# ── constants ─────────────────────────────────────────────────────────────────

PRIORITY_MAP   = {"Low": 1, "Medium": 2, "High": 3}
PRIORITY_LABEL = {1: "Low", 2: "Medium", 3: "High"}
FREQ_OPTIONS   = {"Daily": Frequency.DAILY, "Weekly": Frequency.WEEKLY, "As needed": Frequency.AS_NEEDED}
FREQ_LABEL     = {Frequency.DAILY: "Daily", Frequency.WEEKLY: "Weekly", Frequency.AS_NEEDED: "As needed"}


def ck(owner: str, pet: str) -> str:
    """Unique key for an owner+pet combo."""
    return f"{owner}/{pet}"


# ── session state ─────────────────────────────────────────────────────────────
# combos:    [{owner, pet, budget}]  — ordered list of owner+pet pairs
# pet_tasks: {ck(owner, pet): [task_dicts]}  — tasks for each combo

if "combos" not in st.session_state:
    st.session_state.combos = []
if "pet_tasks" not in st.session_state:
    st.session_state.pet_tasks = {}

# ── owner + pet management ────────────────────────────────────────────────────

st.subheader("Owner & Pets")

with st.form("add_combo_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        owner_in  = st.text_input("Owner name", placeholder="Jordan")
    with col2:
        pet_in    = st.text_input("Pet name", placeholder="Mochi")
    with col3:
        budget_in = st.number_input("Time budget (min)", min_value=10, max_value=480, value=120)
    if st.form_submit_button("Add owner + pet"):
        if not owner_in.strip() or not pet_in.strip():
            st.error("Both owner and pet name are required.")
        else:
            key = ck(owner_in.strip(), pet_in.strip())
            if any(ck(c["owner"], c["pet"]) == key for c in st.session_state.combos):
                st.error(f"{owner_in.strip()} / {pet_in.strip()} already exists.")
            else:
                st.session_state.combos.append({
                    "owner":  owner_in.strip(),
                    "pet":    pet_in.strip(),
                    "budget": int(budget_in),
                })

if st.session_state.combos:
    COL_C = [2, 2, 2, 1]
    header = st.columns(COL_C)
    for col, lbl in zip(header, ["Owner", "Pet", "Time budget", ""]):
        col.caption(lbl)
    for i, c in enumerate(st.session_state.combos):
        cols = st.columns(COL_C)
        cols[0].write(c["owner"])
        cols[1].write(c["pet"])
        cols[2].write(f"{c['budget']} min")
        with cols[3]:
            if st.button("Remove", key=f"rm_combo_{i}"):
                st.session_state.pet_tasks.pop(ck(c["owner"], c["pet"]), None)
                st.session_state.combos.pop(i)
                st.rerun()
else:
    st.info("No owner + pet combos yet. Add one above.")

# ── demo scenario loader ──────────────────────────────────────────────────────

with st.expander("Load a test scenario"):
    scenario_options = {s["label"]: s for s in ALL_TASK_SCENARIOS}
    chosen = st.selectbox(
        "Scenario",
        list(scenario_options.keys()),
        label_visibility="collapsed",
        key="scenario_selectbox",
    )
    st.caption(scenario_options[chosen]["description"])
    if st.button("Load scenario"):
        s   = scenario_options[chosen]
        key = ck(s["owner_name"], s["pet_name"])
        # Add combo if not present yet
        if not any(ck(c["owner"], c["pet"]) == key for c in st.session_state.combos):
            st.session_state.combos.append({
                "owner":  s["owner_name"],
                "pet":    s["pet_name"],
                "budget": s["time_budget"],
            })
        st.session_state.pet_tasks[key] = [dict(t) for t in s["tasks"]]
        if s.get("preloaded_schedule"):
            sched, conflicts, skipped = make_conflict_schedule(s["pet_name"])
            st.session_state.last_schedule       = sched
            st.session_state.last_conflicts      = conflicts
            st.session_state.last_skipped        = skipped
            st.session_state.last_schedule_label = f"{s['owner_name']} — {s['pet_name']}"
        else:
            st.session_state.pop("last_schedule", None)
        st.rerun()

st.divider()

# ── task management ───────────────────────────────────────────────────────────

st.subheader("Tasks")

if not st.session_state.combos:
    st.info("Add an owner + pet combo above to manage tasks.")
else:
    combo_keys_list = [ck(c["owner"], c["pet"]) for c in st.session_state.combos]
    combo_label_map = {ck(c["owner"], c["pet"]): f"{c['owner']} — {c['pet']}"
                       for c in st.session_state.combos}

    sel_key = st.selectbox(
        "Manage tasks for",
        combo_keys_list,
        format_func=lambda k: combo_label_map[k],
        key="task_combo_selector",
    )
    sel_c = next(c for c in st.session_state.combos if ck(c["owner"], c["pet"]) == sel_key)
    c_key = sel_key

    st.caption(
        f"Adding tasks for **{sel_c['owner']}**'s pet **{sel_c['pet']}** "
        f"({sel_c['budget']} min budget)."
    )

    # ── add task form ─────────────────────────────────────────────────────────
    with st.form("add_task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            task_title = st.text_input("Task title", placeholder="e.g. Morning walk")
        with col2:
            task_desc  = st.text_input("Description", placeholder="e.g. 15 min around the block")

        col1, col2, col3 = st.columns(3)
        with col1:
            duration  = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with col2:
            priority  = st.selectbox("Priority", list(PRIORITY_MAP.keys()), index=2)
        with col3:
            frequency = st.selectbox("Frequency", list(FREQ_OPTIONS.keys()))

        col1, col2 = st.columns([1, 2])
        with col1:
            set_due_date = st.checkbox("Set due date")
        with col2:
            due_date_input = st.date_input("Due date", value=date.today())

        if st.form_submit_button("Add task"):
            if not task_title.strip():
                st.error("Task title is required.")
            else:
                st.session_state.pet_tasks.setdefault(c_key, []).append({
                    "title":       task_title.strip(),
                    "description": task_desc.strip(),
                    "duration":    int(duration),
                    "priority":    PRIORITY_MAP[priority],
                    "frequency":   FREQ_OPTIONS[frequency],
                    "due_date":    due_date_input if set_due_date else None,
                    "completed":   False,
                })

    # ── task list ─────────────────────────────────────────────────────────────
    current_tasks = st.session_state.pet_tasks.get(c_key, [])
    pending_t     = [(i, t) for i, t in enumerate(current_tasks) if not t.get("completed", False)]
    completed_t   = [(i, t) for i, t in enumerate(current_tasks) if t.get("completed", False)]

    if current_tasks:
        COL = [4, 1, 2, 1, 2, 1, 1]
        header = st.columns(COL)
        for col, lbl in zip(header, ["Task", "Priority", "Frequency", "Duration", "Due date", "", ""]):
            col.caption(lbl)

        for i, t in pending_t:
            c = st.columns(COL)
            with c[0]:
                st.markdown(f"**{t['title']}**")
                if t["description"]:
                    st.caption(t["description"])
            c[1].write(PRIORITY_LABEL[t["priority"]])
            c[2].write(FREQ_LABEL[t["frequency"]])
            c[3].write(f"{t['duration']} min")
            c[4].write(t["due_date"].isoformat() if t.get("due_date") else "—")
            with c[5]:
                if st.button("Done", key=f"done_{c_key}_{i}"):
                    _pet  = Pet(name=sel_c["pet"])
                    _task = Task(
                        title=t["title"], description=t["description"],
                        priority=t["priority"], duration=t["duration"],
                        pet=_pet, frequency=t["frequency"], due_date=t["due_date"],
                    )
                    _pet.add_task(_task)
                    _task.mark_complete()
                    st.session_state.pet_tasks[c_key][i]["completed"] = True
                    # mark_complete() appended the next occurrence to _pet.tasks
                    if len(_pet.tasks) > 1:
                        nxt = _pet.tasks[1]
                        st.session_state.pet_tasks[c_key].append({
                            "title":       nxt.title,
                            "description": nxt.description,
                            "duration":    nxt.duration,
                            "priority":    nxt.priority,
                            "frequency":   nxt.frequency,
                            "due_date":    nxt.due_date,
                            "completed":   False,
                        })
                    st.rerun()
            with c[6]:
                if st.button("Remove", key=f"del_{c_key}_{i}"):
                    st.session_state.pet_tasks[c_key].pop(i)
                    st.rerun()

        if completed_t:
            with st.expander(f"Completed ({len(completed_t)})"):
                for _, t in completed_t:
                    st.markdown(f"~~{t['title']}~~")
    else:
        st.info(f"No tasks yet for {sel_c['pet']}. Add one above.")

st.divider()

# ── build schedule ────────────────────────────────────────────────────────────

st.subheader("Build Schedule")

if not st.session_state.combos:
    st.info("Add an owner + pet combo above to build a schedule.")
else:
    gen_options = ["All pets"] + [f"{c['owner']} — {c['pet']}" for c in st.session_state.combos]

    col1, col2 = st.columns([1, 2])
    with col1:
        gen_target = st.selectbox("Generate for", gen_options)
    with col2:
        sort_order = st.radio(
            "Sort schedule by",
            ["Priority (high → low)", "Duration (short → long)"],
            horizontal=True,
        )

    if st.button("Generate schedule"):
        targets = (
            st.session_state.combos
            if gen_target == "All pets"
            else [c for c in st.session_state.combos
                  if f"{c['owner']} — {c['pet']}" == gen_target]
        )

        all_scheduled = []
        all_skipped   = []

        for c in targets:
            c_key_t       = ck(c["owner"], c["pet"])
            pending_tasks = [t for t in st.session_state.pet_tasks.get(c_key_t, [])
                             if not t.get("completed", False)]
            if not pending_tasks:
                continue
            pet   = Pet(name=c["pet"])
            owner = Owner(name=c["owner"], time_available_minutes=c["budget"])
            for t in pending_tasks:
                pet.add_task(Task(
                    title=t["title"], description=t["description"],
                    priority=t["priority"], duration=t["duration"],
                    pet=pet, frequency=t["frequency"], due_date=t["due_date"],
                ))
            owner.add_pet(pet)
            sched = owner.get_schedule(pet)
            all_scheduled.extend(sched)
            all_skipped.extend(owner.scheduler.skipped)

        # detect conflicts across the combined multi-pet schedule
        _combined          = Scheduler(time_budget=0)
        _combined.schedule = all_scheduled
        conflicts          = _combined.detect_conflicts()

        st.session_state.last_schedule       = all_scheduled
        st.session_state.last_conflicts      = conflicts
        st.session_state.last_skipped        = all_skipped
        st.session_state.last_schedule_label = gen_target

    # ── schedule display ──────────────────────────────────────────────────────
    if "last_schedule" in st.session_state:
        schedule       = st.session_state.last_schedule
        conflicts      = st.session_state.last_conflicts
        skipped        = st.session_state.last_skipped
        schedule_label = st.session_state.get("last_schedule_label", "")

        if not schedule:
            st.warning("No tasks could fit within the available time.")
        else:
            st.success(f"Today's schedule — {schedule_label}:")

            display_schedule = (
                sorted(schedule, key=lambda e: e.task.duration)
                if sort_order == "Duration (short → long)"
                else schedule
            )

            st.dataframe(
                [
                    {
                        "Time":           entry.start_time.strftime("%H:%M"),
                        "Pet":            entry.task.pet.name,
                        "Task":           entry.task.title,
                        "Duration (min)": entry.task.duration,
                        "Priority":       PRIORITY_LABEL[entry.task.priority],
                        "Frequency":      FREQ_LABEL.get(entry.task.frequency,
                                                         str(entry.task.frequency)),
                        "Due date":       entry.task.due_date.isoformat()
                                          if entry.task.due_date else "—",
                    }
                    for entry in display_schedule
                ],
                use_container_width=True,
                hide_index=True,
            )

            if skipped:
                names = ", ".join(t.title for t in skipped)
                st.warning(
                    f"{len(skipped)} task(s) skipped — didn't fit in the time budget: {names}"
                )

            if conflicts:
                st.markdown("#### Scheduling Conflicts")
                for warning in conflicts:
                    st.warning(warning)
            else:
                st.caption("No scheduling conflicts detected.")
