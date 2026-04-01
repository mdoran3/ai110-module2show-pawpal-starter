# PawPal+ Project Reflection

## 1. System Design

- The system shall be able to add a pet, schedule a walk, and schedule a grooming.

**a. Initial design**

- Briefly describe your initial UML design.
    The UML has 4 classes, Owner, Pet, Scheduler, and Task. The Owner can add and remove 
    pets as well as display a list of all of their pets. A schedule can be created that
    has an owner. The Pet class creates pets with a name, owner, and type. The scheduler can add and remove tasks, generate a schedule and display. Task can also be created with time stamps, durations, and task types. 
    the schedule. 
- What classes did you include, and what responsibilities did you assign to each?
    - Owner: add_pet(), remove_pet(), get_pets()
    - Pet: __str__()
    - Scheduler: add_task(), remove_task(), generate_schedule(), explain_plan()
    - Task: __str__()

**b. Design changes**

- Did your design change during implementation?
    - Yes, some slight changes were made including forcing specific types in lists and adding extra method stubs.
- If yes, describe at least one change and why you made it.
    - The attribute "type" in the pet class was changed to pet_type to avoid any confusion and ambiguity with they Python reserved word "type".

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
