# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
Natural Language- should be able to schedule a walk, schedule what time the dogs need to eat,add a pet

- Briefly describe your initial UML design.
For my design, I created 4 classes with the inital UML design. I also made 3 just for storing data (Owner, Pet and Task). I kept the setup simple so that the owner had pets, and the pets has tasks. Then the scheduler was built to take those tasks and organize them to a plan.

- What classes did you include, and what responsibilities did you assign to each?

  - I created a task to track activity's time and priority, and to update priorities when needed. Pet was also created to store an animal's details and add tasks to this list. Owner was meant for storage of user's names and to add pets to their profile. Scheduler was used to write each tasks into a time budget and to explain the final schedule.

**b. Design changes**

- Did your design change during implementation?

  Yes. I asked my AI coding assistant to review the class skeleton for missing
  relationships and logic bottlenecks, and I made two changes based on its feedback.

- If yes, describe at least one change and why you made it.

  Yes, I changed (task.priority) into an IntEnum to ensure sorting to stay consistent also preventing typos from occuring.
  I held off on linking tasks back to pets, and chose a simple priority sort over a complex algorithm.

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
