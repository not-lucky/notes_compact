# Generators and Iterators

In Python, iterators and generators are the foundation of "Lazy Evaluation"—the practice of delaying computation until the value is actually needed. This is crucial for processing massive datasets that don't fit in memory.

## 1. The Iterator Protocol

An object is an **Iterable** if it defines `__iter__()`. An object is an **Iterator** if it defines both `__iter__()` and `__next__()`.

### How `for` loops work under the hood:
```python
items = [1, 2, 3]
it = iter(items)  # Calls items.__iter__()
while True:
    try:
        x = next(it)  # Calls it.__next__()
        print(x)
    except StopIteration:
        break
```

*   **`__iter__`**: Must return the iterator object itself.
*   **`__next__`**: Returns the next value. If no more values, raises `StopIteration`.

---

## 2. Generators: The `yield` Keyword

Generators are a simple way to create iterators using functions. When a function contains the `yield` keyword, it becomes a **Generator Function**.

### State Preservation
Unlike regular functions that return a value and destroy their local scope, a generator **suspends** execution and saves its entire state (local variables, instruction pointer) when it encounters `yield`.

```python
def fibonacci_gen():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

gen = fibonacci_gen()
print(next(gen))  # 0
print(next(gen))  # 1
```

### Benefits for Senior Engineers:
1.  **Memory Efficiency**: Yielding one item at a time instead of returning a massive list.
2.  **Pipelining**: You can chain generators together (e.g., `gen1` feeds `gen2`), creating efficient data processing pipelines.
3.  **Representing Infinite Streams**: Like the Fibonacci example above.

---

## 3. Advanced Generator Features

### `yield from`
Introduced in Python 3.3, it allows a generator to delegate part of its operations to another generator. It also handles the "sub-generator" interface, passing `send()`, `throw()`, and `close()` calls down to the delegated generator.

```python
def count(n):
    yield from range(n)
```

### Generator as Coroutines
Generators can receive data using `.send(value)`. This was the precursor to modern `async/await`.

```python
def receiver():
    while True:
        val = yield
        print(f"Received: {val}")

r = receiver()
next(r)  # Prime the generator (advance to the first yield)
r.send("Hello")
```

---

## 4. Performance Comparison

| Feature | List Comprehension | Generator Expression |
| :--- | :--- | :--- |
| **Syntax** | `[x*x for x in data]` | `(x*x for x in data)` |
| **Execution** | Eager (Immediate) | Lazy (On-demand) |
| **Memory** | $O(N)$ | $O(1)$ |
| **Access** | Random Access (Indexable) | Sequential Only |

**Staff Tip**: When designing APIs that return collections, default to returning an **Iterator** or **Generator** if the collection size is non-trivial or unknown. This gives the caller the flexibility to consume it lazily or convert it to a list if needed.
