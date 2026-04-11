# =============================================================================
# 02_tuples_sets_dicts.py — Tuples, Sets, and Dicts in Python
# python-ai-journey | 02_intermediate
# =============================================================================
#
# THEORY:
# -------
# Three essential data structures, each with a distinct purpose:
#
#   TUPLE  — immutable, ordered sequence. Faster than list.
#            Used for fixed data, multiple return values, dict keys.
#
#   SET    — mutable, unordered collection of UNIQUE hashable objects.
#            Backed by hash table → O(1) membership, add, remove.
#            Used for deduplication, membership testing, set math.
#
#   DICT   — mutable, ordered (Python 3.7+) mapping of key → value.
#            Backed by hash table → O(1) get, set, delete.
#            Keys must be HASHABLE (immutable).
#
# HASHABILITY:
#   An object is hashable if it has a __hash__() method that returns
#   a consistent integer, AND an __eq__() method for collision resolution.
#   Immutable types are hashable. Mutable types are NOT.
#
#   Hashable:     int, float, bool, str, tuple, frozenset
#   Not hashable: list, dict, set
#
# INTERNALS (CPython):
# ---------------------
# TUPLE:
#   - Stored as PyTupleObject — fixed-size array of PyObject* pointers
#   - No over-allocation — exact size allocated at creation
#   - Faster than list — simpler structure, CPython optimizes tuple creation
#   - Tuples of same content may be interned by CPython
#
# SET:
#   - Stored as PySetObject — open-addressing hash table
#   - Load factor ~2/3 — resizes when 2/3 full
#   - Each slot stores: hash, key pointer
#   - add/remove/in → O(1) average, O(n) worst (hash collision)
#
# DICT:
#   - Stored as PyDictObject — compact hash table (Python 3.6+)
#   - Two arrays: indices array + entries array (key, value, hash)
#   - Insertion order preserved (Python 3.7+ guaranteed)
#   - get/set/delete → O(1) average
#   - Resize at 2/3 load factor — doubles capacity
#
# =============================================================================

import sys
import time


# =============================================================================
# PART 1: TUPLES
# =============================================================================

print("=" * 60)
print("PART 1: TUPLES")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 1: Creating Tuples
# -----------------------------------------------------------------------------

print("\n--- Creating Tuples ---")

empty       = ()
single      = (42,)             # MUST have trailing comma!
not_tuple   = (42)              # just parentheses — this is int 42!
coords      = (10, 20)
mixed       = (1, "hello", 3.14, True)
nested      = ((1, 2), (3, 4))
from_list   = tuple([1, 2, 3])
from_string = tuple("Python")

print(f"empty:      {empty},   type={type(empty)}")
print(f"single:     {single},  type={type(single)}")
print(f"not_tuple:  {not_tuple}, type={type(not_tuple)}")   # int!
print(f"coords:     {coords}")
print(f"from_list:  {from_list}")
print(f"from_str:   {from_string}")


# -----------------------------------------------------------------------------
# SECTION 2: Tuple Immutability
# -----------------------------------------------------------------------------

print("\n--- Tuple Immutability ---")

t = (1, 2, 3)

# Cannot modify in place
try:
    t[0] = 99
except TypeError as e:
    print(f"Cannot modify tuple: {e}")

# But if tuple contains mutable object — that object CAN change!
t = (1, [2, 3], 4)
t[1].append(99)              # modifying the LIST inside tuple — allowed!
print(f"Tuple with mutable inner: {t}")   # (1, [2, 3, 99], 4)
# The tuple itself didn't change — it still points to same list object
# The list object changed — but tuple's reference to it is unchanged


# -----------------------------------------------------------------------------
# SECTION 3: Tuple Operations
# -----------------------------------------------------------------------------

print("\n--- Tuple Operations ---")

t = (3, 1, 4, 1, 5, 9, 2, 6)

print(f"t[0]:         {t[0]}")
print(f"t[-1]:        {t[-1]}")
print(f"t[1:4]:       {t[1:4]}")
print(f"t[::-1]:      {t[::-1]}")       # reversed
print(f"len(t):       {len(t)}")
print(f"min(t):       {min(t)}")
print(f"max(t):       {max(t)}")
print(f"sum(t):       {sum(t)}")
print(f"t.count(1):   {t.count(1)}")    # count occurrences
print(f"t.index(5):   {t.index(5)}")    # index of first occurrence

# Concatenation — creates NEW tuple
t1 = (1, 2, 3)
t2 = (4, 5, 6)
t3 = t1 + t2
print(f"\nt1 + t2 = {t3}")

# Repetition
t4 = (0,) * 5
print(f"(0,)*5  = {t4}")


# -----------------------------------------------------------------------------
# SECTION 4: Tuple Unpacking
# -----------------------------------------------------------------------------

print("\n--- Tuple Unpacking ---")

# Basic unpacking
x, y = (10, 20)
print(f"x={x}, y={y}")

# Extended unpacking
first, *middle, last = (1, 2, 3, 4, 5)
print(f"first={first}, middle={middle}, last={last}")

# Swap variables
a, b = 1, 2
a, b = b, a
print(f"Swapped: a={a}, b={b}")

# Unpack in loop
points = [(1, 2), (3, 4), (5, 6)]
for x, y in points:
    print(f"  point: x={x}, y={y}")

# Function returning multiple values — actually a tuple!
def divmod_custom(a, b):
    return a // b, a % b      # returns tuple

quotient, remainder = divmod_custom(17, 5)
print(f"\n17 ÷ 5 → quotient={quotient}, remainder={remainder}")


# -----------------------------------------------------------------------------
# SECTION 5: Tuple as Dict Key — Hashability
# -----------------------------------------------------------------------------

print("\n--- Hashability ---")

# Tuples are hashable — can be dict keys
locations = {
    (28.6, 77.2): "Delhi",
    (12.9, 77.5): "Bangalore",
    (19.0, 72.8): "Mumbai",
}

print(f"Location lookup: {locations[(12.9, 77.5)]}")
print(f"hash((1,2)):  {hash((1, 2))}")
print(f"hash('name'): {hash('name')}")

# Lists are NOT hashable
try:
    h = hash([1, 2])
except TypeError as e:
    print(f"hash([1,2]) → {e}")

# Why? If list changes, hash changes → dict breaks → not allowed


# -----------------------------------------------------------------------------
# SECTION 6: Tuple vs List Performance
# -----------------------------------------------------------------------------

print("\n--- Tuple vs List Performance ---")

# Memory — tuple is smaller
lst = list(range(100))
tup = tuple(range(100))
print(f"list size:  {sys.getsizeof(lst)} bytes")
print(f"tuple size: {sys.getsizeof(tup)} bytes")
print(f"Tuple saves {sys.getsizeof(lst) - sys.getsizeof(tup)} bytes")

# Creation speed — tuple is faster
n = 1_000_000

start = time.time()
for _ in range(n):
    lst = [1, 2, 3, 4, 5]
list_time = time.time() - start

start = time.time()
for _ in range(n):
    tup = (1, 2, 3, 4, 5)
tuple_time = time.time() - start

print(f"\nList creation  ({n}x): {list_time:.3f}s")
print(f"Tuple creation ({n}x): {tuple_time:.3f}s")
print(f"Tuple is ~{list_time/tuple_time:.1f}x faster to create!")


# =============================================================================
# PART 2: SETS
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: SETS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 7: Creating Sets
# -----------------------------------------------------------------------------

print("\n--- Creating Sets ---")

empty_set = set()              # NOT {} — that's an empty dict!
nums      = {1, 2, 3, 4, 5}
dupes     = {1, 2, 2, 3, 3, 3}  # duplicates removed automatically
from_list = set([3, 1, 4, 1, 5, 9, 2, 6, 5])
from_str  = set("python")

print(f"empty_set: {empty_set},  type={type(empty_set)}")
print(f"nums:      {nums}")
print(f"dupes:     {dupes}")         # {1, 2, 3} — no duplicates
print(f"from_list: {from_list}")
print(f"from_str:  {from_str}")      # unique chars only, unordered


# -----------------------------------------------------------------------------
# SECTION 8: Set Operations
# -----------------------------------------------------------------------------

print("\n--- Set Operations ---")

s = {1, 2, 3, 4, 5}

# Modifying
s.add(6)
print(f"add(6):     {s}")

s.discard(3)            # remove — no error if not found
print(f"discard(3): {s}")

s.remove(2)             # remove — raises KeyError if not found
print(f"remove(2):  {s}")

popped = s.pop()        # remove and return ARBITRARY element (unordered!)
print(f"pop():      removed={popped}, remaining={s}")

# Membership — O(1) hash lookup!
s = {1, 2, 3, 4, 5}
print(f"\n3 in s:  {3 in s}")    # O(1)
print(f"9 in s:  {9 in s}")    # O(1)


# -----------------------------------------------------------------------------
# SECTION 9: Set Math Operations
# -----------------------------------------------------------------------------

print("\n--- Set Math ---")

a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

print(f"a = {a}")
print(f"b = {b}")
print(f"a | b  (union):        {a | b}")          # all elements from both
print(f"a & b  (intersection): {a & b}")          # only common elements
print(f"a - b  (difference):   {a - b}")          # in a but not b
print(f"b - a  (difference):   {b - a}")          # in b but not a
print(f"a ^ b  (symmetric):    {a ^ b}")          # in either but not both

# Method equivalents
print(f"\na.union(b):        {a.union(b)}")
print(f"a.intersection(b): {a.intersection(b)}")
print(f"a.difference(b):   {a.difference(b)}")

# Subset / superset
small = {1, 2}
print(f"\n{{1,2}} <= {{1,2,3}}: {small <= {1, 2, 3}}")   # subset
print(f"{{1,2}} <  {{1,2,3}}: {small < {1, 2, 3}}")    # proper subset
print(f"{{1,2,3}} >= {{1,2}}: {{{1,2,3} >= small}}")


# -----------------------------------------------------------------------------
# SECTION 10: Set Performance — O(1) Membership
# -----------------------------------------------------------------------------

print("\n--- Set vs List Membership Performance ---")

n = 1_000_000
big_list = list(range(n))
big_set  = set(range(n))

target = n - 1    # worst case for list — last element

start = time.time()
target in big_list
list_time = time.time() - start

start = time.time()
target in big_set
set_time = time.time() - start

print(f"List 'in' ({n} elements): {list_time:.6f}s  O(n)")
print(f"Set  'in' ({n} elements): {set_time:.6f}s  O(1)")
print(f"Set is ~{int(list_time/max(set_time,0.000001))}x faster!")

# Deduplication — fastest way
dupes = [1, 3, 2, 1, 4, 3, 5, 2, 6]
unique = list(set(dupes))            # fast but loses order!
print(f"\nDedup (unordered): {unique}")

# Preserve order dedup
seen = set()
unique_ordered = [x for x in dupes if not (x in seen or seen.add(x))]
print(f"Dedup (ordered):   {unique_ordered}")


# =============================================================================
# PART 3: DICTIONARIES
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: DICTIONARIES")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 11: Creating Dicts
# -----------------------------------------------------------------------------

print("\n--- Creating Dicts ---")

empty    = {}
person   = {"name": "Ayush", "age": 30, "city": "Bangalore"}
from_zip = dict(zip(["a", "b", "c"], [1, 2, 3]))
from_kw  = dict(name="Ayush", age=30)
from_list= dict([("x", 1), ("y", 2)])

print(f"person:   {person}")
print(f"from_zip: {from_zip}")
from_kw_result = from_kw
print(f"from_kw:  {from_kw_result}")
print(f"from_list:{from_list}")

# Dict comprehension
squares = {x: x**2 for x in range(1, 6)}
print(f"\nsquares: {squares}")

# Nested dict
config = {
    "database": {"host": "localhost", "port": 5432},
    "cache":    {"host": "redis",     "ttl": 3600},
}
print(f"DB host: {config['database']['host']}")


# -----------------------------------------------------------------------------
# SECTION 12: Dict Methods
# -----------------------------------------------------------------------------

print("\n--- Dict Methods ---")

d = {"name": "Ayush", "age": 30, "city": "Bangalore"}

# Accessing
print(f"d['name']:           {d['name']}")
print(f"d.get('age'):        {d.get('age')}")
print(f"d.get('salary',0):   {d.get('salary', 0)}")    # default if missing

# Views — live views of dict contents
print(f"\nd.keys():   {list(d.keys())}")
print(f"d.values(): {list(d.values())}")
print(f"d.items():  {list(d.items())}")

# Modifying
d["email"] = "ayush@example.com"      # add new key
d["age"] = 31                          # update existing key
print(f"\nAfter add/update: {d}")

d.update({"city": "Mumbai", "phone": "9999"})   # update multiple
print(f"After update(): {d}")

removed = d.pop("phone")              # remove and return value
print(f"pop('phone'): removed={removed}, dict={d}")

last = d.popitem()                    # remove and return last item (LIFO)
print(f"popitem(): removed={last}")

# setdefault — get value, or set default if key missing
d.setdefault("country", "India")
print(f"setdefault: {d}")

# Merge dicts (Python 3.9+)
d1 = {"a": 1, "b": 2}
d2 = {"b": 99, "c": 3}
merged = d1 | d2                      # new dict, d2 values win on conflict
print(f"\nd1 | d2: {merged}")

d1 |= d2                              # in-place merge
print(f"d1 |= d2: {d1}")


# -----------------------------------------------------------------------------
# SECTION 13: Dict Internals — Hash Table
# -----------------------------------------------------------------------------

print("\n--- Dict Internals ---")

# Python 3.7+ — insertion order preserved
d = {}
for char in "python":
    d[char] = ord(char)
print(f"Insertion order preserved: {d}")

# O(1) operations
d = {i: i**2 for i in range(1_000_000)}

start = time.time()
_ = d[999_999]
get_time = time.time() - start
print(f"\nDict get (1M keys): {get_time:.8f}s — O(1)!")

# Memory
small_dict = {"a": 1}
print(f"\nEmpty dict size:  {sys.getsizeof({})} bytes")
print(f"1-key dict size:  {sys.getsizeof(small_dict)} bytes")


# -----------------------------------------------------------------------------
# SECTION 14: Common Dict Patterns
# -----------------------------------------------------------------------------

print("\n--- Common Dict Patterns ---")

# PATTERN 1: Count occurrences
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
print(f"Word counts: {counts}")

# Better — use setdefault
counts2 = {}
for word in words:
    counts2.setdefault(word, 0)
    counts2[word] += 1
print(f"Setdefault:  {counts2}")

# Best — use collections.Counter
from collections import Counter, defaultdict
counts3 = Counter(words)
print(f"Counter:     {dict(counts3)}")

# PATTERN 2: Group by — using defaultdict
data = [("fruits", "apple"), ("vegs", "carrot"), ("fruits", "banana"), ("vegs", "spinach")]
grouped = defaultdict(list)
for category, item in data:
    grouped[category].append(item)
print(f"\nGrouped: {dict(grouped)}")

# PATTERN 3: Invert a dict
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
print(f"\nInverted: {inverted}")

# PATTERN 4: Filter dict
scores = {"Ayush": 95, "Rahul": 72, "Priya": 88, "Kiran": 65}
passed = {name: score for name, score in scores.items() if score >= 75}
print(f"Passed:   {passed}")

# PATTERN 5: Safe nested access
config = {"db": {"host": "localhost"}}
host = config.get("db", {}).get("host", "default")
print(f"\nNested get: {host}")

missing = config.get("cache", {}).get("host", "default")
print(f"Missing nested: {missing}")     # "default" — no KeyError!


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Structure  | Ordered | Mutable | Unique  | Lookup | Use for              |
# |------------|---------|---------|---------|--------|----------------------|
# | tuple      | ✅      | ❌      | ❌      | O(n)   | Fixed data, dict key |
# | list       | ✅      | ✅      | ❌      | O(n)   | Dynamic sequences    |
# | set        | ❌      | ✅      | ✅      | O(1)   | Dedup, membership    |
# | frozenset  | ❌      | ❌      | ✅      | O(1)   | Immutable set, key   |
# | dict       | ✅(3.7) | ✅      | keys ✅ | O(1)   | Key-value mapping    |
#
# HASHABILITY:
#   Hashable (can be dict key/set element): int, float, str, tuple, frozenset
#   Not hashable (mutable):                 list, dict, set
#
# GOLDEN RULES:
# 1. Use tuple for fixed data — smaller, faster, hashable
# 2. Use set for membership checks — O(1) vs list O(n)
# 3. Dict keys must be hashable — immutable types only
# 4. {} is empty dict — use set() for empty set!
# 5. Use .get() not [] for safe dict access with default
# 6. Use Counter for counting, defaultdict for grouping
# 7. Python 3.7+ dicts preserve insertion order
#
# =============================================================================
