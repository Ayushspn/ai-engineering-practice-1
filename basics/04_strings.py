# =============================================================================
# 04_strings.py — Strings in Python
# python-ai-journey | 01_basics
# =============================================================================
#
# THEORY:
# -------
# A string in Python is an IMMUTABLE sequence of Unicode code points.
# Every character in a Python string is a Unicode character — not just ASCII.
#
# Key properties:
#   1. Immutable   — no method modifies the string in place
#   2. Sequence    — supports indexing, slicing, iteration
#   3. Unicode     — every char is a Unicode code point (not just ASCII)
#   4. Interned    — short/identifier-like strings are cached by CPython
#
# INTERNALS (CPython):
# ---------------------
# Strings are stored as PyUnicodeObject — a C struct with:
#   - ob_refcnt       : reference count
#   - ob_type         : &PyUnicode_Type
#   - length          : number of characters
#   - hash            : cached hash value (-1 if not computed yet)
#   - data            : actual character data (latin-1, UCS-2, or UCS-4)
#
# CPython uses 3 internal encodings based on content:
#   - Latin-1  (1 byte/char) → if all chars fit in U+0000–U+00FF
#   - UCS-2    (2 byte/char) → if chars fit in U+0000–U+FFFF
#   - UCS-4    (4 byte/char) → if any char is above U+FFFF
#
# String interning:
#   - Strings that look like identifiers (letters, digits, _) are interned
#   - Interned strings share the same object → faster dict lookups
#   - sys.intern() can force interning for any string
#
# Every string METHOD returns a NEW object — never modifies in place.
#
# =============================================================================

import sys


# -----------------------------------------------------------------------------
# SECTION 1: Creating Strings
# -----------------------------------------------------------------------------

print("=" * 60)
print("SECTION 1: Creating Strings")
print("=" * 60)

# Single, double, triple quotes — all valid
s1 = 'hello'
s2 = "world"
s3 = '''this is
a multiline
string'''
s4 = """also
multiline"""

print(s1, s2)
print(s3)

# Raw strings — backslashes treated literally (useful for file paths, regex)
path = r"C:\Users\Ayush\Documents"
print(f"\nRaw string: {path}")

# Escape sequences in normal strings
escaped = "line1\nline2\ttabbed"
print(f"\nEscaped:\n{escaped}")

# Unicode — Python str natively supports all Unicode characters
hindi = "नमस्ते"
print(f"\nHindi: {hindi}")
print(f"Length of '{hindi}': {len(hindi)}")   # counts characters, not bytes


# -----------------------------------------------------------------------------
# SECTION 2: Immutability — Every Method Returns a New Object
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 2: Immutability")
print("=" * 60)

name = "ayush"
print(f"Original:  '{name}',  id={id(name)}")

upper = name.upper()
print(f"upper():   '{upper}', id={id(upper)}")    # different id — new object!

stripped = "  hello  ".strip()
print(f"strip():   '{stripped}'")

replaced = name.replace("a", "A")
print(f"replace(): '{replaced}', original still='{name}'")   # name unchanged

# Every method leaves original untouched
print(f"\nname after ALL methods: '{name}'")   # still "ayush"

# Trying to modify in place — raises TypeError
try:
    name[0] = "B"
except TypeError as e:
    print(f"\nCannot modify str in place: {e}")


# -----------------------------------------------------------------------------
# SECTION 3: Indexing and Slicing
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 3: Indexing and Slicing")
print("=" * 60)

s = "Python"
#    P  y  t  h  o  n
#    0  1  2  3  4  5    forward index
#   -6 -5 -4 -3 -2 -1    backward index

print(f"s = '{s}'")
print(f"s[0]    = '{s[0]}'")      # 'P'
print(f"s[-1]   = '{s[-1]}'")     # 'n' — last char
print(f"s[1:4]  = '{s[1:4]}'")    # 'yth' — start inclusive, end exclusive
print(f"s[:3]   = '{s[:3]}'")     # 'Pyt' — from start
print(f"s[3:]   = '{s[3:]}'")     # 'hon' — to end
print(f"s[::2]  = '{s[::2]}'")    # 'Pto' — every 2nd char
print(f"s[::-1] = '{s[::-1]}'")   # 'nohtyP' — reversed!

# Slicing never raises IndexError — it clips silently
print(f"\ns[0:100] = '{s[0:100]}'")   # 'Python' — no error even if out of range

# But direct indexing raises IndexError
try:
    print(s[100])
except IndexError as e:
    print(f"s[100] raises: {e}")


# -----------------------------------------------------------------------------
# SECTION 4: String Methods
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 4: String Methods")
print("=" * 60)

text = "  Hello, Python World!  "

# Case methods — all return NEW objects
print(f"upper():      '{text.strip().upper()}'")
print(f"lower():      '{text.strip().lower()}'")
print(f"title():      '{text.strip().title()}'")
print(f"swapcase():   '{text.strip().swapcase()}'")

# Strip methods
print(f"\nstrip():      '{text.strip()}'")      # both ends
print(f"lstrip():     '{text.lstrip()}'")      # left only
print(f"rstrip():     '{text.rstrip()}'")      # right only

# Search methods
s = "Hello, Python World!"
print(f"\nfind('Python'):    {s.find('Python')}")       # 7  — index of match
print(f"find('Java'):      {s.find('Java')}")           # -1 — not found
print(f"count('o'):        {s.count('o')}")             # 2
print(f"startswith('He'):  {s.startswith('He')}")       # True
print(f"endswith('!'):     {s.endswith('!')}")           # True
print(f"'Python' in s:     {'Python' in s}")            # True

# Replace — returns new string
print(f"\nreplace(): '{s.replace('Python', 'AI')}'")    # new object
print(f"original:  '{s}'")                              # unchanged

# Split and Join
sentence = "Python is powerful"
words = sentence.split(" ")           # splits into list — new list object
print(f"\nsplit():  {words}")

joined = "-".join(words)              # joins list into string — new str object
print(f"join():   '{joined}'")

# Split on multiple spaces
messy = "one   two   three"
clean = messy.split()                 # no arg = splits on any whitespace
print(f"split() on whitespace: {clean}")

# Check methods
print(f"\n'hello'.isalpha():   {'hello'.isalpha()}")     # True
print(f"'hello123'.isalnum(): {'hello123'.isalnum()}")   # True
print(f"'123'.isdigit():      {'123'.isdigit()}")        # True
print(f"'  '.isspace():       {'  '.isspace()}")         # True


# -----------------------------------------------------------------------------
# SECTION 5: String Formatting
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 5: String Formatting")
print("=" * 60)

name = "Ayush"
age  = 30
pi   = 3.14159

# Method 1: % formatting (old style — avoid)
print("Old style:  Hello %s, age %d" % (name, age))

# Method 2: .format() (Python 3+)
print("format():   Hello {}, age {}".format(name, age))
print("format():   Hello {name}, age {age}".format(name=name, age=age))

# Method 3: f-strings (Python 3.6+ — preferred, fastest)
print(f"f-string:   Hello {name}, age {age}")
print(f"Expression: 2 + 2 = {2 + 2}")
print(f"Method:     {name.upper()}")
print(f"Pi:         {pi:.2f}")        # 2 decimal places
print(f"Pi:         {pi:.4f}")        # 4 decimal places
print(f"Age:        {age:05d}")       # zero-padded to 5 digits
print(f"Name:       {name:<10}|")     # left-aligned, width 10
print(f"Name:       {name:>10}|")     # right-aligned, width 10
print(f"Name:       {name:^10}|")     # center-aligned, width 10

# f-strings are fastest — compiled directly, no runtime lookup


# -----------------------------------------------------------------------------
# SECTION 6: String Concatenation — Performance
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 6: Concatenation Performance")
print("=" * 60)

import time

n = 50_000

# BAD: + in loop — creates new object every iteration
start = time.time()
result = ""
for i in range(n):
    result = result + str(i)
bad_time = time.time() - start
print(f"+ loop ({n} iters):    {bad_time:.4f}s  — O(n²) new objects!")

# GOOD: join() — builds once
start = time.time()
result = "".join(str(i) for i in range(n))
good_time = time.time() - start
print(f"join() ({n} iters):   {good_time:.4f}s  — O(n) single build")

print(f"\njoin() is ~{int(bad_time/good_time)}x faster!")


# -----------------------------------------------------------------------------
# SECTION 7: String Interning — CPython Optimization
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 7: String Interning")
print("=" * 60)

# Identifier-like strings are automatically interned
a = "hello"
b = "hello"
print(f"'hello' is 'hello': {a is b}")    # True — same interned object

# Strings with spaces are NOT automatically interned
a = "hello world"
b = "hello world"
print(f"'hello world' is 'hello world': {a is b}")   # False — different objects

# Force interning with sys.intern()
a = sys.intern("hello world")
b = sys.intern("hello world")
print(f"After sys.intern(): {a is b}")    # True — now same object

# Why interning matters — dict key lookup speed
# Python dicts use hash + identity check for string keys
# Interned strings skip equality check → pure identity check → faster


# -----------------------------------------------------------------------------
# SECTION 8: ord() and chr() — Characters and Unicode
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 8: Unicode — ord() and chr()")
print("=" * 60)

# ord() → Unicode code point of a character
print(f"ord('A') = {ord('A')}")    # 65
print(f"ord('a') = {ord('a')}")    # 97
print(f"ord('0') = {ord('0')}")    # 48

# chr() → character from Unicode code point
print(f"\nchr(65)  = '{chr(65)}'")   # 'A'
print(f"chr(97)  = '{chr(97)}'")    # 'a'
print(f"chr(8364)= '{chr(8364)}'")  # '€'

# This is why 'Z' < 'a' — Z=90, a=97
print(f"\n'Z' < 'a': {'Z' < 'a'}")   # True — compares code points
print(f"ord('Z') = {ord('Z')}, ord('a') = {ord('a')}")


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Concept          | Key Insight                                           |
# |------------------|-------------------------------------------------------|
# | Immutability     | Every method returns NEW object — original unchanged  |
# | Indexing         | s[0] first, s[-1] last, s[1:4] slice                 |
# | Slicing          | Never raises IndexError — clips silently              |
# | f-strings        | Fastest formatting — use by default                  |
# | Concatenation    | Avoid + in loops → use join() for O(n) performance   |
# | Interning        | Identifier-like strings cached → same object in memory|
# | Unicode          | Every char is a code point — ord()/chr() to convert  |
# | split()          | Returns new list                                      |
# | join()           | Returns new string — builds entire result at once    |
# | Methods          | .upper() .lower() .strip() .replace() → all new objs |
#
# GOLDEN RULES:
# 1. String methods NEVER modify in place — always return new objects
# 2. Use join() not + for building strings in loops
# 3. Use f-strings for formatting — fastest and most readable
# 4. 'in' on string is O(n) — searches character by character
# 5. Interned strings use 'is' safely — all others use '=='
#
# =============================================================================
