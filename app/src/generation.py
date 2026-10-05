from ollama import chat


def generate_answer(query, retrieved_chunks):
    context = "\n\n".join(
        chunk["text"]
        for chunk in retrieved_chunks
    )

    response = chat(
        model="qwen3:8b",
        think=False,
        options={
            "num_predict": 2000,
        },
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer using only the provided context. "
                    "If the information is not available in the provided context, "
                    "do not generate an answer on your own."
                ),
            },
            {
                "role": "user",
                "content": f"Question: {query}\nContext:\n{context}",
            },
        ],
    )
    return response.message.content


if __name__ == "__main__":
    import sys

    from retrieval import retrieve_from_providers

    sys.stdout.reconfigure(encoding="utf-8")

    query = "Compare Groq and Gemini's documented approaches to function/tool calling. Cover: how tools are declared, how tool calls are represented in the model response, how the application supplies the tool result, whether parallel/compositional tool calling is supported, and what MCP-related capabilities are documented for each."
    providers = ["groq", "gemini"]
    retrieval_top_k = 5

    provider_results = retrieve_from_providers(
        query=query,
        providers=providers,
        top_k=retrieval_top_k,
    )

    retrieved_chunks = [
        {"text": document}
        for result in provider_results
        for document in result["documents"][0]
    ]

    print(f"Retrieved {len(retrieved_chunks)} chunks for generation")
    for index, chunk in enumerate(retrieved_chunks, start=1):
        print(f"{index}. {chunk['text'][:120].replace(chr(10), ' ')}...")

    answer = generate_answer(
        query=query,
        retrieved_chunks=retrieved_chunks,
    )

    print("\nGenerated answer:\n")
    print(answer)