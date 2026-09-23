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

def retrieve_for_provider(query, provider, top_k):
    result = collection.query(
        query_texts=[query],
        n_results=top_k,
        where={"provider": provider}
    )

    return result

def retrieve_from_providers(query, providers, top_k=5):
    all_chunks = []

    for provider in providers:
        result = collection.query(
            query_texts=[query],
            n_results=top_k,
            where={"provider": provider}
        )

        all_chunks.append(result)
        
    return all_chunks


def print_results(result):
    for i, document in enumerate(result["documents"][0]):
        print("\n" + "=" * 80)
        print(f"RESULT {i + 1}")
        print("=" * 80)
        print(f"Distance : {result['distances'][0][i]}")
        print(f"ID       : {result['ids'][0][i]}")
        print("\nMetadata:")
        print(result["metadatas"][0][i])
        print("\nDocument:")
        print(document)


if __name__ == "__main__":
    # result = retrieve_for_provider(
    #     query="What are Groq's rate limits?",
    #     provider="groq",
    #     top_k=5
    # )

    result = retrieve_from_providers(
        query="Compare the rate limits of Gemini and Groq",
        providers=["gemini", "groq"],
        top_k=5
    )
    for provider_result in result:
        print_results(provider_result)