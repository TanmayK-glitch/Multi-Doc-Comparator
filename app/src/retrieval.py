import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="./data/chroma"
)

collection = client.get_collection(
    name="my-collection"
)

question = [
    "Does Gemini support function calling?"
]

result = collection.query(
    query_texts=question,
    n_results=5
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