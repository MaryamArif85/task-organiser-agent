from typing import TypedDict, List

class TaskState(TypedDict):
    user_input: str
    extracted_tasks: List[str]
    prioritized_tasks: List[dict]  # [{"task": "...", "priority": "High"}]
    formatted_output: str