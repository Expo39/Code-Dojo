# Try it: m03_embeddings_search

Hands-on, 5 to 15 minutes each. Use any provider's free tier, a local model (for example Ollama) or a fake
model function, so nothing needs a GPU or a paid account unless a task says so. Done when the reading and recall
finish early; never instead of a discussion drill or an exercise. What you type goes in
`workspace/ai_engineering/m03_embeddings_search/try_it/`; what you saw goes in your cheat sheet as "Tried: ...".

- **Similarity search with embeddings** (`similarity_search`): Embed ten short texts with any embedding model (API or local); write cosine similarity yourself and print the top three matches for two queries.
- **Chunking** (`chunking`): Chunk one long document three ways (fixed size, by paragraph, by heading); for five questions, check which chunking returns the answer inside one chunk.
- **Keyword search and BM25** (`keyword_search`): Implement a tiny inverted index over twenty sentences and rank by how many query words match; then note a query where it fails and vectors would not.
- **Vector databases and indexes** (`vector_stores`): Store the same embeddings in an in-memory list and in a small vector store (for example Chroma, FAISS or pgvector); compare the code and the filter options.
- **Ingestion pipelines** (`data_ingestion`): Write a loader that reads a folder, strips boilerplate, hashes each document, and skips documents whose hash has not changed on the second run.
