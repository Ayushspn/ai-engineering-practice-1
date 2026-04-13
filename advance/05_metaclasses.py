# =============================================================================
# 05_metaclasses.py — Metaclasses in Python
# python-ai-journey | 03_advanced
# =============================================================================
#
# THEORY:
# -------
# A metaclass is a class whose INSTANCES are classes!
#
# Normal class:   Dog → instances are objects (dog1, dog2)
# Metaclass:      type → instances are classes (Dog, Cat, int, str)
#
# 'type' is the default metaclass — it creates ALL classes in Python!
#
# Key concepts:
#   1. type()         — creates classes dynamically
#   2. __new__        — controls class CREATION
#   3. __init__       — controls class INITIALIZATION
#   4. Custom metaclass — control how classes behave
#   5. __prepare__    — controls class namespace
#   6. Real world use cases
#
# INTERNALS (CPython):
# ---------------------
# When Python sees 'class Dog:':
#   1. Calls type.__prepare__() → creates empty namespace dict
#   2. Executes class body → populates namespace
#   3. Calls type.__new__()  → creates PyTypeObject
#   4. Calls type.__init__() → initializes the class
#
# Custom metaclass intercepts these steps:
#   → can modify class before it's created
#   → can add/remove methods automatically
#   → can enforce rules on all subclasses
#
# =============================================================================


# =============================================================================
# PART 1: type — THE METACLASS
# =============================================================================

print("=" * 60)
print("PART 1: type — THE METACLASS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 1: Everything is an Instance of type
# -----------------------------------------------------------------------------

print("\n--- Everything is Instance of type ---")

# Normal objects — instances of their class
x    = 42
name = "Ayush"
lst  = [1, 2, 3]

print(f"type(42):        {type(x)}")       # <class 'int'>
print(f"type('Ayush'):   {type(name)}")    # <class 'str'>
print(f"type([1,2,3]):   {type(lst)}")     # <class 'list'>

# Classes — instances of type!
print(f"\ntype(int):       {type(int)}")   # <class 'type'>
print(f"type(str):       {type(str)}")    # <class 'type'>
print(f"type(list):      {type(list)}")   # <class 'type'>

# Your custom classes — also instances of type!
class Dog:
    pass

class Person:
    name = "Ayush"

print(f"\ntype(Dog):       {type(Dog)}")    # <class 'type'>
print(f"type(Person):    {type(Person)}") # <class 'type'>

# The hierarchy:
# type → Dog → dog1
# type creates Dog
# Dog creates dog1

dog1 = Dog()
print(f"\ntype(dog1):      {type(dog1)}")   # <class 'Dog'>
print(f"type(Dog):       {type(Dog)}")     # <class 'type'>
print(f"type(type):      {type(type)}")    # <class 'type'> ← type is its own metaclass!


# -----------------------------------------------------------------------------
# SECTION 2: Creating Classes with type()
# -----------------------------------------------------------------------------

print("\n--- Creating Classes with type() ---")

# type() with 3 arguments creates a NEW class:
# type(name, bases, dict)
#       ↑      ↑      ↑
#    class   parent  methods/attributes
#    name    classes

# Create simple class using type()
Animal = type(
    "Animal",           # class name
    (object,),          # parent classes (tuple!)
    {                   # class body — methods and attributes
        "species": "Unknown",
        "breathe": lambda self: print(f"  {self.__class__.__name__} breathes!"),
    }
)

# Use it like a normal class!
a = Animal()
a.breathe()
print(f"  Animal.species: {Animal.species}")
print(f"  type(Animal):   {type(Animal)}")   # <class 'type'>

# Create class with inheritance
Dog = type(
    "Dog",
    (Animal,),           # inherits from Animal!
    {
        "species": "Canis lupus",
        "bark": lambda self: print("  Woof!"),
        "__init__": lambda self, name: setattr(self, "name", name),
        "__str__": lambda self: f"Dog({self.name})",
    }
)

dog = Dog("Bruno")
dog.breathe()    # inherited from Animal!
dog.bark()       # Dog's own method
print(f"  {dog}")
print(f"  isinstance(dog, Animal): {isinstance(dog, Animal)}")   # True!

# This is EXACTLY what Python does when you write 'class Dog(Animal):'!
print("\n  The above is equivalent to:")
print("  class Dog(Animal):")
print("      species = 'Canis lupus'")
print("      def bark(self): print('Woof!')")


# =============================================================================
# PART 2: CUSTOM METACLASSES
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: CUSTOM METACLASSES")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 3: Creating a Custom Metaclass
# -----------------------------------------------------------------------------

print("\n--- Custom Metaclass ---")

# A metaclass inherits from 'type'
# Override __new__ to control class CREATION
# Override __init__ to control class INITIALIZATION

class LoggingMeta(type):
    """
    Metaclass that logs every class creation.
    Any class using this metaclass will be logged!
    """

    def __new__(mcs, name, bases, namespace):
        # mcs      = the metaclass itself (LoggingMeta)
        # name     = name of class being created
        # bases    = parent classes
        # namespace= class body (methods, attributes)

        print(f"  Creating class: '{name}'")
        print(f"  Parent classes: {[b.__name__ for b in bases]}")
        print(f"  Methods: {[k for k in namespace if not k.startswith('__')]}")

        # Create the class using type.__new__()
        cls = super().__new__(mcs, name, bases, namespace)
        return cls

    def __init__(cls, name, bases, namespace):
        # Called AFTER __new__ — class already created
        print(f"  Initialized class: '{name}'")
        super().__init__(name, bases, namespace)


# Use metaclass= to specify which metaclass to use
class Vehicle(metaclass=LoggingMeta):   # LoggingMeta creates this class!
    def __init__(self, brand):
        self.brand = brand

    def drive(self):
        print(f"  {self.brand} is driving!")

print()

class Car(Vehicle):                     # LoggingMeta creates this too!
    def honk(self):
        print(f"  {self.brand}: Beep!")

print()

# Use them normally
car = Car("Toyota")
car.drive()
car.honk()


# -----------------------------------------------------------------------------
# SECTION 4: Metaclass for Validation
# -----------------------------------------------------------------------------

print("\n--- Validation Metaclass ---")

class ValidatedMeta(type):
    """
    Metaclass that enforces rules on class creation.
    Raises error if required methods are missing!
    """

    # Required methods every class must implement
    REQUIRED_METHODS = ["validate", "save"]

    def __new__(mcs, name, bases, namespace):
        # Skip validation for base classes
        if bases:    # has parent class → it's a subclass → validate!
            missing = [
                method
                for method in mcs.REQUIRED_METHODS
                if method not in namespace
            ]
            if missing:
                raise TypeError(
                    f"Class '{name}' must implement: {missing}"
                )
        return super().__new__(mcs, name, bases, namespace)


# Base class — no validation (no parent classes)
class Model(metaclass=ValidatedMeta):
    pass

# Good subclass — implements required methods
class UserModel(Model):
    def validate(self):
        print("  Validating user...")
        return True

    def save(self):
        print("  Saving user to DB...")

# Bad subclass — missing required methods
try:
    class BadModel(Model):
        def validate(self):   # has validate but missing save!
            pass
        # save() is missing!
except TypeError as e:
    print(f"  Error creating BadModel: {e}")

# Good class works fine
user = UserModel()
user.validate()
user.save()


# -----------------------------------------------------------------------------
# SECTION 5: Metaclass for Auto-Registration
# -----------------------------------------------------------------------------

print("\n--- Auto-Registration Metaclass ---")

class PluginMeta(type):
    """
    Metaclass that automatically registers all subclasses.
    Perfect for plugin systems!
    """
    # Class-level registry — shared across all classes!
    registry = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        # Register every class except the base class
        if bases:    # only register subclasses
            plugin_name = namespace.get("name", name.lower())
            mcs.registry[plugin_name] = cls
            print(f"  Registered plugin: '{plugin_name}' → {name}")

        return cls


# Base plugin class
class Plugin(metaclass=PluginMeta):
    name = "base"

# These automatically register themselves!
class JSONPlugin(Plugin):
    name = "json"

    def process(self, data):
        import json
        return json.dumps(data)

class CSVPlugin(Plugin):
    name = "csv"

    def process(self, data):
        return ",".join(str(x) for x in data)

class XMLPlugin(Plugin):
    name = "xml"

    def process(self, data):
        return f"<data>{data}</data>"

# Look up plugins from registry!
print(f"\n  Registry: {list(PluginMeta.registry.keys())}")

# Use plugin by name
def get_plugin(name):
    plugin_class = PluginMeta.registry.get(name)
    if not plugin_class:
        raise ValueError(f"Plugin '{name}' not found!")
    return plugin_class()

json_plugin = get_plugin("json")
csv_plugin  = get_plugin("csv")

print(f"  JSON: {json_plugin.process({'name': 'Ayush'})}")
print(f"  CSV:  {csv_plugin.process([1, 2, 3, 4, 5])}")


# -----------------------------------------------------------------------------
# SECTION 6: Singleton Metaclass
# -----------------------------------------------------------------------------

print("\n--- Singleton Metaclass ---")

class SingletonMeta(type):
    """
    Metaclass that ensures only ONE instance exists!
    Perfect for config managers, DB connections, etc.
    """
    # stores single instance per class
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # __call__ runs when you do ClassName()
        if cls not in cls._instances:
            # first time → create instance
            print(f"  Creating singleton instance of {cls.__name__}")
            cls._instances[cls] = super().__call__(*args, **kwargs)
        else:
            # already exists → return same instance!
            print(f"  Returning existing singleton of {cls.__name__}")
        return cls._instances[cls]


class DatabaseConfig(metaclass=SingletonMeta):
    def __init__(self):
        self.host = "localhost"
        self.port = 5432

class AppConfig(metaclass=SingletonMeta):
    def __init__(self):
        self.debug = True
        self.version = "1.0"


# Test singleton behavior
db1 = DatabaseConfig()   # creates new instance
db2 = DatabaseConfig()   # returns SAME instance!
db3 = DatabaseConfig()   # returns SAME instance!

print(f"\n  db1 is db2: {db1 is db2}")   # True!
print(f"  db2 is db3: {db2 is db3}")   # True!
print(f"  All same object: {id(db1) == id(db2) == id(db3)}")   # True!

app1 = AppConfig()
app2 = AppConfig()
print(f"  app1 is app2: {app1 is app2}")   # True!


# =============================================================================
# PART 3: __new__ vs __init__ IN DEPTH
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: __new__ vs __init__")
print("=" * 60)

print("\n--- __new__ vs __init__ ---")

class MyClass:
    def __new__(cls, *args, **kwargs):
        # __new__ creates the OBJECT
        # cls = the class itself
        print(f"  __new__: Creating instance of {cls.__name__}")
        instance = super().__new__(cls)   # actually create the object!
        return instance    # MUST return instance!

    def __init__(self, value):
        # __init__ INITIALIZES the already-created object
        # self = the instance created by __new__
        print(f"  __init__: Initializing with value={value}")
        self.value = value

obj = MyClass(42)
print(f"  obj.value: {obj.value}")

# Order:
# 1. __new__  → creates empty object → returns it
# 2. __init__ → receives that object as 'self' → initializes it


# =============================================================================
# PART 4: REAL WORLD USE CASES
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: REAL WORLD USE CASES")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 7: ORM-Style Metaclass (like Django Models!)
# -----------------------------------------------------------------------------

print("\n--- ORM-Style Metaclass ---")

class ORMMeta(type):
    """
    Simplified ORM metaclass — like Django's Model!
    Automatically collects field definitions.
    """

    def __new__(mcs, name, bases, namespace):
        # Collect all Field instances from class body
        fields = {
            key: value
            for key, value in namespace.items()
            if isinstance(value, Field)
        }

        # Store fields on class
        namespace["_fields"] = fields

        # Add table name automatically
        namespace["_table"] = name.lower() + "s"

        cls = super().__new__(mcs, name, bases, namespace)
        return cls


class Field:
    """Represents a database field"""
    def __init__(self, field_type, required=True):
        self.field_type = field_type
        self.required   = required

    def __repr__(self):
        return f"Field({self.field_type.__name__})"


class BaseModel(metaclass=ORMMeta):
    """Base class for all ORM models"""

    def save(self):
        print(f"  INSERT INTO {self._table} VALUES (...)")

    def __repr__(self):
        values = {k: getattr(self, k, None) for k in self._fields}
        return f"{self.__class__.__name__}({values})"


# Define models — just like Django!
class User(BaseModel):
    name  = Field(str)
    age   = Field(int)
    email = Field(str)

class Product(BaseModel):
    title = Field(str)
    price = Field(float)
    stock = Field(int, required=False)


# Inspect what metaclass did automatically!
print(f"  User._table:    {User._table}")      # 'users'
print(f"  User._fields:   {User._fields}")     # all fields!
print(f"  Product._table: {Product._table}")   # 'products'
print(f"  Product._fields:{Product._fields}")


# -----------------------------------------------------------------------------
# SECTION 8: API Rate Limiter Metaclass
# -----------------------------------------------------------------------------

print("\n--- Rate Limiter Metaclass ---")

import time

class RateLimitedMeta(type):
    """
    Metaclass that adds rate limiting to all methods!
    Every method call is tracked and limited.
    """

    def __new__(mcs, name, bases, namespace):
        # Wrap every method with rate limiting
        for attr_name, attr_value in namespace.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                namespace[attr_name] = mcs._rate_limit(attr_value)

        return super().__new__(mcs, name, bases, namespace)

    @staticmethod
    def _rate_limit(func):
        """Wraps function to track calls"""
        call_count = [0]    # list to allow mutation in closure

        def wrapper(*args, **kwargs):
            call_count[0] += 1
            print(f"  [{func.__name__}] Call #{call_count[0]}")
            return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper


class APIClient(metaclass=RateLimitedMeta):
    def get_users(self):
        return [{"id": 1, "name": "Ayush"}]

    def get_orders(self):
        return [{"id": 1, "product": "laptop"}]


client = APIClient()
client.get_users()
client.get_users()    # tracked!
client.get_orders()
client.get_users()    # tracked — call #3!


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Concept           | Key Insight                                          |
# |-------------------|------------------------------------------------------|
# | type              | Default metaclass — creates ALL classes in Python    |
# | type(name,b,d)    | Creates class dynamically with 3 arguments           |
# | Metaclass         | Class whose instances are classes!                   |
# | class Foo(meta=X) | Use X as metaclass instead of type                  |
# | __new__(mcs,...) | Controls class CREATION — returns new class          |
# | __init__(cls,...) | Controls class INITIALIZATION — after __new__        |
# | __call__(cls,...) | Controls what happens when class is called ()        |
# | Real world uses:  |                                                      |
# |   Logging         | Log every class creation automatically               |
# |   Validation      | Enforce required methods on subclasses               |
# |   Registration    | Auto-register plugins/handlers                       |
# |   Singleton       | Ensure only one instance exists                      |
# |   ORM             | Collect field definitions (like Django!)              |
#
# GOLDEN RULES:
# 1. type is the metaclass of all classes — even itself!
# 2. Metaclass __new__ receives: (mcs, name, bases, namespace)
# 3. Must call super().__new__() to actually create the class
# 4. Use metaclass= keyword to specify custom metaclass
# 5. Metaclass affects the class AND all its subclasses!
# 6. Don't overuse metaclasses — prefer decorators or __init_subclass__
# 7. Django uses metaclass for its ORM — that's why models work magically!
#
# =============================================================================
