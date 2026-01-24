import heapq

def find_kth_largest(nums: list[int], k: int) -> int:
    """
    Find the kth largest element in an array.
    Pattern: Heap (Top-K)
    Time: O(n log k)
    Space: O(k)
    """
    if not nums or k > len(nums):
        return -1

    # Min-heap of size k
    heap = nums[:k]
    heapq.heapify(heap)

    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)

    return heap[0]

if __name__ == "__main__":
    # Test cases
    assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    print("All tests passed!")
