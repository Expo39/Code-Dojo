# Labs: m03_embeddings_search

Real services, your own accounts, your own money (`../labs/README.md`: set up, budget alerts, tagging and the
teardown routine first). A lab gives the goal and the checks, never the steps. Estimate the cost before you
start, then compare with the bill the next morning; prices are from 26/11/2026 and change.

## L3.1: Index 10,000 chunks two ways

- **Goal:** Embed about 10,000 chunks of a public document set with an embedding model through a hosted API or Bedrock; store the vectors in memory and in PostgreSQL with pgvector on a small managed instance (a `db.t4g.micro`), and compare latency, recall on 20 labelled queries, and effort.
- **Services:** an embedding model, a managed PostgreSQL instance, a security group limited to your address
- **Estimated cost:** $1 to $4 (embeddings of 3 million tokens cost well under $1; the database is about $0.40 per day plus storage)
- **Time:** about 4 hours
- **Done when:** recall at 3 and 10 for both stores, p95 query latency, and the real cost of the day
- **Teardown:** delete the instance and its snapshots, the security group and the stored credentials

## L3.2: Hybrid search by hand

- **Goal:** Add a keyword index (BM25) next to the vectors and combine the two result lists with reciprocal rank fusion; measure against vectors alone on queries that contain codes and rare names.
- **Services:** the L3.1 data, a local keyword library
- **Estimated cost:** $0 (runs locally on the stored embeddings)
- **Time:** about 3 hours
- **Done when:** a table of queries where keyword search, vector search and the fusion each win or lose
- **Teardown:** none
