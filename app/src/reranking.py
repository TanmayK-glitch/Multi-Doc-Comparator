import os
from pathlib import Path

import cohere
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    raise RuntimeError("COHERE_API_KEY is missing from the project .env file")

co = cohere.ClientV2(api_key=api_key)

def rerank(query, candidates, top_k):
    documents = [
        candidate["text"] for candidate in candidates
    ]

    response = co.rerank(
        model="rerank-v4.0-pro",
        query=query,
        top_n=top_k,
        documents=documents
    )

    ranked_candidates = []

    for result in response.results:
        candidate = candidates[result.index].copy()

        candidate["rerank_score"] = result.relevance_score

        ranked_candidates.append(candidate)

    return ranked_candidates


def build_candidates(provider_results):
    candidates = []

    for result in provider_results:
        documents = result["documents"][0]
        metadatas = result["metadatas"][0]
        ids = result["ids"][0]
        distances = result.get("distances", [[]])[0]

        for index, document in enumerate(documents):
            candidate = {
                "id": ids[index],
                "text": document,
                "metadata": metadatas[index],
            }

            if distances:
                candidate["retrieval_distance"] = distances[index]

            candidates.append(candidate)

    return candidates


if __name__ == "__main__":
    import sys

    from retrieval import retrieve_from_providers

    sys.stdout.reconfigure(encoding="utf-8")

    query = (
        "Compare Groq and Gemini's documented approaches to function/tool calling. Cover: how tools are declared, how tool calls are represented in the model response, how the application supplies the tool result, whether parallel/compositional tool calling is supported, and what MCP-related capabilities are documented for each."
    )

    provider_results = retrieve_from_providers(
        query=query,
        providers=["groq", "gemini"],
        top_k=5,
    )
    candidates = build_candidates(provider_results)

    print(f"Retrieved {len(candidates)} chunks for reranking")

    results = rerank(
        query=query,
        candidates=candidates,
        top_k=3
    )

    for rank, result in enumerate(results, start=1):
        print(
            f"Rank {rank} | score={result['rerank_score']:.4f} | "
            f"{result['metadata']['provider']} / {result['metadata']['section']}"
        )
        print(result["text"])