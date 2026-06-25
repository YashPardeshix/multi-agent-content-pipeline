from tavily import TavilyClient
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def search(query: str) -> list[str]: 
    api_key = os.getenv("TAVILY_API_KEY") 
    if not api_key:
        raise ValueError("TAVILY_API_KEY is missing from .env file")
    client = TavilyClient(api_key)
    results = client.search(query)
    urls =[item["url"] for item in results["results"]]
    return urls

def fetch(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        return response.text
    except Exception as e:
        return f"Error fetching {url}: {e}"