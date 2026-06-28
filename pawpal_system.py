from __future__ import annotations
from dataclasses import dataclass, field, replace
from datetime import date, datetime, time, timedelta
from enum import Enum


class Frequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    AS_NEEDED = "as_needed"


@dataclass
class Task:
    title: str
    description: str
    priority: int
    duration: int  # minutes
    pet: Pet
    frequency: Frequency = Frequency.DAILY
    completed: bool = False
    due_date: date | None = field(default=None)

    def mark_complete(self) -> None:
        """Mark complete and queue the next occurrence for recurring tasks."""
        self.completed = True
        if self.frequency is Frequency.AS_NEEDED:
            return
        delta = timedelta(days=1 if self.frequency is Frequency.DAILY else 7)
        self.pet.add_task(replace(self, completed=False, due_date=date.today() + delta))


@dataclass(frozen=True)
class ScheduledTask:
    task: Task
    start_time: time


@dataclass
class Scheduler:
    time_budget: int  # total minutes available for the day
    schedule: list[ScheduledTask] = field(default_factory=list)
    skipped: list[Task] = field(default_factory=list)

    def filter_tasks(
        self,
        completed: bool | None = None,
        pet: Pet | None = None,
    ) -> list[ScheduledTask]:
        """Return scheduled tasks matching the given filters.

        Pass completed=True/False to filter by completion status.
        Pass a Pet object to filter to only that pet's tasks.
        Omitting a parameter leaves that filter inactive.
        """
        results = self.schedule
        if completed is not None:
            results = [st for st in results if st.task.completed == completed]
        if pet is not None:
            results = [st for st in results if st.task.pet is pet]
        return results

    def detect_conflicts(self) -> list[str]:
        """Return a warning string for every pair of tasks whose time windows overlap."""
        def end_time(st: ScheduledTask) -> time:
            anchor = datetime(2000, 1, 1, st.start_time.hour, st.start_time.minute)
            return (anchor + timedelta(minutes=st.task.duration)).time()

        timed = [(st, end_time(st)) for st in sorted(self.schedule, key=lambda st: st.start_time)]
        warnings = []
        for i, (a, end_a) in enumerate(timed):
            for b, end_b in timed[i + 1:]:
                if b.start_time >= end_a:
                    break  # sorted, so nothing further can overlap a
                warnings.append(
                    f"WARNING: [{a.task.pet.name}] {a.task.title} "
                    f"({a.start_time.strftime('%H:%M')}–{end_a.strftime('%H:%M')}) "
                    f"overlaps [{b.task.pet.name}] {b.task.title} "
                    f"({b.start_time.strftime('%H:%M')}–{end_b.strftime('%H:%M')})"
                )
        return warnings

    def sort_by_duration(self) -> None:
        """Re-order the current schedule from shortest to longest task duration."""
        self.schedule.sort(key=lambda st: st.task.duration)

    def generate(self, tasks: list[Task], start_time: time = time(8, 0)) -> None:
        """Sort tasks by priority and assign start times within the time budget."""
        self.schedule.clear()
        self.skipped.clear()
        today = date.today()
        pending = sorted(
            [t for t in tasks if not t.completed and (t.due_date is None or t.due_date <= today)],
            key=lambda t: t.priority,
            reverse=True,
        )
        anchor = datetime(2000, 1, 1, start_time.hour, start_time.minute)
        minutes_used = 0
        for task in pending:
            if minutes_used + task.duration > self.time_budget:
                self.skipped.append(task)
                continue
            slot = anchor + timedelta(minutes=minutes_used)
            self.schedule.append(ScheduledTask(task=task, start_time=slot.time()))
            minutes_used += task.duration


@dataclass
class Pet:
    name: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)


@dataclass
class Owner:
    name: str
    time_available_minutes: int
    pets: list[Pet] = field(default_factory=list)
    scheduler: Scheduler | None = None

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's pet list."""
        self.pets.remove(pet)

    def get_schedule(self, pet: Pet, start_time: time = time(8, 0)) -> list[ScheduledTask]:
        """Generate and return a daily schedule for the given pet."""
        self.scheduler = Scheduler(time_budget=self.time_available_minutes)
        self.scheduler.generate(pet.tasks, start_time=start_time)
        return self.scheduler.schedule
