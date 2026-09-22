from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer
from chunking import load_documents

from chromadb.errors import NotFoundError

chunks = load_documents()

print(f"Loaded {len(chunks)} chunks")

texts = [chunk["text"] for chunk in chunks]

metadatas = [chunk["metadata"] for chunk in chunks]

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    texts,
    normalize_embeddings=True
).tolist()

client = chromadb.PersistentClient(
    path=Path(__file__).resolve().parent / "data" / "chroma"
)

try:
    client.delete_collection(name="my-collection")
except NotFoundError:
    pass

collection = client.create_collection(
    name="my-collection"
)

ids = [
    f"chunk_{i}"
    for i in range(len(chunks))
]

collection.add(
    ids=ids,
    documents=texts,
    embeddings=embeddings,
    metadatas=metadatas
)


print(f"Successfully added {len(chunks)} chunks to ChromaDB.")