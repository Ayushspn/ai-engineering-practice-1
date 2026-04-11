# =============================================================================
# 04_oop_basics.py — Object Oriented Programming in Python
# python-ai-journey | 02_intermediate
# =============================================================================
#
# THEORY:
# -------
# OOP organizes code around OBJECTS — entities that combine:
#   - Data       (attributes/variables)
#   - Behavior   (methods/functions)
#
# Four pillars of OOP:
#   1. Encapsulation  — bundle data + behavior, control access
#   2. Inheritance    — child class inherits from parent class
#   3. Polymorphism   — same interface, different behavior
#   4. Abstraction    — hide complexity, expose only essentials
#
# Key concepts:
#   - Class          — blueprint / template
#   - Object         — real instance created from class
#   - self           — reference to the current instance
#   - __init__       — constructor, runs on object creation
#   - Class variable — shared across ALL instances
#   - Instance var   — unique to each instance
#   - Dunder methods — special methods like __str__, __repr__, __len__
#
# INTERNALS (CPython):
# ---------------------
# 'class Dog:' creates a PyTypeObject on the heap:
#   - tp_name     → class name string
#   - tp_dict     → dict of methods and class variables
#   - tp_base     → pointer to parent class (default: object)
#   - tp_basicsize→ memory per instance
#
# 'dog1 = Dog()' creates a PyObject:
#   - ob_type     → points to Dog's PyTypeObject
#   - __dict__    → instance's own namespace dict {attr: value}
#
# Method resolution:
#   dog1.bark() → look in dog1.__dict__ → not found
#              → look in Dog.__dict__   → found! call with self=dog1
#
# 'self' is just the first parameter — Python passes the instance
# automatically when you call instance.method()
#
# =============================================================================


# =============================================================================
# PART 1: CLASS BASICS
# =============================================================================

print("=" * 60)
print("PART 1: CLASS BASICS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 1: Defining a Class
# -----------------------------------------------------------------------------

print("\n--- Basic Class ---")

class Dog:
    # Class variable — shared across ALL instances
    species = "Canis lupus familiaris"
    total_dogs = 0

    # Constructor — runs automatically when object is created
    def __init__(self, name, breed, age):
        # Instance variables — unique to each object
        self.name  = name
        self.breed = breed
        self.age   = age
        Dog.total_dogs += 1    # increment shared counter

    # Instance method — operates on the specific instance
    def bark(self):
        print(f"{self.name} says: Woof!")

    def describe(self):
        print(f"{self.name} is a {self.age}yr old {self.breed}")

    # __str__ — called by print() and str()
    def __str__(self):
        return f"Dog({self.name}, {self.breed}, {self.age}yrs)"

    # __repr__ — called by repr(), used in debugging
    def __repr__(self):
        return f"Dog(name={self.name!r}, breed={self.breed!r}, age={self.age})"


# Creating objects (instances)
dog1 = Dog("Bruno", "Labrador", 3)
dog2 = Dog("Coco",  "Poodle",   5)

dog1.bark()
dog2.bark()
dog1.describe()

# Class variable vs instance variable
print(f"\nClass variable:    Dog.species = {Dog.species}")
print(f"Shared counter:    Dog.total_dogs = {Dog.total_dogs}")
print(f"Instance var dog1: {dog1.name}, {dog1.breed}")
print(f"Instance var dog2: {dog2.name}, {dog2.breed}")

# __str__ and __repr__
print(f"\nprint(dog1): {dog1}")          # calls __str__
print(f"repr(dog1):  {repr(dog1)}")     # calls __repr__

# Inspecting object internals
print(f"\ndog1.__dict__: {dog1.__dict__}")   # instance namespace
print(f"Dog.__dict__ keys: {list(Dog.__dict__.keys())}")  # class namespace


# -----------------------------------------------------------------------------
# SECTION 2: Class vs Instance Variables — Deep Dive
# -----------------------------------------------------------------------------

print("\n--- Class vs Instance Variables ---")

class Counter:
    count = 0          # class variable — shared

    def __init__(self, name):
        self.name  = name       # instance variable — unique
        Counter.count += 1

    def show(self):
        print(f"  {self.name}: instance count access = {self.count}")
        print(f"  Counter.count (class) = {Counter.count}")

c1 = Counter("first")
c2 = Counter("second")
c3 = Counter("third")

c1.show()
c2.show()

# PITFALL: setting class variable via instance creates instance variable!
print(f"\nBefore: c1.count={c1.count}, Counter.count={Counter.count}")
c1.count = 99          # creates instance variable on c1, doesn't touch class!
print(f"After:  c1.count={c1.count}, Counter.count={Counter.count}")
print(f"c2.count still = {c2.count}")   # c2 still sees class variable


# =============================================================================
# PART 2: ENCAPSULATION
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: ENCAPSULATION")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 3: Access Control — Public, Protected, Private
# -----------------------------------------------------------------------------

print("\n--- Access Control ---")

class BankAccount:
    def __init__(self, owner, balance):
        self.owner      = owner       # public   — accessible anywhere
        self._balance   = balance     # protected — convention: don't touch
        self.__pin      = "1234"      # private  — name mangled by CPython

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"  Deposited {amount}. Balance: {self._balance}")

    def withdraw(self, amount):
        if amount > self._balance:
            print(f"  Insufficient funds!")
        else:
            self._balance -= amount
            print(f"  Withdrew {amount}. Balance: {self._balance}")

    def get_balance(self):
        return self._balance          # controlled access to protected attr

    def verify_pin(self, pin):
        return pin == self.__pin      # access private via method

    def __str__(self):
        return f"BankAccount({self.owner}, balance={self._balance})"


acc = BankAccount("Ayush", 10000)
acc.deposit(5000)
acc.withdraw(2000)

print(f"\nBalance via method: {acc.get_balance()}")
print(f"Pin valid: {acc.verify_pin('1234')}")

# Public — accessible directly
print(f"\nPublic:    acc.owner = {acc.owner}")

# Protected — accessible but convention says don't
print(f"Protected: acc._balance = {acc._balance}")   # works but bad practice

# Private — name mangled! Cannot access directly
try:
    print(acc.__pin)
except AttributeError as e:
    print(f"Private:   acc.__pin → {e}")

# CPython name mangling: __pin → _BankAccount__pin
print(f"Mangled:   acc._BankAccount__pin = {acc._BankAccount__pin}")


# -----------------------------------------------------------------------------
# SECTION 4: Properties — Getters and Setters
# -----------------------------------------------------------------------------

print("\n--- Properties ---")

class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        """Getter — called on temp.celsius"""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """Setter — called on temp.celsius = value"""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self):
        """Computed property — no setter needed"""
        return self._celsius * 9/5 + 32

    def __str__(self):
        return f"{self._celsius}°C / {self.fahrenheit}°F"


temp = Temperature(25)
print(f"Celsius:    {temp.celsius}")
print(f"Fahrenheit: {temp.fahrenheit}")
print(f"temp:       {temp}")

temp.celsius = 100        # calls setter
print(f"After set:  {temp}")

try:
    temp.celsius = -300   # below absolute zero!
except ValueError as e:
    print(f"Error: {e}")


# =============================================================================
# PART 3: INHERITANCE
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: INHERITANCE")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 5: Basic Inheritance
# -----------------------------------------------------------------------------

print("\n--- Basic Inheritance ---")

class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age  = age

    def eat(self):
        print(f"{self.name} is eating")

    def sleep(self):
        print(f"{self.name} is sleeping")

    def __str__(self):
        return f"{self.__class__.__name__}({self.name}, {self.age}yrs)"


class Dog(Animal):              # Dog inherits from Animal
    def __init__(self, name, age, breed):
        super().__init__(name, age)   # call parent __init__
        self.breed = breed

    def bark(self):             # new method — only in Dog
        print(f"{self.name} barks!")

    def eat(self):              # OVERRIDE parent method
        print(f"{self.name} eats dog food enthusiastically!")


class Cat(Animal):
    def __init__(self, name, age, indoor):
        super().__init__(name, age)
        self.indoor = indoor

    def meow(self):
        print(f"{self.name} meows!")

    def eat(self):              # OVERRIDE parent method
        print(f"{self.name} eats cat food delicately!")


dog = Dog("Bruno", 3, "Labrador")
cat = Cat("Whiskers", 2, True)

dog.eat()        # overridden method
dog.bark()       # Dog-specific method
dog.sleep()      # inherited from Animal

cat.eat()        # overridden method
cat.meow()       # Cat-specific method

print(f"\ndog: {dog}")
print(f"cat: {cat}")

# Check inheritance
print(f"\nisinstance(dog, Dog):    {isinstance(dog, Dog)}")
print(f"isinstance(dog, Animal): {isinstance(dog, Animal)}")   # True!
print(f"issubclass(Dog, Animal): {issubclass(Dog, Animal)}")


# -----------------------------------------------------------------------------
# SECTION 6: Method Resolution Order (MRO)
# -----------------------------------------------------------------------------

print("\n--- Method Resolution Order (MRO) ---")

class A:
    def hello(self):
        print("  Hello from A")

class B(A):
    def hello(self):
        print("  Hello from B")

class C(A):
    def hello(self):
        print("  Hello from C")

class D(B, C):      # multiple inheritance
    pass

d = D()
d.hello()           # which hello() is called?

# MRO — C3 linearization algorithm
print(f"\nD.mro(): {[cls.__name__ for cls in D.mro()]}")
# D → B → C → A → object
# Python searches left to right, depth first, no repeats


# =============================================================================
# PART 4: POLYMORPHISM
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: POLYMORPHISM")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 7: Polymorphism — Same Interface, Different Behavior
# -----------------------------------------------------------------------------

print("\n--- Polymorphism ---")

class Shape:
    def area(self):
        raise NotImplementedError("Subclass must implement area()")

    def describe(self):
        print(f"I am a {self.__class__.__name__} with area {self.area():.2f}")


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width  = width
        self.height = height

    def area(self):
        return self.width * self.height


class Triangle(Shape):
    def __init__(self, base, height):
        self.base   = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height


# Polymorphism in action — same interface, different behavior
shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8)]

print("All shapes using same .describe() interface:")
for shape in shapes:
    shape.describe()     # each calls its OWN area() implementation

# Total area — works for any shape!
total = sum(shape.area() for shape in shapes)
print(f"\nTotal area: {total:.2f}")


# -----------------------------------------------------------------------------
# SECTION 8: Dunder Methods — Operator Overloading
# -----------------------------------------------------------------------------

print("\n--- Dunder Methods ---")

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y})"

    def __add__(self, other):        # v1 + v2
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):        # v1 - v2
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):       # v1 * 3
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other):         # v1 == v2
        return self.x == other.x and self.y == other.y

    def __len__(self):               # len(v)
        return int((self.x**2 + self.y**2) ** 0.5)

    def __abs__(self):               # abs(v) — magnitude
        return (self.x**2 + self.y**2) ** 0.5


v1 = Vector(2, 3)
v2 = Vector(1, 4)

print(f"v1:       {v1}")
print(f"v2:       {v2}")
print(f"v1 + v2:  {v1 + v2}")      # calls __add__
print(f"v1 - v2:  {v1 - v2}")      # calls __sub__
print(f"v1 * 3:   {v1 * 3}")       # calls __mul__
print(f"v1 == v2: {v1 == v2}")     # calls __eq__
print(f"abs(v1):  {abs(v1):.2f}")  # calls __abs__


# -----------------------------------------------------------------------------
# SECTION 9: Class Methods and Static Methods
# -----------------------------------------------------------------------------

print("\n--- Class Methods and Static Methods ---")

class Person:
    population = 0

    def __init__(self, name, age):
        self.name = name
        self.age  = age
        Person.population += 1

    # Regular method — takes self (instance)
    def greet(self):
        print(f"Hi, I'm {self.name}")

    # Class method — takes cls (class), not instance
    @classmethod
    def get_population(cls):
        return cls.population

    # Class method as alternative constructor
    @classmethod
    def from_birth_year(cls, name, birth_year):
        age = 2026 - birth_year
        return cls(name, age)      # creates new Person instance

    # Static method — no self, no cls — just a utility function
    @staticmethod
    def is_adult(age):
        return age >= 18


p1 = Person("Ayush", 30)
p2 = Person("Rahul", 25)
p3 = Person.from_birth_year("Priya", 1995)   # alternative constructor

p1.greet()
p3.greet()

print(f"\nPopulation:       {Person.get_population()}")   # class method
print(f"Is adult (20):    {Person.is_adult(20)}")         # static method
print(f"Is adult (15):    {Person.is_adult(15)}")         # static method

# Difference summary:
# instance method → def method(self)     → access instance + class data
# class method    → def method(cls)      → access class data only
# static method   → def method()         → no access to instance or class


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Concept          | Key Insight                                           |
# |------------------|-------------------------------------------------------|
# | class            | PyTypeObject — blueprint stored once in memory        |
# | object/instance  | PyObject — real data, unique __dict__ per instance    |
# | self             | Reference to current instance — passed automatically  |
# | __init__         | Constructor — runs on object creation                 |
# | Class variable   | Shared across ALL instances — defined outside __init__|
# | Instance variable| Unique per object — defined with self. in __init__    |
# | Encapsulation    | _protected, __private (name mangled), @property       |
# | Inheritance      | Child gets parent's methods — super() calls parent    |
# | MRO              | C3 linearization — left to right, no repeats          |
# | Polymorphism     | Same interface, different behavior per class          |
# | Dunder methods   | __str__, __add__, __eq__ — operator overloading       |
# | @classmethod     | Takes cls — alternative constructors, class state     |
# | @staticmethod    | No self/cls — pure utility function inside class      |
#
# GOLDEN RULES:
# 1. Class variables are shared — instance variables are unique
# 2. Use super().__init__() to call parent constructor
# 3. __str__ for human-readable, __repr__ for debugging
# 4. @property for controlled attribute access with validation
# 5. MRO determines which method is called in multiple inheritance
# 6. Prefer composition over inheritance for complex systems
#
# =============================================================================
