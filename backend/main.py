from graph import app

initial_state ={"topic": "Latest advancements in fusion energy"}
final_state = app.invoke(initial_state)
print(final_state)