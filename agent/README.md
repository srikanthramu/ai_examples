# Agent Sample Implementation

Agnet implementation using Langgraph. Uses MCP for tool calling and LLM Simulator to avoid connecting to an actual LLM.
**Note**: Majority of the code is generated using ChatGPT

## Main Components in Flow

| Component              | Role                                                              |
| ---------------------- | ----------------------------------------------------------------- |
| **User Input**         | Starts the agent by asking a question like `"What is 12 plus 8?"` |
| **LangGraph**          | Orchestrates nodes (`llm`, `tool`) and controls state transitions |
| **SimpleLLMSimulator** | Simulates LLM response (generates tool calls or final answers)    |
| **Tool Node**          | Executes `add` via `MCPClientHandler` and adds observation        |
| **MCPClientHandler**   | Async client calling the MCP server's tool (`add`)                |
| **MCP Server**         | FastMCP server exposing the `add(a, b)` tool                      |
| **Observation**        | Result returned and fed back into the LLM scratchpad              |


# Usage
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt

cd ../mcp_example
python3 mcp_server.py  

python3 math_agent.py
```
# References
- https://www.langchain.com/langgraph
- https://www.langchain.com/