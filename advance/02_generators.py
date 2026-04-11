# =============================================================================
# 02_generators.py — Generators in Python (Deep Dive)
# python-ai-journey | 03_advanced
# =============================================================================
#
# THEORY:
# -------
# A generator is a special function that:
#   1. Uses 'yield' instead of 'return'
#   2. Returns a generator OBJECT when called
#   3. Produces values ONE AT A TIME — lazily
#   4. Remembers its state between calls
#
# Key concepts:
#   1. Generator function    — yield keyword
#   2. Generator expression  — (x for x in ...)
#   3. next()                — get next value
#   4. send()                — send value INTO generator
#   5. throw()               — inject exception into generator
#   6. close()               — stop generator early
#   7. yield from            — delegate to sub-generator
#   8. Infinite generators   — endless sequences
#   9. Generator pipelines   — chain generators together
#
# INTERNALS (CPython):
# ---------------------
# When Python sees 'yield' in a function:
#   → marks it as generator function (CO_GENERATOR flag in code object)
#   → calling it creates PyGenObject (NOT executing the body!)
#
# PyGenObject contains:
#   - gi_frame    → PyFrameObject (suspended execution frame)
#   - gi_code     → code object (bytecode)
#   - gi_running  → bool (is it currently executing?)
#
# PyFrameObject contains:
#   - f_lasti     → last bytecode instruction index (resume point!)
#   - f_locals    → local variables dict
#   - f_stacktop  → value stack pointer
#
# When next() is called:
#   1. Resume PyFrameObject from f_lasti
#   2. Execute until YIELD_VALUE bytecode
#   3. Save frame state (f_lasti, f_locals)
#   4. Return yielded value to caller
#   5. Frame suspended — waiting for next next() call
#
# When StopIteration raised:
#   → generator exhausted → frame destroyed
#
# =============================================================================

import sys
import time


# =============================================================================
# PART 1: GENERATOR BASICS
# =============================================================================

print("=" * 60)
print("PART 1: GENERATOR BASICS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 1: Normal Function vs Generator Function
# -----------------------------------------------------------------------------

print("\n--- Normal vs Generator ---")

# Normal function — returns ALL values at once
def get_numbers_normal():
    print("  Normal: building list...")
    return [1, 2, 3, 4, 5]

# Generator function — yields ONE value at a time
def get_numbers_gen():
    print("  Gen: starting...")
    yield 1
    print("  Gen: after 1")
    yield 2
    print("  Gen: after 2")
    yield 3
    print("  Gen: after 3")

# Normal function — executes immediately, returns list
print("Calling normal function:")
result = get_numbers_normal()
print(f"  type: {type(result)}")
print(f"  value: {result}")

# Generator function — does NOT execute body! Returns generator object
print("\nCalling generator function:")
gen = get_numbers_gen()
print(f"  type: {type(gen)}")
print(f"  value: {gen}")
print("  Body hasn't run yet!")

# Body runs on next() calls
print("\nCalling next():")
print(f"  next(): {next(gen)}")   # runs until first yield
print(f"  next(): {next(gen)}")   # resumes from after first yield
print(f"  next(): {next(gen)}")   # resumes from after second yield

try:
    print(f"  next(): {next(gen)}")   # no more yields!
except StopIteration:
    print("  StopIteration! Generator exhausted!")


# -----------------------------------------------------------------------------
# SECTION 2: Generator Memory Advantage
# -----------------------------------------------------------------------------

print("\n--- Memory Advantage ---")

# Normal function — loads ALL into memory
def squares_list(n):
    return [x**2 for x in range(n)]

# Generator — produces one at a time
def squares_gen(n):
    for x in range(n):
        yield x**2

n = 1_000_000

# Memory comparison
list_result = squares_list(n)
gen_result  = squares_gen(n)

print(f"List size:      {sys.getsizeof(list_result):,} bytes")
print(f"Generator size: {sys.getsizeof(gen_result)} bytes")
print(f"Generator uses constant memory regardless of n!")

# Cleanup
del list_result


# -----------------------------------------------------------------------------
# SECTION 3: Generator Expressions
# -----------------------------------------------------------------------------

print("\n--- Generator Expressions ---")

# List comprehension — builds everything NOW
lst = [x**2 for x in range(10)]

# Generator expression — lazy, builds one at a time
gen = (x**2 for x in range(10))

print(f"List:      {lst}")
print(f"Generator: {gen}")
print(f"List size: {sys.getsizeof(lst)} bytes")
print(f"Gen size:  {sys.getsizeof(gen)} bytes")

# Generator exhaustion — can only iterate ONCE!
gen = (x**2 for x in range(5))
first  = list(gen)   # consumes generator
second = list(gen)   # empty — already exhausted!
print(f"\nFirst iteration:  {first}")
print(f"Second iteration: {second}")   # [] — exhausted!


# =============================================================================
# PART 2: ADVANCED GENERATOR FEATURES
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: ADVANCED FEATURES")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 4: send() — Two-Way Communication
# -----------------------------------------------------------------------------

print("\n--- send() ---")

# yield can RECEIVE values too!
# Use send() to push values INTO the generator

def accumulator():
    """Generator that accumulates sent values"""
    total = 0
    while True:
        value = yield total      # yield sends total OUT, receives value IN
        if value is None:
            break
        total += value
        print(f"  Received: {value}, Total: {total}")

gen = accumulator()
next(gen)               # must call next() first to start generator!
                        # advances to first yield

gen.send(10)            # sends 10 into generator → value = 10
gen.send(20)            # sends 20 into generator → value = 20
gen.send(30)            # sends 30 into generator → value = 30
final = gen.send(None)  # sends None → breaks loop
print(f"  Final total: {final}")

# Practical use — coroutine pattern
def running_average():
    """Calculates running average of sent values"""
    count = 0
    total = 0
    average = 0
    while True:
        value = yield average
        if value is None:
            break
        count += 1
        total += value
        average = total / count

avg = running_average()
next(avg)                           # prime the generator

for num in [10, 20, 30, 40, 50]:
    result = avg.send(num)
    print(f"  Sent {num}, average = {result:.1f}")


# -----------------------------------------------------------------------------
# SECTION 5: throw() — Inject Exceptions
# -----------------------------------------------------------------------------

print("\n--- throw() ---")

def safe_generator():
    """Generator that handles injected exceptions"""
    try:
        while True:
            try:
                value = yield
                print(f"  Processing: {value}")
            except ValueError as e:
                print(f"  Caught ValueError: {e} — continuing...")
    except GeneratorExit:
        print("  Generator closing — cleanup!")

gen = safe_generator()
next(gen)                                    # prime

gen.send("valid data")                       # normal send
gen.throw(ValueError, "bad value!")          # inject exception!
gen.send("more valid data")                  # continues after exception!
gen.close()                                  # close generator


# -----------------------------------------------------------------------------
# SECTION 6: close() — Stop Generator Early
# -----------------------------------------------------------------------------

print("\n--- close() ---")

def countdown(n):
    """Countdown generator with cleanup"""
    print(f"  Starting countdown from {n}")
    try:
        while n > 0:
            yield n
            n -= 1
    finally:
        print(f"  Cleanup! Countdown stopped at {n}")   # always runs!

gen = countdown(10)
print(f"  {next(gen)}")   # 10
print(f"  {next(gen)}")   # 9
print(f"  {next(gen)}")   # 8
gen.close()               # stop early — triggers finally!


# -----------------------------------------------------------------------------
# SECTION 7: yield from — Delegation
# -----------------------------------------------------------------------------

print("\n--- yield from ---")

# Without yield from — manual delegation
def chain_manual(*iterables):
    for it in iterables:
        for item in it:
            yield item

# With yield from — cleaner!
def chain_yield_from(*iterables):
    for it in iterables:
        yield from it       # delegates to sub-iterator!

result1 = list(chain_manual([1,2], [3,4], [5,6]))
result2 = list(chain_yield_from([1,2], [3,4], [5,6]))
print(f"Manual:     {result1}")
print(f"yield from: {result2}")

# yield from with generator
def inner():
    yield 1
    yield 2
    yield 3

def outer():
    print("  Outer: before inner")
    yield from inner()          # delegates to inner generator!
    print("  Outer: after inner")
    yield 4
    yield 5

print(f"\nyield from generator:")
for val in outer():
    print(f"  got: {val}")

# yield from passes send() and throw() through to inner!
def sub_gen():
    value = yield "ready"
    yield f"received: {value}"

def main_gen():
    result = yield from sub_gen()   # transparent delegation!

gen = main_gen()
print(f"\n{next(gen)}")             # "ready"
print(f"{gen.send('hello')}")       # "received: hello"


# =============================================================================
# PART 3: PRACTICAL PATTERNS
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: PRACTICAL PATTERNS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 8: Infinite Generators
# -----------------------------------------------------------------------------

print("\n--- Infinite Generators ---")

# Infinite counter
def counter(start=0, step=1):
    n = start
    while True:
        yield n
        n += step

# Take first n items from infinite generator
def take(n, iterable):
    for i, item in enumerate(iterable):
        if i >= n:
            break
        yield item

# Use infinite generators safely with take()
evens    = counter(0, 2)          # 0, 2, 4, 6, 8...
odds     = counter(1, 2)          # 1, 3, 5, 7, 9...
fibs     = (lambda: (
    lambda f: (f.__setattr__('a', 0) or f.__setattr__('b', 1) or f)
)(type('F', (), {'__call__': lambda self: (
    setattr(self, 'a', self.b) or
    setattr(self, 'b', self.a + self.b) or
    self.a
)})()))()

print(f"First 5 evens: {list(take(5, counter(0, 2)))}")
print(f"First 5 odds:  {list(take(5, counter(1, 2)))}")

# Fibonacci generator
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

print(f"First 10 fibs: {list(take(10, fibonacci()))}")


# -----------------------------------------------------------------------------
# SECTION 9: Generator Pipelines
# -----------------------------------------------------------------------------

print("\n--- Generator Pipelines ---")

# Each generator does ONE thing — chain them together!

def read_numbers(n):
    """Source — generates numbers"""
    for i in range(n):
        yield i

def filter_even(numbers):
    """Filter — keeps only even numbers"""
    for n in numbers:
        if n % 2 == 0:
            yield n

def square(numbers):
    """Transform — squares each number"""
    for n in numbers:
        yield n ** 2

def limit(numbers, max_count):
    """Limit — takes only first n items"""
    count = 0
    for n in numbers:
        if count >= max_count:
            break
        yield n
        count += 1

# Build pipeline — nothing runs until iteration!
numbers  = read_numbers(100)      # lazy
evens    = filter_even(numbers)   # lazy
squared  = square(evens)          # lazy
limited  = limit(squared, 5)      # lazy

print("Pipeline: numbers → filter even → square → limit 5")
print(f"Result: {list(limited)}")

# Real world pipeline — process log file
def read_lines(lines):
    """Simulate reading file lines"""
    yield from lines

def filter_errors(lines):
    """Keep only ERROR lines"""
    for line in lines:
        if "ERROR" in line:
            yield line

def parse_message(lines):
    """Extract message from log line"""
    for line in lines:
        parts = line.split(": ", 1)
        yield parts[1] if len(parts) > 1 else line

def uppercase(messages):
    """Transform to uppercase"""
    for msg in messages:
        yield msg.upper().strip()

# Sample log data
log_data = [
    "2024-01-01 INFO: Server started",
    "2024-01-01 ERROR: Database connection failed",
    "2024-01-01 INFO: User logged in",
    "2024-01-01 ERROR: Payment processing failed",
    "2024-01-01 INFO: Request processed",
    "2024-01-01 ERROR: API timeout",
]

# Chain pipeline
pipeline = uppercase(
    parse_message(
        filter_errors(
            read_lines(log_data)
        )
    )
)

print(f"\nError messages from log:")
for msg in pipeline:
    print(f"  → {msg}")


# -----------------------------------------------------------------------------
# SECTION 10: Generator Performance
# -----------------------------------------------------------------------------

print("\n--- Performance Comparison ---")

n = 1_000_000

# List approach — builds everything first
start = time.time()
total = sum([x**2 for x in range(n)])
list_time = time.time() - start

# Generator approach — streams values
start = time.time()
total = sum(x**2 for x in range(n))    # no [] = generator!
gen_time = time.time() - start

print(f"List comprehension: {list_time:.4f}s")
print(f"Generator expr:     {gen_time:.4f}s")
print(f"Generator uses ~0 extra memory vs O(n) for list!")


# =============================================================================
# PART 4: INTERNALS
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: CPYTHON INTERNALS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 11: Generator Object Internals
# -----------------------------------------------------------------------------

print("\n--- Generator Internals ---")

def simple_gen():
    yield 1
    yield 2
    yield 3

gen = simple_gen()

# Inspect generator object
print(f"Type:          {type(gen)}")
print(f"Name:          {gen.__name__}")
print(f"Qualified name:{gen.__qualname__}")
print(f"Code object:   {gen.gi_code}")
print(f"Frame:         {gen.gi_frame}")
print(f"Running:       {gen.gi_running}")

# Frame contains execution state
frame = gen.gi_frame
print(f"\nFrame info:")
print(f"  f_lineno:  {frame.f_lineno}")       # current line
print(f"  f_locals:  {frame.f_locals}")        # local variables
print(f"  f_lasti:   {frame.f_lasti}")         # last instruction index

# After first next() — frame state changes
next(gen)
print(f"\nAfter first next():")
print(f"  f_lineno:  {gen.gi_frame.f_lineno}") # moved to next line!
print(f"  f_lasti:   {gen.gi_frame.f_lasti}")  # instruction pointer moved!

# After exhaustion — frame is None
list(gen)   # exhaust generator
print(f"\nAfter exhaustion:")
print(f"  gi_frame: {gen.gi_frame}")            # None — frame destroyed!


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Concept           | Key Insight                                          |
# |-------------------|------------------------------------------------------|
# | Generator function| Has yield → returns PyGenObject, body doesn't run   |
# | next()            | Runs until next yield → suspends → returns value    |
# | send(value)       | Resumes generator AND sends value in via yield       |
# | throw(exc)        | Injects exception at yield point                    |
# | close()           | Raises GeneratorExit → triggers finally cleanup     |
# | yield from        | Delegates to sub-generator → transparent passthrough|
# | Generator expr    | (x for x) → lazy, constant memory, one-pass only   |
# | Infinite gen      | while True: yield → use take() to limit             |
# | Pipeline          | Chain generators → each does one thing → lazy!     |
# | PyGenObject       | gi_frame (state), gi_code (bytecode), gi_running    |
# | gi_frame          | None when exhausted — frame destroyed               |
#
# GOLDEN RULES:
# 1. Generator body runs on first next() — NOT on function call!
# 2. Generators are exhausted after one pass — cannot reuse!
# 3. Use yield from for clean sub-generator delegation
# 4. Always prime coroutines with next() before send()
# 5. finally in generator runs when close() called
# 6. Generator pipelines are memory efficient — lazy evaluation
# 7. sum(x for x in range(n)) — no [] needed inside sum()!
#
# =============================================================================
