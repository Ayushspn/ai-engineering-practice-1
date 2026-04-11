# =============================================================================
# 05_error_handling.py — Error Handling in Python
# python-ai-journey | 02_intermediate
# =============================================================================
#
# THEORY:
# -------
# Errors in Python are OBJECTS — instances of exception classes.
# Python uses try/except blocks to handle errors gracefully.
#
# Key concepts:
#   1. Exception hierarchy  — all exceptions inherit from BaseException
#   2. try/except           — catch and handle exceptions
#   3. else                 — runs if NO exception occurred
#   4. finally              — ALWAYS runs, exception or not
#   5. raise                — manually raise an exception
#   6. Custom exceptions    — define your own exception classes
#   7. Context managers     — with statement for resource management
#
# EXCEPTION HIERARCHY:
#   BaseException
#   └── Exception
#       ├── TypeError       — wrong type for operation
#       ├── ValueError      — right type, invalid value
#       ├── AttributeError  — attribute/method doesn't exist
#       ├── NameError       — variable not defined
#       ├── LookupError
#       │   ├── IndexError  — sequence index out of range
#       │   └── KeyError    — dict key not found
#       ├── ImportError     — module import failed
#       ├── OSError
#       │   └── FileNotFoundError
#       └── RuntimeError
#           └── RecursionError
#
# INTERNALS (CPython):
# ---------------------
# When an exception is raised:
#   1. CPython creates an exception OBJECT (instance of exception class)
#   2. Unwinds the call stack looking for matching except clause
#   3. If found → executes except block, then continues after try/except
#   4. If not found → propagates up to caller, eventually crashes with traceback
#
# Exception objects have:
#   - args      → tuple of error message arguments
#   - __traceback__ → traceback object with file/line info
#
# try/except has ZERO performance cost when no exception occurs
# Exception handling is only expensive when exception actually raised
#
# =============================================================================


# =============================================================================
# PART 1: EXCEPTION BASICS
# =============================================================================

print("=" * 60)
print("PART 1: EXCEPTION BASICS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 1: Common Exceptions
# -----------------------------------------------------------------------------

print("\n--- Common Exceptions ---")

# TypeError — wrong type
try:
    result = "hello" + 5
except TypeError as e:
    print(f"TypeError:      {e}")

# ValueError — right type, bad value
try:
    num = int("hello")
except ValueError as e:
    print(f"ValueError:     {e}")

# AttributeError — method/attr doesn't exist
try:
    result = None.upper()
except AttributeError as e:
    print(f"AttributeError: {e}")

# IndexError — index out of range
try:
    lst = [1, 2, 3]
    val = lst[10]
except IndexError as e:
    print(f"IndexError:     {e}")

# KeyError — dict key missing
try:
    d = {"name": "Ayush"}
    val = d["salary"]
except KeyError as e:
    print(f"KeyError:       {e}")

# NameError — variable not defined
try:
    print(undefined_variable)
except NameError as e:
    print(f"NameError:      {e}")

# ZeroDivisionError
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"ZeroDivision:   {e}")

# FileNotFoundError
try:
    with open("nonexistent.txt") as f:
        content = f.read()
except FileNotFoundError as e:
    print(f"FileNotFound:   {e}")


# -----------------------------------------------------------------------------
# SECTION 2: try / except / else / finally
# -----------------------------------------------------------------------------

print("\n--- try/except/else/finally ---")

def divide(a, b):
    try:
        result = a / b              # code that might raise
    except ZeroDivisionError as e:
        print(f"  except: caught {e}")
        return None
    else:
        print(f"  else:   no exception — result = {result}")
        return result              # runs ONLY if no exception
    finally:
        print(f"  finally: always runs!")   # runs NO MATTER WHAT

print("Case 1: divide(10, 2)")
r = divide(10, 2)
print(f"  returned: {r}\n")

print("Case 2: divide(10, 0)")
r = divide(10, 0)
print(f"  returned: {r}")

# finally use case — cleanup always happens
print("\n--- finally for cleanup ---")

def read_file(filename):
    f = None
    try:
        f = open(filename, 'r')
        return f.read()
    except FileNotFoundError:
        print(f"  File '{filename}' not found")
        return None
    finally:
        if f:
            f.close()              # always close file!
            print(f"  File closed in finally")

read_file("nonexistent.txt")


# -----------------------------------------------------------------------------
# SECTION 3: Catching Multiple Exceptions
# -----------------------------------------------------------------------------

print("\n--- Multiple Exceptions ---")

def parse_and_divide(text, divisor):
    try:
        number = int(text)         # might raise ValueError
        result = number / divisor  # might raise ZeroDivisionError
        return result
    except ValueError:
        print(f"  Cannot convert '{text}' to int")
    except ZeroDivisionError:
        print(f"  Cannot divide by zero")
    except Exception as e:         # catch-all for unexpected errors
        print(f"  Unexpected error: {type(e).__name__}: {e}")

parse_and_divide("42", 2)          # works
parse_and_divide("hello", 2)       # ValueError
parse_and_divide("42", 0)          # ZeroDivisionError

# Catch multiple in one line
def safe_index(lst, idx):
    try:
        return lst[idx]
    except (IndexError, TypeError) as e:
        print(f"  Error: {e}")
        return None

print(f"\nsafe_index([1,2,3], 1):   {safe_index([1,2,3], 1)}")
print(f"safe_index([1,2,3], 10):  {safe_index([1,2,3], 10)}")
print(f"safe_index([1,2,3], 'a'): {safe_index([1,2,3], 'a')}")


# -----------------------------------------------------------------------------
# SECTION 4: Exception Hierarchy — Catching Parent Classes
# -----------------------------------------------------------------------------

print("\n--- Exception Hierarchy ---")

def demonstrate_hierarchy(value):
    try:
        result = [1, 2, 3][value]
    except LookupError as e:        # catches both IndexError AND KeyError!
        print(f"  LookupError caught: {type(e).__name__}: {e}")

demonstrate_hierarchy(10)           # IndexError — caught by LookupError!

# Catching Exception catches almost everything
def catch_all(func, *args):
    try:
        return func(*args)
    except Exception as e:
        print(f"  Caught {type(e).__name__}: {e}")
        return None

catch_all(int, "bad")               # ValueError
catch_all(lambda: 1/0)             # ZeroDivisionError

# NEVER catch BaseException — it includes SystemExit, KeyboardInterrupt
# These should NOT be suppressed in normal code


# =============================================================================
# PART 2: RAISING EXCEPTIONS
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: RAISING EXCEPTIONS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 5: raise
# -----------------------------------------------------------------------------

print("\n--- raise ---")

def set_age(age):
    if not isinstance(age, int):
        raise TypeError(f"Age must be int, got {type(age).__name__}")
    if age < 0 or age > 150:
        raise ValueError(f"Age must be 0-150, got {age}")
    return age

try:
    set_age("thirty")
except TypeError as e:
    print(f"TypeError: {e}")

try:
    set_age(-5)
except ValueError as e:
    print(f"ValueError: {e}")

print(f"Valid age: {set_age(30)}")

# Re-raise — catch, do something, then re-raise
def process(data):
    try:
        result = int(data)
    except ValueError as e:
        print(f"  Logging error: {e}")
        raise              # re-raises the same exception!

try:
    process("bad")
except ValueError as e:
    print(f"  Caller caught re-raised: {e}")

# raise from — chain exceptions
def fetch_user(user_id):
    try:
        data = {"1": "Ayush"}
        return data[str(user_id)]
    except KeyError as e:
        raise ValueError(f"User {user_id} not found") from e

try:
    fetch_user(99)
except ValueError as e:
    print(f"\nChained exception: {e}")
    print(f"Caused by: {e.__cause__}")


# =============================================================================
# PART 3: CUSTOM EXCEPTIONS
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: CUSTOM EXCEPTIONS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 6: Custom Exception Classes
# -----------------------------------------------------------------------------

print("\n--- Custom Exceptions ---")

# Base custom exception for your application
class AppError(Exception):
    """Base exception for our application"""
    pass

# Specific exceptions inherit from AppError
class ValidationError(AppError):
    def __init__(self, field, message):
        self.field   = field
        self.message = message
        super().__init__(f"Validation failed for '{field}': {message}")

class NotFoundError(AppError):
    def __init__(self, resource, identifier):
        self.resource   = resource
        self.identifier = identifier
        super().__init__(f"{resource} with id={identifier} not found")

class InsufficientFundsError(AppError):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount  = amount
        super().__init__(
            f"Cannot withdraw {amount}. Balance is {balance}"
        )


# Using custom exceptions
class BankAccount:
    def __init__(self, owner, balance=0):
        if not owner:
            raise ValidationError("owner", "cannot be empty")
        self.owner   = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValidationError("amount", "must be positive")
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        return self.balance


# Test custom exceptions
try:
    acc = BankAccount("")
except ValidationError as e:
    print(f"ValidationError: {e}")
    print(f"  field: {e.field}, message: {e.message}")

acc = BankAccount("Ayush", 1000)

try:
    acc.withdraw(5000)
except InsufficientFundsError as e:
    print(f"\nInsufficientFunds: {e}")
    print(f"  balance: {e.balance}, amount: {e.amount}")

try:
    acc.withdraw(-100)
except ValidationError as e:
    print(f"\nValidation: {e}")

# Catch all app errors at once
try:
    acc.withdraw(99999)
except AppError as e:           # catches ALL custom app exceptions!
    print(f"\nAppError caught: {type(e).__name__}: {e}")


# =============================================================================
# PART 4: CONTEXT MANAGERS
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: CONTEXT MANAGERS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 7: with Statement
# -----------------------------------------------------------------------------

print("\n--- with Statement ---")

# 'with' ensures cleanup happens automatically
# Even if an exception occurs inside the block!

import tempfile
import os

# Write to temp file using context manager
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt',
                                  delete=False) as f:
    f.write("Hello from context manager!\n")
    f.write("Line 2\n")
    fname = f.name
    print(f"Writing to: {fname}")
# File automatically closed here — even if exception occurred!

# Read it back
with open(fname, 'r') as f:
    content = f.read()
    print(f"Content: {content.strip()}")

os.unlink(fname)   # cleanup temp file

# Multiple context managers
print("\nMultiple context managers:")
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt',
                                  delete=False) as src:
    src.write("source content")
    src_name = src.name

with open(src_name, 'r') as source:
    data = source.read()
    print(f"Read: '{data}'")

os.unlink(src_name)


# -----------------------------------------------------------------------------
# SECTION 8: Custom Context Manager
# -----------------------------------------------------------------------------

print("\n--- Custom Context Manager ---")

class Timer:
    """Context manager that times a block of code"""
    import time as _time

    def __enter__(self):
        self.start = self._time.time()
        print("  Timer started")
        return self                    # returned as 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = self._time.time() - self.start
        print(f"  Timer stopped: {self.elapsed:.4f}s")
        return False                   # False = don't suppress exceptions


class DatabaseConnection:
    """Simulated DB connection context manager"""

    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        print(f"  Connecting to {self.db_name}...")
        return self

    def query(self, sql):
        print(f"  Query: {sql}")
        return [{"id": 1, "name": "Ayush"}]

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  Disconnecting from {self.db_name}")
        if exc_type:
            print(f"  Rolling back due to {exc_type.__name__}!")
        return False


# Using Timer context manager
with Timer() as t:
    total = sum(i**2 for i in range(100_000))
print(f"  Result: {total}, Time: {t.elapsed:.4f}s")

# Using DB context manager
print()
with DatabaseConnection("users_db") as db:
    results = db.query("SELECT * FROM users")
    print(f"  Got {len(results)} results")
# Automatically disconnects here!

# Exception inside context manager
print()
try:
    with DatabaseConnection("orders_db") as db:
        results = db.query("SELECT * FROM orders")
        raise RuntimeError("Simulated error!")  # exception mid-block
except RuntimeError as e:
    print(f"  Caught: {e}")
# DB still disconnects cleanly!


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Concept            | Key Insight                                         |
# |--------------------|-----------------------------------------------------|
# | Exception object   | Instance of exception class — has args, traceback  |
# | try/except         | Catch specific exceptions — most specific first     |
# | else               | Runs ONLY if no exception occurred                  |
# | finally            | ALWAYS runs — use for cleanup                       |
# | raise              | Manually raise exception                            |
# | raise from         | Chain exceptions — preserve original cause          |
# | Custom exceptions  | Inherit from Exception — add fields for context     |
# | with statement     | Context manager — automatic cleanup via __exit__    |
# | __enter__          | Runs at start of with block — returns resource      |
# | __exit__           | Runs at end — even if exception occurred            |
# | LookupError        | Parent of IndexError + KeyError — catch both!       |
# | Exception          | Catches almost all — use sparingly                  |
# | BaseException      | NEVER catch — includes SystemExit, KeyboardInterrupt|
#
# GOLDEN RULES:
# 1. Catch specific exceptions — never bare 'except:'
# 2. Most specific exception first, most general last
# 3. Use finally for cleanup — always runs
# 4. Custom exceptions add context — use fields like self.field
# 5. Use 'with' for files, DBs, locks — automatic cleanup
# 6. raise from preserves exception chain for debugging
# 7. Never suppress exceptions silently — at least log them
#
# =============================================================================
