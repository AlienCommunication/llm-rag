from src.processing.text_processor import TextProcessor
from src.database.vector_store import VectorStore

class QueryEngine:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.text_processor = TextProcessor()

    def query(self, query, k=5):
        processed_query = self.text_processor.preprocess(query)
        results = self.vector_store.search(processed_query, k)
        return results