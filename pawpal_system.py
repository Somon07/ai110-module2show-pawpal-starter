"""PawPal system logic layer.

Backend classes generated from the UML draft (see diagrams/uml_draft.mmd).
Data objects (Task, Pet, Owner) use Python dataclasses to keep the code clean.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet-care task."""

    title: str
    duration_minutes: int
    priority: str

    def update_priority(self, new_priority: str) -> None:
        """Change this task's priority."""
        ...


@dataclass
class Pet:
    """A pet that has a list of care tasks."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        ...


@dataclass
class Owner:
    """A pet owner who owns one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        ...


class Scheduler:
    """Builds a daily care plan that fits the available time."""

    def __init__(self, available_time_minutes: int) -> None:
        self.available_time_minutes: int = available_time_minutes
        self.plan: list[Task] = []

    def generate_schedule(self, tasks: list[Task]) -> list[Task]:
        """Select and order tasks that fit within the available time."""
        ...

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the current plan."""
        ...
