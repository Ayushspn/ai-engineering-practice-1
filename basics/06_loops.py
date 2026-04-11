# =============================================================================
# 06_loops.py — Loops in Python
# python-ai-journey | 01_basics
# =============================================================================
#
# THEORY:
# -------
# Python has two loop types:
#   1. for   — iterates over any ITERABLE object
#   2. while — repeats as long as a condition is True
#
# Key concepts:
#   1. Iterable   — any object that implements __iter__()
#   2. Iterator   — object that implements __next__()
#   3. range()    — lazy sequence generator (not a list!)
#   4. break      — exit loop immediately
#   5. continue   — skip to next iteration
#   6. else       — runs when loop completes without break
#   7. enumerate  — loop with index
#   8. zip        — loop over multiple iterables together
#
# INTERNALS (CPython):
# ---------------------
# 'for x in obj:' internally does:
#   1. Calls iter(obj)    → obj.__iter__()  → returns an iterator
#   2. Repeatedly calls next(iterator)     → iterator.__next__()
#   3. When StopIteration is raised → loop ends
#
# range() is a lazy object — does NOT create a list in memory.
# It generates each number on demand → memory efficient for large ranges.
#
# while loop checks condition before each iteration.
# The condition calls bool() on the expression — same truthiness rules.
#
# =============================================================================


# -----------------------------------------------------------------------------
# SECTION 1: for Loop Basics
# -----------------------------------------------------------------------------

print("=" * 60)
print("SECTION 1: for Loop Basics")
print("=" * 60)

# Loop over range
print("range(5):")
for i in range(5):
    print(f"  {i}", end=" ")
print()

# range(start, stop, step)
print("\nrange(1, 10, 2):")
for i in range(1, 10, 2):      # 1,3,5,7,9
    print(f"  {i}", end=" ")
print()

# Countdown with negative step
print("\nrange(5, 0, -1):")
for i in range(5, 0, -1):      # 5,4,3,2,1
    print(f"  {i}", end=" ")
print()

# Loop over list
fruits = ["apple", "banana", "cherry"]
print("\nLooping over list:")
for fruit in fruits:
    print(f"  {fruit}")

# Loop over string — string is iterable!
print("\nLooping over string:")
for char in "Python":
    print(f"  {char}", end=" ")
print()

# Loop over dict — iterates over KEYS by default
person = {"name": "Ayush", "age": 30, "city": "Bangalore"}
print("\nLooping over dict (keys):")
for key in person:
    print(f"  {key}: {person[key]}")

# Loop over dict items — key-value pairs
print("\nLooping over dict.items():")
for key, value in person.items():
    print(f"  {key} → {value}")


# -----------------------------------------------------------------------------
# SECTION 2: range() Internals
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 2: range() Internals")
print("=" * 60)

# range() is LAZY — does not create a list in memory!
r = range(1_000_000)
print(f"type(range(5)):          {type(r)}")
print(f"range object (not list): {r}")
print(f"Memory of range(1M):     {r.__sizeof__()} bytes")   # tiny!

import sys
big_list  = list(range(1_000_000))
big_range = range(1_000_000)
print(f"Memory of list(1M):      {sys.getsizeof(big_list):,} bytes")
print(f"Memory of range(1M):     {sys.getsizeof(big_range)} bytes")
print("range() uses constant memory regardless of size!")

# range supports indexing and slicing
r = range(10)
print(f"\nrange(10)[3]    = {r[3]}")      # 3
print(f"range(10)[-1]   = {r[-1]}")      # 9
print(f"range(10)[2:5]  = {r[2:5]}")     # range(2, 5)
print(f"5 in range(10)  = {5 in r}")     # True — O(1) check!
print(f"11 in range(10) = {11 in r}")    # False


# -----------------------------------------------------------------------------
# SECTION 3: while Loop
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 3: while Loop")
print("=" * 60)

# Basic while
x = 0
print("Counting up:")
while x < 5:
    print(f"  x = {x}")
    x += 1

# while with user-like input simulation
print("\nRetry simulation:")
attempts = 0
max_attempts = 3
success = False

while attempts < max_attempts:
    attempts += 1
    print(f"  Attempt {attempts}...")
    if attempts == 2:       # simulate success on 2nd try
        success = True
        break

if success:
    print("  Connected!")
else:
    print("  Failed after all attempts")

# Infinite loop with break
print("\nInfinite loop with break:")
count = 0
while True:                 # condition is always True
    count += 1
    if count >= 3:
        break               # exit when condition met
print(f"  Broke out after count = {count}")


# -----------------------------------------------------------------------------
# SECTION 4: break, continue, else
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 4: break, continue, else")
print("=" * 60)

# break — exit loop immediately
print("break example:")
for i in range(10):
    if i == 5:
        print(f"  Breaking at i={i}")
        break
    print(f"  i = {i}")

# continue — skip current iteration, continue to next
print("\ncontinue example (skip even):")
for i in range(10):
    if i % 2 == 0:
        continue            # skip even numbers
    print(f"  i = {i}", end=" ")
print()

# else — runs ONLY if loop completed without break
# This is unique to Python — no other language has loop else!
print("\nelse on for loop (no break):")
for i in range(5):
    if i == 10:             # never true
        break
else:
    print("  Loop completed without break → else runs")

print("\nelse on for loop (with break):")
for i in range(5):
    if i == 3:
        print(f"  Breaking at i={i}")
        break
else:
    print("  This will NOT print — break was hit")

# Practical use of loop else — search pattern
print("\nSearch with loop else:")
items = [1, 4, 7, 2, 9, 3]
target = 7

for item in items:
    if item == target:
        print(f"  Found {target}!")
        break
else:
    print(f"  {target} not found in list")


# -----------------------------------------------------------------------------
# SECTION 5: enumerate() and zip()
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 5: enumerate() and zip()")
print("=" * 60)

fruits = ["apple", "banana", "cherry"]

# enumerate — loop with index
print("enumerate():")
for index, fruit in enumerate(fruits):
    print(f"  {index}: {fruit}")

# enumerate with custom start
print("\nenumerate(start=1):")
for index, fruit in enumerate(fruits, start=1):
    print(f"  {index}. {fruit}")

# zip — loop over multiple iterables together
names  = ["Ayush", "Rahul", "Priya"]
scores = [95, 87, 92]
grades = ["A", "B", "A"]

print("\nzip():")
for name, score, grade in zip(names, scores, grades):
    print(f"  {name}: {score} ({grade})")

# zip stops at shortest iterable
long_list  = [1, 2, 3, 4, 5]
short_list = ["a", "b", "c"]
print("\nzip with unequal lengths:")
for a, b in zip(long_list, short_list):
    print(f"  {a}, {b}", end="  ")
print("← stops at shortest!")

# zip to create dict
keys   = ["name", "age", "city"]
values = ["Ayush", 30, "Bangalore"]
d = dict(zip(keys, values))
print(f"\ndict from zip: {d}")


# -----------------------------------------------------------------------------
# SECTION 6: Nested Loops
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 6: Nested Loops")
print("=" * 60)

# Multiplication table
print("3x3 Multiplication table:")
for i in range(1, 4):
    for j in range(1, 4):
        print(f"  {i}x{j}={i*j}", end="  ")
    print()

# break in nested loop — only breaks INNER loop
print("\nbreak in nested loop:")
for i in range(3):
    for j in range(3):
        if j == 1:
            break           # only breaks inner loop
        print(f"  i={i}, j={j}")


# -----------------------------------------------------------------------------
# SECTION 7: List Comprehensions — Pythonic Loops
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 7: List Comprehensions")
print("=" * 60)

# Traditional loop
squares_loop = []
for i in range(1, 6):
    squares_loop.append(i ** 2)
print(f"Loop:          {squares_loop}")

# List comprehension — same thing, one line
squares_comp = [i ** 2 for i in range(1, 6)]
print(f"Comprehension: {squares_comp}")

# With condition
evens = [i for i in range(20) if i % 2 == 0]
print(f"\nEven numbers: {evens}")

# Nested comprehension — flatten 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat   = [num for row in matrix for num in row]
print(f"\nFlattened matrix: {flat}")

# Dict comprehension
squared_dict = {i: i**2 for i in range(1, 6)}
print(f"\nSquared dict: {squared_dict}")

# Set comprehension
unique_lengths = {len(fruit) for fruit in ["apple", "banana", "kiwi", "pear", "plum"]}
print(f"Unique lengths: {unique_lengths}")


# -----------------------------------------------------------------------------
# SECTION 8: for Loop Internals — Iterator Protocol
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 8: Iterator Protocol (Internals)")
print("=" * 60)

# What Python does internally when you write 'for x in obj:'
my_list = [10, 20, 30]

# Step 1: get iterator
iterator = iter(my_list)         # calls my_list.__iter__()
print(f"iterator: {iterator}")

# Step 2: repeatedly call next()
print(f"next(): {next(iterator)}")    # 10
print(f"next(): {next(iterator)}")    # 20
print(f"next(): {next(iterator)}")    # 30

# Step 3: StopIteration ends the loop
try:
    print(f"next(): {next(iterator)}")
except StopIteration:
    print("StopIteration raised → loop ends")

# This is exactly what 'for' does internally!
# for x in my_list:  ≡  while True: try: x = next(iter) except StopIteration: break

# Strings, dicts, sets, range — all implement __iter__()
print(f"\niter('abc'):      {iter('abc')}")
print(f"iter([1,2,3]):    {iter([1,2,3])}")
print(f"iter(range(5)):   {iter(range(5))}")


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Concept        | Key Insight                                             |
# |----------------|---------------------------------------------------------|
# | for loop       | Iterates over any iterable — list, str, dict, range    |
# | while loop     | Repeats until condition is False — for unknown counts   |
# | range()        | Lazy — constant memory regardless of size               |
# | break          | Exit loop immediately                                   |
# | continue       | Skip to next iteration                                  |
# | else           | Runs ONLY if loop completes without break               |
# | enumerate()    | Loop with index — prefer over range(len(x))            |
# | zip()          | Loop multiple iterables together — stops at shortest   |
# | Comprehension  | Pythonic one-line loop — faster than append loop       |
# | __iter__       | Any object with __iter__ and __next__ is iterable      |
#
# GOLDEN RULES:
# 1. Use 'for' for sequences, 'while' for conditions
# 2. range() is lazy — never do list(range(1M)) unless needed
# 3. Use enumerate() not range(len(x)) for indexed loops
# 4. List comprehensions are faster than append() loops
# 5. Loop 'else' runs only when no break occurred — useful for search
# 6. 'for' internally uses __iter__ and __next__ — everything is protocol
#
# =============================================================================
