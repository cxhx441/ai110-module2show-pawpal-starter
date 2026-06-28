"""
Scenario-driven tests for PawPal+.

All test data comes from scenarios.py — the same source the UI demo loader uses —
so any scenario that passes here can also be loaded in the browser to verify
the UI behaves correctly.
"""
import pytest
from datetime import date, timedelta

from pawpal_system import Frequency, Owner, Pet, Task
from scenarios import (
    RECURRING_SCENARIO,
    REMOVAL_SCENARIO,
    make_conflict_schedule,
)


# ── helpers ───────────────────────────────────────────────────────────────────

def build_pet_from_scenario(scenario: dict) -> tuple[Pet, list[dict]]:
    """Return a Pet and its task-dict list as defined in a scenario."""
    pet = Pet(name=scenario["pet_name"])
    for d in scenario["tasks"]:
        pet.add_task(Task(
            title=d["title"],
            description=d["description"],
            duration=d["duration"],
            priority=d["priority"],
            pet=pet,
            frequency=d["frequency"],
            due_date=d["due_date"],
        ))
    return pet, scenario["tasks"]


# ── 1. Conflict detection ─────────────────────────────────────────────────────

class TestConflictScenario:
    def test_conflict_schedule_has_warnings(self):
        """make_conflict_schedule() returns at least one warning."""
        schedule, conflicts, skipped = make_conflict_schedule()
        assert len(conflicts) >= 1

    def test_conflict_warning_names_both_tasks(self):
        """Each warning string must identify both overlapping task titles."""
        _, conflicts, _ = make_conflict_schedule()
        assert any("Long Walk" in w and "Feed" in w for w in conflicts)

    def test_conflict_schedule_has_no_skipped_tasks(self):
        """The conflict scenario injects all tasks so none should be skipped."""
        _, _, skipped = make_conflict_schedule()
        assert skipped == []


# ── 2. Recurrence ─────────────────────────────────────────────────────────────

class TestRecurringScenario:
    def test_daily_task_reappears_after_done(self):
        """Marking the daily Morning Walk done adds a follow-up due tomorrow."""
        pet, task_dicts = build_pet_from_scenario(RECURRING_SCENARIO)
        daily_task = next(t for t in pet.tasks if t.frequency is Frequency.DAILY)

        daily_task.mark_complete()

        new_tasks = [t for t in pet.tasks if not t.completed]
        assert any(t.title == daily_task.title for t in new_tasks)
        assert any(t.due_date == date.today() + timedelta(days=1) for t in new_tasks)

    def test_weekly_task_reappears_next_week(self):
        """Marking the weekly Grooming done adds a follow-up due in 7 days."""
        pet, _ = build_pet_from_scenario(RECURRING_SCENARIO)
        weekly_task = next(t for t in pet.tasks if t.frequency is Frequency.WEEKLY)

        weekly_task.mark_complete()

        follow_ups = [t for t in pet.tasks if t.title == weekly_task.title and not t.completed]
        assert len(follow_ups) == 1
        assert follow_ups[0].due_date == date.today() + timedelta(days=7)

    def test_as_needed_task_does_not_reappear(self):
        """Completing the AS_NEEDED Vet Visit must not spawn another task."""
        pet, _ = build_pet_from_scenario(RECURRING_SCENARIO)
        initial_count = len(pet.tasks)
        one_off = next(t for t in pet.tasks if t.frequency is Frequency.AS_NEEDED)

        one_off.mark_complete()

        assert len(pet.tasks) == initial_count


# ── 3. Task removal ───────────────────────────────────────────────────────────

class TestRemovalScenario:
    def test_removed_task_absent_from_list(self):
        """After removing Feed the pet's task list no longer contains it."""
        pet, _ = build_pet_from_scenario(REMOVAL_SCENARIO)
        feed = next(t for t in pet.tasks if t.title == "Feed")

        pet.remove_task(feed)

        assert feed not in pet.tasks

    def test_other_tasks_unaffected_after_removal(self):
        """Walk and Groom must still be present after Feed is removed."""
        pet, _ = build_pet_from_scenario(REMOVAL_SCENARIO)
        feed = next(t for t in pet.tasks if t.title == "Feed")
        remaining_before = {t.title for t in pet.tasks if t is not feed}

        pet.remove_task(feed)

        assert {t.title for t in pet.tasks} == remaining_before

    def test_schedule_excludes_removed_task(self):
        """Generating a schedule after removal must not include the removed task."""
        pet, _ = build_pet_from_scenario(REMOVAL_SCENARIO)
        feed = next(t for t in pet.tasks if t.title == "Feed")
        pet.remove_task(feed)

        owner = Owner(name="Jordan", time_available_minutes=REMOVAL_SCENARIO["time_budget"])
        owner.add_pet(pet)
        schedule = owner.get_schedule(pet)

        scheduled_titles = [entry.task.title for entry in schedule]
        assert "Feed" not in scheduled_titles
        assert "Walk" in scheduled_titles
