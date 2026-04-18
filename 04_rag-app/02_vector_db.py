# =============================================================================
# 02_vector_db.py — Vector Database with ChromaDB
# python-ai-journey | 05_python_for_ai | 04_rag_app
# =============================================================================
#
# THEORY:
# -------
# A Vector Database stores embeddings and lets you search by SIMILARITY.
# Instead of exact match search → finds nearest neighbors!
#
# Why Vector DB?
#   1. Store millions of embeddings efficiently
#   2. Find similar embeddings in milliseconds
#   3. Persist data between sessions (save to disk!)
#   4. Scale to production!
#
# ChromaDB:
#   - Free and open source
#   - Runs locally (no API key needed!)
#   - Perfect for learning and prototyping
#   - Can scale to production too!
#
# Key concepts:
#   1. Collection  — like a table in SQL (stores related embeddings)
#   2. Documents   — the text you want to store
#   3. Embeddings  — vector representations of documents
#   4. Metadata    — extra info about each document (source, date, etc.)
#   5. IDs         — unique identifier for each document
#   6. Query       — search for similar documents
#
# =============================================================================

import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer


# =============================================================================
# PART 1: CHROMADB BASICS
# =============================================================================

print("=" * 60)
print("PART 1: CHROMADB BASICS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 1: Setup ChromaDB
# -----------------------------------------------------------------------------

print("\n--- Setting Up ChromaDB ---")

# Create ChromaDB client — stores data in memory
# (use chromadb.PersistentClient for saving to disk!)
client = chromadb.Client()

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

print("ChromaDB client created!")
print("Embedding model loaded!")


# -----------------------------------------------------------------------------
# SECTION 2: Create a Collection
# -----------------------------------------------------------------------------

print("\n--- Creating Collection ---")

# Collection = like a table in SQL
# Groups related documents together
collection = client.create_collection(
    name="knowledge_base",      # unique name for collection
    metadata={"description": "My RAG knowledge base"}
)

print(f"Collection created: {collection.name}")
print(f"Total documents: {collection.count()}")   # 0 — empty!


# -----------------------------------------------------------------------------
# SECTION 3: Add Documents to Collection
# -----------------------------------------------------------------------------

print("\n--- Adding Documents ---")

# Our knowledge base documents
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

# Generate embeddings for all documents
print("Generating embeddings...")
embeddings = model.encode(documents).tolist()  # convert to list for ChromaDB

# Add to collection
collection.add(
    documents=documents,           # the actual text
    embeddings=embeddings,         # the vector representations
    ids=[f"doc_{i}" for i in range(len(documents))],  # unique IDs
    metadatas=[{"source": "knowledge_base", "index": i}
               for i in range(len(documents))]  # extra info
)

print(f"Added {len(documents)} documents!")
print(f"Total in collection: {collection.count()}")


# =============================================================================
# PART 2: SEARCHING THE VECTOR DATABASE
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: SEARCHING")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 4: Basic Search
# -----------------------------------------------------------------------------

print("\n--- Basic Search ---")

def search(query, n_results=3):
    """
    Search for most relevant documents.
    This is the RETRIEVAL step in RAG!
    """
    # Step 1 — convert query to embedding
    query_embedding = model.encode(query).tolist()

    # Step 2 — search ChromaDB for similar documents
    results = collection.query(
        query_embeddings=[query_embedding],   # our query vector
        n_results=n_results,                   # how many to return
        include=["documents", "distances", "metadatas"]
    )

    return results

# Test search
queries = [
    "What is RAG?",
    "Tell me about Python",
    "What is cricket?",
]

for query in queries:
    print(f"\nQuery: '{query}'")
    results = search(query)

    print("Top results:")
    for doc, distance in zip(
        results["documents"][0],
        results["distances"][0]
    ):
        # Distance = how far apart (lower = more similar!)
        similarity = 1 - distance    # convert distance to similarity
        print(f"  [{similarity:.4f}] {doc}")


# -----------------------------------------------------------------------------
# SECTION 5: Search with Metadata Filter
# -----------------------------------------------------------------------------

print("\n--- Search with Metadata Filter ---")

# Add more documents with different sources
tech_docs = [
    "FastAPI is a modern web framework for Python.",
    "Docker containers package applications and dependencies.",
    "Git is a version control system.",
]

tech_embeddings = model.encode(tech_docs).tolist()

collection.add(
    documents=tech_docs,
    embeddings=tech_embeddings,
    ids=[f"tech_{i}" for i in range(len(tech_docs))],
    metadatas=[{"source": "tech_docs", "index": i}
               for i in range(len(tech_docs))]
)

print(f"Total documents now: {collection.count()}")

# Search with metadata filter
results = collection.query(
    query_embeddings=[model.encode("Python web development").tolist()],
    n_results=3,
    where={"source": "tech_docs"},   # only search tech_docs!
    include=["documents", "distances"]
)

print("\nSearch 'Python web development' in tech_docs only:")
for doc, dist in zip(results["documents"][0], results["distances"][0]):
    print(f"  [{1-dist:.4f}] {doc}")


# =============================================================================
# PART 3: CRUD OPERATIONS
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: CRUD OPERATIONS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 6: Update and Delete Documents
# -----------------------------------------------------------------------------

print("\n--- Update Documents ---")

# Update a document
collection.update(
    ids=["doc_0"],
    documents=["Python was created by Guido van Rossum in 1991 and is now very popular for AI."],
    embeddings=model.encode(["Python was created by Guido van Rossum in 1991 and is now very popular for AI."]).tolist()
)
print("Updated doc_0!")

# Get a specific document by ID
result = collection.get(ids=["doc_0"])
print(f"Updated doc: {result['documents'][0]}")

print("\n--- Delete Documents ---")

# Delete a document
collection.delete(ids=["doc_9"])   # delete cricket document
print(f"Deleted doc_9!")
print(f"Total after delete: {collection.count()}")


# =============================================================================
# PART 4: PERSISTENT STORAGE
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: PERSISTENT STORAGE")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 7: Save to Disk
# -----------------------------------------------------------------------------

print("\n--- Saving to Disk ---")

import tempfile
import os

# Create persistent client — saves to disk!
tmp_dir = tempfile.mkdtemp()
persistent_client = chromadb.PersistentClient(path=tmp_dir)

# Create collection
persistent_collection = persistent_client.create_collection(
    name="persistent_knowledge"
)

# Add documents
docs = ["Python is great!", "AI is the future!", "RAG is powerful!"]
embs = model.encode(docs).tolist()

persistent_collection.add(
    documents=docs,
    embeddings=embs,
    ids=["p1", "p2", "p3"]
)

print(f"Saved {persistent_collection.count()} documents to disk!")
print(f"Location: {tmp_dir}")

# Load from disk later
loaded_client     = chromadb.PersistentClient(path=tmp_dir)
loaded_collection = loaded_client.get_collection("persistent_knowledge")

print(f"Loaded {loaded_collection.count()} documents from disk!")

# Search loaded collection
results = loaded_collection.query(
    query_embeddings=model.encode(["What is Python?"]).tolist(),
    n_results=2,
    include=["documents"]
)
print(f"Search results: {results['documents'][0]}")

# Cleanup temp directory
import shutil
shutil.rmtree(tmp_dir)


# =============================================================================
# PART 5: COMPLETE RAG RETRIEVAL PIPELINE
# =============================================================================

print("\n" + "=" * 60)
print("PART 5: COMPLETE RAG RETRIEVAL PIPELINE")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 8: Full Retrieval System
# -----------------------------------------------------------------------------

print("\n--- Full Retrieval System ---")

class VectorRetriever:
    """
    Complete retrieval system for RAG.
    Handles:
    1. Adding documents to vector DB
    2. Searching for relevant documents
    3. Returning context for LLM
    """

    def __init__(self, collection_name="rag_retriever"):
        # Setup ChromaDB
        self.client     = chromadb.Client()
        self.model      = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection = self.client.create_collection(collection_name)
        print(f"VectorRetriever initialized: {collection_name}")

    def add_documents(self, documents, source="default"):
        """Add documents to vector database"""
        # Generate embeddings
        embeddings = self.model.encode(documents).tolist()

        # Create unique IDs
        start_id   = self.collection.count()
        ids        = [f"doc_{start_id + i}" for i in range(len(documents))]
        metadatas  = [{"source": source, "chunk_id": i}
                      for i in range(len(documents))]

        # Add to ChromaDB
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )
        print(f"Added {len(documents)} documents. Total: {self.collection.count()}")

    def retrieve(self, query, n_results=3):
        """
        Retrieve most relevant documents for a query.
        Returns context string ready for LLM!
        """
        # Embed query
        query_embedding = self.model.encode(query).tolist()

        # Search vector DB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "distances", "metadatas"]
        )

        # Format results
        retrieved = []
        for doc, dist, meta in zip(
            results["documents"][0],
            results["distances"][0],
            results["metadatas"][0]
        ):
            similarity = 1 - dist
            retrieved.append({
                "document":   doc,
                "similarity": similarity,
                "source":     meta["source"]
            })

        return retrieved

    def get_context(self, query, n_results=3):
        """Get context string for LLM prompt"""
        results  = self.retrieve(query, n_results)
        context  = "\n".join([f"- {r['document']}" for r in results])
        return context


# Test the complete retrieval system
retriever = VectorRetriever("my_rag")

# Add knowledge base
knowledge = [
    "Python is a high-level programming language.",
    "Machine learning uses algorithms to learn from data.",
    "RAG combines retrieval with text generation.",
    "ChromaDB stores and searches vector embeddings.",
    "LangChain simplifies building LLM applications.",
]
retriever.add_documents(knowledge, source="textbook")

# Add more from different source
company_docs = [
    "Our return policy allows returns within 30 days.",
    "Customer support is available 24/7.",
    "Free shipping on orders above Rs 500.",
]
retriever.add_documents(company_docs, source="company_policy")

# Test retrieval
test_queries = [
    "What is machine learning?",
    "What is your return policy?",
    "How does RAG work?",
]

for query in test_queries:
    print(f"\nQuery: '{query}'")
    context = retriever.get_context(query)
    print(f"Retrieved context:\n{context}")
    print(f"\n→ This context would be sent to LLM with the query!")


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Concept           | Key Insight                                          |
# |-------------------|------------------------------------------------------|
# | Vector DB         | Stores embeddings, searches by similarity            |
# | ChromaDB          | Free, local vector DB — perfect for RAG!             |
# | Collection        | Like a table — groups related documents              |
# | add()             | Store documents + embeddings + metadata              |
# | query()           | Find most similar documents to a query               |
# | distance          | Lower = more similar (ChromaDB uses distance)        |
# | similarity        | 1 - distance = easier to understand                 |
# | PersistentClient  | Save to disk — data survives between sessions!       |
# | Metadata filter   | Search within specific subset of documents           |
# | VectorRetriever   | Complete retrieval system for RAG!                   |
#
# RAG FLOW SO FAR:
#   Documents → Embeddings → Vector DB (ChromaDB)
#   Query → Embedding → Search Vector DB → Retrieved Context
#   Retrieved Context + Query → LLM → Answer! (next file!)
#
# GOLDEN RULES:
# 1. Use PersistentClient for real apps — don't regenerate!
# 2. Add metadata — helps filter and organize documents
# 3. n_results = how many docs to retrieve (usually 3-5)
# 4. Lower distance = more similar (ChromaDB default)
# 5. VectorRetriever class wraps everything cleanly!
#
# NEXT STEP:
# We can now store and retrieve documents!
# Next → connect to LLM to generate answers!
# → 03_langchain_basics.py
#
# =============================================================================
