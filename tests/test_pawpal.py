"""Automated test suite for the PawPal+ logic layer.

Covers happy paths and edge cases for the core behaviors:
sorting, recurrence, conflict detection, budget-limited scheduling, and filtering.
"""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Priority, Scheduler, Task


# --- Basic behavior -----------------------------------------------------------

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


# --- Sorting ------------------------------------------------------------------

def test_sort_by_time_orders_chronologically():
    """sort_by_time() returns tasks ordered by their HH:MM clock time."""
    scheduler = Scheduler(available_time_minutes=60)
    tasks = [
        Task("Evening walk", 30, time="18:00"),
        Task("Feed breakfast", 10, time="07:30"),
        Task("Lunch", 15, time="12:00"),
    ]

    ordered = scheduler.sort_by_time(tasks)

    assert [task.time for task in ordered] == ["07:30", "12:00", "18:00"]


# --- Recurrence ---------------------------------------------------------------

def test_daily_recurrence_creates_next_day_task():
    """Completing a daily task produces a fresh task due the following day."""
    scheduler = Scheduler(available_time_minutes=60)
    pet = Pet(name="Rex", species="Dog")
    task = Task("Feed breakfast", 10, "daily", Priority.HIGH,
                due_date=date(2026, 7, 7))
    pet.add_task(task)

    upcoming = scheduler.mark_task_complete(task, pet)

    assert task.completed is True
    assert upcoming is not None
    assert upcoming.completed is False
    assert upcoming.due_date == date(2026, 7, 8)
    assert len(pet.tasks) == 2  # original + next occurrence


def test_weekly_recurrence_advances_seven_days():
    """A weekly task's next occurrence is seven days later."""
    task = Task("Grooming", 45, "weekly", Priority.MEDIUM, due_date=date(2026, 7, 7))

    upcoming = task.next_occurrence()

    assert upcoming.due_date == date(2026, 7, 7) + timedelta(weeks=1)


def test_once_task_does_not_recur():
    """A one-off task returns no next occurrence."""
    task = Task("Vet visit", 60, "once", Priority.HIGH)

    assert task.next_occurrence() is None


# --- Conflict detection -------------------------------------------------------

def test_detect_conflicts_flags_duplicate_times():
    """Two tasks at the exact same time produce a conflict warning."""
    scheduler = Scheduler(available_time_minutes=60)
    tasks = [
        Task("Evening walk", 30, time="18:00"),
        Task("Play", 20, time="18:00"),
    ]

    warnings = scheduler.detect_conflicts(tasks)

    assert len(warnings) == 1
    assert "18:00" in warnings[0]


def test_no_conflicts_when_times_unique():
    """Distinct times produce no conflict warnings."""
    scheduler = Scheduler(available_time_minutes=60)
    tasks = [
        Task("Morning walk", 30, time="08:00"),
        Task("Evening walk", 30, time="18:00"),
    ]

    assert scheduler.detect_conflicts(tasks) == []


def test_completed_tasks_are_ignored_in_conflicts():
    """A completed task does not compete for a time slot."""
    scheduler = Scheduler(available_time_minutes=60)
    done = Task("Old walk", 30, time="18:00")
    done.mark_complete()
    tasks = [done, Task("Evening walk", 30, time="18:00")]

    assert scheduler.detect_conflicts(tasks) == []


# --- Budget-limited scheduling ------------------------------------------------

def test_generate_schedule_respects_time_budget():
    """The plan never exceeds the available time and drops what doesn't fit."""
    scheduler = Scheduler(available_time_minutes=40)
    tasks = [
        Task("Walk", 30, priority=Priority.HIGH, time="08:00"),
        Task("Feed", 10, priority=Priority.HIGH, time="07:30"),
        Task("Play", 20, priority=Priority.LOW, time="18:00"),
    ]

    plan = scheduler.generate_schedule(tasks)

    total = sum(task.duration_minutes for task in plan)
    assert total <= 40
    assert "Play" not in [task.description for task in plan]  # low priority dropped


# --- Edge case: a pet with no tasks -------------------------------------------

def test_pet_with_no_tasks_produces_empty_plan():
    """An owner whose pet has no tasks yields an empty plan and a clear message."""
    scheduler = Scheduler(available_time_minutes=60)
    owner = Owner(name="Betty")
    owner.add_pet(Pet(name="Rex", species="Dog"))

    plan = scheduler.schedule_for_owner(owner)

    assert plan == []
    assert "No tasks scheduled" in scheduler.explain_plan()


# --- Filtering ----------------------------------------------------------------

def test_filter_by_pet_returns_only_that_pets_tasks():
    """filter_by_pet() returns only the named pet's tasks."""
    scheduler = Scheduler(available_time_minutes=60)
    owner = Owner(name="Betty")
    rex = Pet(name="Rex", species="Dog")
    milo = Pet(name="Milo", species="Cat")
    rex.add_task(Task("Walk", 30, time="08:00"))
    milo.add_task(Task("Litter", 15, time="12:00"))
    owner.add_pet(rex)
    owner.add_pet(milo)

    rex_tasks = scheduler.filter_by_pet(owner, "Rex")

    assert [task.description for task in rex_tasks] == ["Walk"]


def test_filter_by_status_splits_done_and_pending():
    """filter_by_status() separates completed from pending tasks."""
    scheduler = Scheduler(available_time_minutes=60)
    done = Task("Walk", 30, time="08:00")
    done.mark_complete()
    tasks = [done, Task("Feed", 10, time="07:30")]

    assert scheduler.filter_by_status(tasks, completed=True) == [done]
    assert [t.description for t in scheduler.filter_by_status(tasks, completed=False)] == ["Feed"]
