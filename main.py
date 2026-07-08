"""Temporary testing ground for the PawPal+ logic layer.

Run with: python main.py
"""

from pawpal_system import Owner, Pet, Priority, Scheduler, Task


def main() -> None:
    """Build a sample setup and exercise scheduling, sorting, filtering, and conflicts."""
    # 1. Create an owner and two pets.
    owner = Owner(name="Betty")
    tyna = Pet(name="Tyna", species="Dog")
    dennis = Pet(name="Dennis", species="Cat")
    owner.add_pet(tyna)
    owner.add_pet(dennis)

    # 2. Add tasks OUT OF ORDER (times are intentionally scrambled).
    tyna.add_task(Task("Evening walk", 30, "daily", Priority.MEDIUM, time="18:00"))
    tyna.add_task(Task("Morning walk", 30, "daily", Priority.HIGH, time="08:00"))
    tyna.add_task(Task("Feed breakfast", 10, "daily", Priority.HIGH, time="07:30"))
    dennis.add_task(Task("Clean litter box", 15, "daily", Priority.MEDIUM, time="12:00"))
    dennis.add_task(Task("Play / enrichment", 20, "weekly", Priority.LOW, time="18:00"))

    scheduler = Scheduler(available_time_minutes=60)

    # --- Today's schedule (greedy by priority, displayed by time) ---
    scheduler.schedule_for_owner(owner)
    print(scheduler.explain_plan())

    # --- Sorting: every task ordered by clock time ---
    print("\nAll tasks sorted by time")
    print("-" * 44)
    for task in scheduler.sort_by_time(owner.all_tasks()):
        print(f"{task.time}  {task.description}  ({task.priority.name.lower()})")

    # --- Filtering: by pet, then by completion status ---
    print("\nTasks for Tyna:")
    for task in scheduler.filter_by_pet(owner, "Tyna"):
        print(f"  - {task.description}")

    # --- Recurring: complete a daily task and auto-create the next occurrence ---
    breakfast = tyna.tasks[2]  # "Feed breakfast", daily
    upcoming = scheduler.mark_task_complete(breakfast, tyna)
    print(f"\nCompleted '{breakfast.description}'. Next occurrence due: {upcoming.due_date}")
    print("Pending tasks for Tyna:")
    for task in tyna.pending_tasks():
        print(f"  - {task.description}")

    # --- Conflict detection: two tasks share 18:00 ---
    print("\nConflict check:")
    conflicts = scheduler.detect_conflicts(owner.all_tasks())
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts found.")


if __name__ == "__main__":
    main()
