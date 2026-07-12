# Production-Grade Multi-Agent Technical Content Pipeline

An autonomous, multi-agent state machine designed to generate high-quality, structured technical content (Pain Point -> Mechanism -> Implementation) from live web research. 

Built in Python using **LangGraph** (StateGraph), **Tavily API**, **BeautifulSoup4**, and **NVIDIA NIM (Llama 3.1 70B)**.

## Architectural Overview: Separation of Concerns

Single-agent systems often suffer from high cognitive load, context-stuffing, and formatting decay when tasked with doing deep research and high-quality writing simultaneously. 

This project solves this bottleneck by explicitly decoupling the lifecycle into a sequential, multi-agent state machine:

1. **The Search Node:** Executes high-relevance queries via Tavily to find authoritative source URLs.
2. **The Fetch Node:** Scrapes raw HTML, strips script/style noise via BeautifulSoup4 to optimize token consumption, and uses an LLM in **Structured JSON Mode** to synthesize the raw text into a defined schema.
3. **The Validation Router (Heuristic Guardrail):** Programmatically validates the data density (checking minimum character limits of the synthesized research) before allowing the workflow to proceed.
4. **The Writer Node:** Focuses entirely on technical prose, drafting a clean, engaging Markdown blog post based exclusively on the validated research.

---

## State Machine Graph Architecture

```text
       +------- START -------+
               |
               v
       +-----------------+
       |   search_node   |  <---+ (If Validation Fails)
       +-----------------+      |
               |                |
               v                |
       +-----------------+      |
       |   fetch_node    |      |
       +-----------------+      |
               |                |
               v                |
    +-----------------------+   |
    | should_continue (Edge) |--+
    +-----------------------+
               |
               +---> (If Validated)
               |
               v
       +-----------------+
       |   writer_node   |
       +-----------------+
               |
               v
        +------- END --------+

Core Production Patterns Implemented 

  - Decoupled Logic Routing (Conditional Edges): Keeps worker nodes pure (only
    transforming data) while flow control is entirely managed by read-only graph
    edge transitions..
  - Heuristic Validation (Fail-Fast Gatekeeping): Runs free, deterministic
    Python string-length validation checks on research data before routing to
    expensive generation nodes, protecting token budgets.
  - Defensive Key Validation: Validates all required environment variables
    (TAVILY_API_KEY, NVIDIA_API_KEY) at execution startup to prevent deep
    runtime crashes inside third-party clients.
  - HTML Stripping & Token Optimization: Leverages BeautifulSoup4 to completely
    decompose non-content markup (<script>, <style>) from scraped pages,
    reducing input token overhead by up to 80%.

Project Directory Structure

backend/
│
├── state.py     # State schema definitions (TypedDict structures)
├── tools.py     # Real-world API tools (Tavily Search, Scraper, BS4)
├── nodes.py     # Worker functions & validation routing functions
├── graph.py     # Centralized StateGraph configuration & compilation
├── main.py      # Script execution entry point
└── .env         # Local API configurations (git-ignored)

Getting Started

1. Installation

Clone the repository and install the dependencies:

pip install tavily-python python-dotenv beautifulsoup4 requests langgraph openai

2. Configuration

Create a .env file in the backend/ directory:

TAVILY_API_KEY=your_tavily_key_here
NVIDIA_API_KEY=your_nvidia_nim_key_here

3. Execution

Navigate to the backend folder and run the execution script:

cd backend
python3 main.py




