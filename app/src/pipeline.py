from retrieval import retrieve_from_providers
from reranking import rerank

# Providers for identify_providers func 
# PROVIDERS = ["gemini", "openrouter", "anthropic", "groq"]

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


# def identify_providers(query):
#     query = query.lower()

#     mentioned_provider = [
#         provider
#         for provider in PROVIDERS
#         for query in provider
#     ]

#     return mentioned_provider if mentioned_provider else PROVIDERS



def search(query, providers, retrieval_top_k=5, rerank_top_k=5):
    provider_results = retrieve_from_providers(
        query=query,
        providers=providers,
        top_k=retrieval_top_k,
    )
    candidates = build_candidates(provider_results)

    return rerank(
        query=query,
        candidates=candidates,
        top_k=rerank_top_k,
    )


if __name__ == "__main__":
    from generation import generate_answer

    query = "Compare Groq and Gemini's documented approaches to function/tool calling. Cover: how tools are declared, how tool calls are represented in the model response, how the application supplies the tool result, whether parallel/compositional tool calling is supported, and what MCP-related capabilities are documented for each."

    results = search(
        query=query,
        providers=["groq", "gemini"],
        retrieval_top_k=5,
        rerank_top_k=5,
    )

    generated_answer = generate_answer(
        query=query,
        retrieved_chunks=results
    )

    # for result in results:
    #     print(result)
    print(generated_answer)
