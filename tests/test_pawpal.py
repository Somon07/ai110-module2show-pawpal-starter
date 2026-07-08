"""Quick tests for the PawPal+ logic layer."""

from pawpal_system import Pet, Priority, Task


def test_mark_complete_changes_status():
    """Calling mark_complete() flips a task's completed flag to True."""
    task = Task("Morning walk", 30, "daily", Priority.HIGH)
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a pet increases that pet's task count."""
    pet = Pet(name="Rex", species="Dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task("Feed breakfast", 10, "daily", Priority.HIGH))

    assert len(pet.tasks) == 1
