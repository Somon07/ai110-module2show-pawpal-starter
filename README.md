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

## ✨ Features

- **Owner → Pet → Task model** — an owner manages multiple pets, and each pet owns a list of care tasks (data classes in `pawpal_system.py`).
- **Priority-based day planning** — the scheduler greedily fits the highest-priority tasks into a fixed time budget and skips those that don't fit.
- **Sorting by time** — tasks are ordered chronologically by their `HH:MM` start time.
- **Filtering** — view tasks by pet or by completion status.
- **Daily/weekly recurrence** — completing a recurring task automatically creates the next occurrence with its due date advanced.
- **Conflict warnings** — the scheduler flags when two pending tasks share the same start time, without crashing.
- **Streamlit UI + CLI demo** — an interactive app (`app.py`) that persists state across reruns, plus a terminal demo (`main.py`).

> **Architecture:** the final class design is in [`diagrams/uml_final.mmd`](diagrams/uml_final.mmd).

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

Run the full test suite from the project root:

```bash
python -m pytest
```

**What the tests cover** (`tests/test_pawpal.py`, 13 tests):

- **Basic behavior** — `mark_complete()` flips a task's status; `add_task()` grows a pet's task list.
- **Sorting** — `sort_by_time()` returns tasks in chronological `HH:MM` order.
- **Recurrence** — completing a daily task creates a new task due the next day; weekly advances 7 days; a `once` task does not recur.
- **Conflict detection** — duplicate times are flagged, unique times are not, and completed tasks are ignored.
- **Budget-limited scheduling** — the plan never exceeds the time budget and drops lower-priority tasks.
- **Edge case** — a pet with no tasks yields an empty plan and a clear message.
- **Filtering** — by pet name and by completion status.

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-9.1.1, pluggy-1.6.0
collected 13 items

tests\test_pawpal.py .............                                       [100%]

============================= 13 passed in 0.23s ==============================
```

**Confidence Level: ★★★★☆ (4/5).** All core behaviors — sorting, recurrence,
conflict detection, budgeting, and filtering — pass their happy-path and edge-case
tests. I dropped one star because conflict detection only catches exact-time matches
(not overlapping durations) and recurrence isn't yet tested across month/year
boundaries.

## 📐 Smarter Scheduling

The scheduling logic lives in `pawpal_system.py`. Each smart feature and the method that
implements it:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks by their `HH:MM` clock time using `sorted()` with a `lambda` key. |
| Priority selection | `Scheduler.generate_schedule()` / `schedule_for_owner()` | Fills a time budget with the highest-priority tasks; skips ones that don't fit. |
| Filtering | `Scheduler.filter_by_pet()`, `Scheduler.filter_by_status()` | Filter all tasks by pet name or by completion status. |
| Conflict detection | `Scheduler.detect_conflicts()` | Groups pending tasks by start time and returns a warning string for any shared time slot (exact-time match; does not crash). |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_task_complete()` | Completing a daily/weekly task auto-creates the next instance with `due_date` advanced via `timedelta`. |

## 📸 Demo Walkthrough

Launch the interactive app with:

```bash
python -m streamlit run app.py
```

**What you can do in the UI**

- Set the **owner name** and **add pets** (name + species). Pets persist across page
  reruns because the `Owner` object lives in `st.session_state`.
- **Add tasks** to any pet: title, start time (`HH:MM`), duration, frequency
  (daily/weekly/once), and priority.
- Review a **Current tasks** table per pet, shown in chronological order.
- Set an **available time budget** and click **Generate schedule** to build the day's plan.

**Example workflow**

1. Enter the owner's name (e.g., *Betty*).
2. Add a pet → *Tyna* (dog), then a second pet → *Dennis* (cat).
3. Add a task → *Morning walk*, `08:00`, 30 min, daily, high priority.
4. Add more tasks, including two at the same time (e.g., both `18:00`) to trigger a conflict.
5. Set the budget to 60 minutes and click **Generate schedule**.

**Key Scheduler behaviors shown**

- The plan lists the highest-priority tasks that fit the budget, **sorted by time**.
- A green **success** banner confirms how many tasks were scheduled.
- Any two tasks sharing a start time raise a **⚠️ conflict warning** telling the owner
  which tasks to reschedule; a clean day shows a success message instead.

**Sample CLI output** (from `python main.py`):

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

Conflict check:
  ⚠️ Conflict at 18:00: Evening walk, Play / enrichment
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
