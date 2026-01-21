# Decorators and Context Managers

Decorators and Context Managers are structural patterns that allow you to inject logic around functions or blocks of code, promoting DRY (Don't Repeat Yourself) principles and safe resource management.

## 1. Closures: The Foundation

A decorator is essentially a function that returns a **closure**. A closure is a function object that remembers values in enclosing scopes even if they are not present in memory.

```python
def outer(message):
    def inner():
        print(message)
    return inner

hi_func = outer("Hi")
hi_func()  # Remembers "Hi" via __closure__ attribute
```

---

## 2. Decorators

Decorators allow you to "wrap" another function to extend its behavior without permanently modifying it.

### Standard Decorator
```python
import functools

def logger(func):
    @functools.wraps(func)  # Preserves metadata (__name__, __doc__)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@logger
def add(a, b):
    return a + b
```

### Decorators with Arguments
To pass arguments to a decorator, you need **three levels** of nested functions.
```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    print(f"Hello {name}")
```

### Class-Based Decorators
Useful for maintaining state across calls.
```python
class CallCounter:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)
```

---

## 3. Context Managers (`with` statement)

Context managers ensure that resources (files, network connections, locks) are properly cleaned up, even if an error occurs.

### The Protocol: `__enter__` and `__exit__`
```python
class ManagedFile:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, 'w')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        # Returning True would suppress exceptions
```

### The `contextlib` approach
For simpler logic, use the `@contextmanager` decorator.
```python
from contextlib import contextmanager

@contextmanager
def temp_lock(lock):
    lock.acquire()
    try:
        yield
    finally:
        lock.release()
```

---

## 4. Staff-Level Use Cases

1.  **Rate Limiting**: Decorators that track call frequency and sleep or raise exceptions if exceeded.
2.  **Circuit Breaker**: Wrapping external API calls to "trip" if failures exceed a threshold.
3.  **Telemetry**: Auto-injecting span IDs for distributed tracing (OpenTelemetry).
4.  **Transaction Management**: Context managers that handle DB `commit` on success and `rollback` on exception.
