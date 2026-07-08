"""PawPal system logic layer.

Backend classes generated from the UML draft (see diagrams/uml_draft.mmd).
Data objects (Task, Pet, Owner) use Python dataclasses to keep the code clean.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum


class Priority(IntEnum):
    """Task priority with a built-in ordering (higher value = more important)."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Task:
    """A single pet-care activity (description, time, frequency, completion)."""

    description: str
    duration_minutes: int
    frequency: str = "daily"
    priority: Priority = Priority.MEDIUM
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def update_priority(self, new_priority: Priority) -> None:
        """Change this task's priority."""
        self.priority = Priority(new_priority)


@dataclass
class Pet:
    """A pet that stores its details and a list of care tasks."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        self.tasks.append(task)

    def pending_tasks(self) -> list[Task]:
        """Return this pet's tasks that are not yet completed."""
        return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
    """A pet owner who manages multiple pets and access to all their tasks."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def all_tasks(self) -> list[Task]:
        """Collect every task across all of this owner's pets into one flat list."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """The brain: retrieves, organizes, and manages tasks across pets."""

    def __init__(self, available_time_minutes: int) -> None:
        """Create a scheduler with a fixed daily time budget in minutes."""
        self.available_time_minutes: int = available_time_minutes
        self.plan: list[Task] = []

    def generate_schedule(self, tasks: list[Task]) -> list[Task]:
        """Greedily pick the highest-priority pending tasks that fit the time budget."""
        candidates = sorted(
            (task for task in tasks if not task.completed),
            key=lambda task: (task.priority, -task.duration_minutes),
            reverse=True,
        )
        self.plan = []
        remaining = self.available_time_minutes
        for task in candidates:
            if task.duration_minutes <= remaining:
                self.plan.append(task)
                remaining -= task.duration_minutes
        return self.plan

    def schedule_for_owner(self, owner: Owner) -> list[Task]:
        """Build the plan straight from an owner's pets via Owner.all_tasks()."""
        return self.generate_schedule(owner.all_tasks())

    def explain_plan(self) -> str:
        """Return a readable, terminal-friendly summary of the current plan."""
        if not self.plan:
            return "No tasks scheduled (nothing fit the available time)."

        lines = ["Today's Schedule", "=" * 40]
        used = 0
        for index, task in enumerate(self.plan, start=1):
            used += task.duration_minutes
            lines.append(
                f"{index}. {task.description:<22} "
                f"{task.duration_minutes:>3} min  "
                f"[{task.priority.name.lower()}, {task.frequency}]"
            )
        lines.append("-" * 40)
        lines.append(
            f"{len(self.plan)} task(s), {used} of "
            f"{self.available_time_minutes} min used."
        )
        return "\n".join(lines)
