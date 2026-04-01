# PawPal+ Project Reflection

## 1. System Design

- The system shall be able to add a pet, schedule a walk, and schedule a grooming.

**a. Initial design**
- Briefly describe your initial UML design.
    - The UML has 4 classes, Owner, Pet, Scheduler, and Task. The Owner can add and remove pets as well as display a list of all of their pets. A schedule can be created that has an owner. The Pet class creates pets with a name, owner, and type. The scheduler can add and remove tasks, generate a schedule and display. Task can also be created with time stamps, durations, and task types. 
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
    - The scheduler considers the users need to filter and to find conflicts.
- How did you decide which constraints mattered most?
    - The app is ultimately a scheduler, so ensuring that you have a schedule with no conflicting blocks takes the highest priority. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    - Claude suggested that I only show one warning for a schedule conflict as opposed to continuualy showing the same warning when a conflict arises again. I declined this implementation because I think users should be stopped at every instance where a conflict could arise, regardless of whether or not it has been shown before. 
- Why is that tradeoff reasonable for this scenario?
    - I feel like average users need to be warned before commiting to something. Plus, it would have made the code more Pythonic and less human readable. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    - AI was used in the project during every step. Initially it helped with brainstorming and generating an initial UML class diagram. From there, skeletons and methods were implemented. Once the MVP was in place, core logic was deepened, revised, and tightened using Claude. Clean up, docstrings, and UI cleanups were also used at various phases using AI prompts and human verification. 
- What kinds of prompts or questions were most helpful?
    - Starting with more generic prompts and allowing th agent to create the best outcome works well in the beginning. As the product becomes more finalized, specific prompts that point to very specifc issues or adjustments becomes more important. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    - The agent suggested to clean up the scheduling warnings if a conflict in the schedule was found. I opted against this choice since I believe that humans of all skill levels in the context of technology need to be saved from themselves and explicitly reminded of potential issues of conflicts. 
- How did you evaluate or verify what the AI suggested?
    - Running pytests was helpful but more importantly, running and refreshing a local copy of the app in the browser and manually testing various scenarios will always be the best way to triple check what is really happening from a user perspective. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    - I tested getter and setter logic, algorithmic sorting, verification of task completness and many other scenarios.
- Why were these tests important?
    - The test help varify scenarios that may be unforseeable at smaller scales or when only a few test cases are manually checked by a human coder. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
    - The AI agent gave me a 4 out of 5 at some point, I would tend to agree that it sits around this score. Its core functions seem to be there but further iterations could really help the human-computer interaction shine. 
- What edge cases would you test next if you had more time?
    - I would like to have looked into an edge case where the same pet was added twice and have the pet adder prooperly handle the scenario. 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    - Running the app in the UI and then fiddling in Claude to get it just right. Also, creating UML diagrams from the agent and then going over to Mermaid.live to view the results was powerful. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    - I don't like that the inital Owner field requires a pet right from the beginning. I feel like each pet should be added explicitly with "add pet". I also would like a way to remove pets or tasks in order to maintain a more customizable experience for the user that would also proivde less friciton. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    - I will absolutey be using Mermaid.live in the future as well as being more aware of a strong planning phase and diagram creation phase before getting started. 
