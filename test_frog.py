def can_cross(stones: list[int]) -> bool:
    target = stones[-1]
    dp = {stone: set() for stone in stones}
    dp[stones[0]].add(0)

    for stone in stones:
        for k in dp[stone]:
            for next_jump in [k - 1, k, k + 1]:
                if next_jump > 0:
                    next_pos = stone + next_jump
                    if next_pos == target:
                        return True
                    if next_pos in dp:
                        dp[next_pos].add(next_jump)

    return False

print("Test 1:", can_cross([0,1,3,5,6,8,12,17])) # Should be true
print("Test 2:", can_cross([0,1,2,3,4,8,9,11])) # Should be false
print("Test 3:", can_cross([0,2])) # Should be false
