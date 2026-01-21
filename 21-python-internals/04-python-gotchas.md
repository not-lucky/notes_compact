# Python Gotchas

Even experienced developers fall into these common traps. Understanding *why* these happen requires knowledge of Python's internal evaluation and object model.

## 1. Mutable Default Arguments

```mermaid
graph TD
    subgraph "Function Definition Time"
    FD[Define function] --> CA[Create 'box' list in memory]
    end
    subgraph "Call 1"
    C1[add_item(1)] --> M1[Append 1 to 'box']
    end
    subgraph "Call 2"
    C2[add_item(2)] --> M2[Append 2 to 'box']
    end
    CA --> M1
    M1 --> M2
```

This is perhaps the most famous Python trap.

```python
def add_item(item, box=[]):
    box.append(item)
    return box

print(add_item(1))  # [1]
print(add_item(2))  # [1, 2] -- Wait, why?
```

**Why?** Default arguments are evaluated **once** at the time the function is defined, not every time it's called. The `box` list object is created at definition and persists across calls.

**The Fix**:
```python
def add_item(item, box=None):
    if box is None:
        box = []
    ...
```

---

## 2. Late Binding in Closures

```python
def create_multipliers():
    return [lambda x: i * x for i in range(4)]

multipliers = create_multipliers()
print([m(2) for m in multipliers])  # Output: [6, 6, 6, 6]
```

**Why?** Python's closures are **late-binding**. The variable `i` is looked up at the time the function is *called*, not when it's defined. By the time the lambdas are called, the loop has finished and `i` is 3.

**The Fix (Force Early Binding)**:
```python
return [lambda x, i=i: i * x for i in range(4)] # i=i captures the value at definition
```

---

## 3. `is` vs `==`

*   `==`: Checks for **Value Equality** (calls `__eq__`).
*   `is`: Checks for **Identity** (compares memory addresses/IDs).

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b) # True
print(a is b) # False
```

### The "Interning" Confusion
Python interns small integers (-5 to 256) and some strings for performance.
```python
x = 256
y = 256
print(x is y) # True (due to interning)

x = 257
y = 257
print(x is y) # False (usually, though REPL behavior varies)
```

---

## 4. Class Variables vs Instance Variables

```python
class Dog:
    tricks = []  # Class variable (shared by all instances!)

    def add_trick(self, trick):
        self.tricks.append(trick)

d1 = Dog()
d2 = Dog()
d1.add_trick("roll over")
print(d2.tricks) # ["roll over"]
```

**Why?** Mutable class variables suffer from the same shared-state problem as mutable default arguments.

---

## 5. Modifying a List while Iterating

```python
nums = [1, 2, 3, 4, 5]
for x in nums:
    if x % 2 == 0:
        nums.remove(x)
print(nums) # [1, 3, 5] -- Works? Try [1, 2, 2, 3]
```

**Why?** Removing items shifts the indices of the remaining items. The iterator, which tracks its current index, will skip the element immediately following a removed one.

**The Fix**: Iterate over a copy (`for x in nums[:]`) or use a list comprehension.
