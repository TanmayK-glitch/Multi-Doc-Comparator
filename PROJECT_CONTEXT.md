# Multi-Doc-Comparator — Project Context

> **Purpose:** This document is a compact but complete orientation guide for an LLM or developer who needs to understand, debug, extend, or operate this project.
>
> **Snapshot date:** 2026-10-05  
> **Repository root:** `C:\Users\Asus\Documents\Multi-Doc-Comparator`

## 1. Project purpose

Multi-Doc-Comparator is a small Python retrieval-augmented generation (RAG) prototype. It stores locally captured documentation for multiple AI providers, retrieves the most relevant sections for a question, reranks those sections with Cohere, and asks a local Ollama model to answer using only the retrieved context.

The current knowledge base contains documentation for:

- **Gemini:** authentication, models, pricing, rate limits, and tool/function calling.
- **Groq:** authentication/MCP connectors, models, rate limits, and tool calling.

The intended use case is comparative questions such as:

> Compare Groq and Gemini's documented approaches to function/tool calling.

This is currently a collection of executable scripts rather than a packaged library or web application. There is no test suite, dependency manifest, CLI wrapper, API server, or README in the repository at the time of this snapshot.

## 2. High-level architecture

```text
app/documents/<provider>/*.md
              |
              v
app/src/chunking.py
  - reads Markdown files
  - splits on level-2 headings
  - attaches provider/section/source URL metadata
              |
              v
app/src/ingestion.py
  - embeds chunks with all-MiniLM-L6-v2
  - recreates Chroma collection "my-collection"
  - persists vectors under app/src/data/chroma/
              |
              v
app/src/retrieval.py
  - queries Chroma per provider
  - returns top-k result batches
              |
              v
app/src/pipeline.py
  - flattens provider result batches
  - sends candidates to Cohere rerank-v4.0-pro
              |
              v
app/src/generation.py
  - concatenates reranked text
  - sends context and question to Ollama qwen3:8b
  - returns the generated answer
```

### Runtime data flow

1. `chunking.load_documents()` scans `app/documents/` in sorted provider/file order.
2. Each Markdown file is divided into chunks at lines beginning with `## `.
3. Each chunk receives:
   - `provider`: directory name, for example `gemini` or `groq`;
   - `section`: Markdown filename without `.md`;
   - `url`: source URL from the provider URL registry.
4. `ingestion.py` embeds every chunk and rebuilds Chroma collection `my-collection`.
5. `pipeline.search()` retrieves `retrieval_top_k` chunks for each requested provider, combines them, and reranks the combined candidate set.
6. `generation.generate_answer()` joins only the candidate text, not the metadata, into a prompt for Ollama.

## 3. Repository tree

Generated and environment files are shown separately below because they are runtime artifacts, not source-of-truth project code.

```text
Multi-Doc-Comparator/
├── .env                         # local secrets; ignored by Git
├── .gitignore                   # ignored files and directories
├── .vscode/
│   └── settings.json            # editor settings
├── app/
│   ├── documents/
│   │   ├── gemini/
│   │   │   ├── auth.md
│   │   │   ├── models.md
│   │   │   ├── pricing.md
│   │   │   ├── rate_limits.md
│   │   │   └── tool_calling.md
│   │   └── groq/
│   │       ├── auth.md
│   │       ├── models.md
│   │       ├── rate_limits.md
│   │       └── tool_calling.md
│   └── src/
│       ├── chunking.py
│       ├── generation.py
│       ├── ingestion.py
│       ├── pipeline.py
│       ├── reranking.py
│       ├── retrieval.py
│       └── data/chroma/       # generated local Chroma files
├── data/chroma/                # another generated Chroma store; not used by current code
└── PROJECT_CONTEXT.md          # this document
```

Additional ignored/generated directories currently present:

- `.venv/`: local Python virtual environment and installed packages.
- `app/src/__pycache__/`: Python bytecode cache.
- `app/src/data/chroma/` and `data/chroma/`: SQLite/HNSW/Chroma persistence artifacts.

Do not copy `.venv`, `__pycache__`, SQLite files, or Chroma binary files into an LLM prompt. They do not explain the source behavior and can be regenerated.

## 4. Source files

### [`app/src/chunking.py`](app/src/chunking.py)

**Role:** document discovery, Markdown section splitting, and metadata construction.

**Important constants and behavior:**

- `URLS` maps the supported provider/section names to the original documentation URLs.
- `DOCUMENTS_DIR` resolves to `app/documents/` using the source file location, so execution does not depend on the current working directory for document discovery.
- `chunk_markdown(text, provider, section, url)`:
  - splits with `re.split(r"\n(?=## )", text)`;
  - trims each part;
  - ignores empty parts;
  - ignores a part beginning with `# `, which removes the document-level title;
  - returns dictionaries with `text` and `metadata`.
- `load_documents()`:
  - iterates provider folders and Markdown files in sorted order;
  - uses the folder name as the provider;
  - uses the filename stem as the section;
  - silently uses an empty URL for a document not represented in `URLS`.
- The `__main__` block prints chunk count, metadata, and the first 500 characters of each chunk.

**Chunk contract:**

```python
{
    "text": str,
    "metadata": {
        "provider": str,
        "section": str,
        "url": str,
    },
}
```

**Implications and limitations:**

- Only level-2 headings are recognized as chunk boundaries.
- Content before the first `## ` is discarded if it is a level-1 title section.
- Tables and code blocks remain part of the surrounding chunk.
- There is no token-based chunk-size limit or overlap.
- New provider folders are discovered automatically, but their source URLs must be added to `URLS` for useful citations/metadata.

### [`app/src/ingestion.py`](app/src/ingestion.py)

**Role:** build/rebuild the local vector index.

**Execution sequence:**

1. Import `load_documents`.
2. Load all chunks.
3. Extract `text` and `metadata`.
4. Load `SentenceTransformer("all-MiniLM-L6-v2")`.
5. Encode all text with `normalize_embeddings=True`.
6. Open a persistent Chroma client at `app/src/data/chroma/`.
7. Delete collection `my-collection` if it exists.
8. Create a fresh `my-collection`.
9. Add IDs `chunk_0`, `chunk_1`, etc., documents, embeddings, and metadata.

**Operational consequence:** running this script is destructive to the current `my-collection`; it intentionally rebuilds the entire index. It must be rerun whenever source documents change.

**Failure behavior:** only `chromadb.errors.NotFoundError` is ignored when deleting the old collection. Other errors propagate.

### [`app/src/retrieval.py`](app/src/retrieval.py)

**Role:** query the persistent Chroma collection.

**Initialization:**

- Creates a `SentenceTransformer("all-MiniLM-L6-v2")` object, although the object is not used by the current query calls.
- Opens Chroma at the same path as ingestion: `app/src/data/chroma/`.
- Gets collection `my-collection`; it must already exist.

**Functions:**

- `retrieve_for_provider(query, provider, top_k)` queries one provider with:

  ```python
  collection.query(
      query_texts=[query],
      n_results=top_k,
      where={"provider": provider},
  )
  ```

- `retrieve_from_providers(query, providers, top_k=5)` performs the same query once per provider and returns a list of raw Chroma result objects, one result object per provider.
- `print_results(result)` prints rank, distance, ID, metadata, and document text for one Chroma result object.

**Important dependency:** Chroma must have a compatible embedding function/configuration for `query_texts`. The ingestion script explicitly stores embeddings, while retrieval relies on Chroma's query-time handling.

**Demo:** the `__main__` block compares Gemini and Groq tool-calling documentation with five retrieved chunks per provider.

### [`app/src/reranking.py`](app/src/reranking.py)

**Role:** rerank retrieved candidates with Cohere.

**Initialization:**

- Loads environment variables from the project-root `.env` using `Path(__file__).resolve().parents[2]`.
- Reads `COHERE_API_KEY`.
- Raises `RuntimeError("COHERE_API_KEY is missing from the project .env file")` immediately if the key is absent.
- Creates `cohere.ClientV2(api_key=api_key)`.

**Function:**

- `rerank(query, candidates, top_k)` extracts `candidate["text"]`, calls Cohere model `rerank-v4.0-pro`, and returns the selected candidates in Cohere result order.
- Each returned candidate is copied and augmented with `rerank_score`.

**Candidate expectation:**

```python
{
    "id": str,
    "text": str,
    "metadata": dict,
    "retrieval_distance": float,  # optional
}
```

**Operational consequence:** importing `pipeline.py` imports this module, so a Cohere API key is required even before a search is performed.

### [`app/src/pipeline.py`](app/src/pipeline.py)

**Role:** orchestration between retrieval and reranking, plus the end-to-end demo.

**Functions:**

- `build_candidates(provider_results)` flattens raw Chroma results:
  - reads the first result group (`[0]`) for documents, metadata, IDs, and distances;
  - creates one candidate per retrieved document;
  - preserves Chroma metadata;
  - adds `retrieval_distance` when distances are present.
- `search(query, providers, retrieval_top_k=5, rerank_top_k=5)`:
  1. calls `retrieve_from_providers`;
  2. flattens results with `build_candidates`;
  3. reranks with Cohere;
  4. returns the reranked list.

The commented `identify_providers` code is not active. The current caller must explicitly pass providers.

**Demo:** when run as a script, it searches Gemini and Groq tool-calling content and passes the result to `generate_answer`.

### [`app/src/generation.py`](app/src/generation.py)

**Role:** final answer generation through a local Ollama model.

**Function:** `generate_answer(query, retrieved_chunks)`:

- concatenates each chunk's `text` with blank lines;
- sends a system instruction requiring answers to use only supplied context;
- sends the question and concatenated context as the user message;
- calls `ollama.chat(model="qwen3:8b", messages=[...])`;
- returns `response.message.content`.

**Runtime requirement:** Ollama must be installed/running locally and the `qwen3:8b` model must be available. This model is not a cloud provider model and is not part of the indexed documentation.

**Current limitation:** metadata, source URLs, IDs, retrieval distances, and rerank scores are not included in the generation prompt, so the generated answer cannot reliably cite source documents unless citation text is added later.

## 5. Documentation corpus

The files under `app/documents/` are local Markdown snapshots used as the retrieval corpus. They are not fetched automatically by the Python code; updating the corpus is a manual process.

### Gemini documents

- [`app/documents/gemini/auth.md`](app/documents/gemini/auth.md): Gemini API key guidance and a testing-oriented OAuth quickstart, including Google Cloud project setup, consent screen/test users, desktop OAuth credentials, and ADC-related setup.
- [`app/documents/gemini/models.md`](app/documents/gemini/models.md): Gemini API model catalog and model metadata captured from Google's model documentation.
- [`app/documents/gemini/pricing.md`](app/documents/gemini/pricing.md): model pricing information for Gemini API usage.
- [`app/documents/gemini/rate_limits.md`](app/documents/gemini/rate_limits.md): Gemini API request/token rate-limit documentation.
- [`app/documents/gemini/tool_calling.md`](app/documents/gemini/tool_calling.md): Gemini function/tool-calling concepts, declaration and response formats, tool results, compositional/parallel behavior, and MCP-related material captured from Google's documentation.

Source URLs configured in `chunking.py`:

- Auth: `https://ai.google.dev/gemini-api/docs/oauth?hl=en`
- Pricing: `https://ai.google.dev/gemini-api/docs/pricing?hl=en`
- Rate limits: `https://ai.google.dev/gemini-api/docs/rate-limits?hl=en`
- Models: `https://ai.google.dev/gemini-api/docs/models?hl=en`
- Tool calling: `https://ai.google.dev/gemini-api/docs/function-calling?hl=en`

### Groq documents

- [`app/documents/groq/auth.md`](app/documents/groq/auth.md): Groq remote MCP connector authentication, OAuth access tokens, connector examples, required scopes, and connector tool examples for Google Calendar, Gmail, and Google Drive.
- [`app/documents/groq/models.md`](app/documents/groq/models.md): Groq supported, production, preview, and deprecated model documentation, including model IDs, context windows, pricing, speed, and limits.
- [`app/documents/groq/rate_limits.md`](app/documents/groq/rate_limits.md): Groq RPM/RPD/TPM/TPD/ASH/ASD concepts, free/developer plan tables, rate-limit headers, and HTTP 429 behavior.
- [`app/documents/groq/tool_calling.md`](app/documents/groq/tool_calling.md): Groq local tool calling and related tool-use documentation.

Source URLs configured in `chunking.py`:

- Auth: `https://console.groq.com/docs/tool-use/remote-mcp/connectors#authentication`
- Models: `https://console.groq.com/docs/models`
- Rate limits: `https://console.groq.com/docs/rate-limits`
- Tool calling: `https://console.groq.com/docs/tool-use/local-tool-calling`

The corpus is time-sensitive. Pricing, model availability, rate limits, and provider APIs can change; treat the local Markdown as the project's captured source of truth, not as current live provider policy.

## 6. Configuration and secrets

### `.env`

The root `.env` is ignored by Git and must not be committed or pasted into an LLM context. The current code requires:

```dotenv
COHERE_API_KEY=your_cohere_key
```

No `.env.example` is currently present. Creating one would improve onboarding without exposing a secret.

### [`.vscode/settings.json`](.vscode/settings.json)

The workspace settings file enables:

```json
{
    "python.analysis.autoImportCompletions": true
}
```

No formatter, linter, test runner, Python interpreter path, or environment variable is configured in workspace settings.

### [`\.gitignore`](.gitignore)

The ignore rules protect:

- `.env` and environment variants;
- virtual environments;
- Python caches and common test/type-check artifacts;
- local Chroma/vector stores and SQLite/DB files;
- build artifacts;
- notebook checkpoints;
- logs/temp files;
- editor/OS files.

## 7. How to run the current pipeline

Run commands from `app/src` because the source uses direct local imports such as `from chunking import load_documents`.

### Rebuild the vector index

```powershell
Set-Location C:\Users\Asus\Documents\Multi-Doc-Comparator\app\src
python ingestion.py
```

This downloads/loads `all-MiniLM-L6-v2` as needed, reads every corpus Markdown file, deletes and recreates `my-collection`, and writes the Chroma store under `app/src/data/chroma/`.

### Run the end-to-end comparison

```powershell
Set-Location C:\Users\Asus\Documents\Multi-Doc-Comparator\app\src
python pipeline.py
```

Prerequisites:

1. A working Python environment with the imported packages installed.
2. A root `.env` containing `COHERE_API_KEY`.
3. A populated Chroma collection; run `ingestion.py` first if needed.
4. A running local Ollama service with `qwen3:8b` available.
5. Network access for Cohere and the first SentenceTransformers model download.

### Inspect retrieval without generation

```powershell
Set-Location C:\Users\Asus\Documents\Multi-Doc-Comparator\app\src
python retrieval.py
```

### Run module-level demonstrations

```powershell
python chunking.py
python reranking.py
```

The reranking demo still requires a valid Cohere key. These scripts are demonstrations, not automated tests.

## 8. Dependencies inferred from imports

There is no `requirements.txt` or `pyproject.toml`. The source imports:

| Package | Used by | Purpose |
|---|---|---|
| `chromadb` | ingestion, retrieval | persistent vector database and query API |
| `sentence-transformers` | ingestion, retrieval | `all-MiniLM-L6-v2` embeddings |
| `cohere` | reranking | Cohere reranking API |
| `python-dotenv` | reranking | loads root `.env` |
| `ollama` | generation | local Ollama chat client |

The Python standard library imports are `pathlib`, `re`, and `os`.

## 9. Important invariants and data contracts

- The Chroma collection name is exactly `my-collection`.
- Ingestion and retrieval must use the same persistence path: `app/src/data/chroma/`.
- Provider filtering depends on metadata key `provider`.
- Section filtering/interpretation depends on metadata key `section`.
- Chroma result arrays are expected in the standard nested form, so the pipeline reads `[0]`.
- `search()` returns reranked candidate dictionaries, not generated text.
- `generate_answer()` expects candidates containing a `text` key.
- `rerank()` expects each candidate's `text` to be a string and adds `rerank_score`.
- The provider list is explicit; provider detection is not implemented.
- Every indexed document should have a stable `provider`, `section`, and ideally a non-empty `url`.

## 10. Known limitations and likely maintenance points

1. **No dependency lock/manifest.** Reproducing the environment requires inferring packages from imports.
2. **No automated tests.** Changes should be manually validated or accompanied by a test structure.
3. **No type annotations.** Function inputs/outputs and Chroma/Cohere response shapes are implicit.
4. **No error handling around external services.** Network, authentication, missing collection, model, and Ollama failures generally propagate as exceptions.
5. **Import-time side effects.** `retrieval.py` loads a SentenceTransformer and opens Chroma at import time; `reranking.py` loads `.env`, validates the key, and constructs a Cohere client at import time.
6. **Unused embedding model in retrieval.** `retrieval.py` creates a SentenceTransformer but does not use it directly.
7. **Potential Chroma embedding configuration coupling.** Ingestion supplies embeddings explicitly, while retrieval uses `query_texts`; the Chroma collection/client configuration must support query-time embedding.
8. **Unbounded context size.** Retrieval and reranking counts are capped by `top_k`, but there is no token budget check before sending all reranked text to Ollama.
9. **No source citations in answers.** Metadata is retained through retrieval/reranking but discarded by generation.
10. **Stale local corpus.** Provider documentation is manually captured and may no longer match current online docs.
11. **Duplicate vector-store locations.** `data/chroma/` exists at the repository root, but current source code uses only `app/src/data/chroma/`. The root store should not be assumed to be active.
12. **Simple Markdown splitting.** Headings, nested sections, long tables, and code examples may produce uneven chunks.
13. **Collection rebuild is not incremental.** Any ingestion run deletes the existing collection before adding all chunks.
14. **No concurrency or batching strategy.** All embedding and provider queries are performed synchronously.
15. **Commented experimental code.** The unused provider-identification block in `pipeline.py` should not be treated as active behavior.

## 11. Safe extension guidance

When adding a provider:

1. Add `app/documents/<provider>/` and Markdown files.
2. Add matching `<section>: <source URL>` entries under the provider in `chunking.py`.
3. Rebuild the index with `ingestion.py`.
4. Pass the provider name explicitly to `pipeline.search()`.
5. Verify metadata filtering and reranked output before enabling generation.

When adding a new document section:

1. Name the file using the section key expected by `URLS`.
2. Ensure the source content uses `## ` headings for useful chunk boundaries.
3. Add or update its URL mapping.
4. Rebuild the collection.

When changing the model or retrieval strategy:

- keep ingestion and retrieval embedding behavior compatible;
- preserve metadata keys used by `where={"provider": ...}`;
- validate Chroma result shapes before changing `build_candidates`;
- decide explicitly whether the generation prompt should include citations and metadata;
- add a token/context budget before increasing retrieval counts.

## 12. Suggested first improvements

If this prototype is being developed further, the highest-value next steps are:

1. Add `pyproject.toml` or `requirements.txt` and a `.env.example`.
2. Move model/client initialization into functions or dependency-injected components.
3. Add type annotations and tests for chunking, candidate flattening, and provider filtering.
4. Add source citations to the generation context and output format.
5. Add explicit error messages for missing Chroma collection, Ollama model/service, and external API failures.
6. Make chunking token-aware with configurable chunk size and overlap.
7. Remove or document the unused retrieval embedding model.
8. Resolve the duplicate root `data/chroma/` directory and make the active storage path explicit.
9. Add a small CLI or application entry point instead of relying on script `__main__` blocks.

## 13. Context handoff prompt

The following short instruction can be sent together with this file to another LLM:

> You are helping me maintain the Multi-Doc-Comparator project. Read `PROJECT_CONTEXT.md` first. Treat `app/src/` as the active Python implementation, `app/documents/` as a manually captured provider-document corpus, and `app/src/data/chroma/` as generated runtime state. Do not expose or request the contents of `.env`. Preserve the contracts for Chroma collection `my-collection`, provider metadata filtering, Cohere reranking, and Ollama `qwen3:8b` generation. Before proposing changes, check whether they affect ingestion, retrieval, reranking, generation, source URLs, or generated data. Prefer precise changes and validate behavior with the smallest relevant command.
