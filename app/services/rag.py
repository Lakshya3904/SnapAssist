import json
import numpy as np
from sentence_transformers import SentenceTransformer


class RAGEngine:

    def __init__(self, knowledge_file="data/knowledge.json"):
        with open(knowledge_file, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.texts = [
            f"{doc['component']}. "
            f"{doc['description']} "
            f"{doc['maintenance']} "
            f"{doc['action']}"
            for doc in self.documents
        ]

        self.embeddings = self.model.encode(
            self.texts,
            normalize_embeddings=True
        )

    def search(self, query, top_k=2):

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )[0]

        scores = np.dot(self.embeddings, query_embedding)

        indices = np.argsort(scores)[::-1][:top_k]

        results = []

        for i in indices:
            results.append({
                "component": self.documents[i]["component"],
                "description": self.documents[i]["description"],
                "safety": self.documents[i]["safety"],
                "maintenance": self.documents[i]["maintenance"],
                "action": self.documents[i]["action"],
                "score": round(float(scores[i]), 3)
            })

        return results


rag_engine = RAGEngine()