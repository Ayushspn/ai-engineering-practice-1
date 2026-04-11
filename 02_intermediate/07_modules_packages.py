# =============================================================================
# 07_modules_packages.py — Modules and Packages in Python
# python-ai-journey | 02_intermediate
# =============================================================================
#
# THEORY:
# -------
# MODULE  — a single .py file containing Python code (functions, classes, vars)
# PACKAGE — a directory containing multiple modules + __init__.py
#
# Key concepts:
#   1. import styles      — import, from...import, as alias
#   2. sys.modules        — module cache — imported once, reused
#   3. __name__           — "__main__" vs module name
#   4. Package structure  — __init__.py, subpackages
#   5. Standard library   — built-in modules (os, sys, math, etc.)
#   6. Third party        — pip installed packages (numpy, requests, etc.)
#   7. __all__            — control what 'from module import *' exports
#   8. Relative imports   — import within same package
#
# INTERNALS (CPython):
# ---------------------
# When you write 'import math':
#   1. Python checks sys.modules['math'] — if found, reuses it (cached!)
#   2. If not found → searches sys.path (list of directories)
#   3. Finds math.py (or math.cpython-3x.so for C extensions)
#   4. Creates a new module object (PyModuleObject)
#   5. Executes the module's code top-to-bottom in module's namespace
#   6. Stores result in sys.modules['math']
#   7. Binds name 'math' in current namespace
#
# sys.path search order:
#   1. Current directory (or script directory)
#   2. PYTHONPATH environment variable directories
#   3. Standard library directories
#   4. Site-packages (pip installed packages)
#
# Module is executed ONLY ONCE — subsequent imports reuse sys.modules cache
# This is why modifying a module object affects all importers!
#
# =============================================================================

import sys
import os
import math
import time
import tempfile
from pathlib import Path


# =============================================================================
# PART 1: IMPORT STYLES
# =============================================================================

print("=" * 60)
print("PART 1: IMPORT STYLES")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 1: Three Ways to Import
# -----------------------------------------------------------------------------

print("\n--- Import Styles ---")

# Style 1: import module — access via module.attribute
import math
print(f"import math:")
print(f"  math.sqrt(16) = {math.sqrt(16)}")
print(f"  math.pi       = {math.pi:.6f}")
print(f"  math.floor(3.7) = {math.floor(3.7)}")

# Style 2: from module import name — direct access, no prefix
from os import getcwd, listdir
print(f"\nfrom os import getcwd, listdir:")
print(f"  getcwd() = {getcwd()}")         # no os. prefix needed

# Style 3: import module as alias — shorter name
import datetime as dt
print(f"\nimport datetime as dt:")
print(f"  dt.date.today() = {dt.date.today()}")
print(f"  dt.datetime.now() = {dt.datetime.now().strftime('%H:%M:%S')}")

# Style 4: from module import * — imports everything (avoid!)
# from math import *    # BAD — pollutes namespace, hard to trace
# print(sqrt(16))       # where did sqrt come from? unclear!

# Style 5: from module import name as alias
from math import sqrt as square_root
print(f"\nfrom math import sqrt as square_root:")
print(f"  square_root(25) = {square_root(25)}")


# -----------------------------------------------------------------------------
# SECTION 2: sys.modules — The Module Cache
# -----------------------------------------------------------------------------

print("\n--- sys.modules Cache ---")

# Every imported module is cached in sys.modules
print(f"'math' in sys.modules:     {'math' in sys.modules}")
print(f"'os' in sys.modules:       {'os' in sys.modules}")
print(f"'numpy' in sys.modules:    {'numpy' in sys.modules}")   # not imported

# Importing again uses cache — does NOT re-execute module!
import math as math1
import math as math2
print(f"\nmath1 is math2: {math1 is math2}")   # True — same object from cache!

# How many modules loaded?
print(f"Total modules in sys.modules: {len(sys.modules)}")

# sys.path — where Python looks for modules
print(f"\nsys.path (first 3 entries):")
for p in sys.path[:3]:
    print(f"  {p}")


# -----------------------------------------------------------------------------
# SECTION 3: __name__ — Main vs Module
# -----------------------------------------------------------------------------

print("\n--- __name__ ---")

# Every module has __name__
# When run directly: __name__ == "__main__"
# When imported:     __name__ == "module_filename"

print(f"This file's __name__: {__name__}")   # "__main__" when run directly

# This pattern is CRITICAL for reusable modules:
# if __name__ == "__main__":
#     # only runs when executed directly
#     # NOT when imported by another module
#     main()

# Example of why this matters:
print(f"\nWhy __name__ == '__main__' matters:")
print(f"  When you run:    python 07_modules_packages.py")
print(f"  __name__ =       '__main__'  → if block runs")
print(f"  When imported:   import 07_modules_packages")
print(f"  __name__ =       '07_modules_packages' → if block skipped!")


# =============================================================================
# PART 2: STANDARD LIBRARY MODULES
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: STANDARD LIBRARY — KEY MODULES")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 4: os and sys
# -----------------------------------------------------------------------------

print("\n--- os module ---")

print(f"os.getcwd():          {os.getcwd()}")
print(f"os.sep:               '{os.sep}'")          # path separator
print(f"os.linesep repr:      {repr(os.linesep)}")  # line separator
print(f"os.cpu_count():       {os.cpu_count()}")

# Environment variables
path_env = os.environ.get("PATH", "not set")
print(f"PATH (first 50):      {path_env[:50]}...")

# os.path — file path operations (use pathlib instead in modern code)
print(f"\nos.path.join:   {os.path.join('folder', 'sub', 'file.txt')}")
print(f"os.path.exists: {os.path.exists('.')}")
print(f"os.path.abspath: {os.path.abspath('.')[:50]}...")

print(f"\n--- sys module ---")
print(f"sys.version:     {sys.version[:30]}...")
print(f"sys.platform:    {sys.platform}")
print(f"sys.executable:  {sys.executable[:50]}...")
print(f"sys.argv:        {sys.argv}")      # command line arguments
print(f"sys.maxsize:     {sys.maxsize}")   # max int size


# -----------------------------------------------------------------------------
# SECTION 5: math and random
# -----------------------------------------------------------------------------

print("\n--- math module ---")

print(f"math.pi:          {math.pi}")
print(f"math.e:           {math.e:.6f}")
print(f"math.sqrt(144):   {math.sqrt(144)}")
print(f"math.pow(2, 10):  {math.pow(2, 10)}")
print(f"math.log(math.e): {math.log(math.e)}")    # natural log
print(f"math.log10(1000): {math.log10(1000)}")
print(f"math.ceil(3.2):   {math.ceil(3.2)}")
print(f"math.floor(3.9):  {math.floor(3.9)}")
print(f"math.factorial(5):{math.factorial(5)}")
print(f"math.gcd(48, 18): {math.gcd(48, 18)}")
print(f"math.inf:         {math.inf}")
print(f"math.isnan(float('nan')): {math.isnan(float('nan'))}")

import random
print(f"\n--- random module ---")
random.seed(42)    # seed for reproducibility
print(f"random.random():        {random.random():.4f}")   # 0.0 to 1.0
print(f"random.randint(1,100):  {random.randint(1, 100)}")
print(f"random.uniform(0,10):   {random.uniform(0, 10):.4f}")

items = ["apple", "banana", "cherry", "mango"]
print(f"random.choice():        {random.choice(items)}")
random.shuffle(items)
print(f"random.shuffle():       {items}")
print(f"random.sample(3):       {random.sample(['a','b','c','d','e'], 3)}")


# -----------------------------------------------------------------------------
# SECTION 6: collections module
# -----------------------------------------------------------------------------

print("\n--- collections module ---")

from collections import Counter, defaultdict, OrderedDict, namedtuple, deque

# Counter — count occurrences
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counter = Counter(words)
print(f"Counter: {counter}")
print(f"Most common 2: {counter.most_common(2)}")

# defaultdict — dict with default value for missing keys
dd = defaultdict(list)
data = [("fruits", "apple"), ("vegs", "carrot"), ("fruits", "banana")]
for category, item in data:
    dd[category].append(item)    # no KeyError — creates [] automatically!
print(f"\ndefaultdict: {dict(dd)}")

# namedtuple — tuple with named fields
Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)
print(f"\nnamedtuple Point: {p}")
print(f"  p.x={p.x}, p.y={p.y}")
print(f"  p[0]={p[0]}, p[1]={p[1]}")   # still works as tuple!

Person = namedtuple("Person", ["name", "age", "city"])
ayush = Person("Ayush", 30, "Bangalore")
print(f"  {ayush.name} from {ayush.city}")

# deque — double-ended queue — O(1) append/pop from both ends!
dq = deque([1, 2, 3, 4, 5])
dq.appendleft(0)      # O(1) — list insert(0) is O(n)!
dq.append(6)          # O(1)
dq.popleft()          # O(1) — list pop(0) is O(n)!
print(f"\ndeque: {dq}")
print(f"O(1) append/pop from both ends — unlike list!")


# -----------------------------------------------------------------------------
# SECTION 7: itertools and functools
# -----------------------------------------------------------------------------

print("\n--- itertools module ---")

import itertools

# chain — combine multiple iterables
chained = list(itertools.chain([1,2], [3,4], [5,6]))
print(f"chain:        {chained}")

# product — cartesian product
product = list(itertools.product([1,2], ['a','b']))
print(f"product:      {product}")

# combinations — unique combinations
combos = list(itertools.combinations([1,2,3,4], 2))
print(f"combinations: {combos}")

# permutations
perms = list(itertools.permutations([1,2,3], 2))
print(f"permutations: {perms}")

# groupby — group consecutive elements
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4), ("C", 5)]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"  Group '{key}': {list(group)}")

# islice — lazy slice of iterator
gen = (x**2 for x in range(1000000))   # lazy generator
first_5 = list(itertools.islice(gen, 5))
print(f"\nislice first 5: {first_5}")

print(f"\n--- functools module ---")

import functools

# reduce — apply function cumulatively
total = functools.reduce(lambda acc, x: acc + x, [1,2,3,4,5])
print(f"reduce (sum):    {total}")

product = functools.reduce(lambda acc, x: acc * x, [1,2,3,4,5])
print(f"reduce (product):{product}")

# partial — fix some arguments of a function
def power(base, exp):
    return base ** exp

square = functools.partial(power, exp=2)
cube   = functools.partial(power, exp=3)
print(f"\npartial square(5): {square(5)}")
print(f"partial cube(3):   {cube(3)}")

# lru_cache — memoize function results
@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(f"\nfibonacci(30): {fibonacci(30)}")
print(f"cache info:    {fibonacci.cache_info()}")


# -----------------------------------------------------------------------------
# SECTION 8: datetime module
# -----------------------------------------------------------------------------

print("\n--- datetime module ---")

import datetime

now   = datetime.datetime.now()
today = datetime.date.today()

print(f"now:          {now}")
print(f"today:        {today}")
print(f"year:         {now.year}")
print(f"formatted:    {now.strftime('%d %B %Y, %H:%M:%S')}")

# Arithmetic with dates
one_week  = datetime.timedelta(weeks=1)
next_week = today + one_week
print(f"next week:    {next_week}")

# Parse date string
date_str = "2026-01-15"
parsed   = datetime.datetime.strptime(date_str, "%Y-%m-%d")
print(f"parsed date:  {parsed.date()}")


# =============================================================================
# PART 3: CREATING YOUR OWN MODULE
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: CREATING YOUR OWN MODULE")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 9: Write and Import a Custom Module
# -----------------------------------------------------------------------------

print("\n--- Custom Module ---")

# Create a simple module file
module_dir  = Path(tempfile.mkdtemp())
module_file = module_dir / "mathutils.py"

module_code = '''
"""
mathutils.py — Custom math utility module
"""

# Module-level variable
VERSION = "1.0.0"

# __all__ controls what 'from mathutils import *' exports
__all__ = ["add", "multiply", "factorial", "is_prime"]

def add(*args):
    """Add any number of values"""
    return sum(args)

def multiply(*args):
    """Multiply any number of values"""
    result = 1
    for n in args:
        result *= n
    return result

def factorial(n):
    """Calculate factorial recursively"""
    if n < 0:
        raise ValueError("Factorial undefined for negative numbers")
    return 1 if n <= 1 else n * factorial(n - 1)

def is_prime(n):
    """Check if number is prime"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def _private_helper():
    """Private — not exported with import *"""
    return "internal use only"

# This runs only when executed directly
if __name__ == "__main__":
    print("Running mathutils directly!")
    print(f"5! = {factorial(5)}")
'''

module_file.write_text(module_code)
print(f"Created module: {module_file}")

# Add module directory to sys.path so we can import it
sys.path.insert(0, str(module_dir))

# Now import our custom module!
import mathutils

print(f"\nimport mathutils:")
print(f"  mathutils.VERSION:        {mathutils.VERSION}")
print(f"  mathutils.add(1,2,3,4):   {mathutils.add(1,2,3,4)}")
print(f"  mathutils.multiply(2,3,4):{mathutils.multiply(2,3,4)}")
print(f"  mathutils.factorial(6):   {mathutils.factorial(6)}")
print(f"  mathutils.is_prime(17):   {mathutils.is_prime(17)}")
print(f"  mathutils.__all__:        {mathutils.__all__}")

# Module metadata
print(f"\nModule internals:")
print(f"  __name__:    {mathutils.__name__}")
print(f"  __file__:    {mathutils.__file__}")
print(f"  __doc__:     {mathutils.__doc__.strip()}")


# -----------------------------------------------------------------------------
# SECTION 10: Package Structure
# -----------------------------------------------------------------------------

print("\n--- Package Structure ---")

# A package is a directory with __init__.py
# mypackage/
# ├── __init__.py          ← makes it a package
# ├── core.py              ← submodule
# ├── utils.py             ← submodule
# └── api/                 ← subpackage
#     ├── __init__.py
#     └── endpoints.py

# Create a package
pkg_dir = module_dir / "mypackage"
pkg_dir.mkdir()

# __init__.py — runs when package is imported
init_code = '''
"""mypackage — Example package"""
VERSION = "1.0.0"

# Import key things to make them available at package level
from .core import greet        # relative import!
from .utils import format_name

__all__ = ["greet", "format_name", "VERSION"]
'''

(pkg_dir / "__init__.py").write_text(init_code)

# core.py
core_code = '''
def greet(name):
    return f"Hello, {name}! Welcome to mypackage."

def farewell(name):
    return f"Goodbye, {name}!"
'''
(pkg_dir / "core.py").write_text(core_code)

# utils.py
utils_code = '''
def format_name(first, last):
    return f"{last}, {first}".title()

def truncate(text, length=50):
    return text[:length] + "..." if len(text) > length else text
'''
(pkg_dir / "utils.py").write_text(utils_code)

# Import the package
import mypackage

print(f"Package imported: mypackage")
print(f"  VERSION:      {mypackage.VERSION}")
print(f"  greet():      {mypackage.greet('Ayush')}")
print(f"  format_name():{mypackage.format_name('ayush', 'sharma')}")

# Import specific submodule
from mypackage import core, utils
print(f"\n  core.farewell():    {core.farewell('Rahul')}")
print(f"  utils.truncate():   {utils.truncate('This is a very long string that needs truncating', 20)}")

# Cleanup
import shutil
sys.path.pop(0)
shutil.rmtree(module_dir)


# =============================================================================
# PART 4: BEST PRACTICES
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: BEST PRACTICES")
print("=" * 60)

print("""
IMPORT ORDER (PEP 8):
─────────────────────
1. Standard library imports
2. Blank line
3. Third-party imports (numpy, requests, etc.)
4. Blank line
5. Local/project imports

Example:
    import os
    import sys
    from pathlib import Path

    import numpy as np
    import requests

    from mypackage import utils
    from mypackage.core import greet

IMPORT STYLE GUIDE:
───────────────────
✅ import math                    → clear origin of math.sqrt()
✅ from os import getcwd          → when using just one thing
✅ import numpy as np             → well-known alias
✅ from collections import Counter→ specific, widely used

❌ from math import *             → pollutes namespace, unclear origin
❌ import os, sys, math           → multiple imports per line
❌ from module import (           → only OK for very long lists
       thing1, thing2, thing3
   )
""")


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Concept          | Key Insight                                           |
# |------------------|-------------------------------------------------------|
# | Module           | Single .py file — executed once, cached in sys.modules|
# | Package          | Directory with __init__.py — groups related modules   |
# | import math      | Whole module, access via math.sqrt()                  |
# | from x import y  | Direct access, no prefix — careful with conflicts     |
# | import x as y    | Alias — shorter name for long module names            |
# | sys.modules      | Cache — module executed ONCE, reused on re-import     |
# | sys.path         | Search path — Python looks here for modules           |
# | __name__         | "__main__" if run directly, module name if imported   |
# | __all__          | List of names exported by 'from module import *'      |
# | __init__.py      | Makes directory a package — runs on package import    |
# | Relative import  | from .module import name — within same package        |
# | lru_cache        | Memoize function results — avoid recomputing          |
# | namedtuple       | Tuple with named fields — lightweight, immutable      |
# | deque            | O(1) append/pop both ends — better than list for queue|
#
# KEY STANDARD LIBRARY MODULES:
#   os, sys, math, random, datetime, pathlib
#   collections, itertools, functools
#   json, csv, re, time, threading, subprocess
#
# GOLDEN RULES:
# 1. Always use if __name__ == "__main__" for runnable modules
# 2. Never use 'from module import *' in production code
# 3. Import order: stdlib → third-party → local (PEP 8)
# 4. Modules execute ONCE — cached in sys.modules after that
# 5. Use __all__ to explicitly define your module's public API
# 6. Prefer pathlib over os.path for file operations
# 7. Use collections.deque for queues — O(1) vs list O(n)
#
# =============================================================================
