"""
Shared scenario definitions used by both tests and the Streamlit UI demo loader.

Task dicts match the session-state format expected by app.py. The conflict
scenario bypasses generate() and returns a pre-wired schedule directly, since
generate() never produces overlapping slots on its own.
"""
from datetime import time
from pawpal_system import Frequency, Pet, Scheduler, ScheduledTask, Task


# ── task-dict scenarios (loaded into session state in the UI) ─────────────────

RECURRING_SCENARIO = {
    "label": "Recurring Tasks",
    "owner_name": "Jordan",
    "description": (
        "A daily walk, weekly grooming, and a one-off vet visit. "
        "Click Done on each to see recurring tasks reappear."
    ),
    "pet_name": "Mochi",
    "time_budget": 120,
    "tasks": [
        {
            "title": "Morning Walk", "description": "15 min around the block",
            "duration": 30, "priority": 3, "frequency": Frequency.DAILY,
            "due_date": None, "completed": False,
        },
        {
            "title": "Grooming", "description": "Brush and trim",
            "duration": 20, "priority": 2, "frequency": Frequency.WEEKLY,
            "due_date": None, "completed": False,
        },
        {
            "title": "Vet Visit", "description": "Annual checkup (one-off)",
            "duration": 60, "priority": 1, "frequency": Frequency.AS_NEEDED,
            "due_date": None, "completed": False,
        },
    ],
}

REMOVAL_SCENARIO = {
    "label": "Task Removal",
    "owner_name": "Jordan",
    "description": (
        "Three tasks loaded. Remove Feed, then regenerate "
        "to confirm the schedule updates."
    ),
    "pet_name": "Biscuit",
    "time_budget": 120,
    "tasks": [
        {
            "title": "Walk",  "description": "Morning jog",
            "duration": 30, "priority": 3, "frequency": Frequency.DAILY,
            "due_date": None, "completed": False,
        },
        {
            "title": "Feed",  "description": "Breakfast",
            "duration": 15, "priority": 2, "frequency": Frequency.DAILY,
            "due_date": None, "completed": False,
        },
        {
            "title": "Groom", "description": "Brushing",
            "duration": 45, "priority": 1, "frequency": Frequency.AS_NEEDED,
            "due_date": None, "completed": False,
        },
    ],
}

CONFLICT_SCENARIO = {
    "label": "Conflict Detection",
    "owner_name": "Jordan",
    "description": (
        "Two tasks with overlapping time windows loaded for Rex. "
        "The schedule is pre-wired so conflict warnings appear immediately — "
        "generate() assigns sequential slots and never overlaps on its own."
    ),
    "pet_name": "Rex",
    "time_budget": 200,
    "preloaded_schedule": True,   # signals the UI loader to also inject the schedule
    "tasks": [
        {
            "title": "Long Walk", "description": "Extended trail",
            "duration": 90, "priority": 3, "frequency": Frequency.DAILY,
            "due_date": None, "completed": False,
        },
        {
            "title": "Feed", "description": "Lunch",
            "duration": 30, "priority": 2, "frequency": Frequency.DAILY,
            "due_date": None, "completed": False,
        },
    ],
}

ALL_TASK_SCENARIOS = [RECURRING_SCENARIO, REMOVAL_SCENARIO, CONFLICT_SCENARIO]


# ── conflict scenario (injects a pre-wired schedule directly) ─────────────────

def make_conflict_schedule(pet_name: str = "Rex"):
    """
    Return (schedule, conflicts, skipped) with two tasks whose time windows
    overlap so conflict detection fires immediately on load.
    """
    pet  = Pet(name=pet_name)
    walk = Task(
        title="Long Walk", description="Extended trail",
        duration=90, priority=3, pet=pet, frequency=Frequency.DAILY,
    )
    feed = Task(
        title="Feed", description="Lunch",
        duration=30, priority=2, pet=pet, frequency=Frequency.DAILY,
    )
    # 09:00–10:30 and 09:45–10:15 → overlap
    scheduler = Scheduler(time_budget=200)
    scheduler.schedule = [
        ScheduledTask(task=walk, start_time=time(9, 0)),
        ScheduledTask(task=feed, start_time=time(9, 45)),
    ]
    return scheduler.schedule, scheduler.detect_conflicts(), scheduler.skipped
