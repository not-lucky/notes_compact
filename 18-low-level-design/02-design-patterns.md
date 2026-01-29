# Design Patterns

Design patterns are typical solutions to common problems in software design. They are like pre-made blueprints that you can customize to solve a recurring design problem in your code.

> **Prerequisites:** [SOLID Principles](./01-solid-principles.md)

## 1. Creational Patterns
How objects are created, abstracting the instantiation process.

### Singleton
Ensures a class has only one instance and provides a global point of access to it.
- **How to recognize**: When you need a single shared resource (e.g., a Database connection, a Logger, or a Configuration manager).
- **Interviewer favorite**: "How do you make it thread-safe?" (Double-checked locking).
- **Use case**: Database connection pool, Logging service.

> **Interview Tip: Thread-safe Singleton in Python**
> In a multi-threaded environment, a simple Singleton can fail. Use a lock to ensure only one instance is created:
> ```python
> import threading
> class Singleton:
>     _instance = None
>     _lock = threading.Lock()
>     def __new__(cls):
>         with cls._lock: # First check
>             if not cls._instance:
>                 cls._instance = super().__new__(cls)
>         return cls._instance
> ```

### Factory Method
Provides an interface for creating objects in a superclass, but allows subclasses to alter the type of objects that will be created.
- **How to recognize**: When the exact type of the object isn't known until runtime (e.g., reading a file extension to decide which parser to use).
- **Use case**: A document reader that supports PDF, Docx, and TXT.

### Abstract Factory
Provides an interface for creating families of related or dependent objects without specifying their concrete classes.
- **How to recognize**: When you have multiple families of products that should be used together (e.g., Windows buttons must go with Windows checkboxes).
- **Use case**: A UI toolkit that creates Windows-style vs Mac-style buttons and checkboxes.

### Builder
Separates the construction of a complex object from its representation.
- **How to recognize**: When an object has many optional parameters or a complex construction process (the "Telescoping Constructor" problem).
- **Use case**: A `QueryBuilder` for SQL or a `PizzaBuilder` with many toppings.

---

## 2. Structural Patterns
How classes and objects are composed to form larger structures.

### Adapter
Allows objects with incompatible interfaces to collaborate.
- **How to recognize**: When you have an existing class but its interface doesn't match the one you need (e.g., a 3rd party API that returns XML while your app expects JSON).
- **Use case**: Integrating a 3rd party legacy library into your modern system.

### Proxy
Provides a surrogate or placeholder for another object to control access to it.
- **How to recognize**: When you need to add "extra" behavior (logging, caching, auth) before/after accessing an object without changing the object itself.
- **Use case**: Lazy loading a heavy object (like an image) or adding an auth layer to a service.

### Facade
Provides a simplified interface to a library, a framework, or any other complex set of classes.
- **How to recognize**: When a subsystem is complex or difficult to use because it has many moving parts.
- **Use case**: A `Computer` class that simplifies the process of starting many subsystems (CPU, RAM, HDD).

### Decorator
Lets you attach new behaviors to objects by placing these objects inside special wrapper objects that contain the behaviors.
- **How to recognize**: When you want to add responsibilities to individual objects dynamically and transparently, without affecting other objects.
- **Use case**: Adding scrollbars to a window, or encryption to a data stream.

---

## 3. Behavioral Patterns
Concerned with algorithms and the assignment of responsibilities between objects.

### Observer
Defines a subscription mechanism to notify multiple objects about any events that happen to the object they’re observing.
- **How to recognize**: When a change to one object requires changing others, and you don't know how many objects need to be changed.
- **Use case**: A YouTube channel notifying subscribers of a new video.

### Command
Turns a request into a stand-alone object that contains all information about the request.
- **How to recognize**: When you want to parametrize objects with operations, queue operations, or support undoable operations.
- **Use case**: A remote control where each button is a command, allowing for "Undo" functionality.

### State
Allows an object to alter its behavior when its internal state changes.
- **How to recognize**: When an object's behavior depends on its state, and it must change its behavior at runtime (avoids giant `if/else` on `self.status`).
- **Use case**: An ATM machine (Idle, HasCard, NoCash) or a Vending Machine.

### Strategy
Defines a family of algorithms, puts each of them into a separate class, and makes their objects interchangeable.
- **How to recognize**: When you have multiple ways of doing the same thing and want to switch between them at runtime.
- **Use case**: Different pathfinding algorithms (Dijkstra vs A*) in a navigation app or different payment methods.

### Template Method
Defines the skeleton of an algorithm in the superclass but lets subclasses override specific steps of the algorithm without changing its structure.
- **How to recognize**: When you have a fixed workflow but individual steps might vary.
- **Use case**: A data mining tool where the sequence of steps (open, extract, parse, close) is fixed, but the extraction logic varies by file type.

---

## Pattern Summary Table

| Pattern | Type | Key Goal | Pitfalls |
|---------|------|----------|----------|
| **Singleton** | Creational | One instance only | Hard to test, hidden dependencies |
| **Factory** | Creational | Defer instantiation | Can lead to many subclasses |
| **Abstract Factory** | Creational | Families of objects | Complex to implement initially |
| **Adapter** | Structural | Interface translation | Adds overhead with wrapper classes |
| **Proxy** | Structural | Access control/Lazy load | May delay responses, adds complexity |
| **Facade** | Structural | Simple interface | Can become a "God Object" |
| **Strategy** | Behavioral | Swappable algorithms | Client must know about different strategies |
| **Observer** | Behavioral | Event notification | Memory leaks if not unsubscribed |
| **Command** | Behavioral | Request as object | Code bloat with many small classes |
| **Template** | Behavioral | Algorithm skeleton | Liskov Substitution violations possible |
