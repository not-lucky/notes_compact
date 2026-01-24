import heapq
from collections import Counter

# 1. Kth Largest Element
def find_kth_largest(nums: list[int], k: int) -> int:
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]

# 2. Top K Frequent Elements (using heap)
def top_k_frequent_heap(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)

# 3. Merge K Sorted Lists
def merge_k_sorted(lists: list[list[int]]) -> list[int]:
    result = []
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
    return result

# 4. Find Median from Data Stream
class MedianFinder:
    def __init__(self):
        self.small = []  # Max-heap (negated)
        self.large = []  # Min-heap

    def add_num(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return -float(self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0

# 5. Task Scheduler
def least_interval(tasks: list[str], n: int) -> int:
    count = Counter(tasks)
    max_heap = [-c for c in count.values()]
    heapq.heapify(max_heap)

    time = 0
    while max_heap:
        temp = []
        for _ in range(n + 1):
            if max_heap:
                cnt = -heapq.heappop(max_heap)
                if cnt > 1:
                    temp.append(-(cnt - 1))
            time += 1
            if not max_heap and not temp:
                break
        for item in temp:
            heapq.heappush(max_heap, item)
    return time

# 6. K Closest Points to Origin
def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    heap = []
    for x, y in points:
        dist = x*x + y*y
        heapq.heappush(heap, (-dist, [x, y]))
        if len(heap) > k:
            heapq.heappop(heap)
    return [p for d, p in heap]

# 7. Ugly Number II
def nth_ugly_number(n: int) -> int:
    heap = [1]
    seen = {1}
    factors = [2, 3, 5]
    curr_ugly = 1
    for _ in range(n):
        curr_ugly = heapq.heappop(heap)
        for f in factors:
            new_ugly = curr_ugly * f
            if new_ugly not in seen:
                seen.add(new_ugly)
                heapq.heappush(heap, new_ugly)
    return curr_ugly

if __name__ == "__main__":
    print("Kth Largest:", find_kth_largest([3,2,3,1,2,4,5,5,6], 4))
    print("Top K Frequent (Heap):", top_k_frequent_heap([1,1,1,2,2,3], 2))
    print("Merge K Sorted:", merge_k_sorted([[1,4,5],[1,3,4],[2,6]]))

    mf = MedianFinder()
    mf.add_num(1); mf.add_num(2)
    print("Median (1, 2):", mf.find_median())
    mf.add_num(3)
    print("Median (1, 2, 3):", mf.find_median())

    print("Task Scheduler:", least_interval(["A","A","A","B","B","B"], 2))
    print("K Closest Points:", k_closest([[1,3],[-2,2]], 1))
    print("Nth Ugly Number (10):", nth_ugly_number(10))
