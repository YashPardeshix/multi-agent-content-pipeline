from state import AgentState, ResearchBinder
from tools import search_web_for_urls, fetch_urls
import json
import os
from openai import OpenAI

os.getenv("NVIDIA_API_KEY")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY") 
)

def search_node(state: AgentState) -> AgentState:
    urls = search_web_for_urls(state[topic])
    return{"urls": urls}

def fetch_node(state: AgentState) -> dict:
    mock_research = []
    
    for url in state["urls"]:
        content = fetch_urls(url)
        if "Error" not in content:     
            mock_research.append(content)

    combined_web_text = "\n\n".join(mock_research)
    
    response = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        response_format={"type": "json_object"}, 
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Senior Technical Researcher. Analyze the provided web research "
                    "and synthesize it into a clean JSON object containing exactly these keys:\n"
                    "1. 'developer_problems': A detailed description of the developer pain points.\n"
                    "2. 'core_solution': The structural mechanism that solves the problem.\n"
                    "3. 'core_implementation': A clear, real-world code example demonstrating the solution."
                )
            },
            {
                "role": "user",
                "content": f"Topic: {state['topic']}\n\nWeb Research Data:\n{combined_web_text}"
            }
        ]
    )

    raw_json_string = response.choices[0].message.content
    parsed_json = json.loads(raw_json_string)

    return {"research_binder": parsed_json}

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
        return "writer"
    else:
        return "search"
     