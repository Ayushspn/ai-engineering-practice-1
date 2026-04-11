# =============================================================================
# 07_functions.py — Functions in Python
# python-ai-journey | 01_basics
# =============================================================================
#
# THEORY:
# -------
# A function is a reusable block of code that performs a specific task.
# In Python, functions are FIRST-CLASS OBJECTS — they can be:
#   - Assigned to variables
#   - Passed as arguments to other functions
#   - Returned from other functions
#   - Stored in data structures (lists, dicts)
#
# Key concepts:
#   1. def             — define a function
#   2. return          — return a value (None if omitted)
#   3. Parameters      — names in function definition
#   4. Arguments       — values passed when calling
#   5. Default args    — fallback values for parameters
#   6. *args           — variable positional arguments
#   7. **kwargs        — variable keyword arguments
#   8. Pass by object  — how Python passes arguments
#   9. Lambda          — anonymous one-line function
#   10. Docstrings     — documentation inside functions
#
# INTERNALS (CPython):
# ---------------------
# When Python executes 'def func():':
#   1. Creates a PyFunctionObject on the heap
#   2. Stores bytecode, default args, name, docstring inside it
#   3. Binds the name 'func' in the current namespace to this object
#
# Function calls create a NEW stack frame (PyFrameObject):
#   - Each call gets its own local namespace (dict)
#   - Arguments are bound as local names in this frame
#   - Frame is destroyed when function returns
#
# PASS BY OBJECT REFERENCE:
#   - Python passes the REFERENCE (memory address) of the object
#   - Mutable objects (list, dict) — mutations visible outside
#   - Immutable objects (int, str) — cannot be mutated, rebinding is local
#   - This is NOT pass-by-value (no copy) NOR pass-by-reference (no alias)
#
# =============================================================================


# -----------------------------------------------------------------------------
# SECTION 1: Defining and Calling Functions
# -----------------------------------------------------------------------------

print("=" * 60)
print("SECTION 1: Defining and Calling Functions")
print("=" * 60)

# Basic function
def greet():
    print("Hello, World!")

greet()    # call the function

# Function with return value
def add(a, b):
    return a + b

result = add(3, 5)
print(f"add(3, 5) = {result}")

# Function returns None if no return statement
def no_return():
    x = 42    # does something but returns nothing

result = no_return()
print(f"no_return() returns: {result}")    # None

# Multiple return values — actually returns a TUPLE
def min_max(numbers):
    return min(numbers), max(numbers)    # returns tuple (min, max)

low, high = min_max([3, 1, 9, 5, 2])
print(f"\nmin={low}, max={high}")
print(f"type of return: {type(min_max([1,2,3]))}")   # tuple


# -----------------------------------------------------------------------------
# SECTION 2: Parameters and Arguments
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 2: Parameters and Arguments")
print("=" * 60)

# Positional arguments — order matters
def describe(name, age, city):
    print(f"{name} is {age} years old from {city}")

describe("Ayush", 30, "Bangalore")        # positional
describe(age=30, city="Bangalore", name="Ayush")  # keyword — order doesn't matter

# Default arguments — used when argument not provided
def greet(name, greeting="Hello"):        # greeting has default
    print(f"{greeting}, {name}!")

greet("Ayush")                  # uses default greeting
greet("Ayush", "Namaste")       # overrides default
greet("Ayush", greeting="Hi")   # keyword override

# PITFALL: Mutable default arguments — common bug!
print("\n--- Mutable Default Argument Bug ---")

def add_item_bug(item, items=[]):    # BAD — list created ONCE at function definition!
    items.append(item)
    return items

print(add_item_bug("apple"))    # ['apple']
print(add_item_bug("banana"))   # ['apple', 'banana'] ← BUG! list persists!
print(add_item_bug("cherry"))   # ['apple', 'banana', 'cherry'] ← still growing!

# FIX: Use None as default, create new list inside
def add_item_fix(item, items=None):   # GOOD
    if items is None:
        items = []                     # new list created each call
    items.append(item)
    return items

print(add_item_fix("apple"))    # ['apple']
print(add_item_fix("banana"))   # ['banana'] ← correct!


# -----------------------------------------------------------------------------
# SECTION 3: *args and **kwargs
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 3: *args and **kwargs")
print("=" * 60)

# *args — collect extra positional args into a TUPLE
def total(*args):
    print(f"args = {args}, type = {type(args)}")
    return sum(args)

print(f"total(1,2,3)     = {total(1, 2, 3)}")
print(f"total(1,2,3,4,5) = {total(1, 2, 3, 4, 5)}")

# **kwargs — collect extra keyword args into a DICT
def display(**kwargs):
    print(f"kwargs = {kwargs}, type = {type(kwargs)}")
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

display(name="Ayush", age=30, city="Bangalore")

# Combining all parameter types
# Order must be: positional, *args, keyword-only, **kwargs
def mixed(a, b, *args, sep="-", **kwargs):
    print(f"a={a}, b={b}")
    print(f"args={args}")
    print(f"sep={sep}")
    print(f"kwargs={kwargs}")

print("\nmixed() call:")
mixed(1, 2, 3, 4, 5, sep="*", name="Ayush", role="dev")

# Unpacking into function call
def add(a, b, c):
    return a + b + c

numbers = [1, 2, 3]
print(f"\nUnpack list:  add(*[1,2,3])   = {add(*numbers)}")

params = {"a": 1, "b": 2, "c": 3}
print(f"Unpack dict:  add(**params)   = {add(**params)}")


# -----------------------------------------------------------------------------
# SECTION 4: Pass by Object Reference
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 4: Pass by Object Reference")
print("=" * 60)

# MUTABLE argument — mutation visible outside
def append_item(lst, item):
    lst.append(item)               # mutates the SAME object
    print(f"  inside: id={id(lst)}, lst={lst}")

my_list = [1, 2, 3]
print(f"Before: id={id(my_list)}, my_list={my_list}")
append_item(my_list, 99)
print(f"After:  id={id(my_list)}, my_list={my_list}")
print("Same id → same object mutated → change visible outside!")

# REBINDING — does NOT affect outside
def rebind_list(lst):
    lst = [9, 9, 9]               # rebinds LOCAL name only
    print(f"  inside after rebind: id={id(lst)}, lst={lst}")

print(f"\nBefore rebind: id={id(my_list)}, my_list={my_list}")
rebind_list(my_list)
print(f"After rebind:  id={id(my_list)}, my_list={my_list}")
print("my_list unchanged — rebinding is local!")

# IMMUTABLE argument — cannot be mutated
def modify_int(x):
    print(f"  inside before: id={id(x)}, x={x}")
    x = x + 10                    # creates NEW int object, rebinds local x
    print(f"  inside after:  id={id(x)}, x={x}")

num = 5
print(f"\nBefore: id={id(num)}, num={num}")
modify_int(num)
print(f"After:  id={id(num)}, num={num}")
print("num unchanged — int is immutable, rebinding is local!")


# -----------------------------------------------------------------------------
# SECTION 5: Functions are First-Class Objects
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 5: Functions are First-Class Objects")
print("=" * 60)

def square(x):
    return x ** 2

def cube(x):
    return x ** 3

# Assign function to variable
fn = square
print(f"fn(4) = {fn(4)}")            # 16 — fn points to square

# Store functions in a list
operations = [square, cube]
for op in operations:
    print(f"{op.__name__}(3) = {op(3)}")

# Pass function as argument
def apply(func, value):
    return func(value)

print(f"\napply(square, 5) = {apply(square, 5)}")   # 25
print(f"apply(cube, 3)   = {apply(cube, 3)}")       # 27

# Return function from function
def make_multiplier(n):
    def multiplier(x):
        return x * n              # n is captured from outer scope (closure!)
    return multiplier              # returns the function object

double = make_multiplier(2)
triple = make_multiplier(3)

print(f"\ndouble(5) = {double(5)}")   # 10
print(f"triple(5) = {triple(5)}")    # 15
print(f"type(double): {type(double)}")  # function


# -----------------------------------------------------------------------------
# SECTION 6: Lambda Functions
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 6: Lambda Functions")
print("=" * 60)

# Lambda — anonymous one-line function
# Syntax: lambda args: expression

square = lambda x: x ** 2
add    = lambda x, y: x + y

print(f"square(4) = {square(4)}")
print(f"add(3, 5) = {add(3, 5)}")

# Most common use — as argument to higher-order functions
numbers = [5, 2, 8, 1, 9, 3]

sorted_asc  = sorted(numbers)
sorted_desc = sorted(numbers, key=lambda x: -x)   # sort descending
print(f"\nsorted asc:  {sorted_asc}")
print(f"sorted desc: {sorted_desc}")

# Sort list of dicts by a field
people = [
    {"name": "Ayush", "age": 30},
    {"name": "Rahul", "age": 25},
    {"name": "Priya", "age": 28},
]
sorted_people = sorted(people, key=lambda p: p["age"])
print(f"\nSorted by age:")
for p in sorted_people:
    print(f"  {p['name']}: {p['age']}")

# Lambda limitations — only ONE expression, no statements
# Use def for complex logic, lambda only for simple one-liners


# -----------------------------------------------------------------------------
# SECTION 7: Docstrings
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 7: Docstrings")
print("=" * 60)

def calculate_bmi(weight_kg, height_m):
    """
    Calculate Body Mass Index (BMI).

    Args:
        weight_kg (float): Weight in kilograms
        height_m  (float): Height in meters

    Returns:
        float: BMI value rounded to 2 decimal places

    Example:
        >>> calculate_bmi(70, 1.75)
        22.86
    """
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

print(f"BMI: {calculate_bmi(70, 1.75)}")
print(f"\nDocstring:\n{calculate_bmi.__doc__}")

# Access function metadata
print(f"Function name: {calculate_bmi.__name__}")


# -----------------------------------------------------------------------------
# SECTION 8: Scope — LEGB Rule
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("SECTION 8: Scope — LEGB Rule")
print("=" * 60)

# Python resolves names in this order:
# L → Local (inside current function)
# E → Enclosing (outer function, for nested functions)
# G → Global (module level)
# B → Built-in (Python builtins like print, len)

x = "global"   # Global scope

def outer():
    x = "enclosing"   # Enclosing scope

    def inner():
        x = "local"   # Local scope
        print(f"inner sees:    x = '{x}'")   # local

    inner()
    print(f"outer sees:    x = '{x}'")       # enclosing

outer()
print(f"global sees:   x = '{x}'")           # global

# global keyword — modify global variable inside function
counter = 0

def increment():
    global counter        # declare we want the global one
    counter += 1

increment()
increment()
print(f"\nCounter after 2 increments: {counter}")   # 2

# nonlocal keyword — modify enclosing variable
def make_counter():
    count = 0
    def increment():
        nonlocal count    # modify enclosing 'count'
        count += 1
        return count
    return increment

counter_fn = make_counter()
print(f"\nClosure counter: {counter_fn()}")   # 1
print(f"Closure counter: {counter_fn()}")   # 2
print(f"Closure counter: {counter_fn()}")   # 3


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Concept              | Key Insight                                       |
# |----------------------|---------------------------------------------------|
# | def                  | Creates PyFunctionObject, binds name in namespace |
# | return               | Returns None if omitted                           |
# | Multiple returns     | Actually returns a tuple                          |
# | Default mutable arg  | NEVER use [] or {} as default — use None instead  |
# | *args                | Collects extra positional args into tuple         |
# | **kwargs             | Collects extra keyword args into dict             |
# | Pass by object ref   | Reference passed — mutation visible, rebind local |
# | First-class function | Functions are objects — assign, pass, return them |
# | Lambda               | One-line anonymous function — use for simple ops  |
# | LEGB                 | Local → Enclosing → Global → Built-in scope order |
# | global               | Declare to modify global variable inside function |
# | nonlocal             | Declare to modify enclosing variable in closure   |
#
# GOLDEN RULES:
# 1. Never use mutable objects as default args — use None instead
# 2. Mutation of mutable args is visible outside — rebinding is not
# 3. Functions are first-class — pass them, return them, store them
# 4. Lambda for simple one-liners, def for anything complex
# 5. LEGB — Python looks Local first, then outward to Built-in
# 6. Use global/nonlocal sparingly — prefer returning values
#
# =============================================================================
