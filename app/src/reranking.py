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

if __name__ == "__main__":

    candidates = [
        {
            "text": (
                "Production models are intended for production environments. "
                "They meet or exceed Groq's standards for speed, quality, and reliability."
            ),
            "metadata": {"provider": "groq", "section": "Production Models"},
        },
        {
            "text": (
                "Preview models are intended for evaluation purposes only and should not "
                "be used in production because they may be discontinued at short notice."
            ),
            "metadata": {"provider": "groq", "section": "Preview Models"},
        },
        {
            "text": (
                "Groq provides model-specific rate limits, context windows, and maximum "
                "completion token limits in its model documentation."
            ),
            "metadata": {"provider": "groq", "section": "Rate Limits"},
        },
        {
            "text": (
                "Gemini pricing documentation lists the input and output token prices "
                "for each supported model."
            ),
            "metadata": {"provider": "gemini", "section": "Pricing"},
        },
    ]

    query = (
        "What is the documented difference between Groq's Production Models and "
        "Preview Models? Why does the documentation recommend against using Preview "
        "Models in production?"
    )

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