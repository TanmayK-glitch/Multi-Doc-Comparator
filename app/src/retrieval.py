from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path=Path(__file__).resolve().parent / "data" / "chroma"
)

collection = client.get_collection(
    name="my-collection"
)

question = [
    "What are Groq's rate limits?"
]

result = collection.query(
    query_texts=question,
    n_results=5,
    where={"provider": "groq"}
)

for i in range(len(result["documents"][0])):
    print("\n" + "=" * 80)
    print(f"RESULT {i + 1}")
    print("=" * 80)

    print(f"Distance : {result['distances'][0][i]}")
    print(f"ID       : {result['ids'][0][i]}")

    print("\nMetadata:")
    print(result["metadatas"][0][i])

    print("\nDocument:")
    print(result["documents"][0][i])