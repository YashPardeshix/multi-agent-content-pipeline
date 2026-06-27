from state import AgentState
from nodes import search_node, fetch_node, writer_node, should_continue
from langgraph.graph import StateGraph, START, END



workflow = StateGraph(AgentState)

workflow.add_node("search", search_node)
workflow.add_node("fetch", fetch_node)
workflow.add_node("writer", writer_node)
workflow.add_edge(START, "search")
workflow.add_edge("search", "fetch")
workflow.add_conditional_edges(
    "fetch",                  
    should_continue,         
)
workflow.add_edge("writer", END)


app = workflow.compile()