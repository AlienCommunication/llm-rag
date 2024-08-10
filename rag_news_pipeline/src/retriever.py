import faiss
import numpy as np

class Retriever:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []

    def add_documents(self, documents, embeddings):
        self.index.add(embeddings)
        self.documents.extend(documents)

    def retrieve(self, query_embedding, k=5):
        distances, indices = self.index.search(np.array([query_embedding]), k)
        return [self.documents[i] for i in indices[0]]