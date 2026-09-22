from pathlib import Path
import re

URLS = {
    "gemini": {
        "auth": "https://ai.google.dev/gemini-api/docs/oauth?hl=en",
        "pricing": "https://ai.google.dev/gemini-api/docs/pricing?hl=en",
        "rate_limits": "https://ai.google.dev/gemini-api/docs/rate-limits?hl=en",
        "models": "https://ai.google.dev/gemini-api/docs/models?hl=en",
        "tool_calling": "https://ai.google.dev/gemini-api/docs/function-calling?hl=en"
    },
    "groq": {
        "auth": "https://console.groq.com/docs/tool-use/remote-mcp/connectors#authentication",
        "models": "https://console.groq.com/docs/models",
        "rate_limits": "https://console.groq.com/docs/rate-limits",
        "tool_calling": "https://console.groq.com/docs/tool-use/local-tool-calling"
    }
}


DOCUMENTS_DIR = Path(__file__).resolve().parent.parent / "documents"


def chunk_markdown(text, provider, section, url):
    parts = re.split(r"\n(?=## )", text)

    chunks = []

    for part in parts:
        part = part.strip()

        if not part:
            continue

        if part.startswith("# "):
            continue

        chunks.append({
            "text": part,
            "metadata": {
                "provider": provider,
                "section": section,
                "url": url
            }
        })

    return chunks


def load_documents():
    all_chunks = []

    for provider_dir in sorted(DOCUMENTS_DIR.iterdir()):
        if not provider_dir.is_dir():
            continue

        provider = provider_dir.name
        provider_urls = URLS.get(provider, {})

        for file_path in sorted(provider_dir.glob("*.md")):
            section = file_path.stem

            text = file_path.read_text(encoding="utf-8")

            chunks = chunk_markdown(
                text=text,
                provider=provider,
                section=section,
                url=provider_urls.get(section, "")
            )

            all_chunks.extend(chunks)

    return all_chunks


if __name__ == "__main__":
    chunks = load_documents()

    print(f"Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print("\n" + "=" * 60)
        print(f"CHUNK {i + 1}")
        print("=" * 60)
        print(chunk["metadata"])
        print(chunk["text"][:500])  