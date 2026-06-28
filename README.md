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

## Features

- **Priority-based scheduling** — `Scheduler.generate()` sorts pending tasks from highest to lowest priority before assigning time slots. Tasks that would exceed the remaining time budget are skipped and collected in `scheduler.skipped` rather than dropped silently.

- **Due-date filtering** — `generate()` excludes tasks whose `due_date` is in the future, so only tasks that are due today or overdue appear in the schedule.

- **Daily/weekly recurrence** — `Task.mark_complete()` automatically creates a follow-up copy of the task with `due_date` set to tomorrow (DAILY) or +7 days (WEEKLY) and adds it back to the pet's task list. `AS_NEEDED` tasks complete without spawning a recurrence.

- **Conflict detection** — `Scheduler.detect_conflicts()` sorts tasks by start time, then does a forward scan with an early-exit break to find overlapping time windows. Returns a list of human-readable warning strings without modifying the schedule.

- **Sort by duration** — `Scheduler.sort_by_duration()` re-orders the current schedule in-place from shortest to longest task duration (useful for batching quick tasks first).

- **Filter by pet or completion status** — `Scheduler.filter_tasks(completed, pet)` returns a filtered slice of the schedule. Arguments are optional and composable — pass one, both, or neither.

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

```
Today's Schedule for Biscuit:
------------------------------
  08:00  Morning Walk (30 min) [priority: 3]
  08:30  Feeding (10 min) [priority: 2]
  08:40  Grooming (20 min) [priority: 1]

Today's Schedule for Mochi:
------------------------------
  08:00  Feeding (5 min) [priority: 3]
  08:05  Litter Box (10 min) [priority: 2]
  08:15  Playing (10 min) [priority: 1]
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest tests/

# Run with coverage:
pytest --cov
```

The suite covers four areas:
1. **sorting** (generated schedule is chronological;  higher-priority tasks get earlier slots),
2. **recurrence** (daily/weekly tasks spawn a follow-up on completion; AS_NEEDED tasks do not),
3. **conflict detection** (overlapping windows are flagged; back-to-back tasks are not), and
4. **time budget** (over-budget and already-completed tasks are excluded from the schedule).

based on the test results below, I have a 5/5 confidence level in system reliability.

Sample test output:
```
============================= test session starts ==============================
platform darwin -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/char/Documents/git_repos/ai110-module2show-pawpal-starter
collected 15 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [  6%]
tests/test_pawpal.py::test_add_task_increases_count PASSED               [ 13%]
tests/test_pawpal.py::TestSortingCorrectness::test_generated_schedule_is_chronological PASSED [ 20%]
tests/test_pawpal.py::TestSortingCorrectness::test_higher_priority_task_gets_earlier_slot PASSED [ 26%]
tests/test_pawpal.py::TestSortingCorrectness::test_generate_with_no_tasks_returns_empty_schedule PASSED [ 33%]
tests/test_pawpal.py::TestRecurrenceLogic::test_daily_task_creates_occurrence_for_next_day PASSED [ 40%]
tests/test_pawpal.py::TestRecurrenceLogic::test_weekly_task_creates_occurrence_for_next_week PASSED [ 46%]
tests/test_pawpal.py::TestRecurrenceLogic::test_as_needed_task_does_not_recur PASSED [ 53%]
tests/test_pawpal.py::TestRecurrenceLogic::test_new_recurring_task_starts_as_not_completed PASSED [ 60%]
tests/test_pawpal.py::TestConflictDetection::test_same_start_time_is_flagged PASSED [ 66%]
tests/test_pawpal.py::TestConflictDetection::test_overlapping_windows_produce_warning PASSED [ 73%]
tests/test_pawpal.py::TestConflictDetection::test_back_to_back_tasks_are_not_a_conflict PASSED [ 80%]
tests/test_pawpal.py::TestConflictDetection::test_empty_schedule_has_no_conflicts PASSED [ 86%]
tests/test_pawpal.py::TestTimeBudget::test_task_exceeding_remaining_budget_is_skipped PASSED [ 93%]
tests/test_pawpal.py::TestTimeBudget::test_completed_tasks_are_excluded_from_schedule PASSED [100%]

============================== 15 passed in 0.02s ==============================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sort by duration | `Scheduler.sort_by_duration()` | Re-orders the current schedule in-place from shortest to longest task duration |
| Sort by priority | `Scheduler.generate()` | Tasks are sorted highest-to-lowest priority before slots are assigned; lower-priority tasks are skipped if they exceed the remaining time budget |
| Filter by pet or status | `Scheduler.filter_tasks(completed, pet)` | Returns a filtered slice of the schedule; pass a `Pet` object, a `bool` for completion status, or both |
| Conflict detection | `Scheduler.detect_conflicts()` | Sorts tasks by start time, then scans forward with an early break to find overlapping time windows; returns warning strings without crashing |
| Recurring tasks | `Task.mark_complete()` | When a `DAILY` or `WEEKLY` task is marked complete, a new copy is automatically created with `due_date` set to tomorrow or 7 days out and added back to the pet's task list; `AS_NEEDED` tasks do not recur |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:
1. Add one or several Owner and Pets.
2. add one or several tasks for the specific owner+pet combination from the dropdown menu, filling in the appropriate parameters
3. Select either "all pets" or a specific owner + pet combination from the dropdown in the Build Schedule section
4. click Generate schedule button.
5. the generated schedule may be sorted by priority (default) or duration. Just select the radio button to change.
6. If a schedule has tasks where the sum of their duration exceeds the available time, a warning is shown to the user.
7. If a schedule is generated for all the pets, it's possible to have overlapping tasks scheduled. A warning will be shown to the user.


# Sample CLI Output from Running main.py
```
=== Combined Schedule — sorted by priority ===
  08:00  [Biscuit] Morning Walk (30 min) [pending]
  08:30  [Mochi] Feeding (5 min) [pending]
  08:35  [Biscuit] Feeding (10 min) [pending]
  08:45  [Mochi] Litter Box (10 min) [pending]
  08:55  [Biscuit] Grooming (20 min) [pending]
  09:15  [Mochi] Playing (15 min) [pending]

=== After sort_by_duration() — shortest first ===
  08:30  [Mochi] Feeding (5 min) [pending]
  08:35  [Biscuit] Feeding (10 min) [pending]
  08:45  [Mochi] Litter Box (10 min) [pending]
  09:15  [Mochi] Playing (15 min) [pending]
  08:55  [Biscuit] Grooming (20 min) [pending]
  08:00  [Biscuit] Morning Walk (30 min) [pending]

=== filter_tasks(pet=dog) ===
  08:35  [Biscuit] Feeding (10 min) [pending]
  08:55  [Biscuit] Grooming (20 min) [pending]
  08:00  [Biscuit] Morning Walk (30 min) [pending]

=== filter_tasks(pet=cat) ===
  08:30  [Mochi] Feeding (5 min) [pending]
  08:45  [Mochi] Litter Box (10 min) [pending]
  09:15  [Mochi] Playing (15 min) [pending]

=== filter_tasks(completed=False) — still pending ===
  08:30  [Mochi] Feeding (5 min) [pending]
  08:35  [Biscuit] Feeding (10 min) [pending]
  08:45  [Mochi] Litter Box (10 min) [pending]
  09:15  [Mochi] Playing (15 min) [pending]
  08:55  [Biscuit] Grooming (20 min) [pending]

=== filter_tasks(completed=True) — done ===
  08:00  [Biscuit] Morning Walk (30 min) [done]

=== Conflict detection demo ===
  08:00  [Biscuit] Bath (45 min) [pending]
  08:20  [Mochi] Vet Check (30 min) [pending]

  WARNING: [Biscuit] Bath (08:00–08:45) overlaps [Mochi] Vet Check (08:20–08:50)
```
