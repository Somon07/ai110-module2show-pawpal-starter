"""Temporary testing ground for the PawPal+ logic layer.

Run with: python main.py
"""

from pawpal_system import Owner, Pet, Priority, Scheduler, Task


def main() -> None:
    """Build a small owner/pet/task setup and print today's schedule."""
    # 1. Create an owner and two pets.
    owner = Owner(name="Sharon")
    rex = Pet(name="Rex", species="Dog")
    milo = Pet(name="Milo", species="Cat")
    owner.add_pet(rex)
    owner.add_pet(milo)

    # 2. Add several tasks with different durations and priorities.
    rex.add_task(Task("Morning walk", 30, "daily", Priority.HIGH))
    rex.add_task(Task("Feed breakfast", 10, "daily", Priority.HIGH))
    milo.add_task(Task("Clean litter box", 15, "daily", Priority.MEDIUM))
    milo.add_task(Task("Play / enrichment", 20, "daily", Priority.LOW))

    # 3. Build the schedule from the owner's pets within a 60-minute budget.
    scheduler = Scheduler(available_time_minutes=60)
    scheduler.schedule_for_owner(owner)

    # 4. Print the plan.
    print(scheduler.explain_plan())


if __name__ == "__main__":
    main()
