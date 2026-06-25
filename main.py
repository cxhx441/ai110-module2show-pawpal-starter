from pawpal_system import Owner, Pet, Task, Frequency

owner = Owner(name="Alex", time_available_minutes=120)

dog = Pet(name="Biscuit")
dog.add_task(Task(title="Morning Walk", description="30 min walk around the block", priority=3, duration=30))
dog.add_task(Task(title="Feeding", description="1 cup dry food", priority=2, duration=10))
dog.add_task(Task(title="Grooming", description="Brush coat", priority=1, duration=20, frequency=Frequency.WEEKLY))

cat = Pet(name="Mochi")
cat.add_task(Task(title="Feeding", description="Wet food", priority=3, duration=5))
cat.add_task(Task(title="Litter Box", description="Scoop litter box", priority=2, duration=10))
cat.add_task(Task(title="Playing", description="Wand", priority=1, duration=10))

owner.add_pet(dog)
owner.add_pet(cat)

for pet in owner.pets:
    schedule = owner.get_schedule(pet)
    print(f"\nToday's Schedule for {pet.name}:")
    print("-" * 30)
    if not schedule:
        print("  No tasks scheduled.")
    for entry in schedule:
        print(f"  {entry.start_time.strftime('%H:%M')}  {entry.task.title} ({entry.task.duration} min) [priority: {entry.task.priority}]")
