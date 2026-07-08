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

Time and priority ( like a high, medium or low)setting was highly considered
- How did you decide which constraints mattered most?

I decided priority mattered most because there ARE some essential things that a pet needs to survive with an owner, so the scheduler picks tasks by priority first and treats the available time as a hard limit that lower-priority tasks get dropped from when the day runs out.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

  I designed the conflict detection to only flag uncompleted tasks that share the exact same start time, meaning it ignores task durations and won't catch overlapping schedules.

- Why is that tradeoff reasonable for this scenario?

  I used simple exact-time matching to catch common errors safely. True interval-overlap detection requires complex code, so I kept this early build lightweight and noted full overlap detection for a future update.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
I used Ai to help me make the uml diagram and brainstorm to fix the bugs in the app. The prompts that were more detailed were very helpful to help the Ai stay in between the constraints of what was asked

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

  When the AI reviewed my class skeleton, it suggested adding a back-reference from each Task to its Pet so the schedule could print the pet's name. I did not accept it because it would create a two-way link between Pet and Task and make the data classes more complicated than they needed to be, so I kept the one-way Owner → Pet → Task structure and left that idea as a future improvement.

- How did you evaluate or verify what the AI suggested?

  I verified the AI's code by actually running it instead of trusting it on sight. When I ran main.py, I noticed the conflict detector was flagging a false conflict caused by a recurring task's next occurrence, so I traced it back and fixed detect_conflicts to skip completed tasks, then confirmed the fix with the terminal output and by running python -m pytest until all tests passed.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested when saving the animal if the app would store it in its memory. These tests are important as it would render the app useless if it did not.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am confident it works correctly.

If I had more time, I would test edge cases like two tasks that overlap by duration but not exact start time (for example a 30-minute walk at 08:00 running into a feeding at 08:15), recurring tasks that roll over a month or year boundary, an owner with no pets or a pet with no tasks, and invalid input such as a badly formatted time or a task longer than the whole time budget.

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am most satisfied with making the tasks the pet had to do and having the freedom to figure out what I wanted the app to include

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would upgrade the conflict detection to look at each task's duration so it catches overlapping schedules instead of only exact-time matches, and I would let the owner mark tasks complete right in the Streamlit UI so the recurring-task logic is visible in the app and not just in the terminal demo.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned that AI tends to do more than you ask and overcomplicate the tasks at time.