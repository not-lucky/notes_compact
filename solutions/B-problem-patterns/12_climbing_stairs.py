def climbing_stairs(n: int) -> int:
    """
    Count ways to climb n stairs (1 or 2 steps).
    Pattern: Dynamic Programming
    Time: O(n)
    Space: O(1)
    """
    if n <= 2:
        return n

    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current

    return prev1

if __name__ == "__main__":
    # Test cases
    assert climbing_stairs(2) == 2
    assert climbing_stairs(3) == 3
    assert climbing_stairs(4) == 5
    print("All tests passed!")
