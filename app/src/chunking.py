from pathlib import Path
import re

URLS = {
    "auth": "https://ai.google.dev/gemini-api/docs/oauth?hl=en",
    "pricing": "https://ai.google.dev/gemini-api/docs/pricing?hl=en",
    "rate_limits": "https://ai.google.dev/gemini-api/docs/rate-limits?hl=en",
    "models": "https://ai.google.dev/gemini-api/docs/models?hl=en",
    "tool_calling": "https://ai.google.dev/gemini-api/docs/function-calling?hl=en"
}


DOCUMENTS_DIR = Path(__file__).resolve().parent.parent / "documents" / "gemini"


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
                "url": URLS[section]
            }
        })

    return chunks


def load_documents():
    all_chunks = []

    for file_path in DOCUMENTS_DIR.glob("*.md"):

        section = file_path.stem

        text = file_path.read_text(encoding="utf-8")

        chunks = chunk_markdown(
            text=text,
            provider="gemini",
            section=section,
            url="PUT_URL_HERE"
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