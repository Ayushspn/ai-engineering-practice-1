# =============================================================================
# 03_comprehensions.py — Comprehensions and Generators in Python
# python-ai-journey | 02_intermediate
# =============================================================================
#
# THEORY:
# -------
# Comprehensions are concise, readable ways to build collections.
# Python has 4 types:
#   1. List comprehension   → [expr for x in iterable if condition]
#   2. Dict comprehension   → {k: v for x in iterable if condition}
#   3. Set comprehension    → {expr for x in iterable if condition}
#   4. Generator expression → (expr for x in iterable if condition)
#
# GENERATOR vs COMPREHENSION:
#   - List comprehension → evaluates ALL at once → stores in memory
#   - Generator expression → evaluates LAZILY → one value at a time
#   - Generator is memory efficient for large/infinite sequences
#   - Generator can only be iterated ONCE — then exhausted
#
# INTERNALS (CPython):
# ---------------------
# List comprehension:
#   - Compiled to a nested function with its own scope
#   - Executes immediately, returns fully built list
#   - Faster than equivalent for loop + append()
#   - Uses LIST_APPEND bytecode instruction internally
#
# Generator expression:
#   - Compiled to a generator object (PyGenObject)
#   - Contains a code object + frame that resumes on each next() call
#   - Uses 'yield' internally — suspends and resumes execution
#   - Constant memory regardless of sequence size
#   - StopIteration raised when exhausted
#
# Generator function (with yield):
#   - Function that contains 'yield' becomes a generator factory
#   - Calling it returns a generator object — does NOT execute body
#   - Each next() call runs until next yield, then suspends
#   - Frame state (local variables, instruction pointer) is preserved
#
# =============================================================================

import sys
import time


# =============================================================================
# PART 1: COMPREHENSIONS
# =============================================================================

print("=" * 60)
print("PART 1: COMPREHENSIONS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 1: List Comprehensions
# -----------------------------------------------------------------------------

print("\n--- List Comprehensions ---")

# Basic — transform every element
squares = [x**2 for x in range(1, 6)]
print(f"Squares:          {squares}")

# With condition — filter elements
evens = [x for x in range(20) if x % 2 == 0]
print(f"Evens:            {evens}")

# Transform + filter together
even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
print(f"Even squares:     {even_squares}")

# String operations
words = ["hello", "world", "python", "ai", "code"]
upper_long = [w.upper() for w in words if len(w) > 4]
print(f"Upper long words: {upper_long}")

# Conditional expression inside comprehension
scores = [45, 82, 91, 38, 76, 55, 67]
labels = ["pass" if s >= 60 else "fail" for s in scores]
print(f"Labels:           {labels}")

# Nested comprehension — flatten 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat   = [num for row in matrix for num in row]
print(f"Flattened:        {flat}")

# Nested comprehension — build 2D matrix
grid = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print(f"Grid:")
for row in grid:
    print(f"  {row}")


# -----------------------------------------------------------------------------
# SECTION 2: Dict Comprehensions
# -----------------------------------------------------------------------------

print("\n--- Dict Comprehensions ---")

# Basic — build dict from sequence
squares_dict = {x: x**2 for x in range(1, 6)}
print(f"Squares dict: {squares_dict}")

# Transform keys and values
words = ["apple", "banana", "cherry"]
lengths = {word: len(word) for word in words}
print(f"Lengths:      {lengths}")

# Filter — only include entries matching condition
scores = {"Ayush": 95, "Rahul": 72, "Priya": 88, "Kiran": 65}
passed = {name: score for name, score in scores.items() if score >= 75}
print(f"Passed:       {passed}")

# Invert a dict — swap keys and values
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
print(f"Inverted:     {inverted}")

# Combine two lists into dict
keys   = ["name", "age", "city"]
values = ["Ayush", 30, "Bangalore"]
combined = {k: v for k, v in zip(keys, values)}
print(f"Combined:     {combined}")


# -----------------------------------------------------------------------------
# SECTION 3: Set Comprehensions
# -----------------------------------------------------------------------------

print("\n--- Set Comprehensions ---")

# Unique squares
unique_squares = {x**2 for x in range(-5, 6)}
print(f"Unique squares: {sorted(unique_squares)}")   # sorted for display

# Unique lengths
words = ["apple", "banana", "kiwi", "pear", "mango", "plum"]
unique_lengths = {len(w) for w in words}
print(f"Unique lengths: {unique_lengths}")

# Filter unique chars from string
chars = {c.lower() for c in "Hello World" if c != " "}
print(f"Unique chars:   {sorted(chars)}")


# -----------------------------------------------------------------------------
# SECTION 4: Comprehension Performance vs Loop
# -----------------------------------------------------------------------------

print("\n--- Comprehension Performance ---")

n = 100_000

# Loop + append
start = time.time()
result = []
for i in range(n):
    if i % 2 == 0:
        result.append(i**2)
loop_time = time.time() - start

# List comprehension
start = time.time()
result = [i**2 for i in range(n) if i % 2 == 0]
comp_time = time.time() - start

print(f"Loop time:         {loop_time:.4f}s")
print(f"Comprehension:     {comp_time:.4f}s")
print(f"Comprehension is faster — uses LIST_APPEND bytecode directly!")


# =============================================================================
# PART 2: GENERATORS
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: GENERATORS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 5: Generator Expressions
# -----------------------------------------------------------------------------

print("\n--- Generator Expressions ---")

# List comprehension — builds everything NOW
lst = [x**2 for x in range(10)]
gen = (x**2 for x in range(10))   # lazy — nothing computed yet!

print(f"List type:  {type(lst)}")   # list
print(f"Gen type:   {type(gen)}")   # generator

# Memory comparison
lst_mem = sys.getsizeof([x**2 for x in range(10000)])
gen_mem = sys.getsizeof(x**2 for x in range(10000))
print(f"\nList (10000 items): {lst_mem:,} bytes")
print(f"Generator:          {gen_mem} bytes — constant regardless of size!")

# Generator produces values one at a time via next()
gen = (x**2 for x in range(5))
print(f"\nManual iteration:")
print(f"  next(): {next(gen)}")   # 0
print(f"  next(): {next(gen)}")   # 1
print(f"  next(): {next(gen)}")   # 4
print(f"  next(): {next(gen)}")   # 9
print(f"  next(): {next(gen)}")   # 16

try:
    print(f"  next(): {next(gen)}")   # StopIteration!
except StopIteration:
    print("  StopIteration — generator exhausted!")

# Generator is EXHAUSTED after one pass
gen = (x for x in range(5))
first_pass  = list(gen)
second_pass = list(gen)    # empty — already exhausted!
print(f"\nFirst pass:  {first_pass}")
print(f"Second pass: {second_pass}")   # []


# -----------------------------------------------------------------------------
# SECTION 6: Generator Functions — yield
# -----------------------------------------------------------------------------

print("\n--- Generator Functions (yield) ---")

# A function with 'yield' becomes a GENERATOR FACTORY
def count_up(start, stop):
    print(f"  [generator] starting from {start}")
    current = start
    while current <= stop:
        print(f"  [generator] yielding {current}")
        yield current          # suspend here, return value to caller
        current += 1           # resumes here on next next() call
    print(f"  [generator] done!")

# Calling the function does NOT execute the body — returns generator object
gen = count_up(1, 3)
print(f"type: {type(gen)}")    # generator — body not run yet!

print("\nIterating:")
for val in gen:                # each iteration calls next() internally
    print(f"  caller got: {val}")


# -----------------------------------------------------------------------------
# SECTION 7: yield — How it Works Internally
# -----------------------------------------------------------------------------

print("\n--- yield Internals ---")

def simple_gen():
    print("  Step 1")
    yield 10           # suspend, return 10
    print("  Step 2")
    yield 20           # suspend, return 20
    print("  Step 3")
    yield 30           # suspend, return 30
    print("  Step 4 — done")

gen = simple_gen()

print("Calling next() manually:")
print(f"  Got: {next(gen)}")    # runs until first yield
print(f"  Got: {next(gen)}")    # resumes from step 2
print(f"  Got: {next(gen)}")    # resumes from step 3
# next call would raise StopIteration


# -----------------------------------------------------------------------------
# SECTION 8: Practical Generator Patterns
# -----------------------------------------------------------------------------

print("\n--- Practical Generator Patterns ---")

# PATTERN 1: Infinite sequence — impossible with list!
def infinite_counter(start=0):
    n = start
    while True:
        yield n
        n += 1

counter = infinite_counter(1)
first_5 = [next(counter) for _ in range(5)]
print(f"First 5 from infinite: {first_5}")

# PATTERN 2: Read large file line by line — memory efficient
def read_lines(filename):
    """Generator that reads file line by line — never loads whole file"""
    try:
        with open(filename, 'r') as f:
            for line in f:
                yield line.strip()
    except FileNotFoundError:
        yield from []   # empty if file not found

# Simulate with list
def simulate_large_data(n):
    """Simulates reading n rows of data lazily"""
    for i in range(n):
        yield {"id": i, "value": i * 2}

# Process 1M rows without loading all into memory!
total = sum(row["value"] for row in simulate_large_data(1_000_000))
print(f"\nSum of 1M rows (generator): {total}")

# PATTERN 3: Pipeline — chain generators together
def integers(n):
    yield from range(n)

def squared(nums):
    for n in nums:
        yield n ** 2

def even_only(nums):
    for n in nums:
        if n % 2 == 0:
            yield n

# Chain: integers → squared → even_only
pipeline = even_only(squared(integers(10)))
result = list(pipeline)
print(f"\nPipeline result: {result}")

# PATTERN 4: yield from — delegate to sub-generator
def chain(*iterables):
    for it in iterables:
        yield from it          # yield each element from sub-iterable

result = list(chain([1, 2], [3, 4], [5, 6]))
print(f"chain result: {result}")


# -----------------------------------------------------------------------------
# SECTION 9: Generator vs List — When to Use Which
# -----------------------------------------------------------------------------

print("\n--- Generator vs List: When to Use ---")

# Use LIST when:
# - Need to access elements multiple times
# - Need indexing (result[3])
# - Need len()
# - Small data that fits in memory

lst = [x**2 for x in range(10)]
print(f"List — random access: lst[5] = {lst[5]}")   # O(1) indexing
print(f"List — length: len={len(lst)}")
print(f"List — reusable: {lst}")

# Use GENERATOR when:
# - Iterating only once
# - Large or infinite sequences
# - Memory is a concern
# - Building pipelines

gen = (x**2 for x in range(10))
print(f"\nGenerator — no indexing: next={next(gen)}")  # must use next()
# print(len(gen))     # TypeError — no len on generator
# print(gen[5])       # TypeError — no indexing on generator

# Performance for sum — generator wins on memory
n = 1_000_000

start = time.time()
total_list = sum([x**2 for x in range(n)])   # builds full list first
list_time = time.time() - start

start = time.time()
total_gen = sum(x**2 for x in range(n))      # streams values one at a time
gen_time = time.time() - start

print(f"\nsum() with list ({n}):      {list_time:.4f}s")
print(f"sum() with generator ({n}): {gen_time:.4f}s")
print(f"Generator uses constant memory vs O(n) for list!")


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Type          | Syntax    | Memory  | Reusable | Indexing | Speed    |
# |---------------|-----------|---------|----------|----------|----------|
# | List comp     | [x for x] | O(n)    | ✅ Yes   | ✅ Yes   | Fast     |
# | Dict comp     | {k:v ...} | O(n)    | ✅ Yes   | ✅ Yes   | Fast     |
# | Set comp      | {x for x} | O(n)    | ✅ Yes   | ❌ No    | Fast     |
# | Generator exp | (x for x) | O(1)    | ❌ Once  | ❌ No    | Lazy     |
# | Generator fn  | yield     | O(1)    | ❌ Once  | ❌ No    | Lazy     |
#
# HOW yield WORKS:
#   1. First next() → runs until yield → suspends → returns value
#   2. Next next()  → resumes from after yield → runs until next yield
#   3. No more yields → raises StopIteration → for loop ends
#
# GOLDEN RULES:
# 1. Use list comp for small data you need multiple times
# 2. Use generator for large/infinite data you iterate once
# 3. sum(x**2 for x in range(n)) — no [] needed inside sum()!
# 4. Generator functions don't execute on call — only on next()
# 5. yield from delegates to sub-generator — cleaner than nested loops
# 6. Generators are the foundation of async/await in Python
#
# =============================================================================
