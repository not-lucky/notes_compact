from itertools import combinations, permutations, product, combinations_with_replacement, groupby, accumulate
import operator

# 1. Subsets
def subsets(nums: list[int]) -> list[list[int]]:
    res = []
    for r in range(len(nums) + 1):
        res.extend([list(c) for c in combinations(nums, r)])
    return res

# 2. Permutations
def permute(nums: list[int]) -> list[list[int]]:
    return [list(p) for p in permutations(nums)]

# 3. Letter Combinations of a Phone Number
def letter_combinations(digits: str) -> list[str]:
    if not digits: return []
    phone = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    letters = [phone[d] for d in digits]
    return ["".join(p) for p in product(*letters)]

# 4. Combination Sum (Simplified: finding combinations of length k that sum to target)
def combination_sum_k(nums: list[int], k: int, target: int) -> list[list[int]]:
    return [list(c) for c in combinations_with_replacement(nums, k) if sum(c) == target]

# 5. Generate Parentheses (Brute force using product)
def generate_parenthesis(n: int) -> list[str]:
    def is_valid(p):
        bal = 0
        for c in p:
            if c == '(': bal += 1
            else: bal -= 1
            if bal < 0: return False
        return bal == 0

    res = []
    for p in product("()", repeat=2*n):
        if is_valid(p):
            res.append("".join(p))
    return res

# 6. Count and Say
def count_and_say(n: int) -> str:
    s = "1"
    for _ in range(n - 1):
        s = "".join(f"{len(list(group))}{key}" for key, group in groupby(s))
    return s

# 7. Running Sum
def running_sum(nums: list[int]) -> list[int]:
    return list(accumulate(nums))

if __name__ == "__main__":
    print("Subsets:", subsets([1,2,3]))
    print("Permutations:", permute([1,2,3]))
    print("Letter Combos (23):", letter_combinations("23"))
    print("Combination Sum (nums=[2,3,5], k=3, target=8):", combination_sum_k([2,3,5], 3, 8))
    print("Generate Parentheses (2):", generate_parenthesis(2))
    print("Count and Say (4):", count_and_say(4))
    print("Running Sum:", running_sum([1,2,3,4]))
