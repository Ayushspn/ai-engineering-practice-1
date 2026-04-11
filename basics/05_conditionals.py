# =============================================================================
# 05_conditionals.py — Conditionals in Python
# python-ai-journey | 01_basics
# =============================================================================
#
# THEORY:
# -------
# Conditionals let you execute code based on whether a condition is True or False.
# Python evaluates conditions using TRUTHINESS — every object has a boolean value.
#
# Key concepts:
#   1. Truthy/Falsy   — every object evaluates to True or False
#   2. if/elif/else   — branch execution based on conditions
#   3. Ternary        — one-line conditional expression
#   4. Match/Case     — structural pattern matching (Python 3.10+)
#
# INTERNALS (CPython):
# ---------------------
# When Python evaluates 'if x:', it calls:
#   1. x.__bool__()  → if defined, uses this
#   2. x.__len__()   → if defined, True if len > 0
#   3. True          → default if neither is defined
#
# This means truthiness is fully customizable in your own classes.
#
# FALSY VALUES (evaluate to False):
#   None, False, 0, 0.0, 0j, "", [], (), {}, set(), frozenset()
#
# TRUTHY VALUES:
#   Everything else — non-zero numbers, non-empty sequences, objects
#
# =============================================================================


# -----------------------------------------------------------------------------
# SECTION 1: Truthy and Falsy
# -----------------------------------------------------------------------------

print("=" * 60)
print("SECTION 1: Truthy and Falsy")
print("=" * 60)

# Falsy values
falsy_values = [0, 0.0, 0j, "", [], (), {}, set(), frozenset(), None, False]

print("Falsy values:")
for v in falsy_values:
    print(f"  bool({str(v):<15}) = {bool(v)}")

# Truthy values
truthy_values = [1, -1, 0.1, "hello", [0], (0,), {"a": 1}, {0}, True]

print("\nTruthy values:")
for v in truthy_values:
    print(f"  bool({str(v):<15}) = {bool(v)}")

# Surprising truthy — [0] is truthy even though it contains 0!
print(f"\nbool([0])  = {bool([0])}")    # True  — list is non-empty
print(f"bool([])   = {bool([])}")      # False — list is empty
print(f"bool(-1)   = {bool(-1)}")      # True  — non-zero int


# -----------------------------------------------------------------------------
# SECTION 2: if / elif / else
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 2: if / elif / else")
print("=" * 60)

# Basic if/else
score = 75

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Score: {score} → Grade: {grade}")

# Nested if
age = 20
has_id = True

if age >= 18:
    if has_id:
        print("\nEntry allowed — adult with ID")
    else:
        print("\nEntry denied — no ID")
else:
    print("\nEntry denied — minor")

# Multiple conditions with and/or
username = "ayush"
password = "secret123"

if username == "ayush" and password == "secret123":
    print("Login successful!")
else:
    print("Invalid credentials")


# -----------------------------------------------------------------------------
# SECTION 3: Truthy/Falsy in Practice
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 3: Truthy/Falsy in Practice")
print("=" * 60)

# if x == 0  vs  if not x — NOT the same!
def check_difference(x):
    print(f"\nx = {repr(x)}")
    print(f"  x == 0    → {x == 0}")
    print(f"  not x     → {not x}")
    print(f"  same?     → {(x == 0) == (not x)}")

check_difference(0)       # both True
check_difference("")      # == 0 is False, not x is True
check_difference([])      # == 0 is False, not x is True
check_difference(None)    # == 0 is False, not x is True
check_difference(0.0)     # both True (0.0 == 0 in Python!)

# Pythonic way — use truthiness directly
name = ""

# Not Pythonic
if name != "" and name is not None:
    print(f"\nHello {name}")
else:
    print("\nNo name provided (verbose check)")

# Pythonic
if name:
    print(f"Hello {name}")
else:
    print("No name provided (Pythonic)")

# Checking empty collections
items = []

if not items:                       # Pythonic way to check empty
    print("\nNo items in list")

if len(items) == 0:                 # works but less Pythonic
    print("List is empty (verbose)")


# -----------------------------------------------------------------------------
# SECTION 4: Ternary (Conditional Expression)
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 4: Ternary Expression")
print("=" * 60)

# Syntax: value_if_true if condition else value_if_false
age = 20
status = "adult" if age >= 18 else "minor"
print(f"Age {age} → {status}")

# Inline assignment
score = 85
result = "pass" if score >= 60 else "fail"
print(f"Score {score} → {result}")

# Ternary in f-string
items = [1, 2, 3]
print(f"Cart: {len(items)} item{'s' if len(items) != 1 else ''}")

# Nested ternary — avoid! hard to read
score = 75
grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F"
print(f"\nNested ternary grade: {grade}")   # works but hard to read
# Use if/elif/else for more than 2 conditions


# -----------------------------------------------------------------------------
# SECTION 5: Short-circuit as Conditional
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 5: Short-circuit as Conditional")
print("=" * 60)

# 'or' for default values
user_input = ""
name = user_input or "Guest"         # if user_input is falsy, use "Guest"
print(f"Name: {name}")               # "Guest"

user_input = "Ayush"
name = user_input or "Guest"
print(f"Name: {name}")               # "Ayush"

# 'and' for safe attribute access
user = None
email = user and user.get("email")   # safely returns None if user is falsy
print(f"\nEmail: {email}")           # None — no AttributeError

user = {"name": "Ayush", "email": "ayush@example.com"}
email = user and user.get("email")
print(f"Email: {email}")             # "ayush@example.com"

# None coalescing pattern (Python 3.8+ use walrus for complex cases)
config = None
timeout = config or 30               # default timeout
print(f"\nTimeout: {timeout}")       # 30


# -----------------------------------------------------------------------------
# SECTION 6: Match / Case (Python 3.10+)
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 6: Match / Case (Python 3.10+)")
print("=" * 60)

# Basic match — like switch/case in other languages
def handle_command(command):
    match command:
        case "quit":
            return "Quitting..."
        case "help":
            return "Available commands: quit, help, start"
        case "start":
            return "Starting..."
        case _:                      # default case (wildcard)
            return f"Unknown command: '{command}'"

print(handle_command("help"))
print(handle_command("start"))
print(handle_command("fly"))

# Match with conditions (guards)
def classify_number(n):
    match n:
        case 0:
            return "zero"
        case n if n < 0:
            return "negative"
        case n if n % 2 == 0:
            return "positive even"
        case _:
            return "positive odd"

for num in [0, -5, 4, 7]:
    print(f"{num:>3} → {classify_number(num)}")

# Match with structure — very powerful for dicts/tuples
def handle_event(event):
    match event:
        case {"type": "click", "x": x, "y": y}:
            return f"Click at ({x}, {y})"
        case {"type": "keypress", "key": key}:
            return f"Key pressed: {key}"
        case _:
            return "Unknown event"

print(f"\n{handle_event({'type': 'click', 'x': 100, 'y': 200})}")
print(f"{handle_event({'type': 'keypress', 'key': 'Enter'})}")


# -----------------------------------------------------------------------------
# SECTION 7: Common Patterns and Pitfalls
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 7: Common Patterns and Pitfalls")
print("=" * 60)

# PITFALL 1: Comparing to True/False explicitly
x = [1, 2, 3]

# Wrong
if x == True:
    print("this never prints — list != True")

# Right
if x:
    print("List is non-empty (Pythonic)")

# PITFALL 2: Using 'is' for value comparison
a = 1000
b = 1000

# Wrong — unreliable for large ints
if a is b:
    print("same object")     # may or may not print!

# Right
if a == b:
    print("same value (correct)")

# PITFALL 3: assignment in condition (common bug)
x = 5
# if x = 10:   ← SyntaxError in Python (unlike C/Java)
#     print(x)
# Python protects you — use == for comparison

# PATTERN: Guard clause — fail fast, reduce nesting
def process_user(user):
    if not user:
        return "No user provided"
    if not user.get("name"):
        return "User has no name"
    if not user.get("email"):
        return "User has no email"
    return f"Processing {user['name']} ({user['email']})"

print(f"\n{process_user(None)}")
print(f"{process_user({'name': 'Ayush'})}")
print(f"{process_user({'name': 'Ayush', 'email': 'a@b.com'})}")


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Concept          | Key Insight                                           |
# |------------------|-------------------------------------------------------|
# | Truthy/Falsy     | Every object has bool value — 0,"",[],(},None=False  |
# | if not x         | Checks ANY falsy value — not just x == 0             |
# | if x == 0        | Checks ONLY integer/float zero                       |
# | __bool__         | CPython calls this to determine truthiness           |
# | Ternary          | val_true if condition else val_false                  |
# | Short-circuit    | 'or' for defaults, 'and' for safe access             |
# | Match/Case       | Structural pattern matching — Python 3.10+           |
# | Guard clause     | Return early — keeps code flat and readable           |
#
# GOLDEN RULES:
# 1. Use truthiness directly — 'if items:' not 'if len(items) > 0:'
# 2. 'if not x' catches ALL falsy values — not just None or 0
# 3. Use '==' for value comparison, 'is' only for None/True/False
# 4. Guard clauses reduce nesting — return early for invalid cases
# 5. Ternary for simple 2-way choices, if/elif/else for complex logic
#
# =============================================================================
