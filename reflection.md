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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
