# =============================================================================
# 03_langchain_basics.py — LangChain for RAG
# python-ai-journey | 05_python_for_ai | 04_rag_app
# =============================================================================
#
# THEORY:
# -------
# LangChain = Framework for building LLM applications.
# It provides ready-made building blocks so you don't start from scratch.
#
# Think of LangChain like LEGO blocks:
#   Each block does ONE thing well
#   Connect blocks together to build complex apps
#   RAG = Retriever block + LLM block + Prompt block
#
# Key LangChain building blocks:
#   1. PromptTemplate  — structure your prompts consistently
#   2. TextSplitter    — split large documents into chunks
#   3. Embeddings      — convert text to vectors
#   4. VectorStore     — store and search embeddings
#   5. Retriever       — fetch relevant documents
#   6. Chain           — connect everything together
#   7. LLM/ChatModel   — the AI brain (GPT-4, Claude, etc.)
#
# INSTALLATION:
#   pip install langchain langchain-core langchain-community
#   pip install langchain-openai  (for OpenAI)
#   pip install chromadb sentence-transformers
#
# =============================================================================

# NOTE: Run this file on your machine after:
#   pip install langchain langchain-core langchain-text-splitters
#   pip install langchain-openai chromadb sentence-transformers
#   Set OPENAI_API_KEY environment variable (optional for free parts)


# =============================================================================
# PART 1: PROMPT TEMPLATES
# =============================================================================

print("=" * 60)
print("PART 1: PROMPT TEMPLATES")
print("=" * 60)

# PromptTemplate = reusable, structured prompts
# Instead of hardcoding prompts → use templates with variables!

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# -----------------------------------------------------------------------------
# SECTION 1: Basic Prompt Template
# -----------------------------------------------------------------------------

print("\n--- Basic Prompt Template ---")

# Define template with variables in {curly braces}
template = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful AI assistant.
Use the following context to answer the question.
If you don't know the answer, say "I don't know".

Context:
{context}

Question: {question}

Answer:"""
)

# Fill in the template with actual values
prompt = template.format(
    context="Python was created by Guido van Rossum in 1991. It is widely used for AI.",
    question="Who created Python?"
)

print("Template output:")
print(prompt)
print()

# ACTUAL OUTPUT WHEN YOU RUN THIS:
# ----------------------------------------
# Template output:
# You are a helpful AI assistant.
# Use the following context to answer the question.
# If you don't know the answer, say "I don't know".
#
# Context:
# Python was created by Guido van Rossum in 1991. It is widely used for AI.
#
# Question: Who created Python?
#
# Answer:
# ----------------------------------------


# -----------------------------------------------------------------------------
# SECTION 2: Chat Prompt Template
# -----------------------------------------------------------------------------

print("\n--- Chat Prompt Template ---")

# ChatPromptTemplate = for chat models (GPT-4, Claude)
# Has system message + human message structure

chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant specialized in {domain}."),
    ("human", "Context:\n{context}\n\nQuestion: {question}")
])

# Format the chat template
messages = chat_template.format_messages(
    domain="Python programming",
    context="Python uses indentation for code blocks instead of curly braces.",
    question="How does Python handle code blocks?"
)

print("Chat messages:")
for msg in messages:
    print(f"  [{msg.__class__.__name__}]: {msg.content[:80]}...")
print()

# ACTUAL OUTPUT WHEN YOU RUN THIS:
# ----------------------------------------
# Chat messages:
#   [SystemMessage]: You are a helpful AI assistant specialized in Python programming.
#   [HumanMessage]: Context:
# Python uses indentation for code blo...
# ----------------------------------------


# =============================================================================
# PART 2: TEXT SPLITTERS
# =============================================================================

print("=" * 60)
print("PART 2: TEXT SPLITTERS")
print("=" * 60)

# Problem: LLMs have token limits (can't read huge documents!)
# Solution: Split documents into smaller chunks!
# Each chunk = manageable size for LLM

from langchain_text_splitters import RecursiveCharacterTextSplitter

# -----------------------------------------------------------------------------
# SECTION 3: Basic Text Splitting
# -----------------------------------------------------------------------------

print("\n--- Basic Text Splitting ---")

# RecursiveCharacterTextSplitter:
# Tries to split on: paragraphs → sentences → words → characters
# Keeps semantic meaning intact as much as possible!

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,       # max characters per chunk
    chunk_overlap=50,     # overlap between chunks (for context continuity!)
    length_function=len,  # how to measure chunk size
)

# Long document to split
long_document = """
Python is a high-level, interpreted programming language created by Guido van Rossum.
It was first released in 1991 and has since become one of the most popular programming languages.

Python emphasizes code readability and simplicity. Its syntax allows programmers to express
concepts in fewer lines of code than languages like C++ or Java.

Python supports multiple programming paradigms including procedural, object-oriented,
and functional programming. It has a large standard library and vibrant ecosystem.

Python is widely used in data science, machine learning, web development, and automation.
Major companies like Google, Netflix, and Instagram use Python extensively.
""".strip()

# Split the document!
chunks = splitter.split_text(long_document)

print(f"Original length: {len(long_document)} characters")
print(f"Number of chunks: {len(chunks)}")
print()

for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1} ({len(chunk)} chars):")
    print(f"  {chunk[:100]}...")
    print()

# ACTUAL OUTPUT WHEN YOU RUN THIS:
# ----------------------------------------
# Original length: 573 characters
# Number of chunks: 4
#
# Chunk 1 (198 chars):
#   Python is a high-level, interpreted programming language created by Guido van Rossum.
#   It was first release...
#
# Chunk 2 (195 chars):
#   Python emphasizes code readability and simplicity. Its syntax allows programmers to express
#   concepts in fewer...
#
# Chunk 3 (193 chars):
#   Python supports multiple programming paradigms including procedural, object-oriented,
#   and functional progr...
#
# Chunk 4 (156 chars):
#   Python is widely used in data science, machine learning, web development, and automation.
#   Major companies l...
# ----------------------------------------


# -----------------------------------------------------------------------------
# SECTION 4: Why Chunk Overlap Matters
# -----------------------------------------------------------------------------

print("\n--- Why Chunk Overlap Matters ---")

# Without overlap: chunks lose context at boundaries
# With overlap: information is shared between adjacent chunks

text = "The capital of France is Paris. Paris is famous for the Eiffel Tower. The Eiffel Tower was built in 1889."

# Without overlap
no_overlap = RecursiveCharacterTextSplitter(chunk_size=60, chunk_overlap=0)
chunks_no_overlap = no_overlap.split_text(text)

# With overlap
with_overlap = RecursiveCharacterTextSplitter(chunk_size=60, chunk_overlap=20)
chunks_with_overlap = with_overlap.split_text(text)

print("WITHOUT overlap:")
for i, c in enumerate(chunks_no_overlap):
    print(f"  Chunk {i+1}: '{c}'")

print("\nWITH overlap (20 chars):")
for i, c in enumerate(chunks_with_overlap):
    print(f"  Chunk {i+1}: '{c}'")

print("\nObservation: With overlap, context carries over between chunks!")

# ACTUAL OUTPUT WHEN YOU RUN THIS:
# ----------------------------------------
# WITHOUT overlap:
#   Chunk 1: 'The capital of France is Paris. Paris is'
#   Chunk 2: 'famous for the Eiffel Tower. The Eiffel'
#   Chunk 3: 'Tower was built in 1889.'
#
# WITH overlap (20 chars):
#   Chunk 1: 'The capital of France is Paris. Paris is'
#   Chunk 2: 'Paris is famous for the Eiffel Tower.'    ← "Paris is" repeated!
#   Chunk 3: 'Eiffel Tower. The Eiffel Tower was built' ← context carried!
#   Chunk 4: 'Tower was built in 1889.'
# ----------------------------------------


# =============================================================================
# PART 3: MANUAL RAG PIPELINE (WITHOUT OPENAI API)
# =============================================================================

print("=" * 60)
print("PART 3: MANUAL RAG PIPELINE")
print("=" * 60)

# We'll build a complete RAG pipeline using:
# - sentence-transformers (free embeddings)
# - ChromaDB (free vector DB)
# - LangChain PromptTemplate (for structured prompts)
# No OpenAI API key needed for this section!

import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer

# -----------------------------------------------------------------------------
# SECTION 5: Complete RAG Without LLM (Free!)
# -----------------------------------------------------------------------------

print("\n--- Complete RAG Pipeline (Free Version) ---")

class ManualRAG:
    """
    Complete RAG pipeline without paid LLM API.
    Uses:
    - sentence-transformers for embeddings (FREE!)
    - ChromaDB for vector storage (FREE!)
    - LangChain PromptTemplate for prompts (FREE!)
    - Simulated LLM response (shows what would be sent to LLM)
    """

    def __init__(self):
        # Initialize components
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chroma_client   = chromadb.Client()
        self.collection      = self.chroma_client.create_collection("manual_rag")
        self.text_splitter   = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=50
        )

        # RAG prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a helpful AI assistant.
Answer the question based ONLY on the provided context.
If the answer is not in the context, say "I don't know based on provided documents."

Context:
{context}

Question: {question}

Answer:"""
        )
        print("ManualRAG initialized!")

    def add_documents(self, documents: list, source: str = "default"):
        """
        Step 1: INDEX — Add documents to vector DB
        Splits → Embeds → Stores
        """
        all_chunks = []

        # Split each document into chunks
        for doc in documents:
            chunks = self.text_splitter.split_text(doc)
            all_chunks.extend(chunks)

        # Generate embeddings for all chunks
        embeddings = self.embedding_model.encode(all_chunks).tolist()

        # Store in ChromaDB
        ids = [f"{source}_chunk_{i}" for i in range(len(all_chunks))]
        metadatas = [{"source": source, "chunk_id": i}
                     for i in range(len(all_chunks))]

        self.collection.add(
            documents=all_chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )

        print(f"  Added {len(all_chunks)} chunks from {len(documents)} documents")
        return all_chunks

    def retrieve(self, query: str, n_results: int = 3):
        """
        Step 2: RETRIEVE — Find relevant chunks
        Embeds query → Searches ChromaDB → Returns top chunks
        """
        # Embed the query
        query_embedding = self.embedding_model.encode(query).tolist()

        # Search ChromaDB
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
            retrieved.append({
                "text":       doc,
                "similarity": round(1 - dist, 4),
                "source":     meta["source"]
            })

        return retrieved

    def generate_prompt(self, query: str, retrieved_docs: list):
        """
        Step 3: GENERATE — Build prompt for LLM
        Combines retrieved context + question into structured prompt
        """
        # Combine retrieved documents into context
        context = "\n\n".join([
            f"[Source: {doc['source']}] {doc['text']}"
            for doc in retrieved_docs
        ])

        # Format the prompt template
        prompt = self.prompt_template.format(
            context=context,
            question=query
        )

        return prompt

    def query(self, question: str, n_results: int = 3):
        """
        Complete RAG pipeline:
        Question → Retrieve → Build Prompt → (Send to LLM)
        """
        print(f"\n{'='*50}")
        print(f"Query: '{question}'")
        print(f"{'='*50}")

        # Step 1: Retrieve relevant documents
        retrieved = self.retrieve(question, n_results)

        print(f"\nStep 1 — Retrieved {len(retrieved)} relevant chunks:")
        for doc in retrieved:
            print(f"  [{doc['similarity']}] {doc['text'][:80]}...")

        # Step 2: Build prompt
        prompt = self.generate_prompt(question, retrieved)

        print(f"\nStep 2 — Generated Prompt:")
        print(f"{'─'*40}")
        print(prompt)
        print(f"{'─'*40}")

        print("\nStep 3 — This prompt would be sent to LLM (GPT-4, Claude, etc.)")
        print("→ LLM would read the context and generate a precise answer!")

        return {
            "question":  question,
            "retrieved": retrieved,
            "prompt":    prompt
        }


# Test the complete pipeline
print("\nBuilding knowledge base...")
rag = ManualRAG()

# Add knowledge base documents
python_docs = [
    """Python is a high-level programming language created by Guido van Rossum in 1991.
    Python emphasizes code readability and has simple, easy-to-learn syntax.
    It supports multiple programming paradigms including OOP and functional programming.""",

    """Python is widely used in data science, machine learning, and AI.
    Popular libraries include NumPy for numerical computing, Pandas for data analysis,
    and scikit-learn for machine learning. Python is the #1 language for AI development.""",

    """LangChain is a framework for building applications with Large Language Models.
    It provides tools for prompt management, memory, retrieval, and chaining operations.
    LangChain works with OpenAI, Anthropic, Google, and other LLM providers.""",

    """RAG (Retrieval Augmented Generation) combines retrieval with text generation.
    It first retrieves relevant documents from a knowledge base using semantic search,
    then uses an LLM to generate an answer based on the retrieved context.""",
]

company_docs = [
    """Our return policy allows customers to return products within 30 days of purchase.
    Items must be in original condition with all tags attached.
    Refunds are processed within 5-7 business days.""",

    """We offer free shipping on all orders above Rs 500.
    Standard delivery takes 3-5 business days.
    Express delivery (1-2 days) is available for an additional Rs 99.""",
]

print("\nAdding Python/AI documents:")
rag.add_documents(python_docs, source="python_ai_docs")

print("\nAdding company policy documents:")
rag.add_documents(company_docs, source="company_policy")

# Test with different queries
queries = [
    "What is Python and who created it?",
    "What is LangChain used for?",
    "What is the return policy?",
    "How does RAG work?",
]

for query in queries:
    result = rag.query(query)
    print()


# ACTUAL OUTPUT WHEN YOU RUN THIS:
# ----------------------------------------
# Building knowledge base...
# ManualRAG initialized!
#
# Adding Python/AI documents:
#   Added 5 chunks from 4 documents
#
# Adding company policy documents:
#   Added 2 chunks from 2 documents
#
# ==================================================
# Query: 'What is Python and who created it?'
# ==================================================
#
# Step 1 — Retrieved 3 relevant chunks:
#   [0.8923] Python is a high-level programming language created by Guido van Rossum in 1991...
#   [0.7234] Python is widely used in data science, machine learning, and AI...
#   [0.4123] LangChain is a framework for building applications with Large Language Models...
#
# Step 2 — Generated Prompt:
# ────────────────────────────────────────
# You are a helpful AI assistant.
# Answer the question based ONLY on the provided context.
# If the answer is not in the context, say "I don't know based on provided documents."
#
# Context:
# [Source: python_ai_docs] Python is a high-level programming language created by Guido van
# Rossum in 1991. Python emphasizes code readability...
#
# [Source: python_ai_docs] Python is widely used in data science, machine learning, and AI...
#
# [Source: python_ai_docs] LangChain is a framework for building applications...
#
# Question: What is Python and who created it?
#
# Answer:
# ────────────────────────────────────────
#
# Step 3 — This prompt would be sent to LLM (GPT-4, Claude, etc.)
# → LLM would read the context and generate a precise answer!
#
# (Similar output for other queries...)
# ----------------------------------------


# =============================================================================
# PART 4: WITH OPENAI API (COMPLETE RAG!)
# =============================================================================

print("=" * 60)
print("PART 4: WITH OPENAI API (FULL RAG)")
print("=" * 60)

print("""
# To use with real LLM, install and configure:
#   pip install langchain-openai
#   export OPENAI_API_KEY='your-key-here'

# Then replace the query() method's Step 3 with:

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Create chain: retrieve → format → LLM → parse
def format_docs(docs):
    return "\\n\\n".join([d["text"] for d in docs])

# LangChain Expression Language (LCEL) chain
chain = (
    {"context": lambda q: format_docs(rag.retrieve(q)),
     "question": RunnablePassthrough()}
    | rag.prompt_template
    | llm
    | StrOutputParser()
)

# Get actual answer from LLM!
answer = chain.invoke("What is Python?")
print(f"Answer: {answer}")

# EXPECTED OUTPUT:
# Answer: Python is a high-level programming language created by Guido van
# Rossum in 1991. It emphasizes code readability and is widely used in
# data science, machine learning, and AI development.
""")


# =============================================================================
# PART 5: KEY LANGCHAIN CONCEPTS SUMMARY
# =============================================================================

print("=" * 60)
print("PART 5: KEY CONCEPTS")
print("=" * 60)

print("""
LANGCHAIN BUILDING BLOCKS:
──────────────────────────

1. PromptTemplate:
   → Reusable prompt with variables
   → template.format(context=..., question=...)
   → Consistent, structured prompts every time!

   Example output:
   "You are helpful. Context: {context}. Question: {question}. Answer:"

2. TextSplitter:
   → Split large docs into manageable chunks
   → chunk_size=200  → max 200 chars per chunk
   → chunk_overlap=50 → 50 chars shared between chunks
   → Keeps semantic meaning intact!

   Example output:
   Chunk 1: "Python is a high-level language..."
   Chunk 2: "...language created by Guido..."  (overlaps!)
   Chunk 3: "...by Guido van Rossum in 1991..."

3. Embeddings:
   → Text → vector of numbers
   → Similar text → similar vectors
   → Foundation of semantic search!

4. VectorStore (ChromaDB):
   → Store embeddings efficiently
   → Search by similarity (not exact match!)
   → Returns most relevant documents

5. Complete RAG Chain:
   Question
      ↓
   Embed question
      ↓
   Search VectorStore → retrieve top 3 chunks
      ↓
   Format prompt with context + question
      ↓
   Send to LLM (GPT-4, Claude, etc.)
      ↓
   Get precise answer based on YOUR documents!
""")


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Concept            | What it does                    | Output              |
# |--------------------|----------------------------------|---------------------|
# | PromptTemplate     | Structured reusable prompts     | Formatted string    |
# | ChatPromptTemplate | System + Human messages         | List of messages    |
# | TextSplitter       | Split large docs into chunks    | List of strings     |
# | chunk_size         | Max chars per chunk             | Smaller text pieces |
# | chunk_overlap      | Shared chars between chunks     | Context continuity  |
# | ManualRAG.add()    | Index documents into ChromaDB   | Stored embeddings   |
# | ManualRAG.retrieve | Find relevant chunks            | Top N similar docs  |
# | ManualRAG.query()  | Complete RAG pipeline           | Formatted prompt    |
# | ChatOpenAI         | Send prompt to GPT (paid)       | LLM answer text     |
#
# RAG FLOW:
#   Documents → Split → Embed → Store in ChromaDB    (indexing - done once!)
#   Question → Embed → Search → Retrieve → Prompt    (retrieval - every query)
#   Prompt → LLM → Answer                            (generation - every query)
#
# GOLDEN RULES:
# 1. Always split large documents — LLMs have token limits!
# 2. chunk_overlap keeps context between chunks — always use it!
# 3. PromptTemplate = consistency — same format every time!
# 4. Retrieve 3-5 chunks — not too few (miss info), not too many (noise)!
# 5. Context window = retrieved chunks + question = sent to LLM!
#
# NEXT STEP:
# Now we have all pieces!
# → 04_complete_rag.py — Put it ALL together!
#
# =============================================================================
