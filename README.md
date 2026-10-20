# Task Organiser Agent - LangGraph + Gemini

An AI assistant that transforms informal natural language into a prioritized to-do list.

### Problem
People write tasks informally like: "I need to finish my assignment tomorrow, buy groceries today, and prepare for my meeting next week."
We need to extract, prioritize, and format them.

### Solution
A 3-node LangGraph workflow powered by Gemini that handles any variation of examples.

### Workflow Architecture
### Workflow Architecture
[START]
   |
   v
User Input (raw string: "finish assignment tomorrow, buy groceries today...")
   |
   v
Node 1: Task Extraction (Gemini)
Job: Split informal sentence into separate tasksInput: user_inputOutput: extracted_tasks = ["finish assignment tomorrow", "buy groceries today",...]
|
v
Node 2: Task Prioritization (Gemini)Job: Assign priority based on urgencyLogic:
High = today, ASAP, urgent, bills, deadline
Medium = tomorrow, this week, important
Low = next week, next month, sometime, no deadline / hobbiesInput: extracted_tasksOutput: prioritized_tasks = [{"task": "...", "priority": "High"},...]
|
v
Node 3: Format Results (Python - No LLM)Job: Make it readableOutput:Buy groceries - TodayFinish assignment - TomorrowPrepare for meeting - Next Week
|
v
[END] -> formatted_output


**State (Shared Memory):**
- `user_input`: raw string
- `extracted_tasks`: list (filled by Node 1)
- `prioritized_tasks`: list with priority (filled by Node 2)
- `formatted_output`: final string (filled by Node 3)

### Tech Stack
- LangGraph - Graph orchestration & state management
- Gemini 2.0-flash - LLM for Node 1 & Node 2
- Python, python-dotenv

### Project Structure
task-organiser-agent/
├── state.py # TypedDict State definition
├── nodes.py # All 3 nodes + LLM handling
├── graph.py # StateGraph builder (START -> extraction -> prioritization -> formatting -> END)
├── main.py # Test runner
├── requirements.txt
├──.env # GOOGLE_API_KEY
├── README.md
└── images/
    └── output.png # Working proof screenshot




