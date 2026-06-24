from __future__ import annotations
from dataclasses import dataclass, field
from datetime import time


@dataclass
class Task:
    title: str
    description: str
    priority: int
    duration: int  # minutes


@dataclass
class ScheduledTask:
    task: Task
    start_time: time


@dataclass
class DailyPlan:
    time_budget: int  # total minutes available for the day
    scheduled_tasks: list[ScheduledTask] = field(default_factory=list)

    def generate(self, tasks: list[Task]) -> None:
        pass


@dataclass
class Pet:
    name: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass


@dataclass
class Owner:
    name: str
    time_available_minutes: int
    pets: list[Pet] = field(default_factory=list)
    daily_plan: DailyPlan | None = None

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass
