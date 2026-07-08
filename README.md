# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Below is the terminal output from running `python main.py`. The owner (Betty) has
two pets — Tyna (dog) and Dennis (cat) — with five tasks added out of order. The
scheduler greedily fits the highest-priority tasks into a 60-minute budget (displayed
by time), then demonstrates sorting, filtering, a recurring task, and conflict
detection:

```
Today's Schedule
============================================
07:30  Feed breakfast        10 min  [high]
08:00  Morning walk          30 min  [high]
12:00  Clean litter box      15 min  [medium]
--------------------------------------------
3 task(s), 55 of 60 min used.

All tasks sorted by time
--------------------------------------------
07:30  Feed breakfast  (high)
08:00  Morning walk  (high)
12:00  Clean litter box  (medium)
18:00  Evening walk  (medium)
18:00  Play / enrichment  (low)

Tasks for Tyna:
  - Evening walk
  - Morning walk
  - Feed breakfast

Completed 'Feed breakfast'. Next occurrence due: 2026-07-08
Pending tasks for Tyna:
  - Evening walk
  - Morning walk
  - Feed breakfast

Conflict check:
  ⚠️ Conflict at 18:00: Evening walk, Play / enrichment
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-9.1.1, pluggy-1.6.0
collected 2 items

tests\test_pawpal.py ..                                                  [100%]

============================== 2 passed in 1.59s ==============================
```

## 📐 Smarter Scheduling

The scheduling logic lives in `pawpal_system.py`. Each smart feature and the method that
implements it:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks by their `HH:MM` clock time using `sorted()` with a `lambda` key. |
| Priority selection | `Scheduler.generate_schedule()` / `schedule_for_owner()` | Greedily fills a time budget with the highest-priority tasks; skips ones that don't fit. |
| Filtering | `Scheduler.filter_by_pet()`, `Scheduler.filter_by_status()` | Filter all tasks by pet name or by completion status. |
| Conflict detection | `Scheduler.detect_conflicts()` | Groups pending tasks by start time and returns a warning string for any shared `HH:MM` slot (exact-time match; does not crash). |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_task_complete()` | Completing a `daily`/`weekly` task auto-creates the next instance with `due_date` advanced via `timedelta`. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
