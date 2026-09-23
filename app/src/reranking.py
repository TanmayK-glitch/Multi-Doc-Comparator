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
        {"text": "Gemini rate limits information...", "metadata": {"provider": "gemini"}},
        {"text": "Groq rate limits information...", "metadata": {"provider": "groq"}},
        {"text": "Gemini pricing information...", "metadata": {"provider": "gemini"}},
    ]

    query = "Compare rate limits of Gemini and Groq"

    results = rerank(
        query=query,
        candidates=candidates,
        top_k=3
    )

    for result in results:
        print(result)