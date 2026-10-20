import os
import json
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from state import TaskState

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

def get_text(response):
    # Gemini sometimes returns list, handle both
    content = response.content
    if isinstance(content, list):
        # Join all text parts
        text = ""
        for part in content:
            if isinstance(part, dict) and "text" in part:
                text += part["text"]
            elif isinstance(part, str):
                text += part
            else:
                text += str(part)
        return text
    return str(content)

def task_extraction_node(state: TaskState):
    prompt = f"""
    You are a task extractor. Extract individual actionable tasks from this text.
    Text: "{state['user_input']}"
    
    Return ONLY valid JSON list like: ["task1", "task2"]
    No explanation, no markdown.
    """
    response = llm.invoke(prompt)
    text = get_text(response).strip()
    
    # Try to extract JSON from response
    try:
        # Remove ```json ``` wrapper if present
        text = re.sub(r"```json|```", "", text).strip()
        tasks = json.loads(text)
        if isinstance(tasks, list):
            return {"extracted_tasks": tasks}
    except:
        pass
    
    # Fallback: split by lines/commas
    tasks = [t.strip("-•* ") for t in text.split("\n") if t.strip()]
    if len(tasks) == 1 and "," in tasks[0]:
        tasks = [t.strip() for t in tasks[0].split(",")]
    
    return {"extracted_tasks": tasks}

def task_prioritization_node(state: TaskState):
    prompt = f"""
    You are a task prioritizer. Assign priority High/Medium/Low.
    High: today, ASAP, urgent, bills
    Medium: tomorrow, this week
    Low: next week, next month, sometime, no deadline
    
    Tasks: {state['extracted_tasks']}
    
    Return ONLY valid JSON like:
    [{{"task": "buy groceries today", "priority": "High"}}]
    No markdown.
    """
    response = llm.invoke(prompt)
    text = get_text(response).strip()
    
    try:
        text = re.sub(r"```json|```", "", text).strip()
        prioritized = json.loads(text)
        return {"prioritized_tasks": prioritized}
    except:
        # Fallback if JSON fails
        fallback = [{"task": t, "priority": "Medium"} for t in state['extracted_tasks']]
        return {"prioritized_tasks": fallback}

def format_results_node(state: TaskState):
    formatted = "Organized To-Do List:\n"
    for i, item in enumerate(state['prioritized_tasks'], 1):
        task = item.get("task", "Unknown task")
        priority = item.get("priority", "Medium")
        formatted += f"{i}. [{priority}] {task}\n"
    return {"formatted_output": formatted}