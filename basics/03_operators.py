# =============================================================================
# 03_operators.py — Operators in Python
# python-ai-journey | 01_basics
# =============================================================================
#
# THEORY:
# -------
# Operators are special symbols that perform operations on objects.
# Every operator in Python maps to a DUNDER METHOD on the object:
#
#   a + b   →  a.__add__(b)        called on the left operand
#   a > b   →  a.__gt__(b)         gt = greater than
#   a == b  →  a.__eq__(b)         eq = equal
#
# This means operators are fully customizable — you can define how
# your own classes behave with +, -, *, ==, etc.
#
# OPERATOR CATEGORIES:
# --------------------
#   1. Arithmetic    → + - * / // % **
#   2. Comparison    → == != > < >= <=
#   3. Logical       → and or not
#   4. Assignment    → = += -= *= /= //= %= **=
#   5. Identity      → is, is not
#   6. Membership    → in, not in
#   7. Bitwise       → & | ^ ~ << >>
#
# INTERNALS:
# ----------
# - Comparison always returns a bool (PyBool_Type)
# - 'and'/'or' use short-circuit evaluation — lazy, stops early
# - 'is' checks ob_refcnt identity (memory address via id())
# - 'in' on list = O(n), on set/dict = O(1) — hash lookup
# - Bitwise ops work on raw binary representation of integers
#
# =============================================================================


# -----------------------------------------------------------------------------
# SECTION 1: Arithmetic Operators
# -----------------------------------------------------------------------------

print("=" * 60)
print("SECTION 1: Arithmetic Operators")
print("=" * 60)

a, b = 10, 3

print(f"{a} +  {b} = {a + b}")    # 13  — addition
print(f"{a} -  {b} = {a - b}")    # 7   — subtraction
print(f"{a} *  {b} = {a * b}")    # 30  — multiplication
print(f"{a} /  {b} = {a / b}")    # 3.3333 — true division, always float
print(f"{a} // {b} = {a // b}")   # 3   — floor division, drops decimal
print(f"{a} %  {b} = {a % b}")    # 1   — modulus (remainder)
print(f"{a} ** {b} = {a ** b}")   # 1000 — exponentiation

# Floor division — goes toward NEGATIVE infinity, not zero
print(f"\n-7 // 2 = {-7 // 2}")   # -4 (not -3!)
print(f" 7 // 2 = {7 // 2}")      # 3

# Modulus practical use — check even/odd
num = 17
if num % 2 == 0:
    print(f"{num} is even")
else:
    print(f"\n{num} is odd")       # 17 is odd

# True division always returns float — even for whole numbers
print(f"\n10 / 2 = {10 / 2}")     # 5.0, not 5!
print(f"type: {type(10 / 2)}")    # float

# INTERNALS: operators map to dunder methods
print(f"\n10 + 3 via dunder: {(10).__add__(3)}")   # same as 10 + 3
print(f"10 / 3 via dunder: {(10).__truediv__(3)}") # same as 10 / 3


# -----------------------------------------------------------------------------
# SECTION 2: Comparison Operators
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 2: Comparison Operators")
print("=" * 60)

x, y = 10, 20

print(f"{x} == {y} → {x == y}")   # False
print(f"{x} != {y} → {x != y}")   # True
print(f"{x} >  {y} → {x > y}")    # False
print(f"{x} <  {y} → {x < y}")    # True
print(f"{x} >= {y} → {x >= y}")   # False
print(f"{x} <= {y} → {x <= y}")   # True

# Comparison always returns bool
result = x < y
print(f"\ntype of (x < y): {type(result)}")   # bool

# Python allows CHAINING comparisons — very readable!
age = 25
print(f"\nAge chaining: {18 <= age <= 60}")    # True — valid adult range
print(f"Range check:  {1 < 5 < 10 < 100}")    # True

# String comparison — compares Unicode code points
print(f"\n'apple' < 'banana': {'apple' < 'banana'}")   # True (a < b)
print(f"'Z' < 'a': {'Z' < 'a'}")                       # True (Z=90, a=97)


# -----------------------------------------------------------------------------
# SECTION 3: Logical Operators — and, or, not
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 3: Logical Operators")
print("=" * 60)

# Basic logic
print(f"True and True   → {True and True}")    # True
print(f"True and False  → {True and False}")   # False
print(f"False or True   → {False or True}")    # True
print(f"False or False  → {False or False}")   # False
print(f"not True        → {not True}")         # False
print(f"not False       → {not False}")        # True

# SHORT-CIRCUIT EVALUATION — Python is lazy!
# 'and' stops at first False, 'or' stops at first True
print("\n--- Short-circuit Evaluation ---")

def check(val, label):
    print(f"  [{label}] evaluated!")
    return val

# 'and' — stops at first False, never evaluates right side
print("False and ...:")
result = check(False, "left") and check(True, "right")   # right never runs!
print(f"Result: {result}")

# 'or' — stops at first True, never evaluates right side
print("\nTrue or ...:")
result = check(True, "left") or check(False, "right")    # right never runs!
print(f"Result: {result}")

# PRACTICAL PATTERNS using short-circuit:
print("\n--- Practical Short-circuit Patterns ---")

# Safe attribute access — avoids AttributeError
user = None
name = user and user.name    # user is None (falsy) → stops, returns None safely
print(f"Safe access: {name}")   # None — no AttributeError!

# Default value pattern
config = None
value = config or "default"
print(f"Default value: {value}")   # "default"

config = "production"
value = config or "default"
print(f"Config value: {value}")    # "production"

# IMPORTANT: 'and'/'or' return the ACTUAL object, not just True/False!
print(f"\n'hello' and 'world' → {'hello' and 'world'}")  # 'world' (last truthy)
print(f"'' and 'world'      → {'' and 'world'}")         # '' (first falsy)
print(f"'' or 'world'       → {'' or 'world'}")          # 'world' (first truthy)
print(f"0 or 42             → {0 or 42}")                # 42


# -----------------------------------------------------------------------------
# SECTION 4: Assignment Operators
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 4: Assignment Operators")
print("=" * 60)

x = 10
print(f"initial x = {x}")

x += 5;  print(f"x += 5  → {x}")    # 15
x -= 3;  print(f"x -= 3  → {x}")    # 12
x *= 2;  print(f"x *= 2  → {x}")    # 24
x /= 4;  print(f"x /= 4  → {x}")    # 6.0  (becomes float!)
x //= 2; print(f"x //= 2 → {x}")    # 3.0
x **= 3; print(f"x **= 3 → {x}")    # 27.0
x %= 5;  print(f"x %%= 5  → {x}")   # 2.0

# Walrus operator := (Python 3.8+) — assign AND use in one expression
print("\n--- Walrus Operator := ---")
numbers = [1, 15, 3, 42, 8, 99, 2]

# Without walrus
filtered = []
for n in numbers:
    doubled = n * 2
    if doubled > 20:
        filtered.append(doubled)
print(f"Without walrus: {filtered}")

# With walrus — cleaner
filtered = [doubled for n in numbers if (doubled := n * 2) > 20]
print(f"With walrus:    {filtered}")


# -----------------------------------------------------------------------------
# SECTION 5: Identity Operators — is, is not
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 5: Identity Operators")
print("=" * 60)

# 'is' checks memory address (id()), not value
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(f"a == b: {a == b}")    # True  — same VALUE
print(f"a is b: {a is b}")    # False — different OBJECTS in memory
print(f"a is c: {a is c}")    # True  — c points to same object as a

print(f"\nid(a) = {id(a)}")
print(f"id(b) = {id(b)}")     # different address
print(f"id(c) = {id(c)}")     # same as a

# Correct use of 'is' — only for None, True, False (singletons)
value = None
print(f"\nvalue is None:     {value is None}")      # ✅ correct
print(f"value == None:     {value == None}")        # works but wrong style

# Integer interning — small ints share objects
x = 100
y = 100
print(f"\n100 is 100: {x is y}")    # True  — interned (-5 to 256)

x = 1000
y = 1000
print(f"1000 is 1000: {x is y}")   # False — not interned, new objects


# -----------------------------------------------------------------------------
# SECTION 6: Membership Operators — in, not in
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 6: Membership Operators")
print("=" * 60)

fruits = ["apple", "banana", "cherry"]
print(f"'apple' in fruits:     {'apple' in fruits}")      # True
print(f"'mango' not in fruits: {'mango' not in fruits}")  # True

# String membership
sentence = "Python is powerful"
print(f"\n'Python' in sentence: {'Python' in sentence}")  # True
print(f"'Java' in sentence:   {'Java' in sentence}")      # False

# INTERNALS: Performance difference is massive!
import time

big_list = list(range(1_000_000))
big_set  = set(range(1_000_000))

# List 'in' → O(n) linear scan
start = time.time()
999_999 in big_list
list_time = time.time() - start

# Set 'in' → O(1) hash lookup
start = time.time()
999_999 in big_set
set_time = time.time() - start

print(f"\nList lookup time: {list_time:.6f}s  O(n)")
print(f"Set  lookup time: {set_time:.6f}s  O(1)")
print("Set is dramatically faster for membership checks!")

# Dict membership — checks KEYS by default
person = {"name": "Ayush", "age": 30}
print(f"\n'name' in person:  {'name' in person}")    # True  — checks keys
print(f"'Ayush' in person: {'Ayush' in person}")     # False — not a key
print(f"'Ayush' in person.values(): {'Ayush' in person.values()}")  # True


# -----------------------------------------------------------------------------
# SECTION 7: Bitwise Operators
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 7: Bitwise Operators")
print("=" * 60)

a = 0b1010   # 10 in decimal
b = 0b1100   # 12 in decimal

print(f"a     = {a:04b}  ({a})")
print(f"b     = {b:04b}  ({b})")
print(f"a & b = {(a&b):04b}  ({a&b})  AND  — 1 only where BOTH are 1")
print(f"a | b = {(a|b):04b}  ({a|b})  OR   — 1 where EITHER is 1")
print(f"a ^ b = {(a^b):04b}  ({a^b})   XOR  — 1 where DIFFERENT")
print(f"~a    = {~a}        NOT  — flips all bits")
print(f"a << 1 = {a<<1:04b} ({a<<1})  LEFT SHIFT  — multiply by 2")
print(f"a >> 1 = {a>>1:04b}  ({a>>1})   RIGHT SHIFT — divide by 2")

# Practical use — check if number is even/odd using bitwise
num = 17
print(f"\n{num} is {'even' if num & 1 == 0 else 'odd'}")  # odd (last bit is 1)
print(f"num & 1 = {num & 1}")   # 1 = odd, 0 = even

# Left/right shift = fast multiply/divide by powers of 2
x = 5
print(f"\n5 << 1 = {5 << 1}   (5 × 2 = 10)")
print(f"5 << 2 = {5 << 2}   (5 × 4 = 20)")
print(f"20 >> 2 = {20 >> 2}  (20 ÷ 4 = 5)")


# -----------------------------------------------------------------------------
# SECTION 8: Operator Precedence
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 8: Operator Precedence")
print("=" * 60)

# Higher precedence = evaluated first
# ** > * / // % > + - > comparisons > not > and > or

print(f"2 + 3 * 4     = {2 + 3 * 4}")       # 14, not 20 (* before +)
print(f"(2 + 3) * 4   = {(2 + 3) * 4}")     # 20 (parens first)
print(f"2 ** 3 ** 2   = {2 ** 3 ** 2}")     # 512 (** is right-associative!)
print(f"(2 ** 3) ** 2 = {(2 ** 3) ** 2}")   # 64

# Logical precedence: not > and > or
print(f"\nTrue or False and False  = {True or False and False}")  # True
# Evaluated as: True or (False and False) = True or False = True


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Category    | Operators              | Returns       | Key Insight               |
# |-------------|------------------------|---------------|---------------------------|
# | Arithmetic  | + - * / // % **        | int or float  | / always float, // floors |
# | Comparison  | == != > < >= <=        | bool          | chainable: 1 < x < 10     |
# | Logical     | and or not             | actual object | short-circuit evaluation  |
# | Assignment  | = += -= *= /= //= %=   | —             | rebinds name to new object|
# | Identity    | is, is not             | bool          | checks memory address     |
# | Membership  | in, not in             | bool          | set O(1) vs list O(n)     |
# | Bitwise     | & | ^ ~ << >>          | int           | operates on raw bits      |
#
# GOLDEN RULES:
# 1. 'is' only for None/True/False — never for value comparison
# 2. 'and'/'or' return actual objects, not just True/False
# 3. Use set for membership checks — O(1) vs list O(n)
# 4. '/' always returns float — use '//' for integer division
# 5. Every operator maps to a dunder method (__add__, __eq__, etc.)
#
# =============================================================================
