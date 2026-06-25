from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
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
    frequency: Frequency = Frequency.DAILY
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass(frozen=True)
class ScheduledTask:
    task: Task
    start_time: time


@dataclass
class Scheduler:
    time_budget: int  # total minutes available for the day
    schedule: list[ScheduledTask] = field(default_factory=list)

    def generate(self, tasks: list[Task], start_time: time = time(8, 0)) -> None:
        """Sort tasks by priority and assign start times within the time budget."""
        self.schedule.clear()
        pending = sorted(
            [t for t in tasks if not t.completed],
            key=lambda t: t.priority,
            reverse=True,
        )
        anchor = datetime(2000, 1, 1, start_time.hour, start_time.minute)
        minutes_used = 0
        for task in pending:
            if minutes_used + task.duration > self.time_budget:
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

    def get_schedule(self, pet: Pet) -> list[ScheduledTask]:
        """Generate and return a daily schedule for the given pet."""
        self.scheduler = Scheduler(time_budget=self.time_available_minutes)
        self.scheduler.generate(pet.tasks)
        return self.scheduler.schedule
