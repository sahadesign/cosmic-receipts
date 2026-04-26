from .LLM import LLM
from .state import AgentState
from langchain_core.messages import HumanMessage


class Planner:
    def __init__(self):
        self.llm = LLM()

    def planner_node(self, state: AgentState):
        print("INFO - Planning the vibe")
        prompt = f"""
        User Query = {state.query}

        "You are the Lead Planner for 'Cosmic Receipts.' You're like a high-IQ intern 
        who knows everything about space. 
        Analyze the user's query and follow this 2-step plan:
        1. Identify the key NASA technical term/date to search.
        2. Identify the cultural 'vibe' to match in the library receipts.

        Output your response as JSON with two keys: 
        'reasoning' (the text plan) and 'nasa_date' (the YYYY-MM-DD date to search).
        """
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return {"plan": [str(response.content)]}


def planner(state: AgentState):
    p = Planner()
    p.planner_node(state)
    return state
