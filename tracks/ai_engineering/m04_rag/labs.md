# Labs: m04_rag

Real services, your own accounts, your own money (`../labs/README.md`: set up, budget alerts, tagging and the
teardown routine first). A lab gives the goal and the checks, never the steps. Estimate the cost before you
start, then compare with the bill the next morning; prices are from 26/11/2026 and change.

## L4.1: A managed RAG on AWS, with the cheap vector store

- **Goal:** Build a question-answering service with a managed knowledge base on AWS over 50 to 200 documents in S3, using **S3 Vectors as the store** (not the default OpenSearch Serverless collection), and answer 20 labelled questions with citations.
- **Services:** S3, a managed knowledge base, S3 Vectors, one generation model
- **Estimated cost:** $1 to $5 (storage at $0.06 per GB-month, queries at $2.50 per million, embeddings and 20 to 50 answers; **not** the vector collection)
- **Time:** about 4 hours
- **Done when:** answers with citations, the share of questions whose right passage was retrieved, and a note of every setting you chose and why
- **Teardown:** delete the knowledge base, the vector bucket and index, the S3 data and any OpenSearch collection; then confirm by tag that nothing remains. **If you let the console create an OpenSearch Serverless collection, it bills about $175 to $350 per month until you delete it.**

## L4.2: The same RAG in your own code

- **Goal:** Rebuild the L4.1 service as a program you wrote (P1 in `projects/`) against the same documents and questions, and compare cost, quality and control with the managed version.
- **Services:** the L3.1 store or a local store, one model
- **Estimated cost:** $1 to $3 (about 20 questions and a re-embedding run)
- **Time:** about 5 hours
- **Done when:** a comparison table: retrieval hit rate, answer quality on your 20 questions, cost per question, lines of code, what you could not change in the managed one
- **Teardown:** as L3.1
