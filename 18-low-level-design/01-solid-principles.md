# SOLID Principles

SOLID is a mnemonic acronym for five design principles intended to make software designs more understandable, flexible, and maintainable.

> **Note**: Python code examples below use `ABC` and `@abstractmethod` from the `abc` module.

> **Prerequisites:** [Chapter 18 README](./README.md)

## 1. S: Single Responsibility Principle (SRP)

**Definition**: A class should have one, and only one, reason to change.

### How to Recognize Violation
- **The "And" Test**: If you describe what a class does and use the word "and", it's likely violating SRP. ("It calculates salary *and* formats the report").
- **Fat Class**: Too many imports from unrelated modules (e.g., `import sqlalchemy` and `import matplotlib`).
- **Frequent Changes**: If multiple unrelated feature requests lead to changes in the same file.

### Building Intuition
Imagine a Swiss Army Knife. It's great for camping, but if the screwdriver part breaks, you might have to replace the whole knife. In software, if a class handles "Calculating Salary" AND "Saving to Database", a change in the database schema might break the salary calculation logic.

### Python Example
```python
# ❌ BAD: Multiple responsibilities
class Employee:
    def calculate_salary(self):
        pass
    def save_to_db(self):
        pass

# ✅ GOOD: Separated responsibilities
class Employee:
    def calculate_salary(self):
        pass

class EmployeeRepository:
    def save(self, employee):
        pass
```

---

## 2. O: Open/Closed Principle (OCP)

**Definition**: Software entities should be open for extension, but closed for modification.

### How to Recognize Violation
- **Giant If/Else or Switch Blocks**: If you find yourself adding a new `elif` every time a new business requirement comes in (e.g., `if type == 'CREDIT_CARD'`, `elif type == 'CRYPTO'`).
- **Fear of Breaking Things**: If adding a new feature requires you to change code that has been working for months.

### Building Intuition
You should be able to add new functionality without touching existing code. This prevents "regression bugs" where fixing one thing breaks another.

### Python Example
```python
from abc import ABC, abstractmethod

# ❌ BAD: Modifying class for new types
class Discount:
    def apply(self, price, type):
        if type == "VIP": return price * 0.8
        elif type == "SALE": return price * 0.9

# ✅ GOOD: Extension via inheritance/interfaces
class Discount(ABC):
    @abstractmethod
    def apply(self, price): pass

class VIPDiscount(Discount):
    def apply(self, price): return price * 0.8

class SaleDiscount(Discount):
    def apply(self, price): return price * 0.9
```

---

## 3. L: Liskov Substitution Principle (LSP)

**Definition**: Objects of a superclass should be replaceable with objects of its subclasses without breaking the application.

### How to Recognize Violation
- **`isinstance()` checks**: If you see code like `if isinstance(obj, Ostrich): raise Error()`, you are violating LSP.
- **Empty Method Overrides**: If a subclass implements a method from an interface with `pass` or `raise NotImplementedError`.
- **Strengthening Pre-conditions**: If a subclass requires more strict input than the parent.

### Building Intuition
If `Ostrich` is a subclass of `Bird`, but `Bird` has a `fly()` method, you can't substitute `Bird` with `Ostrich` everywhere without potential crashes.

### Python Example
```python
# ❌ BAD: Subclass breaks superclass contract
class Bird:
    def fly(self): pass

class Ostrich(Bird):
    def fly(self):
        raise Exception("Can't fly") # Breaking substitution

# ✅ GOOD: Better hierarchy
class Bird: pass
class FlyingBird(Bird):
    def fly(self): pass
class Ostrich(Bird): pass
```

---

## 4. I: Interface Segregation Principle (ISP)

**Definition**: No client should be forced to depend on methods it does not use.

### How to Recognize Violation
- **"Polluted" Interfaces**: An interface has 20 methods, but most implementations only care about 3.
- **Throwing `UnsupportedOperationException`**: Similar to LSP, if you are forced to implement a method just to throw an error.

### Building Intuition
Instead of one "Fat Interface", create many small, specific ones. A `SimplePrinter` shouldn't be forced to implement `scan()` or `fax()`.

### Python Example
```python
from abc import ABC, abstractmethod

# ❌ BAD: Fat interface
class SmartDevice(ABC):
    @abstractmethod
    def print(self): pass
    @abstractmethod
    def fax(self): pass

class BasicPrinter(SmartDevice):
    def print(self): print("Printing")
    def fax(self): raise NotImplementedError() # Forced to implement

# ✅ GOOD: Segregated interfaces
class Printer(ABC):
    @abstractmethod
    def print(self): pass

class Fax(ABC):
    @abstractmethod
    def fax(self): pass

class BasicPrinter(Printer):
    def print(self): print("Printing")
```

---

## 5. D: Dependency Inversion Principle (DIP)

**Definition**: High-level modules should not depend on low-level modules. Both should depend on abstractions.

### How to Recognize Violation
- **`new` keyword everywhere**: (In Python, direct class instantiation like `self.db = MySQLDB()`). This hardcodes the dependency.
- **Hard to Test**: If you can't unit test a class without setting up a real database or network connection.

### Building Intuition
Your laptop doesn't care if you plug in a Dell monitor or an LG monitor, because both use the **HDMI interface**. The laptop (high-level) doesn't depend on the specific monitor (low-level), but on the HDMI standard (abstraction).

### Python Example
```python
# ❌ BAD: High-level depends on low-level
class SQLDatabase:
    def save(self, data): pass

class UserRepo:
    def __init__(self):
        self.db = SQLDatabase() # Hard dependency

# ✅ GOOD: Depend on abstraction
class Database(ABC):
    @abstractmethod
    def save(self, data): pass

class UserRepo:
    def __init__(self, db: Database):
        self.db = db # Dependency injection
```


## Practice Problem: Design a Notification System
Apply SOLID to design a system that supports Email and SMS notifications, and can easily add Push notifications later.
