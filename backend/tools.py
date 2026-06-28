from tavily import TavilyClient
import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup

load_dotenv()

def search_web_for_urls(query: str) -> list[str]:
    api_key = os.getenv("TAVILY_API_KEY") 
    if not api_key:
        raise ValueError("TAVILY_API_KEY is missing from .env file")
    client = TavilyClient(api_key)
    results = client.search(query)
    urls = [item["url"] for item in results["results"]]
    return urls

def fetch_urls(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        clean_text = soup.get_text()
        return " ".join(clean_text.split())
    except Exception as e:
        return f"Error fetching {url}: {e}"
