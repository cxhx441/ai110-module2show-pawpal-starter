from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    description: str
    priority: int
    duration: int  # minutes


@dataclass
class ScheduledTask:
    task: Task
    start_time: str  # "HH:MM"


@dataclass
class DailyPlan:
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
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass

    def generate_daily_plan(self, pet: Pet) -> DailyPlan:
        pass
