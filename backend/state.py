from typing import TypedDict

class ResearchBinder(TypedDict):
    developer_problems: str
    core_solution: str
    core_implementation: str

class AgentState(TypedDict):
    topic: str
    research_binder: ResearchBinder 
    full_article: str
    retry_count: int
    pass_feedback: str
