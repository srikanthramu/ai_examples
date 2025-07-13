import asyncio
import re
from typing import TypedDict, Optional

from langgraph.graph import StateGraph, END

from llm_simulator import SimpleLLMSimulator
from mcp_client_handler import MCPClientHandler

# Agent implementation using Langraph

# Define the graph state
class AgentState(TypedDict):
    question: str
    scratchpad: str
    last_observation: Optional[str]


# Simulated LLM
llm = SimpleLLMSimulator()
# MCP Client tool calling
client_handler = MCPClientHandler()


# LLM node (sync)
def llm_node(state: AgentState) -> AgentState:
    prompt = f"{state['scratchpad']}\nQuestion: {state['question']}"
    response = llm.invoke(prompt)
    return {
        **state,
        "scratchpad": state["scratchpad"] + "\n" + response
    }


# Tool node (async)
async def tool_node(state: AgentState) -> AgentState:
    match = re.search(r"Action Input:\s*(.*)", state["scratchpad"])
    if match:
        input_str = match.group(1)
        a, b = map(int, input_str.strip().split())
        result = await client_handler.add_request(a, b)
        new_scratch = state["scratchpad"] + f"\nObservation: {result}"
        return {
            **state,
            "last_observation": result,
            "scratchpad": new_scratch
        }
    return state


# Routing logic
def router(state: AgentState) -> str:
    if "Final Answer:" in state["scratchpad"]:
        return END
    elif "Action:" in state["scratchpad"]:
        return "tool"
    else:
        return "llm"


# Graph setup
graph = StateGraph(AgentState)
graph.add_node("llm", llm_node)
graph.add_node("tool", tool_node, is_async=True)
graph.set_entry_point("llm")
graph.add_conditional_edges("llm", router)
graph.add_edge("tool", "llm")
app = graph.compile()


# Main runner
if __name__ == "__main__":
    async def main():
        inputs = {
            "question": "What is 12 plus 8?",
            "scratchpad": "",
            "last_observation": None
        }
        final_state = await app.ainvoke(inputs)
        print("\n--- FINAL STATE ---")
        print(final_state["scratchpad"])

    asyncio.run(main())
