# Keyword search, vectors and vector databases

*Reference explainer, checked against the official documentation in November 2026. Features and prices change quickly:
the tutor re-checks the live documentation before teaching from it.*

These are the two ways a system finds the passages relevant to a question, the retrieval step
of RAG (see [RAG](../../m04_rag/explainers/rag.md)).

## Keyword search

Keyword search finds documents that contain the words of the query.

**How it is fast: an inverted index.** Like the index at the back of a book, it lists every word
once with the documents that contain it, built ahead of time:

```text
refund  -> tickets 87, 112, 140
policy    -> tickets 87, 112, 95, 201
delay -> tickets 12, 87, 300
```

A query "refund policy" looks up two lines instead of reading every ticket, and ticket 87 and
112, which contain both words, come first.

**How results are ranked: BM25,** the standard scoring formula. A document scores higher when
it contains more of the query words, when those words are *rare* in the whole collection (a
match on "refund" says much more than a match on "the" or "camera", which appear everywhere),
and it does not win just by being long.

- **Strength:** exact strings. An error code (`ERR_PAYMENT_DECLINED`), a product code, a
  person's name, a version number are found reliably.
- **Weakness:** it only knows words, not meaning. "Zero delays after the update" does not
  match a ticket that says "inference policy rebuilt for the wrong refund version", although
  both describe the same problem: they share no important word.

Most tools already have keyword search: a help-centre search box, `grep`, PostgreSQL full-text
search, Elasticsearch.

## Vectors and embeddings

A **vector** is simply a list of numbers, such as `[0.9, 0.1]`. A list of two numbers can be
drawn as a point on a flat map; a list of three as a point in a room; longer lists work the same
way, only in more directions than can be drawn.

An **embedding** is a vector that an *embedding model* (a neural network trained for this job)
produces from a piece of text, so that **texts with similar meaning get points close together**.

A toy version with only two numbers, imagining one number means "about cameras" and the other
"about payments":

```text
"camera shows no delays"      -> [0.90, 0.10]
"zero people counted since update" -> [0.85, 0.15]   close to the first: same meaning
"customer wants a refund"          -> [0.05, 0.95]   far away: different topic
```

Real embedding models produce several hundred to a few thousand numbers per text, and the
individual numbers have no human-readable meaning: the model learned them from huge amounts of
text so that the distances work out. Closeness is usually measured with *cosine similarity*
(how nearly two vectors point the same way; 1 means the same direction).

So a search by meaning becomes a geometry question: turn the question into a vector with the
same model, then find the stored vectors nearest to it. That is how the "zero delays"
question finds the refund ticket with no word in common.

- **Strength:** meaning, synonyms, different phrasing, even different languages.
- **Weakness:** exact codes and rare names, which carry little "meaning" for the model.

This is why *hybrid search* runs both kinds and merges the results.

## Vector databases

A **vector database** stores, for each chunk of text, its vector, the text itself and metadata
(ticket number, device, date), and answers one question fast: "give me the k stored vectors
nearest to this one".

- With a few thousand chunks, comparing the query with every stored vector is quick enough.
- With millions, it uses an *approximate nearest-neighbour index* (the common one is HNSW, a
  graph that links each vector to its near neighbours so a search hops towards the closest ones
  instead of checking all of them). It trades a tiny chance of missing the very best match for a
  large gain in speed.

It need not be a new product: **pgvector** is an extension for PostgreSQL that adds a `vector`
column type, a distance operator and these indexes, so a team that already runs PostgreSQL keeps
its vectors next to its normal tables and can filter by ordinary columns in the same query.
Dedicated vector databases (Qdrant, Pinecone, Weaviate, Chroma) exist for very large or
specialised loads.
