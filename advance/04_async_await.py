# =============================================================================
# 04_async_await.py — Async/Await in Python
# python-ai-journey | 03_advanced
# =============================================================================
#
# THEORY:
# -------
# Async/await allows Python to handle multiple I/O operations
# concurrently WITHOUT using multiple threads or processes.
#
# Key idea:
#   Instead of BLOCKING (waiting) for I/O to complete,
#   Python can PAUSE a task and work on others while waiting!
#
# Key concepts:
#   1. Coroutine      — async def function
#   2. await          — pause here, let others run
#   3. Event loop     — manager that schedules coroutines
#   4. asyncio.gather — run multiple coroutines concurrently
#   5. Task           — coroutine scheduled on event loop
#   6. async with     — async context manager
#   7. async for      — async iteration
#
# WHEN TO USE ASYNC:
#   ✅ Network requests (APIs, web scraping)
#   ✅ Database queries
#   ✅ File I/O (large files)
#   ✅ Multiple API calls (OpenAI, etc.)
#   ❌ CPU-heavy work (use multiprocessing instead!)
#   ❌ Simple scripts (overkill!)
#
# INTERNALS (CPython):
# ---------------------
# Event Loop — the heart of async Python:
#   - Single thread that manages all coroutines
#   - Maintains a queue of ready-to-run coroutines
#   - When coroutine hits 'await' → suspends it
#   - Picks next ready coroutine → runs it
#   - I/O completes → resumes suspended coroutine
#
# Coroutine is a generator under the hood:
#   - 'await' compiles to 'yield from'
#   - Event loop calls next() on coroutines
#   - Suspension/resumption via PyFrameObject (same as generators!)
#
# =============================================================================

import asyncio
import time


# =============================================================================
# PART 1: COROUTINE BASICS
# =============================================================================

print("=" * 60)
print("PART 1: COROUTINE BASICS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 1: Normal Function vs Coroutine
# -----------------------------------------------------------------------------

print("\n--- Normal vs Coroutine ---")

# Normal function — runs synchronously
def greet_sync(name):
    print(f"  Hello {name}!")
    return f"Done: {name}"

# Coroutine — defined with 'async def'
async def greet_async(name):
    print(f"  Hello {name}!")
    return f"Done: {name}"

# Normal function — runs immediately when called
result = greet_sync("Ayush")
print(f"  sync result: {result}")

# Coroutine — calling it does NOT run the body!
# Returns a coroutine OBJECT (like generator!)
coro = greet_async("Ayush")
print(f"  coro type: {type(coro)}")    # <class 'coroutine'>
print(f"  coro: {coro}")               # coroutine object — not run yet!

# Must run coroutine on event loop!
result = asyncio.run(greet_async("Ayush"))
print(f"  async result: {result}")

# Close the coroutine object to avoid warning
coro.close()


# -----------------------------------------------------------------------------
# SECTION 2: await — Pause and Resume
# -----------------------------------------------------------------------------

print("\n--- await ---")

async def fetch_data(name, delay):
    """Simulates fetching data from API with delay"""
    print(f"  [{name}] Starting fetch...")
    await asyncio.sleep(delay)    # pause here! let others run!
                                   # asyncio.sleep = async version of time.sleep
    print(f"  [{name}] Done after {delay}s!")
    return f"{name}: data"

# Run single coroutine
async def main_single():
    result = await fetch_data("User API", 0.1)
    print(f"  Result: {result}")

asyncio.run(main_single())


# -----------------------------------------------------------------------------
# SECTION 3: Sequential vs Concurrent
# -----------------------------------------------------------------------------

print("\n--- Sequential vs Concurrent ---")

async def task(name, delay):
    """Simulates an async task"""
    await asyncio.sleep(delay)
    return f"{name} done!"

# Sequential — one at a time (slow!)
async def sequential():
    start = time.time()

    # await each one — waits for each before starting next!
    r1 = await task("Task1", 0.1)
    r2 = await task("Task2", 0.1)
    r3 = await task("Task3", 0.1)

    elapsed = time.time() - start
    print(f"  Sequential: {elapsed:.2f}s — {[r1, r2, r3]}")

# Concurrent — all at same time (fast!)
async def concurrent():
    start = time.time()

    # gather runs ALL at same time!
    results = await asyncio.gather(
        task("Task1", 0.1),
        task("Task2", 0.1),
        task("Task3", 0.1),
    )

    elapsed = time.time() - start
    print(f"  Concurrent: {elapsed:.2f}s — {results}")

asyncio.run(sequential())
asyncio.run(concurrent())
# Sequential ≈ 0.30s (3 × 0.1s)
# Concurrent ≈ 0.10s (all run at same time!)


# =============================================================================
# PART 2: CORE ASYNC PATTERNS
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: CORE ASYNC PATTERNS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 4: asyncio.gather — Run Multiple Concurrently
# -----------------------------------------------------------------------------

print("\n--- asyncio.gather ---")

async def fetch_user(user_id):
    """Simulate fetching user from API"""
    await asyncio.sleep(0.05)    # simulate network delay
    return {"id": user_id, "name": f"User_{user_id}"}

async def fetch_all_users():
    """Fetch 10 users concurrently"""
    start = time.time()

    # Create all tasks
    tasks = [fetch_user(i) for i in range(10)]

    # Run ALL concurrently!
    users = await asyncio.gather(*tasks)

    elapsed = time.time() - start
    print(f"  Fetched {len(users)} users in {elapsed:.2f}s")
    print(f"  First user: {users[0]}")
    print(f"  Last user:  {users[-1]}")
    return users

asyncio.run(fetch_all_users())


# -----------------------------------------------------------------------------
# SECTION 5: asyncio.create_task — Background Tasks
# -----------------------------------------------------------------------------

print("\n--- asyncio.create_task ---")

async def background_task(name, delay):
    """Task that runs in background"""
    print(f"  [{name}] Started")
    await asyncio.sleep(delay)
    print(f"  [{name}] Completed after {delay}s")
    return f"{name} result"

async def main_with_tasks():
    """Run tasks in background while doing other work"""
    # create_task schedules coroutine immediately
    # but doesn't wait for it yet!
    task1 = asyncio.create_task(background_task("Download", 0.2))
    task2 = asyncio.create_task(background_task("Upload", 0.1))

    print("  Tasks created — doing other work!")
    await asyncio.sleep(0.05)    # simulate other work
    print("  Other work done!")

    # NOW wait for tasks to complete
    result1 = await task1
    result2 = await task2
    print(f"  Task1: {result1}")
    print(f"  Task2: {result2}")

asyncio.run(main_with_tasks())


# -----------------------------------------------------------------------------
# SECTION 6: Error Handling in Async
# -----------------------------------------------------------------------------

print("\n--- Error Handling ---")

async def risky_task(name, should_fail=False):
    """Task that might fail"""
    await asyncio.sleep(0.05)
    if should_fail:
        raise ValueError(f"{name} failed!")
    return f"{name} success!"

# Handle errors in gather
async def gather_with_errors():
    try:
        # return_exceptions=True → errors returned as results
        # not return_exceptions → first error cancels all!
        results = await asyncio.gather(
            risky_task("Task1"),
            risky_task("Task2", should_fail=True),  # this fails!
            risky_task("Task3"),
            return_exceptions=True    # don't raise — return exception as result
        )
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"  Task{i+1} failed: {result}")
            else:
                print(f"  Task{i+1} succeeded: {result}")
    except Exception as e:
        print(f"  Unexpected error: {e}")

asyncio.run(gather_with_errors())


# -----------------------------------------------------------------------------
# SECTION 7: Async Context Manager
# -----------------------------------------------------------------------------

print("\n--- Async Context Manager ---")

class AsyncDatabaseConnection:
    """
    Async context manager for database connections.
    Uses __aenter__ and __aexit__ instead of __enter__/__exit__
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.connected = False

    async def __aenter__(self):
        # async setup — can await here!
        await asyncio.sleep(0.01)    # simulate async connection
        self.connected = True
        print(f"  Connected to {self.db_name}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # async cleanup — can await here!
        await asyncio.sleep(0.01)    # simulate async disconnect
        self.connected = False
        print(f"  Disconnected from {self.db_name}")
        if exc_type:
            print(f"  Error: {exc_val}")
        return False

    async def query(self, sql):
        """Async query"""
        await asyncio.sleep(0.01)    # simulate query time
        return [{"result": f"data from {self.db_name}"}]


async def use_async_db():
    # 'async with' for async context managers!
    async with AsyncDatabaseConnection("users_db") as db:
        results = await db.query("SELECT * FROM users")
        print(f"  Query results: {results}")
    # disconnected automatically!

asyncio.run(use_async_db())


# -----------------------------------------------------------------------------
# SECTION 8: Async Generator and async for
# -----------------------------------------------------------------------------

print("\n--- Async Generator ---")

async def async_range(n, delay=0.01):
    """Async generator — yields values with async delay"""
    for i in range(n):
        await asyncio.sleep(delay)    # async operation between yields
        yield i                        # yield value

async def use_async_generator():
    # 'async for' to iterate async generator!
    results = []
    async for num in async_range(5, delay=0.01):
        results.append(num)
    print(f"  Async generator results: {results}")

asyncio.run(use_async_generator())


# =============================================================================
# PART 3: REAL WORLD PATTERNS
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: REAL WORLD PATTERNS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 9: Rate Limited API Calls
# -----------------------------------------------------------------------------

print("\n--- Rate Limited API Calls ---")

async def call_api(endpoint, semaphore):
    """
    Simulate API call with rate limiting.
    Semaphore limits concurrent calls — prevents overwhelming API!
    """
    async with semaphore:    # only N calls at a time!
        await asyncio.sleep(0.05)    # simulate API call
        return f"Response from {endpoint}"

async def fetch_with_rate_limit():
    # Semaphore — limits to 3 concurrent calls at a time!
    # Like a traffic light — only 3 cars can go at once!
    semaphore = asyncio.Semaphore(3)

    endpoints = [f"/api/users/{i}" for i in range(10)]
    tasks = [call_api(ep, semaphore) for ep in endpoints]

    start = time.time()
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start

    print(f"  Fetched {len(results)} endpoints in {elapsed:.2f}s")
    print(f"  Max 3 concurrent — rate limited! ✅")

asyncio.run(fetch_with_rate_limit())


# -----------------------------------------------------------------------------
# SECTION 10: Async Pipeline — For RAG App!
# -----------------------------------------------------------------------------

print("\n--- Async Pipeline (RAG Pattern) ---")

async def embed_text(text):
    """Simulate generating embeddings (OpenAI API call)"""
    await asyncio.sleep(0.05)    # simulate API delay
    return f"embedding_of_{text[:10]}"

async def search_vector_db(embedding):
    """Simulate searching vector DB (ChromaDB)"""
    await asyncio.sleep(0.03)    # simulate DB query
    return [f"doc1_for_{embedding}", f"doc2_for_{embedding}"]

async def generate_response(query, docs):
    """Simulate LLM response generation"""
    await asyncio.sleep(0.1)    # simulate LLM delay
    context = " ".join(docs)
    return f"Answer to '{query}' based on: {context[:30]}..."

async def rag_pipeline(queries):
    """
    Complete RAG pipeline — processes multiple queries concurrently!
    
    For each query:
    1. Generate embedding (async API call)
    2. Search vector DB (async DB query)  
    3. Generate response (async LLM call)
    """
    async def process_query(query):
        # Step 1 — embed query
        embedding = await embed_text(query)

        # Step 2 — search vector DB
        docs = await search_vector_db(embedding)

        # Step 3 — generate response
        response = await generate_response(query, docs)

        return {"query": query, "response": response}

    # Process ALL queries concurrently!
    start = time.time()
    results = await asyncio.gather(
        *[process_query(q) for q in queries]
    )
    elapsed = time.time() - start

    print(f"  Processed {len(queries)} queries in {elapsed:.2f}s")
    for r in results:
        print(f"  Q: {r['query'][:30]}")
        print(f"  A: {r['response'][:50]}")
        print()

    return results

queries = [
    "What is machine learning?",
    "How does RAG work?",
    "What is LangChain?",
]

asyncio.run(rag_pipeline(queries))


# -----------------------------------------------------------------------------
# SECTION 11: Timeout Handling
# -----------------------------------------------------------------------------

print("\n--- Timeout Handling ---")

async def slow_api_call(delay):
    """Simulates slow API call"""
    await asyncio.sleep(delay)
    return "Finally got response!"

async def with_timeout():
    # asyncio.wait_for — cancel if takes too long!
    try:
        result = await asyncio.wait_for(
            slow_api_call(2.0),    # takes 2 seconds
            timeout=0.5            # but we only wait 0.5 seconds!
        )
        print(f"  Result: {result}")
    except asyncio.TimeoutError:
        print("  ⏱ Request timed out! Moving on...")

asyncio.run(with_timeout())


# =============================================================================
# PART 4: SYNC VS ASYNC COMPARISON
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: SYNC VS ASYNC COMPARISON")
print("=" * 60)

print("""
SYNCHRONOUS (Normal Python):
─────────────────────────────
Task1 ████████░░░░░░░░░░░░░░░░   wait   → done
Task2           ████████░░░░░   wait   → done
Task3                   ████████░░░░░  → done
Time: 3 units

ASYNCHRONOUS (async/await):
────────────────────────────
Task1 ████░░░░░░░░░░░░░░░░░░░ → done (resumed when response arrived)
Task2 ████░░░░░░░░░░░░░░░░░░░ → done (ran while Task1 was waiting!)
Task3 ████░░░░░░░░░░░░░░░░░░░ → done (ran while Task1,2 were waiting!)
Time: 1 unit ← ALL ran concurrently!

USE ASYNC WHEN:
  ✅ Making multiple API calls (OpenAI, etc.)
  ✅ Querying multiple databases
  ✅ Building web servers (FastAPI!)
  ✅ RAG pipelines with multiple LLM calls
  
DON'T USE ASYNC WHEN:
  ❌ CPU-heavy work (use multiprocessing!)
  ❌ Simple scripts
  ❌ Single API call (overkill!)
""")


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Concept            | Key Insight                                         |
# |--------------------|-----------------------------------------------------|
# | async def          | Defines coroutine — body doesn't run on call!      |
# | await              | Pause here, let event loop run other coroutines     |
# | asyncio.run()      | Entry point — runs coroutine on event loop          |
# | asyncio.gather()   | Run multiple coroutines CONCURRENTLY               |
# | asyncio.sleep()    | Async sleep — doesn't block event loop!             |
# | create_task()      | Schedule coroutine — starts immediately             |
# | Semaphore          | Limit concurrent operations — rate limiting         |
# | async with         | Async context manager — uses __aenter__/__aexit__  |
# | async for          | Iterate async generator                             |
# | wait_for()         | Add timeout to any coroutine                        |
# | return_exceptions  | gather() — return errors as results not raise      |
#
# GOLDEN RULES:
# 1. async def → coroutine, calling returns object not result!
# 2. Must use 'await' to actually get the result!
# 3. Use asyncio.gather() for concurrent execution
# 4. Use Semaphore to rate limit concurrent calls
# 5. async with/for for async context managers/generators
# 6. asyncio.run() is the entry point — call once at top level
# 7. Don't mix sync blocking calls inside async functions!
#
# =============================================================================
