from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    task = Task(title="Walk", description="Morning walk", priority=2, duration=30)
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet(name="Biscuit")
    task = Task(title="Walk", description="Morning walk", priority=2, duration=30)
    pet.add_task(task)
    assert len(pet.tasks) == 1
