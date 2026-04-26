import chromadb
from sentence_transformers import SentenceTransformer

from source.state import AgentState

class MemoryReceipts:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name="cosmic_receipts")

        if self.collection.count() == 0:
            print("INFO - Memory is empty. Seeding with 70s space receipts...")
            documents = [
                "Murmurs of Earth by Carl Sagan (1978): A detailed account of the Voyager Golden Record project.",
                "Lucifer's Hammer (1977): A classic sci-fi novel about a comet hitting Earth, reflecting 70s cosmic anxiety.",
                "The High Frontier (1976): Gerard K. O'Neill's vision of human colonies in space.",
                "The Right Stuff (1979): Tom Wolfe's look at the psychology of early space pioneers."
            ]
            ids = ["doc1", "doc2", "doc3", "doc4"]
            self.add_receipts_to_memory(documents, ids)
        else:
            print(f"INFO - Memory already contains {self.collection.count()} receipts. Skipping seed.")

    def add_receipts_to_memory(self, documents: list, ids: list):
        embeddings = self.model.encode(documents).tolist()
        self.collection.add(documents=documents, embeddings=embeddings, ids=ids)

    def query_receipts(self, query: str):
        query_embeddings = self.model.encode([query]).tolist()
        results = self.collection.query(query_embeddings=query_embeddings, n_results=2)
        return results["documents"]

    def receipt_hunter_node(self, state: AgentState):
        search_context = state.nasa_results if state.nasa_results else state.query
        found_books = self.query_receipts(search_context)
        flattened_receipts = [item for sublist in found_books for item in sublist]

        return {"library_receipts": flattened_receipts}
    
def memory(state: AgentState):
    m = MemoryReceipts()
    return m.receipt_hunter_node(state)