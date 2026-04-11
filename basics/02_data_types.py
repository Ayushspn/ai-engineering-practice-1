# =============================================================================
# 02_data_types.py — Data Types in Python
# python-ai-journey | 01_basics
# =============================================================================
#
# THEORY:
# -------
# Every object in Python has a TYPE stored in its PyObject as ob_type.
# The type tells CPython:
#   1. How much memory to allocate
#   2. What operations are allowed
#   3. How to interpret the raw bytes
#
# The most critical property of a type is MUTABILITY:
#   - Immutable: object's value CANNOT change after creation
#   - Mutable:   object's value CAN change after creation
#
# What looks like "modifying" an immutable object is actually:
#   1. Creating a NEW object with the new value
#   2. Rebinding the name to the new object
#   3. Old object's refcount drops → Garbage Collected
#
# BUILT-IN TYPES MAP:
# -------------------
# Numeric   → int, float, complex, bool
# Sequence  → str, list, tuple
# Mapping   → dict
# Set       → set, frozenset
# None      → NoneType
#
# MUTABILITY TABLE:
# -----------------
# int, float, bool, str, tuple, frozenset → IMMUTABLE
# list, dict, set                         → MUTABLE
#
# =============================================================================


# -----------------------------------------------------------------------------
# SECTION 1: Numeric Types
# -----------------------------------------------------------------------------

print("=" * 60)
print("SECTION 1: Numeric Types")
print("=" * 60)

# int — whole numbers, unlimited precision in Python
age = 25
big_num = 10 ** 100          # Python int has no overflow!
negative = -42

print(f"int:     {age},  type: {type(age)}")
print(f"big int: {big_num}")
print(f"neg int: {negative}")

# float — double precision (64-bit IEEE 754)
pi = 3.14159
temperature = -98.6
scientific = 1.5e10          # 1.5 × 10^10

print(f"\nfloat:      {pi},  type: {type(pi)}")
print(f"scientific: {scientific}")

# bool — subclass of int! True=1, False=0
is_active = True
is_done = False

print(f"\nbool: {is_active},  type: {type(is_active)}")
print(f"bool is subclass of int: {isinstance(True, int)}")  # True!
print(f"True + True = {True + True}")   # = 2, because True == 1
print(f"True * 5   = {True * 5}")       # = 5

# complex — real + imaginary
z = 3 + 4j
print(f"\ncomplex: {z},  type: {type(z)}")
print(f"real: {z.real}, imaginary: {z.imag}")


# -----------------------------------------------------------------------------
# SECTION 2: Immutability of Numeric Types
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 2: Immutability of Numeric Types")
print("=" * 60)

x = 10
print(f"Before: id(x)={id(x)}, x={x}")

x = x + 5    # Does NOT modify the int object 10
             # Creates NEW object 15, rebinds x to it
print(f"After:  id(x)={id(x)}, x={x}")
print("Notice: id changed → x was rebound to a NEW object")


# -----------------------------------------------------------------------------
# SECTION 3: String — Immutable Sequence
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 3: String — Immutable Sequence")
print("=" * 60)

name = "Ayush"
greeting = 'hello'
multiline = """This is
a multiline string"""

print(f"str: {name},  type: {type(name)}")
print(f"length: {len(name)}")
print(f"index:  {name[0]}")        # 'A'
print(f"slice:  {name[1:4]}")      # 'yus'
print(f"upper:  {name.upper()}")   # new object returned, name unchanged

# Immutability proof
try:
    name[0] = "B"              # This will raise an error
except TypeError as e:
    print(f"\nCannot modify str in place: {e}")

# String concatenation — creates NEW object each time
s = "hello"
print(f"\nBefore concat: id(s)={id(s)}")
s = s + " world"
print(f"After concat:  id(s)={id(s)}")
print(f"s = '{s}'")
print("Notice: id changed → NEW str object was created")

# PERFORMANCE: avoid + in loops, use join()
# BAD  → result = result + str(i)   [creates new object every iteration]
# GOOD → result = "".join(items)    [builds once]
words = ["Python", "is", "powerful"]
sentence = " ".join(words)
print(f"\njoin result: '{sentence}'")


# -----------------------------------------------------------------------------
# SECTION 4: List — Mutable Sequence
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 4: List — Mutable Sequence")
print("=" * 60)

fruits = ["apple", "banana", "cherry"]
mixed = [1, "hello", 3.14, True, None]   # can hold any types!

print(f"list: {fruits},  type: {type(fruits)}")
print(f"index:  {fruits[0]}")
print(f"slice:  {fruits[1:3]}")

# Mutation — modifies the SAME object in memory
print(f"\nBefore append: id={id(fruits)}, list={fruits}")
fruits.append("mango")
print(f"After append:  id={id(fruits)}, list={fruits}")
print("Notice: id is SAME → same object was mutated!")

# This is the key difference from str
fruits[0] = "avocado"         # can modify in place
print(f"After modify:  {fruits}")

# Shared reference gotcha (from 01_variables.py)
a = [1, 2, 3]
b = a                          # b is NOT a copy
b.append(99)
print(f"\nShared ref — a={a}, b={b}")   # both show [1, 2, 3, 99]

# To make a real copy:
c = a.copy()                   # shallow copy
c.append(100)
print(f"After copy  — a={a}, c={c}")   # a unchanged


# -----------------------------------------------------------------------------
# SECTION 5: Tuple — Immutable Sequence
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 5: Tuple — Immutable Sequence")
print("=" * 60)

point = (10, 20)
rgb = (255, 128, 0)
single = (42,)                 # trailing comma needed for single element!

print(f"tuple: {point},  type: {type(point)}")
print(f"index: {point[0]}")
print(f"single element tuple: {single}, type: {type(single)}")

# Immutability proof
try:
    point[0] = 99
except TypeError as e:
    print(f"\nCannot modify tuple: {e}")

# Tuple is faster than list — CPython optimizes immutable sequences
# Use tuple for fixed data, list for dynamic data

# Tuple unpacking
x, y = point
print(f"\nUnpacked: x={x}, y={y}")


# -----------------------------------------------------------------------------
# SECTION 6: Dictionary — Mutable Mapping
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 6: Dictionary — Mutable Mapping")
print("=" * 60)

person = {
    "name": "Ayush",
    "age": 30,
    "skills": ["Python", "React"]
}

print(f"dict: {person},  type: {type(person)}")
print(f"access: {person['name']}")
print(f"get:    {person.get('salary', 'not found')}")  # safe access

# Mutation
person["city"] = "Bangalore"
print(f"\nAfter adding key: {person}")

# Keys must be immutable (int, str, tuple) — not list!
valid_keys = {1: "int key", "name": "str key", (1,2): "tuple key"}
print(f"\nValid dict keys: {valid_keys}")

try:
    invalid = {[1,2]: "list key"}   # list is mutable → not hashable
except TypeError as e:
    print(f"List as key fails: {e}")


# -----------------------------------------------------------------------------
# SECTION 7: Set — Mutable, Unique, Unordered
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 7: Set — Mutable, Unique, Unordered")
print("=" * 60)

nums = {1, 2, 3, 2, 1}           # duplicates removed automatically
print(f"set: {nums},  type: {type(nums)}")   # {1, 2, 3}

nums.add(4)
nums.discard(2)
print(f"After add/discard: {nums}")

# Set operations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(f"\nUnion:        {a | b}")
print(f"Intersection: {a & b}")
print(f"Difference:   {a - b}")

# frozenset — immutable version of set
fs = frozenset({1, 2, 3})
print(f"\nfrozenset: {fs},  type: {type(fs)}")
try:
    fs.add(4)
except AttributeError as e:
    print(f"Cannot modify frozenset: {e}")


# -----------------------------------------------------------------------------
# SECTION 8: NoneType — The Null Value
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 8: NoneType")
print("=" * 60)

result = None
print(f"None: {result},  type: {type(result)}")

# None is a SINGLETON — only one object exists in all of CPython
a = None
b = None
print(f"a is b: {a is b}")   # Always True — same object
print(f"id(a) == id(b): {id(a) == id(b)}")

# Always check None with 'is', not '=='
def get_user(found=False):
    return {"name": "Ayush"} if found else None

user = get_user()
if user is None:              # correct way
    print("User not found")


# -----------------------------------------------------------------------------
# SECTION 9: type() and isinstance()
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 9: type() vs isinstance()")
print("=" * 60)

values = [42, 3.14, "hello", [1,2], (1,2), {1,2}, {"a":1}, None, True]

for v in values:
    print(f"{str(v):<20} type={str(type(v).__name__):<12}")

# isinstance() is better for type checking — respects inheritance
print(f"\nisinstance(True, int):  {isinstance(True, int)}")   # True — bool subclasses int
print(f"type(True) == int:      {type(True) == int}")         # False — exact type check


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Type       | Mutable | Category  | Key Characteristic                    |
# |------------|---------|-----------|---------------------------------------|
# | int        | ❌      | Numeric   | Unlimited precision, interned -5→256  |
# | float      | ❌      | Numeric   | 64-bit IEEE 754 double precision       |
# | bool       | ❌      | Numeric   | Subclass of int! True=1, False=0      |
# | complex    | ❌      | Numeric   | Real + imaginary parts                |
# | str        | ❌      | Sequence  | + creates new object (use join!)      |
# | tuple      | ❌      | Sequence  | Faster than list, for fixed data      |
# | frozenset  | ❌      | Set       | Immutable set, can be dict key        |
# | list       | ✅      | Sequence  | append/modify in place, same id       |
# | dict       | ✅      | Mapping   | Keys must be immutable (hashable)     |
# | set        | ✅      | Set       | Unique elements, unordered            |
# | NoneType   | ❌      | None      | Singleton — always use 'is None'      |
#
# GOLDEN RULE:
# Immutable = "modifying" creates NEW object + rebinds name
# Mutable   = modifying changes the SAME object in memory
#
# =============================================================================
