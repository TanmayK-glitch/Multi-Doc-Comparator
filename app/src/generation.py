import ollama


def generate_answer(query, retrieved_chunks):
    source_blocks = []

    for index, chunk in enumerate(retrieved_chunks, start=1):
        metadata = chunk.get("metadata", {})

        provider = metadata.get("provider", "unknown")
        section = metadata.get("section", "unknown")
        url = metadata.get("url", "unknown")

        source_blocks.append(
            f"""
[SOURCE {index}]
provider: {provider}
section: {section}
url: {url}

content:
{chunk["text"]}
"""
        )

    context = "\n".join(source_blocks)

    system_prompt = """
You are a documentation comparison assistant.

Answer the user's question using ONLY the supplied sources.

Rules:
1. Do not use outside knowledge.
2. Do not infer or assume a capability that is not explicitly supported by the sources.
3. Every factual claim about a provider must include a citation in this format:
   [SOURCE N]
4. Keep provider-specific evidence separate. Do not transfer a capability from one provider to another.
5. If the supplied sources do not establish an answer for a provider, explicitly write:
   "Not specified in the retrieved documentation."
6. Follow every part of the user's question.
7. Prefer a structured comparison with clear sections or a table.
"""

    user_prompt = f"""
Question:
{query}

Retrieved documentation:
{context}
"""

    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        options={
            "num_predict": 1500,
        },
    )

    return response.message.content