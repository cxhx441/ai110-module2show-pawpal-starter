# PawPal+ Project Reflection

## 1. System Design

User needs to be able to:
- add an owner + pet to the system
- add / edit tasks with priority ranking
- generate and display a plan for tasks


**a. Initial design**

- Briefly describe your initial UML design.
There are 5 classes each with methods and attributes.
- What classes did you include, and what responsibilities did you assign to each?
The UML design includes classes: pet, owner, task, scheduled_task, daily_plan. Owners have pets, and pets have tasks, a scheduled task is just a task with a start time, and the daily_plan lists out the scheduled tasks. Owners can add and remove pets, pets can add/remove tasks.

**b. Design changes**

- Did your design change during implementation?
Yes.
- If yes, describe at least one change and why you made it.
Yes. I made start times a datetime object instead of a string as they are easier to compare directly.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
The scheduler considers the owner's total time budget and each task's priority and duration. It was a clear decision that priority mattered most because some pet tasks are non-negotiable (like feeding or medication) and the owner needs those handled first before anything optional gets scheduled.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
The scheduler fills tasks in priority order and skips any task that doesn't fit, even if a shorter one could. This can leave unused time in the budget. This is important because for a pet owner, priority order matters more than packing in as many tasks as possible. e.g. medicine is more important than groooming, even if it takes longer and pushes out lower priority taskes.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used the AI tool for lots of refactoring, adding features to the UI, and creating tests and verification scanrios for the UI.
- What kinds of prompts or questions were most helpful?
keeping the scope small and using numbered lists seemed to help keep the AI in check.


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
At one point, the AI suggested putting the start time on the schedule builder but I was trying to add it to the task creater. Had to reject it.
- How did you evaluate or verify what the AI suggested?
For the pawpal_system.py logic and tests, I read every line and confirm it made sense with the ultimate goal. For the UI design, I'm not as familiar with streamlit so I did let it take teh reins a bit. I tried to scan the code and make sure it was attempting to do the correct thing, but the library methods weren't obvious in all cases.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I made sure that the tasks could be added/removed/completed, that owner and pets could be added, that the schedule builder sorted correctly and would show warning on scheduled task conflicts and over scheduling.
- Why were these tests important?
These are considered core functions of the app. It's important to test core functions of the app.

**b. Confidence**

- How confident are you that your scheduler works correctly?
based on playing around with the UI, i'm highly confident that it works.
- What edge cases would you test next if you had more time?
Adding multiple pet/owner combos with the same information should flash a warning since ther's no way to distinguish them in the UI.
Adding a single task with duration greater than the total allowable time should flash a warning as well.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I'm actually quite happy with the AI tools when making the UMLs, the logic files, and testing files.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
When designing the UI, I did not have clear goals, and I let the AI runaway with what it thought was best. By the end I have only a medium level understanding of what's actually happening there. Next time, i'll have more clear goals from the start.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
As mentioned above, it's easy to let the AI do what it wants but then quickly lose the mental model of what the code is doing. This felt like what people call "vibe-coding" and is not something I want to repeat. It's best to go in with small goals and small changes to keep things focused and not lose control of the project. 
