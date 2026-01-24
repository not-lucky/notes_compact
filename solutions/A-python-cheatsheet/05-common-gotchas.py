# Practice: Spot the Bug (from notes)

# Bug 1: Mutable Default Arguments
def append_to(element, to=None):
    if to is None:
        to = []
    to.append(element)
    return to

# Bug 2: Shallow Copy in Matrix Creation
def create_matrix(rows, cols):
    # WRONG: matrix = [[0] * cols] * rows
    return [[0] * cols for _ in range(rows)]

# Bug 3: Late Binding Closures
def create_lambdas():
    # WRONG: return [lambda: i for i in range(3)]
    return [lambda i=i: i for i in range(3)]

# 4. Modifying List While Iterating
def remove_evens(nums):
    # WRONG: for n in nums: if n%2==0: nums.remove(n)
    return [n for n in nums if n % 2 != 0]

# 5. String Concatenation
def join_strings(strings):
    # WRONG: res = ""; for s in strings: res += s
    return "".join(strings)

if __name__ == "__main__":
    # Test Bug 1
    print("Append to (1):", append_to(1))
    print("Append to (2):", append_to(2)) # Should be [2], not [1, 2]

    # Test Bug 2
    matrix = create_matrix(3, 3)
    matrix[0][0] = 1
    print("Matrix (row 1 modified):", matrix) # Only first element should be 1

    # Test Bug 3
    funcs = create_lambdas()
    print("Lambdas:", [f() for f in funcs]) # Should be [0, 1, 2]

    # Test 4
    print("Remove Evens:", remove_evens([1, 2, 3, 4]))

    # Test 5
    print("Join Strings:", join_strings(["a", "b", "c"]))
