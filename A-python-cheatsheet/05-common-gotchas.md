# Common Python Gotchas

> **Prerequisites:** Basic Python knowledge

## Interview Context

Python's design choices can trip you up in interviews. Knowing these gotchas helps you:

- **Avoid bugs**: Catch issues before the interviewer does
- **Explain trade-offs**: Show you understand the language deeply
- **Debug quickly**: Recognize common patterns of errors

---

## 1. Mutable Default Arguments

**The bug**: Default mutable arguments are shared across calls.

```python
# WRONG
def add_item(item, lst=[]):
    lst.append(item)
    return lst

print(add_item(1))  # [1]
print(add_item(2))  # [1, 2] - NOT [2]!
print(add_item(3))  # [1, 2, 3] - Keeps growing!

# The same list object is reused for all calls
```

**The fix**: Use `None` as default.

```python
# CORRECT
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(add_item(1))  # [1]
print(add_item(2))  # [2] - Fresh list each time
```

**Why it happens**: Default arguments are evaluated once when the function is defined, not each time it's called.

---

## 2. Shallow vs Deep Copy

**The bug**: Copying a list doesn't copy nested objects.

```python
# Shallow copy (default)
original = [[1, 2], [3, 4]]
shallow = original.copy()  # or list(original) or original[:]

shallow[0][0] = 999
print(original)  # [[999, 2], [3, 4]] - Original changed!

# The inner lists are the same objects
```

**The fix**: Use `deepcopy` for nested structures.

```python
import copy

# Deep copy
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)

deep[0][0] = 999
print(original)  # [[1, 2], [3, 4]] - Original unchanged
```

**Quick reference**:

```python
# Shallow copy methods (same result):
b = a.copy()
b = list(a)
b = a[:]
b = [x for x in a]

# Deep copy:
import copy
b = copy.deepcopy(a)
```

---

## 3. Integer Caching

**The gotcha**: Python caches small integers (-5 to 256).

```python
a = 256
b = 256
print(a is b)  # True - Same object

a = 257
b = 257
print(a is b)  # False - Different objects!

# ALWAYS use == for value comparison
print(a == b)  # True - Values are equal
```

**The rule**: Use `==` for value comparison, `is` only for `None` checks.

```python
# CORRECT
if x == 5:  # Value comparison
    ...

if x is None:  # Identity check (only for None)
    ...

# WRONG
if x is 5:  # Don't do this!
    ...
```

---

## 4. List Comprehension Scope

**The gotcha**: Loop variable leaks in Python 2, but not in list comprehensions in Python 3.

```python
# Loop variable leaks
for i in range(5):
    pass
print(i)  # 4 - Still accessible!

# List comprehension doesn't leak
[x for x in range(5)]
# print(x)  # NameError in Python 3
```

**The closure gotcha**:

```python
# WRONG - All functions capture the same i
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])  # [2, 2, 2] - All return 2!

# CORRECT - Capture i by default argument
funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])  # [0, 1, 2]
```

---

## 5. Modifying List While Iterating

**The bug**: Modifying a list while iterating over it causes unexpected behavior.

```python
# WRONG
nums = [1, 2, 3, 4, 5]
for num in nums:
    if num % 2 == 0:
        nums.remove(num)
print(nums)  # [1, 3, 5] - Works here, but...

nums = [2, 4, 6, 8]
for num in nums:
    if num % 2 == 0:
        nums.remove(num)
print(nums)  # [4, 8] - Skips elements!
```

**The fix**: Iterate over a copy or use list comprehension.

```python
# Solution 1: Iterate over copy
nums = [2, 4, 6, 8]
for num in nums[:]:  # Slice creates a copy
    if num % 2 == 0:
        nums.remove(num)
print(nums)  # []

# Solution 2: List comprehension (preferred)
nums = [2, 4, 6, 8]
nums = [num for num in nums if num % 2 != 0]
print(nums)  # []

# Solution 3: filter
nums = list(filter(lambda x: x % 2 != 0, nums))
```

---

## 6. String Concatenation Inefficiency

**The gotcha**: String concatenation in a loop is O(n²).

```python
# SLOW - O(n²)
result = ""
for s in strings:
    result += s  # Creates new string each time

# FAST - O(n)
result = "".join(strings)
```

**Why**: Strings are immutable. Each `+=` creates a new string object and copies all previous characters.

---

## 7. Dictionary Key Ordering

**The gotcha**: Before Python 3.7, dictionaries didn't preserve order.

```python
# Python 3.7+: Insertion order preserved
d = {'b': 2, 'a': 1, 'c': 3}
list(d.keys())  # ['b', 'a', 'c'] - Preserved!

# For guaranteed order, use OrderedDict (or just know your Python version)
from collections import OrderedDict
```

---

## 8. `is` vs `==`

**The gotcha**: `is` checks identity, `==` checks equality.

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # True - Same values
print(a is b)  # False - Different objects
print(a is c)  # True - Same object

# Special cases (due to interning):
a = "hello"
b = "hello"
print(a is b)  # True - Interned strings

a = "hello world"
b = "hello world"
print(a is b)  # Might be False! (Not always interned)
```

**The rule**: Always use `==` for comparisons, except for `None`.

```python
if x is None:     # CORRECT
if x == None:     # Works but not Pythonic
if x is not None: # CORRECT
```

---

## 9. Float Precision

**The gotcha**: Floating point numbers have precision issues.

```python
print(0.1 + 0.2)  # 0.30000000000000004
print(0.1 + 0.2 == 0.3)  # False!

# Solution 1: Use tolerance
def almost_equal(a, b, tol=1e-9):
    return abs(a - b) < tol

# Solution 2: Use Decimal for exact arithmetic
from decimal import Decimal
print(Decimal('0.1') + Decimal('0.2') == Decimal('0.3'))  # True

# Solution 3: Use fractions
from fractions import Fraction
print(Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10))  # True
```

---

## 10. Variable Scope in Nested Functions

**The gotcha**: Can't modify outer variable without `nonlocal`.

```python
# WRONG
def outer():
    count = 0
    def inner():
        count += 1  # UnboundLocalError!
    inner()
    return count

# CORRECT
def outer():
    count = 0
    def inner():
        nonlocal count
        count += 1
    inner()
    return count  # 1
```

**Workaround without nonlocal** (useful in interviews):

```python
def outer():
    count = [0]  # List is mutable
    def inner():
        count[0] += 1  # Modifying element, not reassigning
    inner()
    return count[0]  # 1
```

---

## 11. Tuple Gotchas

**The gotcha**: Single-element tuple needs a comma.

```python
not_a_tuple = (42)    # Just an int: 42
is_a_tuple = (42,)    # Tuple: (42,)
also_tuple = 42,      # Tuple: (42,)

# Empty tuple
empty = ()
```

**Tuple unpacking gotcha**:

```python
# Works
a, b = 1, 2

# Error
a, b = 1  # TypeError: cannot unpack non-iterable int

# Be careful with single-value returns
def get_values():
    return 1, 2  # Returns tuple (1, 2)

def get_value():
    return 1,    # Returns tuple (1,) - probably a bug!
```

---

## 12. Boolean Evaluation

**The gotcha**: Empty containers are falsy.

```python
# Falsy values:
# False, None, 0, 0.0, '', [], {}, set(), ()

# This is usually helpful:
if my_list:  # True if not empty
    process(my_list)

# But watch out:
def process(items=None):
    if not items:  # Bug if items=[] is valid input!
        items = get_default_items()

# CORRECT
def process(items=None):
    if items is None:
        items = get_default_items()
```

---

## 13. Exception Handling

**The gotcha**: Catching too broadly.

```python
# WRONG - Catches everything including KeyboardInterrupt
try:
    risky_operation()
except:
    pass

# WRONG - Still too broad
try:
    risky_operation()
except Exception:
    pass

# CORRECT - Catch specific exceptions
try:
    risky_operation()
except (ValueError, KeyError) as e:
    handle_error(e)
```

---

## 14. Walrus Operator Gotcha (Python 3.8+)

```python
# Useful for avoiding repeated computation
if (n := len(data)) > 10:
    print(f"Data has {n} elements")

# Gotcha: Works in comprehensions but modifies outer scope
[y := x + 1 for x in range(3)]
print(y)  # 3 - y is accessible outside!
```

---

## Quick Reference Table

| Gotcha | Wrong | Right |
|--------|-------|-------|
| Mutable default | `def f(l=[])` | `def f(l=None)` |
| Copy nested | `b = a.copy()` | `b = copy.deepcopy(a)` |
| Value comparison | `x is 5` | `x == 5` |
| None check | `x == None` | `x is None` |
| String concat | `s += char` in loop | `''.join(chars)` |
| Modify while iterate | `for x in lst: lst.remove(x)` | `lst = [x for x in lst if ...]` |
| Single tuple | `(42)` | `(42,)` |

---

## Interview Tips

1. **Mention gotchas proactively**: "I'll use `is None` instead of `== None`"
2. **Use defensive patterns**: `if lst is None: lst = []`
3. **Know the why**: Be able to explain why these behaviors exist
4. **Test edge cases**: Empty lists, None, boundary values

---

## Practice: Spot the Bug

```python
# Bug 1
def append_to(element, to=[]):
    to.append(element)
    return to

# Bug 2
matrix = [[0] * 3] * 3
matrix[0][0] = 1
print(matrix)  # What prints?

# Bug 3
funcs = []
for i in range(3):
    funcs.append(lambda: i)
print([f() for f in funcs])  # What prints?
```

<details>
<summary>Answers</summary>

1. Mutable default argument - all calls share the same list
2. `[[1, 0, 0], [1, 0, 0], [1, 0, 0]]` - All rows are the same object
3. `[2, 2, 2]` - All lambdas capture the same variable `i`

</details>

---

## Related Sections

- [Collections Module](./01-collections-module.md) - defaultdict avoids KeyError
- [Itertools Module](./04-itertools-module.md) - Iterator consumption gotchas
