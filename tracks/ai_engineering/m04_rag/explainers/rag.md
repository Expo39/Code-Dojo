# RAG (retrieval-augmented generation)

*Reference explainer, checked against the official documentation in November 2026. Features and prices change quickly:
the tutor re-checks the live documentation before teaching from it.*

## The problem it solves

A language model only knows what was in its training data, up to a cut-off date. It has never
seen a company's own documents: a 40-page staff handbook, product manuals, last month's tickets.
Asked "what is our refund policy for damaged items?", it will either say it does not know or,
worse, invent a plausible policy (a *hallucination*: confident text not backed by any source).

There are four ways to give the model knowledge it was not trained on:

1. **Paste everything into the prompt (long context).** Simple, and fine when the material is
   small (a few documents) and the same every time. It breaks down when the material is large:
   every question pays for every page in tokens (cost and latency), and models attend less well
   to facts buried in the middle of a very long prompt (*context rot*).
2. **Fine-tuning** (training the model further on your documents). Poor for facts: it is slow
   and costly to redo whenever a document changes, the model still cannot cite where a fact came
   from, and it can still mix facts up. Fine-tuning suits style and format, not knowledge.
3. **Let the model look things up with tools (agentic retrieval).** Give the model a table of
   contents with a short description of each section and a tool to read a section; the model
   decides what to open. This is a common agent pattern (only short descriptions are
   loaded until one is needed) and how an assistant that runs CLI commands against a database
   works. It suits structured data and well-organised documents.
4. **RAG.** Before the model is called, the system itself searches the documents for the few
   passages most relevant to the question and pastes only those into the prompt.

## How classic RAG works, step by step

Done once, ahead of time (*indexing*):

1. **Chunk.** Split each document into passages of a few hundred words (*chunks*), usually
   along headings or paragraphs, often with a small overlap so a sentence is not cut in half.
2. **Embed.** Turn each chunk into an *embedding*: a list of numbers (a vector, often 1,000 or
   more numbers long) produced by an embedding model, such that texts with similar meaning get
   vectors that are close together. "Refund for broken goods" and "returns of damaged items"
   end up close, although they share almost no words.
3. **Store** the vectors with their text in a *vector database* (or a database with vector
   search, such as PostgreSQL with the pgvector extension).

Done for every question:

4. **Embed the question** with the same embedding model.
5. **Retrieve** the top few chunks (the *top-k*, for example 5) whose vectors are closest to
   the question's vector.
6. **Augment** the prompt: "Answer using only the passages below; cite the section; if the
   answer is not in them, say so." followed by the retrieved chunks and the question.
7. **Generate.** The model writes the answer, grounded in (backed by) the retrieved text.

## Making retrieval good

- **Hybrid search.** Embeddings capture meaning but are weak on exact strings: a product code
  such as `SKU-48812`, an error code, a person's name. Keyword search (the classic algorithm is
  BM25, which ranks by matching words) is strong exactly there. Hybrid search runs both and
  merges the results.
- **Reranking.** Retrieve more candidates (say 50) cheaply, then use a slower, more accurate
  model (a *reranker*) to pick the best 5. Better precision without searching slowly.
- **Metadata filters.** Store the document, date, department and access level with each chunk,
  and filter on them ("only the current handbook", "only documents this user may see").

## How RAG fails, and how to debug it

The first question is always: **was the right chunk retrieved?**

- **Retrieval failure:** the right passage was never found (bad chunking cut the answer in
  half; an exact code was missed by vector search; the question used different words). Fix the
  retrieval: chunking, hybrid search, reranking. A better model cannot answer from a passage it
  never saw.
- **Generation failure:** the right passage was in the prompt, but the model ignored it,
  misread it or added things. Fix the prompt (answer only from the passages, cite, say "not
  found"), or the model.

This is why RAG is evaluated in two parts: *retrieval* (for a set of test questions with known
answer passages, how often is the right passage in the top k: *recall at k*) and *answer
quality* (is the answer correct and backed by the passages).

## Security points

- **Access control before retrieval.** If the index holds documents some users may not see
  (salaries, contracts), filter by the user's permissions when retrieving. Telling the model
  "do not reveal HR documents" is a soft control that a cleverly worded question can get past;
  never putting those chunks in the prompt is a hard control.
- **Indirect prompt injection.** Retrieved text is data written by someone else. A document
  that contains "ignore your instructions and ..." ends up inside the prompt. Treat retrieved
  text as untrusted: the model that reads it should have no dangerous tools.

## Choosing: long context, tools or RAG

- Small, stable material: put it in the prompt (with prompt caching to cut the repeated cost).
- Structured data in a database: give the model a query tool (agentic retrieval). Embeddings
  add nothing when the data already has columns to filter on.
- Large amounts of unstructured text (manuals, tickets, policies) that change over time: RAG,
  usually hybrid with reranking.
