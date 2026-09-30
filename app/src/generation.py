from ollama import chat


def generate_answer(query, retrieved_chunks):
    context = "\n\n".join(
        chunk["text"]
        for chunk in retrieved_chunks
    )

    response = chat(
        model="qwen3:8b",
        messages=[{
            "role":"system",
            "content":"Answer using only provided context, if the information is not available"
                      "in the provided context then do not generate an answer on your own."
        },
        {
            "role":"user",
            "content": f"Question: {query}\nContext:\n{context}",
        },
    ],
)
    return response.message.content