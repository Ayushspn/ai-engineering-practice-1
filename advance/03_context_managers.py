# =============================================================================
# 03_context_managers.py — Context Managers in Python
# python-ai-journey | 03_advanced
# =============================================================================
#
# THEORY:
# -------
# A context manager is an object that manages RESOURCES automatically.
# It guarantees:
#   1. SETUP   → resource is prepared before your code runs
#   2. USE     → your code runs with the resource
#   3. CLEANUP → resource is ALWAYS released — even if exception occurs!
#
# Use 'with' whenever you:
#   → open a file       (needs close)
#   → connect to DB     (needs disconnect)
#   → acquire a lock    (needs release)
#   → start a timer     (needs stop)
#   → create temp dir   (needs delete)
#
# Two ways to create context managers:
#   1. Class-based  → define __enter__ and __exit__
#   2. Function-based → use @contextmanager decorator with yield
#
# INTERNALS (CPython):
# ---------------------
# 'with X as y:' compiles to:
#   mgr = X                          # create context manager
#   y   = mgr.__enter__()            # setup — returns resource
#   try:
#       [your code]                  # use resource
#   except:
#       if not mgr.__exit__(*sys.exc_info()):
#           raise                    # re-raise if __exit__ returns False
#   else:
#       mgr.__exit__(None,None,None) # no exception — cleanup
#
# __exit__ arguments:
#   exc_type → exception class  (None if no exception)
#   exc_val  → exception value  (None if no exception)
#   exc_tb   → traceback object (None if no exception)
#   return False → let exception propagate
#   return True  → suppress exception (swallow it)
#
# =============================================================================

import time
import tempfile
import shutil
import json
import threading
from pathlib import Path
from contextlib import contextmanager, suppress


# =============================================================================
# PART 1: CLASS-BASED CONTEXT MANAGERS
# =============================================================================

print("=" * 60)
print("PART 1: CLASS-BASED CONTEXT MANAGERS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 1: Basic Context Manager — Understanding the Flow
# -----------------------------------------------------------------------------

print("\n--- Basic Context Manager ---")

# A class becomes a context manager by implementing:
#   __enter__ → setup code, returns resource
#   __exit__  → cleanup code, always runs

class ManagedResource:
    # __enter__ runs at START of 'with' block
    def __enter__(self):
        print("  1. __enter__: Setting up resource!")
        return self    # 'self' becomes 'r' in 'with X as r'
                       # you can return anything here:
                       # return self    → r = this object
                       # return file    → r = file object
                       # return conn    → r = db connection

    # __exit__ runs at END of 'with' block — ALWAYS!
    # receives info about any exception that occurred
    def __exit__(self,
                 exc_type,   # exception TYPE  e.g. ValueError — None if no error
                 exc_val,    # exception VALUE e.g. "bad input" — None if no error
                 exc_tb):    # traceback object                 — None if no error
        print("  3. __exit__: Cleaning up resource!")
        # return False → exception propagates normally ✅
        # return True  → exception is suppressed ⚠️
        return False


# Usage — 'with' activates the context manager
with ManagedResource() as r:
    # runs AFTER __enter__ completes
    print("  2. Inside with block: Using resource!")
    # when block ends → __exit__ called automatically!

# Output order:
# 1. __enter__: Setting up resource!
# 2. Inside with block: Using resource!
# 3. __exit__: Cleaning up resource!


# -----------------------------------------------------------------------------
# SECTION 2: Context Manager with Exception Handling
# -----------------------------------------------------------------------------

print("\n--- Exception Handling ---")

class SafeResource:
    def __enter__(self):
        print("  Setting up...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # no exception occurred — normal cleanup
            print("  No error — cleaning up normally!")
        else:
            # exception occurred — still clean up!
            print(f"  Error occurred: {exc_type.__name__}: {exc_val}")
            print("  Cleaning up after error!")
        return False    # False = let exception propagate to caller


# Case 1 — no exception
print("Case 1: No exception")
with SafeResource() as r:
    print("  Working normally...")
# __exit__ called with exc_type=None, exc_val=None, exc_tb=None

# Case 2 — exception occurs
print("\nCase 2: Exception occurs")
try:
    with SafeResource() as r:
        print("  Working...")
        raise ValueError("Something broke!")   # exception raised!
        print("  This never runs!")            # skipped!
    # __exit__ called with exc_type=ValueError, exc_val="Something broke!"
except ValueError as e:
    print(f"  Caller caught: {e}")             # exception propagated!


# -----------------------------------------------------------------------------
# SECTION 3: File Manager — Real World Example
# -----------------------------------------------------------------------------

print("\n--- File Manager ---")

class FileManager:
    # Constructor — stores filename and mode
    def __init__(self, filename, mode="r"):
        self.filename = filename    # file path to open
        self.mode     = mode        # r=read, w=write, a=append
        self.file     = None        # will hold file object after open

    def __enter__(self):
        print(f"  Opening {self.filename} in '{self.mode}' mode")
        # open() returns file object — store it AND return it
        self.file = open(self.filename, self.mode, encoding="utf-8")
        return self.file    # 'f' in 'with FileManager() as f' = this file!

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()    # ALWAYS close file — even if exception!
            print(f"  File {self.filename} closed!")
        if exc_type:
            # log the error but still let it propagate
            print(f"  Error while working with file: {exc_val}")
        return False    # don't suppress exceptions


# Create a temp file to demonstrate
tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt',
                                   delete=False, encoding='utf-8')
tmp.write("Hello from context manager!\nLine 2\nLine 3")
tmp_path = tmp.name
tmp.close()

# Read using our custom FileManager
with FileManager(tmp_path, "r") as f:
    content = f.read()
    print(f"  Content: {content[:30]}...")

# Write using our custom FileManager
with FileManager(tmp_path, "w") as f:
    f.write("New content written!\n")
    f.write("Line 2\n")

import os
os.unlink(tmp_path)    # cleanup temp file


# -----------------------------------------------------------------------------
# SECTION 4: Database Connection Manager
# -----------------------------------------------------------------------------

print("\n--- Database Connection Manager ---")

# Simulated database for demonstration
class SimulatedDB:
    """Simulates a database connection"""
    def __init__(self, name):
        self.name = name
        self.connected = False

    def connect(self):
        self.connected = True
        print(f"  Connected to {self.name}")

    def query(self, sql):
        if not self.connected:
            raise RuntimeError("Not connected!")
        print(f"  Executing: {sql}")
        return [{"id": 1, "name": "Ayush"}]

    def close(self):
        self.connected = False
        print(f"  Connection to {self.name} closed!")


class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name    # name of database to connect to
        self.db      = None       # will hold DB object after connect

    def __enter__(self):
        # create connection when entering 'with' block
        self.db = SimulatedDB(self.db_name)
        self.db.connect()
        return self.db    # return connection so caller can use it

    def __exit__(self, exc_type, exc_val, exc_tb):
        # ALWAYS close connection — even if query raised exception!
        if self.db:
            self.db.close()
        if exc_type:
            # log error, could also rollback transaction here
            print(f"  DB Error: {exc_val} — connection still closed!")
        return False    # let exception propagate


# Normal usage — connection always closed!
with DatabaseManager("users_db") as db:
    results = db.query("SELECT * FROM users")
    print(f"  Results: {results}")

# Exception case — connection STILL closed!
print()
try:
    with DatabaseManager("orders_db") as db:
        results = db.query("SELECT * FROM orders")
        raise RuntimeError("Processing failed!")    # simulate error
except RuntimeError as e:
    print(f"  Caught error: {e}")
    print("  But connection was still closed! ✅")


# =============================================================================
# PART 2: FUNCTION-BASED CONTEXT MANAGERS
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: FUNCTION-BASED (@contextmanager)")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 5: @contextmanager Decorator
# -----------------------------------------------------------------------------

print("\n--- @contextmanager ---")

# Alternative to class-based — simpler for straightforward cases!
# Uses a generator function with yield

# Everything BEFORE yield = __enter__ (setup)
# yield value             = what 'as' variable receives
# Everything AFTER yield  = __exit__ (cleanup)

@contextmanager
def managed_file(filepath, mode="r"):
    """Simple file context manager using @contextmanager"""
    print(f"  Opening {filepath}")
    f = open(filepath, mode, encoding="utf-8")  # setup
    try:
        yield f                # yield = give file to 'with' block
                               # everything pauses here until block ends!
    finally:
        f.close()              # cleanup — always runs (like __exit__)!
        print(f"  Closed {filepath}")


# Create temp file
tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt',
                                   delete=False, encoding='utf-8')
tmp.write("Hello from @contextmanager!")
tmp_path = tmp.name
tmp.close()

# Use our function-based context manager
with managed_file(tmp_path) as f:
    print(f"  Read: {f.read()}")

os.unlink(tmp_path)

# How @contextmanager works internally:
# 1. Calls the generator function → gets generator object
# 2. __enter__  → calls next(gen) → runs until yield → returns yielded value
# 3. __exit__   → calls next(gen) again → runs finally block → cleanup!


# -----------------------------------------------------------------------------
# SECTION 6: Timer Context Manager
# -----------------------------------------------------------------------------

print("\n--- Timer ---")

@contextmanager
def timer(label=""):
    """Measures execution time of a code block"""
    start = time.time()              # setup — record start time
    print(f"  ⏱ Timer started: {label}")
    try:
        yield                        # yield nothing — no 'as' variable needed
                                     # your code runs here
    finally:
        elapsed = time.time() - start  # cleanup — calculate elapsed time
        print(f"  ⏱ {label} took {elapsed:.4f}s")


# Measure any block of code!
with timer("List comprehension"):
    result = [x**2 for x in range(100_000)]

with timer("Generator expression"):
    result = sum(x**2 for x in range(100_000))

with timer("String join"):
    result = "".join(str(i) for i in range(10_000))


# -----------------------------------------------------------------------------
# SECTION 7: Temporary Directory
# -----------------------------------------------------------------------------

print("\n--- Temporary Directory ---")

@contextmanager
def temp_directory():
    """Creates temp dir, yields path, always deletes after!"""
    # setup — create temp directory
    tmp_dir = Path(tempfile.mkdtemp())
    print(f"  Created temp dir: {tmp_dir}")
    try:
        yield tmp_dir              # give path to 'with' block
    finally:
        # cleanup — ALWAYS delete temp dir and all contents!
        shutil.rmtree(tmp_dir)
        print(f"  Deleted temp dir: {tmp_dir}")


# Use temp directory safely
with temp_directory() as tmp:
    # create some files in temp dir
    (tmp / "model.txt").write_text("AI model data")
    (tmp / "config.json").write_text('{"version": "1.0"}')

    # list what we created
    files = list(tmp.iterdir())
    print(f"  Files created: {[f.name for f in files]}")
# temp dir ALWAYS deleted here — no disk clutter! ✅

# verify it's gone
print(f"  Temp dir exists after: {tmp.exists()}")   # False!


# =============================================================================
# PART 3: ADVANCED PATTERNS
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: ADVANCED PATTERNS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 8: Nested Context Managers
# -----------------------------------------------------------------------------

print("\n--- Nested Context Managers ---")

# Multiple context managers — two ways to nest them

# Way 1 — nested 'with' blocks
tmp1 = tempfile.NamedTemporaryFile(mode='w', suffix='.txt',
                                    delete=False, encoding='utf-8')
tmp1.write("file 1 content")
tmp1_path = tmp1.name
tmp1.close()

tmp2 = tempfile.NamedTemporaryFile(mode='w', suffix='.txt',
                                    delete=False, encoding='utf-8')
tmp2.write("file 2 content")
tmp2_path = tmp2.name
tmp2.close()

with open(tmp1_path, "r", encoding="utf-8") as f1:
    with open(tmp2_path, "r", encoding="utf-8") as f2:
        print(f"  f1: {f1.read()}")
        print(f"  f2: {f2.read()}")
# both files closed here!

# Way 2 — comma-separated (cleaner!)
with open(tmp1_path, "r", encoding="utf-8") as f1, \
     open(tmp2_path, "r", encoding="utf-8") as f2:
    print(f"\n  f1: {f1.read()}")
    print(f"  f2: {f2.read()}")
# both files closed here!

os.unlink(tmp1_path)
os.unlink(tmp2_path)


# -----------------------------------------------------------------------------
# SECTION 9: Suppressing Exceptions
# -----------------------------------------------------------------------------

print("\n--- Suppressing Exceptions ---")

# Sometimes you WANT to suppress specific exceptions
# Use contextlib.suppress or return True from __exit__

class SuppressError:
    """Context manager that suppresses specific exception types"""
    def __init__(self, *exception_types):
        # store which exception types to suppress
        self.exception_types = exception_types

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, self.exception_types):
            print(f"  Suppressed: {exc_type.__name__}: {exc_val}")
            return True     # True = SUPPRESS the exception! swallow it!
        return False        # False = let other exceptions propagate


# Suppress specific exceptions
with SuppressError(FileNotFoundError):
    open("nonexistent_file.txt")    # would normally crash!
print("  Continued after FileNotFoundError!")   # keeps running!

# Python's built-in suppress — same thing!
with suppress(FileNotFoundError):
    open("another_nonexistent.txt")
print("  Continued after suppress!")


# -----------------------------------------------------------------------------
# SECTION 10: Transaction Context Manager
# -----------------------------------------------------------------------------

print("\n--- Transaction Manager ---")

class Transaction:
    """
    Manages database transactions.
    Commits on success, rolls back on failure.
    This is critical for data consistency!
    """
    def __init__(self, db_name):
        self.db_name  = db_name
        self.operations = []    # track all operations

    def __enter__(self):
        print(f"  Transaction started on {self.db_name}")
        return self    # return self so caller can call .execute()

    def execute(self, operation):
        """Record an operation"""
        self.operations.append(operation)
        print(f"  Executed: {operation}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # no exception → commit all operations!
            print(f"  ✅ Committing {len(self.operations)} operations!")
            # in real DB: conn.commit()
        else:
            # exception → rollback everything!
            print(f"  ❌ Error: {exc_val}")
            print(f"  🔄 Rolling back {len(self.operations)} operations!")
            # in real DB: conn.rollback()
        return False    # always let exception propagate


# Success case — all operations commit
print("Case 1: All operations succeed")
with Transaction("orders_db") as tx:
    tx.execute("INSERT INTO orders VALUES (1, 'pizza')")
    tx.execute("UPDATE inventory SET stock = stock - 1")
    tx.execute("INSERT INTO payments VALUES (1, 500)")
# all three committed! ✅

# Failure case — all operations rollback
print("\nCase 2: Operation fails → rollback!")
try:
    with Transaction("orders_db") as tx:
        tx.execute("INSERT INTO orders VALUES (2, 'burger')")
        tx.execute("UPDATE inventory SET stock = stock - 1")
        raise RuntimeError("Payment gateway down!")   # simulate failure
        tx.execute("INSERT INTO payments VALUES (2, 300)")  # never runs
except RuntimeError:
    print("  All operations rolled back — data is consistent! ✅")


# =============================================================================
# PART 4: AI ENGINEERING USE CASES
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: AI ENGINEERING USE CASES")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 11: RAG Application Context Managers
# -----------------------------------------------------------------------------

print("\n--- RAG App Context Managers ---")

# These are the context managers you'll use in your RAG app!

@contextmanager
def vector_db_connection(collection_name):
    """
    Manages ChromaDB connection for RAG applications.
    Always closes connection — prevents connection leaks!
    """
    client = None
    try:
        # setup — simulate ChromaDB connection
        print(f"  Connecting to vector DB: {collection_name}")
        client = {"name": collection_name, "connected": True}
        yield client           # give connection to 'with' block
    except Exception as e:
        print(f"  Vector DB error: {e}")
        raise                  # re-raise — let caller handle it
    finally:
        # cleanup — ALWAYS disconnect!
        if client:
            client["connected"] = False
            print(f"  Disconnected from vector DB: {collection_name}")


@contextmanager
def llm_session(model_name, max_tokens=1000):
    """
    Manages LLM API session.
    Tracks token usage and ensures session cleanup.
    """
    session = {
        "model": model_name,
        "tokens_used": 0,
        "max_tokens": max_tokens
    }
    print(f"  LLM session started: {model_name}")
    try:
        yield session          # give session to 'with' block
    finally:
        # cleanup — log usage, close session
        print(f"  LLM session ended. Tokens used: {session['tokens_used']}")


@contextmanager
def model_inference():
    """
    Manages PyTorch/TensorFlow inference context.
    Disables gradient calculation for faster inference.
    Similar to torch.no_grad()
    """
    print("  Inference mode: ON (gradients disabled)")
    try:
        yield              # model inference runs here
    finally:
        print("  Inference mode: OFF")


# Simulate RAG pipeline using context managers
print("RAG Pipeline:")

with vector_db_connection("documents") as db:
    # search for relevant documents
    query = "What is machine learning?"
    print(f"  Searching for: '{query}'")
    results = [{"doc": "ML is...", "score": 0.95}]  # simulated results

    with llm_session("gpt-4", max_tokens=500) as session:
        # generate answer using retrieved docs
        context = " ".join(r["doc"] for r in results)
        prompt  = f"Context: {context}\nQuestion: {query}"

        with model_inference():
            # generate response
            response = f"Based on context: {context}"
            session["tokens_used"] = 150    # simulate token usage

        print(f"  Response: {response[:50]}...")

# All connections closed, sessions ended, resources freed! ✅


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Concept              | Key Insight                                       |
# |----------------------|---------------------------------------------------|
# | __enter__            | Setup — runs at START of 'with' block            |
# | __exit__             | Cleanup — ALWAYS runs at END — even on exception |
# | return self          | 'as' variable = whatever __enter__ returns        |
# | exc_type/val/tb      | Exception info passed to __exit__ (None if none) |
# | return False         | Let exception propagate — use this by default    |
# | return True          | Suppress exception — use rarely!                 |
# | @contextmanager      | Simpler way — yield splits enter/exit            |
# | before yield         | = __enter__ (setup)                              |
# | yield value          | = what 'as' variable receives                    |
# | after yield (finally)| = __exit__ (cleanup)                             |
# | nested 'with'        | Use comma syntax: with A() as a, B() as b:      |
# | suppress()           | contextlib.suppress — swallow specific errors    |
#
# WHEN TO USE 'with':
#   ✅ File operations    (read, write, append — all need close!)
#   ✅ DB connections     (always need disconnect!)
#   ✅ API sessions       (always need cleanup!)
#   ✅ Locks              (always need release!)
#   ✅ Timers             (always need stop!)
#   ✅ Temp directories   (always need delete!)
#   ✅ Vector DBs (RAG)   (always need disconnect!)
#   ❌ Simple math        (no resource, no cleanup needed)
#   ❌ Variable creation  (no resource, no cleanup needed)
#
# GOLDEN RULES:
# 1. If it needs cleanup → use 'with'!
# 2. __exit__ ALWAYS runs — even if exception occurs
# 3. return False in __exit__ → exception propagates (default!)
# 4. return True in __exit__ → exception suppressed (use rarely!)
# 5. @contextmanager is simpler for straightforward cases
# 6. always put cleanup in 'finally' inside @contextmanager
# 7. Nest context managers with comma syntax for cleaner code
#
# =============================================================================
