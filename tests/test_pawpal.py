"""
Test suite for PawPal+ core scheduler logic.

Components tested:
  1. Sorting Correctness  – generated schedule is chronological; priority ordering holds
  2. Recurrence Logic     – daily/weekly tasks spawn the next occurrence; AS_NEEDED does not
  3. Conflict Detection   – overlapping windows are flagged; back-to-back and empty cases are safe
  4. Time Budget          – over-budget tasks are skipped; completed tasks are excluded
"""
from datetime import date, time, timedelta

import pytest

from pawpal_system import Frequency, Pet, Scheduler, ScheduledTask, Task


# ── helpers ───────────────────────────────────────────────────────────────────

def make_pet(name="Biscuit"):
    return Pet(name=name)


def make_task(pet, title="Walk", priority=2, duration=30,
              frequency=Frequency.DAILY, completed=False):
    return Task(
        title=title,
        description="",
        priority=priority,
        duration=duration,
        pet=pet,
        frequency=frequency,
        completed=completed,
    )


# ── fixed originals ───────────────────────────────────────────────────────────

def test_mark_complete_changes_status():
    pet = make_pet()
    task = make_task(pet, "Walk")
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    pet = make_pet()
    task = make_task(pet, "Walk")
    pet.add_task(task)
    assert len(pet.tasks) == 1


# ── 1. Sorting Correctness ────────────────────────────────────────────────────

class TestSortingCorrectness:
    def test_generated_schedule_is_chronological(self):
        """Start times in the generated schedule must be strictly ascending."""
        pet = make_pet()
        tasks = [
            make_task(pet, "Feed", priority=1, duration=15),
            make_task(pet, "Walk", priority=3, duration=30),
            make_task(pet, "Bath", priority=2, duration=45),
        ]
        scheduler = Scheduler(time_budget=200)
        scheduler.generate(tasks, start_time=time(8, 0))

        times = [st.start_time for st in scheduler.schedule]
        assert times == sorted(times)

    def test_higher_priority_task_gets_earlier_slot(self):
        """Higher-priority tasks occupy earlier time slots."""
        pet = make_pet()
        low = make_task(pet, "Low", priority=1, duration=20)
        high = make_task(pet, "High", priority=5, duration=20)
        scheduler = Scheduler(time_budget=200)
        scheduler.generate([low, high], start_time=time(9, 0))

        assert scheduler.schedule[0].task.title == "High"
        assert scheduler.schedule[1].task.title == "Low"

    def test_generate_with_no_tasks_returns_empty_schedule(self):
        scheduler = Scheduler(time_budget=120)
        scheduler.generate([])
        assert scheduler.schedule == []


# ── 2. Recurrence Logic ───────────────────────────────────────────────────────

class TestRecurrenceLogic:
    def test_daily_task_creates_occurrence_for_next_day(self):
        """Completing a DAILY task adds a new task due tomorrow."""
        pet = make_pet()
        task = make_task(pet, frequency=Frequency.DAILY)
        pet.add_task(task)
        task.mark_complete()

        assert len(pet.tasks) == 2
        new_task = pet.tasks[1]
        assert new_task.due_date == date.today() + timedelta(days=1)

    def test_weekly_task_creates_occurrence_for_next_week(self):
        """Completing a WEEKLY task adds a new task due in seven days."""
        pet = make_pet()
        task = make_task(pet, frequency=Frequency.WEEKLY)
        pet.add_task(task)
        task.mark_complete()

        assert len(pet.tasks) == 2
        assert pet.tasks[1].due_date == date.today() + timedelta(days=7)

    def test_as_needed_task_does_not_recur(self):
        """Completing an AS_NEEDED task must not add a follow-up."""
        pet = make_pet()
        task = make_task(pet, frequency=Frequency.AS_NEEDED)
        pet.add_task(task)
        task.mark_complete()

        assert len(pet.tasks) == 1

    def test_new_recurring_task_starts_as_not_completed(self):
        """The spawned follow-up task must not already be marked complete."""
        pet = make_pet()
        task = make_task(pet, frequency=Frequency.DAILY)
        pet.add_task(task)
        task.mark_complete()

        assert not pet.tasks[1].completed


# ── 3. Conflict Detection ─────────────────────────────────────────────────────

class TestConflictDetection:
    def test_same_start_time_is_flagged(self):
        """Two tasks starting at identical times must produce exactly one warning."""
        pet = make_pet()
        t1 = make_task(pet, "Walk", duration=30)
        t2 = make_task(pet, "Feed", duration=15)
        scheduler = Scheduler(time_budget=200)
        scheduler.schedule = [
            ScheduledTask(task=t1, start_time=time(9, 0)),
            ScheduledTask(task=t2, start_time=time(9, 0)),
        ]

        warnings = scheduler.detect_conflicts()
        assert len(warnings) == 1

    def test_overlapping_windows_produce_warning(self):
        """A task starting inside another's window triggers a WARNING string."""
        pet = make_pet()
        t1 = make_task(pet, "Walk", duration=60)   # 09:00–10:00
        t2 = make_task(pet, "Feed", duration=30)   # 09:30–10:00  ← inside Walk
        scheduler = Scheduler(time_budget=200)
        scheduler.schedule = [
            ScheduledTask(task=t1, start_time=time(9, 0)),
            ScheduledTask(task=t2, start_time=time(9, 30)),
        ]

        warnings = scheduler.detect_conflicts()
        assert len(warnings) == 1
        assert "WARNING" in warnings[0]

    def test_back_to_back_tasks_are_not_a_conflict(self):
        """Tasks ending exactly when the next one starts do not conflict."""
        pet = make_pet()
        t1 = make_task(pet, "Walk", duration=30)   # 09:00–09:30
        t2 = make_task(pet, "Feed", duration=30)   # 09:30–10:00
        scheduler = Scheduler(time_budget=200)
        scheduler.schedule = [
            ScheduledTask(task=t1, start_time=time(9, 0)),
            ScheduledTask(task=t2, start_time=time(9, 30)),
        ]

        assert scheduler.detect_conflicts() == []

    def test_empty_schedule_has_no_conflicts(self):
        scheduler = Scheduler(time_budget=120)
        assert scheduler.detect_conflicts() == []


# ── 4. Time Budget ────────────────────────────────────────────────────────────

class TestTimeBudget:
    def test_task_exceeding_remaining_budget_is_skipped(self):
        """A task that won't fit in the remaining budget is omitted from the schedule."""
        pet = make_pet()
        # heavy has higher priority so it is tried first and skipped (90 > 60 budget)
        heavy = make_task(pet, "Groom", priority=5, duration=90)
        short = make_task(pet, "Feed",  priority=3, duration=20)
        scheduler = Scheduler(time_budget=60)
        scheduler.generate([heavy, short])

        titles = [st.task.title for st in scheduler.schedule]
        assert "Groom" not in titles
        assert "Feed" in titles

    def test_completed_tasks_are_excluded_from_schedule(self):
        """Already-completed tasks must not appear in a freshly generated schedule."""
        pet = make_pet()
        done    = make_task(pet, "Walk", priority=5, duration=30, completed=True)
        pending = make_task(pet, "Feed", priority=3, duration=20)
        scheduler = Scheduler(time_budget=200)
        scheduler.generate([done, pending])

        titles = [st.task.title for st in scheduler.schedule]
        assert "Walk" not in titles
        assert "Feed" in titles
