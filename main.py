import uuid
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from rich.console import Console
from rich.markdown import Markdown

from source.state import AgentState
from source.planner import planner
from source.nasa import nasa
from source.memory import memory
from source.synthesizer import synthesizer

class CosmicReceipts:
    def __init__(self):
        self.memory = MemorySaver()
        self.workflow = self._create_workflow()
        self.app = self.workflow.compile(checkpointer=self.memory)
        print("INFO - Cosmic Receipts Agent initialized")

    def _create_workflow(self) -> StateGraph:
        builder = StateGraph(AgentState)

        builder.add_node("planner", planner)
        builder.add_node("nasa_specialist", nasa)
        builder.add_node("receipt_hunter", memory)
        builder.add_node("synthesizer", synthesizer)

        builder.add_edge(START, "planner")
        builder.add_edge("planner", "nasa_specialist")
        builder.add_edge("nasa_specialist", "receipt_hunter")
        builder.add_edge("receipt_hunter", "synthesizer")
        builder.add_edge("synthesizer", END)
        
        return builder

    def get_plan(self, query: str, user_id: str):
        config = {"configurable": {"thread_id": user_id}}
        inputs = {"query": query}
        return self.app.invoke(inputs, config)


if __name__ == "__main__":
    agent = CosmicReceipts()
    result = agent.get_plan(
        query="What was the energy like when the Voyager golden record launched?",
        user_id=str(uuid.uuid4()),
    )

    result = agent.get_plan(
        query="What was the energy like when the Voyager golden record launched?",
        user_id=str(uuid.uuid4()),
    )

    console = Console()
    if result.get('final_report'):
        console.print("\n[bold magenta]☄️ COSMIC RECEIPTS FINAL REPORT[/bold magenta]")
        console.print(Markdown(result['final_report']))