from datetime import time
from pawpal_system import Owner, Pet, Task, Frequency, Scheduler, ScheduledTask

owner = Owner(name="Alex", time_available_minutes=120)

dog = Pet(name="Biscuit")
cat = Pet(name="Mochi")

# Tasks added out of order by duration so sort_by_duration() has a visible effect
dog.add_task(Task(title="Grooming",      description="Brush coat",               priority=1, duration=20, pet=dog, frequency=Frequency.WEEKLY))
dog.add_task(Task(title="Morning Walk",  description="30 min walk around block", priority=3, duration=30, pet=dog))
dog.add_task(Task(title="Feeding",       description="1 cup dry food",           priority=2, duration=10, pet=dog))

cat.add_task(Task(title="Playing",       description="Wand toy",                 priority=1, duration=15, pet=cat))
cat.add_task(Task(title="Litter Box",    description="Scoop litter box",         priority=2, duration=10, pet=cat))
cat.add_task(Task(title="Feeding",       description="Wet food",                 priority=3, duration=5,  pet=cat))

owner.add_pet(dog)
owner.add_pet(cat)

# Build a single combined scheduler across all pets
all_tasks = [task for pet in owner.pets for task in pet.tasks]
scheduler = Scheduler(time_budget=owner.time_available_minutes)
scheduler.generate(all_tasks)

def print_entries(entries):
    for e in entries:
        status = "done" if e.task.completed else "pending"
        print(f"  {e.start_time.strftime('%H:%M')}  [{e.task.pet.name}] {e.task.title} ({e.task.duration} min) [{status}]")

print("=== Combined Schedule — sorted by priority ===")
print_entries(scheduler.schedule)

scheduler.sort_by_duration()
print("\n=== After sort_by_duration() — shortest first ===")
print_entries(scheduler.schedule)

print("\n=== filter_tasks(pet=dog) ===")
print_entries(scheduler.filter_tasks(pet=dog))

print("\n=== filter_tasks(pet=cat) ===")
print_entries(scheduler.filter_tasks(pet=cat))

# Mark one task complete, then filter by completion status
dog.tasks[1].mark_complete()  # Morning Walk

print("\n=== filter_tasks(completed=False) — still pending ===")
print_entries(scheduler.filter_tasks(completed=False))

print("\n=== filter_tasks(completed=True) — done ===")
print_entries(scheduler.filter_tasks(completed=True))

# --- Conflict detection demo ---
# Manually inject two tasks that overlap: dog's Bath starts at 08:00 (45 min),
# cat's Vet Check also starts at 08:20 — they collide in the 08:20–08:45 window.
conflict_scheduler = Scheduler(time_budget=120)
bath      = Task(title="Bath",      description="Tub bath",    priority=2, duration=45, pet=dog)
vet_check = Task(title="Vet Check", description="Annual exam", priority=3, duration=30, pet=cat)
conflict_scheduler.schedule = [
    ScheduledTask(task=bath,      start_time=time(8, 0)),
    ScheduledTask(task=vet_check, start_time=time(8, 20)),
]

print("\n=== Conflict detection demo ===")
print_entries(conflict_scheduler.schedule)
conflicts = conflict_scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"\n  {warning}")
else:
    print("  No conflicts found.")
