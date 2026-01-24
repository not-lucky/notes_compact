import heapq

class MedianFinder:
    """
    Find median from a stream of numbers.
    Pattern: Two Heaps
    Time: add_num O(log n), find_median O(1)
    Space: O(n)
    """
    def __init__(self):
        # max_heap for the lower half (negated to use heapq min-heap)
        self.max_heap = []
        # min_heap for the upper half
        self.min_heap = []

    def add_num(self, num: int) -> None:
        # 1. Add to max_heap (negated)
        heapq.heappush(self.max_heap, -num)

        # 2. Rebalance: move largest from max_heap to min_heap
        heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))

        # 3. Keep size balanced: max_heap can have one more than min_heap
        if len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))

    def find_median(self) -> float:
        if len(self.max_heap) > len(self.min_heap):
            return float(-self.max_heap[0])
        return (-self.max_heap[0] + self.min_heap[0]) / 2.0

if __name__ == "__main__":
    # Test cases
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    assert mf.find_median() == 1.5
    mf.add_num(3)
    assert mf.find_median() == 2.0
    print("All tests passed!")
