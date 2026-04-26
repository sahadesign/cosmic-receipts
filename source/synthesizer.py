from source.state import AgentState
from source.LLM import LLM
from langchain_core.messages import SystemMessage, HumanMessage


class Synthesizer:
    def __init__(self):
        self.llm = LLM()

    def synthesizer_node(self, state: AgentState):
        s_prompt = f"""
            "You are the 'Cosmic Receipts' orator. Your job is to take technical NASA data "
            "and cultural book receipts and synthesize them into a witty, high-IQ response. "
            "Be punchy, use headers, and bridge the gap between the science and the 'vibe'."
        """

        user_content = f"""
        Nasa Data: {state.nasa_results}
        Cultural Receipts: {state.library_receipts}
        Original User Query: {state.query}
        """

        response = self.llm.invoke(
            [SystemMessage(content=s_prompt), HumanMessage(content=user_content)]
        )

        return {"final_report": response.content}
    

def synthesizer(state: AgentState):
    s = Synthesizer()
    return s.synthesizer_node(state)