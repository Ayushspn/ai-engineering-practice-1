# =============================================================================
# 04_complete_rag.py — Complete RAG Application
# python-ai-journey | 05_python_for_ai | 04_rag_app
# =============================================================================
#
# THEORY:
# -------
# This is the COMPLETE RAG pipeline — everything comes together here!
#
# RAG = Retrieval Augmented Generation
#
# Two phases:
#   PHASE 1 — INDEXING (done once, offline):
#     Raw documents
#         ↓ DocumentProcessor — load and split into chunks
#     Text chunks
#         ↓ VectorStore — embed and store in ChromaDB
#     Searchable vector database
#
#   PHASE 2 — QUERYING (done every time user asks):
#     User question
#         ↓ VectorStore — embed question, find similar chunks
#     Relevant context
#         ↓ RAGPrompt — build structured prompt
#     Formatted prompt
#         ↓ LLM (GPT-4 / Claude / local model)
#     Final answer!
#
# INSTALLATION:
#   pip install langchain langchain-core langchain-text-splitters
#   pip install chromadb sentence-transformers
#   pip install langchain-openai  (optional, for real LLM)
#
# =============================================================================

import os
import json
import time
import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter


# =============================================================================
# COMPONENT 1: DOCUMENT PROCESSOR
# =============================================================================

class DocumentProcessor:
    """
    Handles loading and splitting documents into chunks.

    Responsibilities:
    - Load documents from various sources (text, files, URLs)
    - Split large documents into smaller, manageable chunks
    - Maintain metadata about each chunk (source, page, etc.)

    Why split?
    - LLMs have token limits (can't read 100-page docs at once!)
    - Smaller chunks = more precise retrieval
    - chunk_overlap = context continuity between chunks
    """

    def __init__(self, chunk_size=300, chunk_overlap=50):
        self.chunk_size    = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter      = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            # Split order: paragraphs → sentences → words → characters
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        print(f"DocumentProcessor initialized (chunk_size={chunk_size}, overlap={chunk_overlap})")

    def process_text(self, text, source="manual"):
        """Split raw text into chunks with metadata"""
        chunks    = self.splitter.split_text(text)
        documents = []

        for i, chunk in enumerate(chunks):
            documents.append({
                "text":     chunk,
                "metadata": {
                    "source":    source,
                    "chunk_id":  i,
                    "chunk_len": len(chunk)
                }
            })

        return documents

    def process_texts(self, texts, sources=None):
        """Process multiple texts at once"""
        all_documents = []

        for i, text in enumerate(texts):
            source = sources[i] if sources else f"doc_{i}"
            docs   = self.process_text(text, source=source)
            all_documents.extend(docs)

        return all_documents

    def process_file(self, filepath):
        """Load and process a text file"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            return self.process_text(text, source=filepath)
        except FileNotFoundError:
            print(f"File not found: {filepath}")
            return []


# =============================================================================
# COMPONENT 2: VECTOR STORE
# =============================================================================

class VectorStore:
    """
    Manages embeddings storage and retrieval using ChromaDB.

    Responsibilities:
    - Generate embeddings using sentence-transformers
    - Store embeddings + text + metadata in ChromaDB
    - Search for similar documents given a query
    - Return relevant context for LLM

    Why ChromaDB?
    - Free and open source
    - Runs locally (no API key needed!)
    - Fast similarity search
    - Supports metadata filtering
    """

    def __init__(self, collection_name="rag_store", persist_dir=None):
        # Initialize embedding model
        print("Loading embedding model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Embedding model loaded! (384 dimensions)")

        # Initialize ChromaDB
        if persist_dir:
            # Save to disk — data survives between sessions!
            self.client = chromadb.PersistentClient(path=persist_dir)
            print(f"ChromaDB persisting to: {persist_dir}")
        else:
            # In-memory — faster but lost when program ends
            self.client = chromadb.Client()

        # Create or get collection
        try:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}  # use cosine similarity!
            )
            print(f"Created new collection: '{collection_name}'")
        except Exception:
            self.collection = self.client.get_collection(collection_name)
            print(f"Loaded existing collection: '{collection_name}'")

    def add_documents(self, documents):
        """
        Add documents to vector store.
        documents = list of {"text": ..., "metadata": ...}
        """
        if not documents:
            print("No documents to add!")
            return

        texts     = [doc["text"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]

        # Generate embeddings for all chunks at once (batch = fast!)
        print(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(texts, show_progress_bar=False).tolist()

        # Create unique IDs
        start_id = self.collection.count()
        ids      = [f"chunk_{start_id + i}" for i in range(len(texts))]

        # Store in ChromaDB
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        print(f"Added {len(texts)} chunks. Total: {self.collection.count()}")

    def search(self, query, n_results=3, filter_source=None):
        """
        Search for most relevant documents.

        Args:
            query: user's question
            n_results: how many chunks to retrieve (usually 3-5)
            filter_source: only search specific source (optional)

        Returns:
            list of {"text", "similarity", "metadata"}
        """
        # Embed the query
        query_embedding = self.model.encode(query).tolist()

        # Build filter if needed
        where = {"source": filter_source} if filter_source else None

        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, self.collection.count()),
            where=where,
            include=["documents", "distances", "metadatas"]
        )

        # Format and return results
        retrieved = []
        for text, distance, metadata in zip(
            results["documents"][0],
            results["distances"][0],
            results["metadatas"][0]
        ):
            # Convert distance to similarity score
            # ChromaDB cosine distance: 0 = identical, 2 = opposite
            similarity = 1 - (distance / 2)

            retrieved.append({
                "text":       text,
                "similarity": round(similarity, 4),
                "metadata":   metadata
            })

        return retrieved

    def get_stats(self):
        """Get statistics about the vector store"""
        return {
            "total_chunks": self.collection.count(),
            "collection":   self.collection.name
        }


# =============================================================================
# COMPONENT 3: RAG PROMPT BUILDER
# =============================================================================

class RAGPrompt:
    """
    Builds structured prompts for the LLM.

    A good RAG prompt:
    1. Sets the AI's role (system message)
    2. Provides retrieved context clearly
    3. Asks the question clearly
    4. Instructs what to do if answer not in context
    """

    # Main RAG prompt template
    RAG_TEMPLATE = """You are a helpful AI assistant that answers questions based on provided context.

INSTRUCTIONS:
- Answer the question using ONLY the information in the context below
- If the answer is not in the context, say "I don't have information about this in my knowledge base"
- Be concise and precise
- Cite the source when possible

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

    # Conversational RAG template (with chat history)
    CONVERSATIONAL_TEMPLATE = """You are a helpful AI assistant.

CONTEXT FROM KNOWLEDGE BASE:
{context}

CHAT HISTORY:
{chat_history}

CURRENT QUESTION: {question}

ANSWER:"""

    def __init__(self):
        self.rag_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=self.RAG_TEMPLATE
        )
        self.conv_prompt = PromptTemplate(
            input_variables=["context", "chat_history", "question"],
            template=self.CONVERSATIONAL_TEMPLATE
        )

    def build_context(self, retrieved_docs):
        """Format retrieved documents into context string"""
        context_parts = []

        for i, doc in enumerate(retrieved_docs, 1):
            source = doc["metadata"].get("source", "unknown")
            sim    = doc["similarity"]
            text   = doc["text"]
            context_parts.append(
                f"[Document {i} | Source: {source} | Relevance: {sim:.2f}]\n{text}"
            )

        return "\n\n".join(context_parts)

    def build_rag_prompt(self, question, retrieved_docs):
        """Build complete RAG prompt"""
        context = self.build_context(retrieved_docs)
        return self.rag_prompt.format(
            context=context,
            question=question
        )

    def build_conversational_prompt(self, question, retrieved_docs, chat_history):
        """Build prompt with conversation history"""
        context      = self.build_context(retrieved_docs)
        history_text = "\n".join([
            f"Human: {h['question']}\nAI: {h['answer']}"
            for h in chat_history[-3:]  # last 3 turns
        ])
        return self.conv_prompt.format(
            context=context,
            chat_history=history_text or "No previous conversation",
            question=question
        )


# =============================================================================
# COMPONENT 4: SIMULATED LLM
# =============================================================================

class SimulatedLLM:
    """
    Simulates LLM responses for testing WITHOUT an API key.

    In production, replace this with:
    - OpenAI: ChatOpenAI(model="gpt-4")
    - Anthropic: ChatAnthropic(model="claude-3-sonnet")
    - Local: Ollama(model="llama2")

    This simulated version extracts the most relevant sentence
    from the context as a simple "answer".
    """

    def generate(self, prompt):
        """Simulate LLM response by extracting relevant context"""
        # Extract context from prompt
        context_start = prompt.find("CONTEXT:\n") + 9
        context_end   = prompt.find("\n\nQUESTION:")
        question_start= prompt.find("QUESTION: ") + 10
        question_end  = prompt.find("\n\nANSWER:")

        if context_start == 8 or context_end == -1:
            return "Could not generate answer — context not found in prompt."

        context  = prompt[context_start:context_end]
        question = prompt[question_start:question_end]

        # Simple simulation: find most relevant sentence
        sentences = [s.strip() for s in context.replace('\n', ' ').split('.') if len(s.strip()) > 20]

        if not sentences:
            return "I don't have information about this in my knowledge base."

        # Return first relevant sentence as simulated answer
        answer = sentences[0] + "."
        return f"[SIMULATED LLM RESPONSE]\nBased on the provided context: {answer}\n\n(Replace SimulatedLLM with real LLM for actual AI answers!)"


# =============================================================================
# COMPONENT 5: COMPLETE RAG PIPELINE
# =============================================================================

class RAGPipeline:
    """
    The COMPLETE RAG Pipeline — connects all components!

    Flow:
    INDEXING:
      add_documents() → DocumentProcessor → VectorStore

    QUERYING:
      query() → VectorStore.search() → RAGPrompt → LLM → answer

    Usage:
      rag = RAGPipeline()
      rag.add_documents(["doc1...", "doc2..."])
      answer = rag.query("What is Python?")
    """

    def __init__(self, collection_name="complete_rag", persist_dir=None):
        print("\n" + "="*50)
        print("Initializing RAG Pipeline...")
        print("="*50)

        # Initialize all components
        self.processor    = DocumentProcessor(chunk_size=300, chunk_overlap=50)
        self.vector_store = VectorStore(collection_name, persist_dir)
        self.prompt_builder = RAGPrompt()
        self.llm           = SimulatedLLM()
        self.chat_history  = []

        print("\nRAG Pipeline ready! ✅")
        print("="*50)

    def add_documents(self, texts, sources=None):
        """
        INDEXING PHASE:
        Add documents to the RAG knowledge base.

        Steps:
        1. Split documents into chunks
        2. Generate embeddings
        3. Store in ChromaDB
        """
        print(f"\n📚 Indexing {len(texts)} documents...")
        start_time = time.time()

        # Step 1: Process and split documents
        documents = self.processor.process_texts(texts, sources)
        print(f"  Split into {len(documents)} chunks")

        # Step 2 & 3: Embed and store
        self.vector_store.add_documents(documents)

        elapsed = time.time() - start_time
        print(f"  Indexing complete in {elapsed:.2f}s ✅")

    def add_file(self, filepath):
        """Add a text file to the knowledge base"""
        print(f"\n📄 Indexing file: {filepath}")
        documents = self.processor.process_file(filepath)
        if documents:
            self.vector_store.add_documents(documents)

    def query(self, question, n_results=3, verbose=True):
        """
        QUERYING PHASE:
        Answer a question using the RAG pipeline.

        Steps:
        1. Embed the question
        2. Retrieve relevant chunks from ChromaDB
        3. Build prompt with context
        4. Send to LLM
        5. Return answer
        """
        if verbose:
            print(f"\n{'='*50}")
            print(f"🔍 Query: '{question}'")
            print(f"{'='*50}")

        start_time = time.time()

        # Step 1 & 2: Retrieve relevant documents
        retrieved = self.vector_store.search(question, n_results=n_results)

        if verbose:
            print(f"\n📌 Retrieved {len(retrieved)} relevant chunks:")
            for i, doc in enumerate(retrieved, 1):
                print(f"  {i}. [{doc['similarity']:.4f}] {doc['text'][:80]}...")

        # Step 3: Build RAG prompt
        if self.chat_history:
            prompt = self.prompt_builder.build_conversational_prompt(
                question, retrieved, self.chat_history
            )
        else:
            prompt = self.prompt_builder.build_rag_prompt(question, retrieved)

        if verbose:
            print(f"\n📝 Generated Prompt:")
            print(f"{'─'*40}")
            print(prompt)
            print(f"{'─'*40}")

        # Step 4: Generate answer with LLM
        answer = self.llm.generate(prompt)

        # Step 5: Update chat history
        self.chat_history.append({
            "question": question,
            "answer":   answer
        })

        elapsed = time.time() - start_time

        if verbose:
            print(f"\n💡 Answer:")
            print(f"{'─'*40}")
            print(answer)
            print(f"{'─'*40}")
            print(f"⏱ Response time: {elapsed:.2f}s")

        return {
            "question":  question,
            "answer":    answer,
            "retrieved": retrieved,
            "time":      elapsed
        }

    def get_stats(self):
        """Get pipeline statistics"""
        stats = self.vector_store.get_stats()
        stats["chat_history_turns"] = len(self.chat_history)
        return stats

    def clear_history(self):
        """Clear conversation history"""
        self.chat_history = []
        print("Chat history cleared!")


# =============================================================================
# MAIN — RUN THE COMPLETE RAG APP!
# =============================================================================

def main():
    print("\n" + "🚀 " * 20)
    print("COMPLETE RAG APPLICATION")
    print("🚀 " * 20)

    # ─────────────────────────────────────────────
    # STEP 1: Initialize RAG Pipeline
    # ─────────────────────────────────────────────
    rag = RAGPipeline(collection_name="my_rag_app")

    # ─────────────────────────────────────────────
    # STEP 2: Build Knowledge Base
    # ─────────────────────────────────────────────
    print("\n📚 Building Knowledge Base...")

    # Python & AI documents
    python_docs = [
        """Python is a high-level programming language created by Guido van Rossum in 1991.
        Python emphasizes code readability and simplicity with clean, easy-to-understand syntax.
        It is one of the most popular programming languages in the world.""",

        """Python is the #1 language for artificial intelligence and machine learning.
        Key Python libraries for AI include:
        - NumPy: numerical computing with arrays
        - Pandas: data manipulation and analysis
        - Scikit-learn: traditional machine learning
        - PyTorch and TensorFlow: deep learning
        - LangChain: building LLM applications""",

        """RAG (Retrieval Augmented Generation) is a technique that combines:
        1. Retrieval: finding relevant documents from a knowledge base
        2. Augmentation: adding retrieved context to the prompt
        3. Generation: LLM generates answer based on the context
        RAG allows LLMs to answer questions about specific, private documents.""",

        """LangChain is an open-source framework for building LLM applications.
        Key features include:
        - PromptTemplate: structured, reusable prompts
        - TextSplitter: split large documents into chunks
        - VectorStore: store and search embeddings
        - Chain: connect multiple LLM operations
        - Agent: LLM that can use tools and APIs""",

        """ChromaDB is an open-source vector database designed for AI applications.
        It stores text embeddings and enables fast similarity search.
        ChromaDB can run locally (no cloud needed) making it perfect for development.
        It supports metadata filtering and persistent storage.""",
    ]

    # Company/product documents
    company_docs = [
        """Our return policy allows customers to return any product within 30 days of purchase.
        Items must be unused and in original packaging.
        To initiate a return, contact support@company.com or call 1800-XXX-XXXX.
        Refunds are processed within 5-7 business days after we receive the item.""",

        """Shipping Policy:
        - Free standard shipping on orders above Rs 500
        - Standard delivery: 3-5 business days
        - Express delivery: 1-2 business days (Rs 99 extra)
        - International shipping available to 50+ countries
        - Orders placed before 2 PM are dispatched same day""",

        """Customer Support:
        - Email: support@company.com (response within 24 hours)
        - Phone: 1800-XXX-XXXX (Monday-Friday, 9 AM - 6 PM IST)
        - Live chat available on website (9 AM - 9 PM IST)
        - WhatsApp support: +91-XXXXXXXXXX""",
    ]

    # Index all documents
    rag.add_documents(
        python_docs,
        sources=["python_guide"] * len(python_docs)
    )

    rag.add_documents(
        company_docs,
        sources=["company_policy"] * len(company_docs)
    )

    # Show stats
    print(f"\n📊 Knowledge Base Stats: {rag.get_stats()}")

    # ─────────────────────────────────────────────
    # STEP 3: Query the RAG System
    # ─────────────────────────────────────────────
    print("\n" + "🔍 " * 20)
    print("QUERYING THE RAG SYSTEM")
    print("🔍 " * 20)

    # Test queries
    test_queries = [
        "What is Python and who created it?",
        "What libraries does Python have for AI?",
        "What is RAG and how does it work?",
        "What is your return policy?",
        "How long does shipping take?",
        "How can I contact customer support?",
    ]

    results = []
    for query in test_queries:
        result = rag.query(query, n_results=3, verbose=True)
        results.append(result)
        print()

    # ─────────────────────────────────────────────
    # STEP 4: Show Summary
    # ─────────────────────────────────────────────
    print("\n" + "📊 " * 20)
    print("PIPELINE SUMMARY")
    print("📊 " * 20)

    print(f"\nTotal documents indexed: {rag.get_stats()['total_chunks']} chunks")
    print(f"Total queries answered: {len(results)}")
    avg_time = sum(r["time"] for r in results) / len(results)
    print(f"Average response time: {avg_time:.2f}s")

    print("\nQuery Results Summary:")
    print(f"{'─'*60}")
    for result in results:
        top_sim = result["retrieved"][0]["similarity"] if result["retrieved"] else 0
        print(f"Q: {result['question'][:50]}")
        print(f"   Top similarity: {top_sim:.4f} | Time: {result['time']:.2f}s")
    print(f"{'─'*60}")

    # ─────────────────────────────────────────────
    # STEP 5: Production Upgrade Path
    # ─────────────────────────────────────────────
    print("\n" + "🚀 " * 20)
    print("UPGRADING TO PRODUCTION")
    print("🚀 " * 20)

    print("""
To make this production-ready, replace SimulatedLLM with real LLM:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Option 1 — OpenAI (GPT-4):
─────────────────────────
pip install langchain-openai
export OPENAI_API_KEY='sk-...'

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4", temperature=0)
answer = llm.invoke(prompt).content

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Option 2 — Anthropic (Claude):
──────────────────────────────
pip install langchain-anthropic
export ANTHROPIC_API_KEY='sk-ant-...'

from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-sonnet-20240229")
answer = llm.invoke(prompt).content

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Option 3 — Local LLM (FREE! No API key):
─────────────────────────────────────────
pip install ollama
ollama pull llama2  (download model)

from langchain_community.llms import Ollama
llm = Ollama(model="llama2")
answer = llm.invoke(prompt)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Option 4 — FastAPI Web Server:
───────────────────────────────
pip install fastapi uvicorn

from fastapi import FastAPI
app = FastAPI()
rag = RAGPipeline()

@app.post("/query")
async def query(question: str):
    return rag.query(question)

# Run: uvicorn main:app --reload
# Then: curl -X POST "http://localhost:8000/query?question=What+is+Python"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")


# =============================================================================
# RUN THE APP!
# =============================================================================

if __name__ == "__main__":
    main()


# =============================================================================
# EXPECTED OUTPUT WHEN YOU RUN THIS:
# =============================================================================
#
# 🚀 🚀 🚀 ... COMPLETE RAG APPLICATION ... 🚀 🚀 🚀
#
# Initializing RAG Pipeline...
# DocumentProcessor initialized (chunk_size=300, overlap=50)
# Loading embedding model...
# Embedding model loaded! (384 dimensions)
# Created new collection: 'my_rag_app'
# RAG Pipeline ready! ✅
#
# 📚 Building Knowledge Base...
# 📚 Indexing 5 documents...
#   Split into 8 chunks
#   Generating embeddings for 8 chunks...
#   Added 8 chunks. Total: 8
#   Indexing complete in 1.23s ✅
#
# 📚 Indexing 3 documents...
#   Split into 4 chunks
#   Generating embeddings for 4 chunks...
#   Added 4 chunks. Total: 12
#   Indexing complete in 0.45s ✅
#
# 📊 Knowledge Base Stats: {'total_chunks': 12, 'collection': 'my_rag_app', ...}
#
# ==================================================
# 🔍 Query: 'What is Python and who created it?'
# ==================================================
#
# 📌 Retrieved 3 relevant chunks:
#   1. [0.8923] Python is a high-level programming language created by Guido van Rossum...
#   2. [0.7234] Python is the #1 language for artificial intelligence and machine learning...
#   3. [0.4123] LangChain is an open-source framework for building LLM applications...
#
# 📝 Generated Prompt:
# ────────────────────────────────────────
# You are a helpful AI assistant...
# CONTEXT:
# [Document 1 | Source: python_guide | Relevance: 0.89]
# Python is a high-level programming language created by Guido van Rossum in 1991...
# QUESTION: What is Python and who created it?
# ANSWER:
# ────────────────────────────────────────
#
# 💡 Answer:
# ────────────────────────────────────────
# [SIMULATED LLM RESPONSE]
# Based on the provided context: Python is a high-level programming language
# created by Guido van Rossum in 1991.
# (Replace SimulatedLLM with real LLM for actual AI answers!)
# ────────────────────────────────────────
# ⏱ Response time: 0.12s
#
# (Similar output for all 6 queries...)
#
# 📊 Pipeline Summary:
# Total documents indexed: 12 chunks
# Total queries answered: 6
# Average response time: 0.15s
#
# =============================================================================
# SUMMARY
# =============================================================================
#
# | Component         | Role                              | Technology          |
# |-------------------|-----------------------------------|---------------------|
# | DocumentProcessor | Load + split documents            | LangChain splitter  |
# | VectorStore       | Embed + store + search            | ChromaDB + ST       |
# | RAGPrompt         | Build structured prompts          | LangChain templates |
# | SimulatedLLM      | Generate answers (replace me!)   | Your choice of LLM  |
# | RAGPipeline       | Connect all components            | Python classes      |
#
# COMPLETE RAG FLOW:
#   INDEXING:  Documents → Split → Embed → ChromaDB
#   QUERYING:  Question → Embed → Search → Prompt → LLM → Answer
#
# PRODUCTION UPGRADE:
#   Replace SimulatedLLM with:
#   → OpenAI GPT-4 (best quality, paid)
#   → Claude (great quality, paid)
#   → Ollama Llama2 (free, local, private!)
#
# GOLDEN RULES:
# 1. chunk_size=300, overlap=50 → good starting point
# 2. n_results=3 → retrieve 3 chunks (not too few, not too many)
# 3. Always include source in metadata → trace where answers come from!
# 4. PersistentClient → save embeddings to disk (don't regenerate!)
# 5. SimulatedLLM → replace with real LLM for production!
#
# =============================================================================
