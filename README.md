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

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
