from langchain.llms.base import LLM
from typing import Optional, List
import re

# This is a fake llm sumulator to support ReAct Agent requests
# This calls add tools
class SimpleLLMSimulator(LLM):
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if "Final Answer:" in prompt:
            return ""

        if "Observation:" in prompt:
            match = re.search(r"Observation:\s*(\d+)", prompt)
            if match:
                return f"Thought: I now know the final answer.\nFinal Answer: {match.group(1)}"

        match = re.search(r"(\d+)\s*(?:\+|plus)\s*(\d+)", prompt)
        if match:
            a, b = match.groups()
            return f"Thought: I need to add {a} and {b}.\nAction: AddNumbers\nAction Input: {a} {b}"
        return "Final Answer: Unknown"

    @property
    def _llm_type(self) -> str:
        return "simple-llm-simulator"
