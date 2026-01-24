def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """
    Merge overlapping intervals.
    Pattern: Merge Intervals
    Time: O(n log n) due to sorting
    Space: O(n) for the output list
    """
    if not intervals:
        return []

    # 1. Sort by start time
    intervals.sort(key=lambda x: x[0])

    merged = [intervals[0]]

    for i in range(1, len(intervals)):
        current = intervals[i]
        last_merged = merged[-1]

        # 2. Check for overlap
        if current[0] <= last_merged[1]:
            # Overlap: extend the last merged interval
            last_merged[1] = max(last_merged[1], current[1])
        else:
            # No overlap: add current interval
            merged.append(current)

    return merged

if __name__ == "__main__":
    # Test cases
    assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]
    assert merge_intervals([[1, 4], [2, 3]]) == [[1, 4]]
    print("All tests passed!")
