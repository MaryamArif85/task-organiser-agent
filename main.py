from graph import graph

user_text = "I need to finish my assignment tomorrow, buy groceries today, and prepare for my meeting next week."

result = graph.invoke({"user_input": user_text})

print(result["formatted_output"])