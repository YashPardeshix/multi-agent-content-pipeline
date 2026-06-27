from state import AgentState, ResearchBinder

def search_node(state: AgentState) -> dict:
    print("--- RUNNING SEARCH NODE ---")
    return {}

def fetch_node(state: AgentState) -> dict:
    print("--- RUNNING FETCH NODE ---")
    mock_research: ResearchBinder = {
        "developer_problems": "Developers struggle with setting up OAuth2 authentication.",
        "core_solution": "Use a standardized library like Authlib instead of custom code.",
        "core_implementation": "pip install authlib\n# Implement client setup..."
    }
    return {"research_binder": mock_research}

def writer_node(state: AgentState) -> dict:
    print("--- RUNNING WRITER NODE ---")
    mock_article = "# Solving OAuth2 Setup Struggles\n\nMany developers struggle with OAuth..."
    return {"full_article": mock_article}


def should_continue(state: AgentState) -> str:
    print("--- RUNNING VALIDATION ROUTER ---")
    binder = state.get("research_binder", {})
    

    problems = binder.get("developer_problems", "")
    solution = binder.get("core_solution", "")
    implementation = binder.get("core_implementation", "")
    

    if len(problems) > 50 and len(solution) > 50 and len(implementation) > 50: 
        return "writer_node"
    else:
        return "search_node"
     