# =============================================================================
# 01_lists.py — Lists in Python (Deep Dive)
# python-ai-journey | 02_intermediate
# =============================================================================
#
# THEORY:
# -------
# A list is a MUTABLE, ORDERED sequence of objects.
# Lists can hold any mix of types — ints, strings, other lists, functions.
#
# Key concepts:
#   1. Mutability        — modify in place, same object in memory
#   2. Dynamic resizing  — list grows/shrinks automatically
#   3. Shallow copy      — copies outer list only, inner objects shared
#   4. Deep copy         — copies everything recursively
#   5. List methods      — append, insert, remove, pop, sort, reverse
#   6. Comprehensions    — Pythonic one-line list building
#   7. Sorting           — sorted() vs .sort(), key parameter
#   8. Performance       — O(1) vs O(n) operations
#
# INTERNALS (CPython):
# ---------------------
# A list is stored as PyListObject — a C struct containing:
#   - ob_refcnt    : reference count
#   - ob_type      : &PyList_Type
#   - ob_size      : current number of elements
#   - ob_item      : pointer to array of PyObject* pointers
#   - allocated    : total allocated slots (>= ob_size)
#
# Lists use DYNAMIC ARRAY with OVER-ALLOCATION:
#   - When list is full, CPython allocates MORE space than needed
#   - Growth pattern: 0→4→8→16→25→35→46... (roughly 1.125x each time)
#   - This amortizes the cost of resizing — append() is O(1) amortized
#
# COMPLEXITY TABLE:
#   append()     O(1) amortized  — add to end
#   pop()        O(1)            — remove from end
#   insert(i)    O(n)            — shift elements right
#   remove(x)    O(n)            — search then shift
#   index(x)     O(n)            — linear search
#   x in list    O(n)            — linear search
#   len()        O(1)            — stored in ob_size
#   sort()       O(n log n)      — Timsort algorithm
#   reverse()    O(n)            — in-place reversal
#   slice        O(k)            — k = slice size
#
# =============================================================================

import copy
import sys
import time


# -----------------------------------------------------------------------------
# SECTION 1: Creating Lists
# -----------------------------------------------------------------------------

print("=" * 60)
print("SECTION 1: Creating Lists")
print("=" * 60)

# Different ways to create lists
empty       = []
numbers     = [1, 2, 3, 4, 5]
mixed       = [1, "hello", 3.14, True, None]    # any types!
nested      = [[1, 2], [3, 4], [5, 6]]
from_range  = list(range(1, 6))
from_string = list("Python")                    # ['P','y','t','h','o','n']

print(f"empty:       {empty}")
print(f"numbers:     {numbers}")
print(f"mixed:       {mixed}")
print(f"nested:      {nested}")
print(f"from range:  {from_range}")
print(f"from string: {from_string}")

# List constructor from any iterable
from_tuple = list((1, 2, 3))
from_set   = list({3, 1, 2})       # order not guaranteed!
print(f"\nfrom tuple: {from_tuple}")
print(f"from set:   {from_set}")


# -----------------------------------------------------------------------------
# SECTION 2: Indexing and Slicing
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 2: Indexing and Slicing")
print("=" * 60)

fruits = ["apple", "banana", "cherry", "mango", "orange"]
#          0        1         2         3        4       forward
#         -5       -4        -3        -2       -1       backward

print(f"fruits[0]    = {fruits[0]}")      # apple
print(f"fruits[-1]   = {fruits[-1]}")     # orange
print(f"fruits[1:3]  = {fruits[1:3]}")    # ['banana', 'cherry']
print(f"fruits[:3]   = {fruits[:3]}")     # first 3
print(f"fruits[2:]   = {fruits[2:]}")     # from index 2 to end
print(f"fruits[::2]  = {fruits[::2]}")    # every 2nd
print(f"fruits[::-1] = {fruits[::-1]}")   # reversed

# Slice assignment — replace a range of elements
nums = [1, 2, 3, 4, 5]
nums[1:3] = [20, 30]       # replace index 1 and 2
print(f"\nAfter slice assignment: {nums}")   # [1, 20, 30, 4, 5]

nums[1:3] = [200, 300, 400]  # can insert more than replaced
print(f"After wider replacement: {nums}")   # [1, 200, 300, 400, 4, 5]


# -----------------------------------------------------------------------------
# SECTION 3: List Methods
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 3: List Methods")
print("=" * 60)

items = [3, 1, 4, 1, 5, 9, 2, 6]

# Adding elements
items.append(7)               # add to END — O(1)
print(f"append(7):        {items}")

items.insert(0, 99)           # insert at index — O(n)
print(f"insert(0, 99):    {items}")

items.extend([10, 11])        # add multiple — O(k)
print(f"extend([10,11]):  {items}")

# Removing elements
items.pop()                   # remove LAST — O(1)
print(f"pop():            {items}")

items.pop(0)                  # remove at index — O(n)
print(f"pop(0):           {items}")

items.remove(1)               # remove FIRST occurrence of value — O(n)
print(f"remove(1):        {items}")

# Searching
nums = [3, 1, 4, 1, 5, 9, 2, 6, 1]
print(f"\nindex(1):         {nums.index(1)}")    # first occurrence index
print(f"count(1):         {nums.count(1)}")     # count occurrences
print(f"1 in nums:        {1 in nums}")          # membership — O(n)

# Sorting
nums_copy = nums.copy()
nums_copy.sort()                                 # in-place sort — modifies list
print(f"\nsort():           {nums_copy}")

sorted_nums = sorted(nums)                       # returns NEW list
print(f"sorted():         {sorted_nums}")
print(f"original nums:    {nums}")               # unchanged!

nums_copy.sort(reverse=True)                     # descending
print(f"sort(reverse):    {nums_copy}")

# Reversing
nums_copy.reverse()                              # in-place reverse — O(n)
print(f"reverse():        {nums_copy}")

# Other methods
print(f"\nlen():            {len(nums)}")
nums_copy.clear()                                # remove all elements
print(f"clear():          {nums_copy}")          # []


# -----------------------------------------------------------------------------
# SECTION 4: Shallow vs Deep Copy
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 4: Shallow vs Deep Copy")
print("=" * 60)

# Assignment — same object, no copy
a = [1, 2, 3]
b = a
b.append(99)
print(f"Assignment: a={a}, b={b}")    # both changed!
print(f"a is b: {a is b}")           # True — same object

# Shallow copy — new outer list, shared inner objects
a = [[1, 2], [3, 4]]
b = a.copy()         # shallow copy
c = a[:]             # also shallow copy

print(f"\nShallow copy:")
print(f"a is b:    {a is b}")        # False — different outer lists
print(f"a[0] is b[0]: {a[0] is b[0]}")  # True — shared inner list!

b[0].append(99)      # mutates SHARED inner list
print(f"After b[0].append(99):")
print(f"  a = {a}")  # [[1, 2, 99], [3, 4]] ← affected!
print(f"  b = {b}")  # [[1, 2, 99], [3, 4]]

# Deep copy — fully independent at all levels
a = [[1, 2], [3, 4]]
b = copy.deepcopy(a)

print(f"\nDeep copy:")
print(f"a is b:       {a is b}")         # False
print(f"a[0] is b[0]: {a[0] is b[0]}")  # False — independent inner list!

b[0].append(99)
print(f"After b[0].append(99):")
print(f"  a = {a}")   # [[1, 2], [3, 4]] ← untouched!
print(f"  b = {b}")   # [[1, 2, 99], [3, 4]]


# -----------------------------------------------------------------------------
# SECTION 5: List Comprehensions
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 5: List Comprehensions")
print("=" * 60)

# Basic comprehension
squares = [x ** 2 for x in range(1, 6)]
print(f"Squares:          {squares}")

# With condition
evens = [x for x in range(20) if x % 2 == 0]
print(f"Evens:            {evens}")

# Transform and filter
words = ["hello", "world", "python", "ai", "code"]
long_upper = [w.upper() for w in words if len(w) > 4]
print(f"Long uppercase:   {long_upper}")

# Nested comprehension — flatten 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(f"Flattened:        {flat}")

# Conditional expression in comprehension
scores = [45, 82, 91, 38, 76, 55, 67]
results = ["pass" if s >= 60 else "fail" for s in scores]
print(f"Results:          {results}")

# Performance — comprehension vs append loop
n = 100_000

start = time.time()
result = []
for i in range(n):
    result.append(i ** 2)
loop_time = time.time() - start

start = time.time()
result = [i ** 2 for i in range(n)]
comp_time = time.time() - start

print(f"\nLoop time:        {loop_time:.4f}s")
print(f"Comprehension:    {comp_time:.4f}s")
print(f"Comprehension is faster — optimized at bytecode level!")


# -----------------------------------------------------------------------------
# SECTION 6: Sorting — Timsort
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 6: Sorting — Timsort")
print("=" * 60)

# sort() vs sorted()
nums = [5, 2, 8, 1, 9, 3]

sorted_new = sorted(nums)     # returns NEW list, original unchanged
print(f"sorted():   {sorted_new}, original: {nums}")

nums.sort()                   # modifies IN PLACE, returns None
print(f"sort():     {nums}")

# Sort with key — sort by transformed value
words = ["banana", "apple", "cherry", "kiwi", "mango"]
by_length  = sorted(words, key=len)
by_last    = sorted(words, key=lambda w: w[-1])   # sort by last char
print(f"\nBy length:  {by_length}")
print(f"By last:    {by_last}")

# Sort list of dicts
people = [
    {"name": "Ayush", "age": 30},
    {"name": "Rahul", "age": 25},
    {"name": "Priya", "age": 28},
]
by_age  = sorted(people, key=lambda p: p["age"])
by_name = sorted(people, key=lambda p: p["name"])
print(f"\nBy age:  {[p['name'] for p in by_age]}")
print(f"By name: {[p['name'] for p in by_name]}")

# Timsort — Python's sorting algorithm
# Hybrid of merge sort + insertion sort
# Best case:    O(n)       — already sorted
# Average case: O(n log n)
# Worst case:   O(n log n)
# Stable:       YES — equal elements keep original order
print(f"\nTimsort is STABLE — equal elements keep original order")
data = [(1, "b"), (2, "a"), (1, "a")]
print(f"Before: {data}")
print(f"After:  {sorted(data, key=lambda x: x[0])}")   # (1,'b') before (1,'a')


# -----------------------------------------------------------------------------
# SECTION 7: CPython Internals — Dynamic Array
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 7: CPython Internals — Dynamic Array")
print("=" * 60)

# Lists over-allocate memory to make append() O(1) amortized
lst = []
prev_allocated = 0

print("Growth pattern as elements are appended:")
print(f"{'Elements':<12} {'Size (bytes)':<15} {'Allocated slots (est)'}")
print("-" * 50)

for i in range(17):
    lst.append(i)
    size = sys.getsizeof(lst)
    if size != prev_allocated:
        # Estimate allocated slots from size
        # Each slot is 8 bytes (pointer), base size ~56 bytes
        slots = (size - 56) // 8
        print(f"{len(lst):<12} {size:<15} ~{slots} slots")
        prev_allocated = size

print("\nOver-allocation means NOT every append triggers resize!")
print("append() is O(1) AMORTIZED — occasional O(n) resize is rare")

# Memory of list vs tuple for same data
data = list(range(100))
tup  = tuple(range(100))
print(f"\nlist(range(100)) size:  {sys.getsizeof(data)} bytes")
print(f"tuple(range(100)) size: {sys.getsizeof(tup)} bytes")
print("Tuple is smaller — no over-allocation, immutable")


# -----------------------------------------------------------------------------
# SECTION 8: Common Patterns and Pitfalls
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 8: Common Patterns and Pitfalls")
print("=" * 60)

# PATTERN 1: Unpack list into variables
first, *middle, last = [1, 2, 3, 4, 5]
print(f"first={first}, middle={middle}, last={last}")

# PATTERN 2: Swap without temp variable
a, b = 1, 2
a, b = b, a
print(f"\nSwapped: a={a}, b={b}")

# PATTERN 3: Flatten nested list
nested = [[1, 2], [3, 4], [5, 6]]
flat = [x for sublist in nested for x in sublist]
print(f"\nFlattened: {flat}")

# PATTERN 4: Remove duplicates (preserve order)
dupes = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
seen = set()
unique = [x for x in dupes if not (x in seen or seen.add(x))]
print(f"Unique (ordered): {unique}")

# PATTERN 5: Zip two lists into dict
keys   = ["name", "age", "city"]
values = ["Ayush", 30, "Bangalore"]
d = dict(zip(keys, values))
print(f"\nZip to dict: {d}")

# PITFALL 1: Multiplying nested lists — shares inner lists!
bad_matrix = [[0] * 3] * 3      # BAD — all rows are same object!
bad_matrix[0][0] = 99
print(f"\nBad matrix (shared rows): {bad_matrix}")   # all rows changed!

good_matrix = [[0] * 3 for _ in range(3)]   # GOOD — each row is new list
good_matrix[0][0] = 99
print(f"Good matrix (independent): {good_matrix}")   # only first row changed

# PITFALL 2: Modifying list while iterating — skip elements!
nums = [1, 2, 3, 4, 5]
for n in nums:
    if n % 2 == 0:
        nums.remove(n)           # BAD — skips elements!
print(f"\nBad removal while iterating: {nums}")   # [1, 3, 5]? not always!

nums = [1, 2, 3, 4, 5]
nums = [n for n in nums if n % 2 != 0]   # GOOD — comprehension
print(f"Good removal (comprehension): {nums}")


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Concept           | Key Insight                                          |
# |-------------------|------------------------------------------------------|
# | PyListObject      | Dynamic array of PyObject* pointers on the heap     |
# | Over-allocation   | CPython allocates extra slots — append() is O(1)    |
# | append()          | O(1) amortized — fastest way to add to list         |
# | insert(i)         | O(n) — shifts all elements right of i               |
# | remove(x)         | O(n) — linear search + shift                        |
# | x in list         | O(n) — use set for O(1) membership                  |
# | sort()            | O(n log n) Timsort — stable, in-place               |
# | sorted()          | O(n log n) — returns NEW list, original unchanged   |
# | Shallow copy      | New outer list, SHARED inner objects                |
# | Deep copy         | Fully independent at ALL levels                     |
# | Comprehension     | Faster than append loop — optimized bytecode        |
# | [[0]*3]*3         | PITFALL — all rows share same object!               |
# | Modify while iter | PITFALL — skips elements, use comprehension instead |
#
# GOLDEN RULES:
# 1. Use append() not insert(0) — O(1) vs O(n)
# 2. Use set for membership checks — O(1) vs list O(n)
# 3. Never use mutable default in [[val]*n]*n — use comprehension
# 4. Never modify a list while iterating — use comprehension instead
# 5. Shallow copy shares inner objects — use deepcopy for nested lists
# 6. sorted() returns new list, sort() modifies in place
#
# =============================================================================
