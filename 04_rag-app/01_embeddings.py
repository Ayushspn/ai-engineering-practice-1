# =============================================================================
# 01_embeddings.py — Text Embeddings for RAG
# python-ai-journey | 05_python_for_ai | 04_rag_app
# =============================================================================
#
# THEORY:
# -------
# Embeddings = converting text into numbers (vectors)
# that capture MEANING of the text.
#
# Similar meaning → similar numbers → close in vector space!
#
# Why embeddings?
#   Computers can't understand words directly.
#   They need numbers to do math!
#   Embeddings = bridge between human language and computer math.
#
# How embeddings work:
#   1. Text → tokenize (split into words/subwords)
#   2. Tokens → pass through neural network
#   3. Neural network → outputs vector of numbers
#   4. Vector captures meaning, context, relationships!
#
# Embedding models:
#   - sentence-transformers (free, local, fast!)
#   - OpenAI text-embedding-ada-002 (paid, cloud)
#   - Google PaLM embeddings (paid, cloud)
#
# =============================================================================

import numpy as np
from sentence_transformers import SentenceTransformer


# =============================================================================
# PART 1: UNDERSTANDING EMBEDDINGS
# =============================================================================

print("=" * 60)
print("PART 1: UNDERSTANDING EMBEDDINGS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 1: Load Embedding Model
# -----------------------------------------------------------------------------

print("\n--- Loading Embedding Model ---")

# Load a free, local embedding model
# 'all-MiniLM-L6-v2' = fast, good quality, 384 dimensions
model = SentenceTransformer('all-MiniLM-L6-v2')
print(f"Model loaded: all-MiniLM-L6-v2")
print(f"Embedding dimensions: 384")


# -----------------------------------------------------------------------------
# SECTION 2: Convert Text to Embedding
# -----------------------------------------------------------------------------

print("\n--- Converting Text to Embedding ---")

# Single sentence → embedding vector
sentence = "Python is great for AI"
embedding = model.encode(sentence)

print(f"Text:           '{sentence}'")
print(f"Embedding type: {type(embedding)}")
print(f"Embedding shape:{embedding.shape}")    # (384,) ← 384 numbers!
print(f"First 5 values: {embedding[:5]}")      # peek at first 5 numbers
print(f"Min value:      {embedding.min():.4f}")
print(f"Max value:      {embedding.max():.4f}")

# Key insight: every sentence → exactly 384 numbers
# Short or long sentence → always 384 numbers!
short = model.encode("Hi")
long  = model.encode("Python is a great programming language for AI and machine learning applications")

print(f"\nShort sentence shape: {short.shape}")  # (384,)
print(f"Long sentence shape:  {long.shape}")     # (384,) ← same!


# -----------------------------------------------------------------------------
# SECTION 3: Cosine Similarity — Measure Text Similarity
# -----------------------------------------------------------------------------

print("\n--- Cosine Similarity ---")

def cosine_similarity(a, b):
    """
    Measure similarity between two embeddings.
    Returns value between -1 and 1:
      1.0  = identical meaning
      0.0  = unrelated
     -1.0  = opposite meaning
    """
    # dot product of a and b
    dot = np.dot(a, b)
    # magnitude (length) of each vector
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    # cosine similarity formula
    return dot / (norm_a * norm_b)

# Test with related and unrelated sentences
sentences = [
    "Python is great for AI",              # A
    "Machine learning with Python",        # B — similar to A
    "Cricket match in India",              # C — different from A
    "Deep learning and neural networks",   # D — somewhat related to A
    "Cooking recipe for biryani",          # E — very different from A
]

# Generate embeddings for all sentences
embeddings = model.encode(sentences)
print(f"Embeddings shape: {embeddings.shape}")  # (5, 384) ← 5 sentences, 384 dims each

# Compare sentence A with all others
print(f"\nSimilarity with: '{sentences[0]}'")
print("-" * 50)
for i, (sent, emb) in enumerate(zip(sentences, embeddings)):
    sim = cosine_similarity(embeddings[0], emb)
    bar = "█" * int(sim * 20)    # visual bar
    print(f"  [{sim:.4f}] {bar:<20} {sent}")


# =============================================================================
# PART 2: EMBEDDINGS FOR RAG
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: EMBEDDINGS FOR RAG")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 4: Document Embedding — Index Your Knowledge Base
# -----------------------------------------------------------------------------

print("\n--- Document Embedding ---")

# Simulate a knowledge base (your documents!)
documents = [
    "Python was created by Guido van Rossum in 1991.",
    "NumPy is used for numerical computing in Python.",
    "Pandas is used for data manipulation and analysis.",
    "Machine learning is a subset of artificial intelligence.",
    "RAG stands for Retrieval Augmented Generation.",
    "Embeddings convert text into numerical vectors.",
    "ChromaDB is a vector database for storing embeddings.",
    "LangChain is a framework for building LLM applications.",
    "The Eiffel Tower is located in Paris, France.",
    "Cricket is the most popular sport in India.",
]

print(f"Total documents: {len(documents)}")
print("Generating embeddings for all documents...")

# Convert all documents to embeddings
doc_embeddings = model.encode(documents)
print(f"Document embeddings shape: {doc_embeddings.shape}")
# (10, 384) ← 10 documents, 384 dimensions each


# -----------------------------------------------------------------------------
# SECTION 5: Query Embedding — Search Your Knowledge Base
# -----------------------------------------------------------------------------

print("\n--- Searching with Query ---")

def search_documents(query, documents, doc_embeddings, top_k=3):
    """
    Search for most relevant documents for a query.
    This is the RETRIEVAL step in RAG!

    Steps:
    1. Convert query to embedding
    2. Compare with all document embeddings
    3. Return top_k most similar documents
    """
    # Step 1 — embed the query
    query_embedding = model.encode(query)

    # Step 2 — calculate similarity with all documents
    similarities = []
    for i, doc_emb in enumerate(doc_embeddings):
        sim = cosine_similarity(query_embedding, doc_emb)
        similarities.append((sim, i, documents[i]))

    # Step 3 — sort by similarity (highest first)
    similarities.sort(reverse=True)

    # Return top_k results
    return similarities[:top_k]


# Test search with different queries
queries = [
    "What is RAG?",
    "How does Python handle data?",
    "What is cricket?",
]

for query in queries:
    print(f"\nQuery: '{query}'")
    print("Top 3 relevant documents:")
    results = search_documents(query, documents, doc_embeddings)
    for sim, idx, doc in results:
        print(f"  [{sim:.4f}] {doc}")


# -----------------------------------------------------------------------------
# SECTION 6: Batch Embedding — Efficient Processing
# -----------------------------------------------------------------------------

print("\n--- Batch Embedding (Efficient) ---")

# Process multiple texts at once — much faster than one by one!
batch_texts = [
    "What is machine learning?",
    "How does Python work?",
    "What are embeddings?",
]

# Single call for all texts — batch processing!
batch_embeddings = model.encode(batch_texts)
print(f"Batch shape: {batch_embeddings.shape}")  # (3, 384)
print("All embeddings generated in ONE call — efficient!")


# =============================================================================
# PART 3: PRACTICAL PATTERNS
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: PRACTICAL PATTERNS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 7: Similarity Matrix — Compare All with All
# -----------------------------------------------------------------------------

print("\n--- Similarity Matrix ---")

texts = [
    "Python programming",
    "Machine learning",
    "Artificial intelligence",
    "Cricket sport",
    "Cooking food",
]

embs = model.encode(texts)

# Calculate similarity between ALL pairs
print(f"{'':20}", end="")
for t in texts:
    print(f"{t[:10]:12}", end="")
print()

for i, t1 in enumerate(texts):
    print(f"{t1[:20]:20}", end="")
    for j, t2 in enumerate(texts):
        sim = cosine_similarity(embs[i], embs[j])
        print(f"{sim:.2f}{'':8}", end="")
    print()

print("\nObservation:")
print("  Python/ML/AI → high similarity (related topics!)")
print("  Cricket/Cooking → low similarity with Python (unrelated!)")


# -----------------------------------------------------------------------------
# SECTION 8: Save and Load Embeddings
# -----------------------------------------------------------------------------

print("\n--- Save and Load Embeddings ---")

# In real RAG apps — generate embeddings ONCE, save to disk!
# Don't regenerate every time!

# Save embeddings
np.save("doc_embeddings.npy", doc_embeddings)
print("Embeddings saved to doc_embeddings.npy")

# Load embeddings later
loaded_embeddings = np.load("doc_embeddings.npy")
print(f"Loaded embeddings shape: {loaded_embeddings.shape}")
print(f"Same as original: {np.allclose(doc_embeddings, loaded_embeddings)}")

# Cleanup
import os
os.remove("doc_embeddings.npy")


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Concept              | Key Insight                                       |
# |----------------------|---------------------------------------------------|
# | Embedding            | Text → vector of numbers capturing meaning        |
# | Dimensions           | all-MiniLM-L6-v2 → 384 numbers per text          |
# | Similar text         | → similar vectors → high cosine similarity        |
# | Cosine similarity    | dot(a,b) / (|a| × |b|) → between -1 and 1       |
# | 1.0                  | identical meaning                                 |
# | 0.0                  | completely unrelated                              |
# | Batch encoding       | encode([text1, text2, ...]) → faster!             |
# | Save embeddings      | np.save() → don't regenerate every time!         |
# | RAG retrieval        | query → embed → find similar docs → retrieve      |
#
# GOLDEN RULES:
# 1. Similar meaning → similar vectors → high cosine similarity!
# 2. Always batch encode — don't encode one by one!
# 3. Save embeddings to disk — don't regenerate every time!
# 4. Embedding shape is always fixed — regardless of text length!
# 5. Cosine similarity > 0.7 = very similar, < 0.3 = unrelated
#
# NEXT STEP:
# Now that we can create and compare embeddings,
# we need somewhere to STORE them efficiently!
# → 02_vector_db.py — ChromaDB vector database!
#
# =============================================================================
