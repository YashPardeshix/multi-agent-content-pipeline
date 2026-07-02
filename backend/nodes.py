import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from state import AgentState, ResearchBinder
from tools import search_web_for_urls, fetch_urls

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY") 
)

def search_node(state: AgentState) -> dict:
    urls = search_web_for_urls(state["topic"])
    return {"urls": urls}

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
    
    binder = state["research_binder"]
    problems = binder.get("developer_problems", "")
    solution = binder.get("core_solution", "")
    implementation = binder.get("core_implementation", "")
    
    response = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a World-Class Technical Writer. Write a stunning, highly detailed "
                    "blog post in Markdown format designed for engineers. You must structure the post "
                    "with these three clear sections:\n"
                    "1. The Pain Point (What problem we are solving)\n"
                    "2. The Underlying Mechanism (How the solution works under the hood)\n"
                    "3. The Implementation (A clear, real-world code example with explanations)"
                )
            },
            {
                "role": "user",
                "content": (
                    f"Topic: {state['topic']}\n\n"
                    f"Use this research data to write the post:\n"
                    f"- Pain Points: {problems}\n"
                    f"- Mechanism: {solution}\n"
                    f"- Code Implementation: {implementation}"
                )
            }
        ]
    )
    
    article = response.choices[0].message.content
    return {"full_article": article}

def should_continue(state: AgentState) -> str:
    binder = state.get("research_binder", {})
    
    problems = binder.get("developer_problems", "")
    solution = binder.get("core_solution", "")
    implementation = binder.get("core_implementation", "")
    
    if len(problems) > 50 and len(solution) > 50 and len(implementation) > 50: 
        return "writer"
    else:
        return "search"