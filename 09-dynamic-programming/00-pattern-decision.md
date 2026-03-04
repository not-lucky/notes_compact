# DP Pattern Selection Decision Diagram

```mermaid
flowchart TD
    START([Is this DP?]) --> Q1{Optimal Substructure<br/>Overlapping Subproblems?}
    Q1 -->|No| NOT_DP[Not DP<br/>Greedy or Divide]
    Q1 -->|Yes| INPUT{What is INPUT?}
    
    INPUT -->|Single Array or String| Q2{Constraint or Goal?}
    Q2 -->|Cant pick adjacent| HOUSE_ROBBER[House Robber<br/>dp[i]=max(dp[i-1],dp[i-2]+val)]
    Q2 -->|Contiguous subarray| KADANE[Kadane<br/>dp[i]=max(nums[i],dp[i-1]+nums[i])]
    Q2 -->|Count ways| FIB[1D Linear Fibonacci<br/>dp[i]=dp[i-1]+dp[i-2]]
    Q2 -->|Unlimited items| UNBOUNDED[Unbounded Knapsack<br/>Coin Change]
    Q2 -->|Multiple states| STATE_MACHINE[State Machine<br/>Stock Buy Sell]
    Q2 -->|Palindrome or Interval| INTERVAL[Interval DP<br/>Palindrome problems]
    Q2 -->|Split at any point| ADV_INTERVAL[Advanced Interval<br/>Matrix Chain Burst]
    
    INPUT -->|Two Strings| Q3{What is Goal?}
    Q3 -->|Longest common|LCS[LCS<br/>dp[i][j]=dp[i-1][j-1]+1 or max]
    Q3 -->|Edit operations| EDIT[Edit Distance<br/>Insert Delete Replace]
    Q3 -->|Pattern matching| REGEX[Regex Matching]
    
    INPUT -->|Grid or Matrix| Q4{Movement?}
    Q4 -->|Down Right only| GRID_BASIC[2D Grid<br/>Unique Paths]
    Q4 -->|3 directions| FALLING[Min Falling Path<br/>dp from 3 above]
    Q4 -->|Diagonal| SQUARE[Maximal Square<br/>min(left,top,diag)+1]
    
    INPUT -->|Items plus Capacity| Q5{Usage?}
    Q5 -->|Once| K01[0 1 Knapsack<br/>Iterate backwards]
    Q5 -->|Multiple| KUNBOUND[Unbounded<br/>Iterate forwards]
```

## Quick Reference

| Pattern | Input | Key Clue | Complexity |
|---------|-------|----------|------------|
| 1D Linear | Single array | Fixed prev states | O(n), O(1) |
| House Robber | Single array | Can't pick adjacent | O(n), O(1) |
| Kadane's | Single array | Contiguous subarray | O(n), O(1) |
| Unbounded | Items+Target | Unlimited usage | O(n×T), O(T) |
| 0/1 Knapsack | Items+Capacity | Each item once | O(n×W), O(W) |
| 2D Grid | Matrix | Grid traversal | O(mn), O(mn) |
| LCS | Two strings | Relative order | O(mn), O(min) |
| State Machine | Array+states | Multiple states | O(n), O(1) |
| Interval DP | String | Expanding intervals | O(n²) |
| Matrix Chain | Multiple items | Split anywhere | O(n³) |

## Decision Path

1. **Is it DP?** → Optimal substructure + overlapping subproblems
2. **Input type** → Single array, Two strings, Grid, or Items+Capacity
3. **Constraint/Goal** → Can't pick adjacent, Contiguous, Unlimited, Multiple states
4. **Match to pattern** → Use the table above
