from langgraph.graph import StateGraph, START, END
from state import TaskState
from nodes import task_extraction_node, task_prioritization_node, format_results_node

def build_graph():
    builder = StateGraph(TaskState)
    
    builder.add_node("extraction", task_extraction_node)
    builder.add_node("prioritization", task_prioritization_node)
    builder.add_node("formatting", format_results_node)
    
    builder.add_edge(START, "extraction")
    builder.add_edge("extraction", "prioritization")
    builder.add_edge("prioritization", "formatting")
    builder.add_edge("formatting", END)
    
    return builder.compile()

graph = build_graph()