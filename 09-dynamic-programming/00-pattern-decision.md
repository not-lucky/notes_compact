# DP Pattern Selection Decision Diagram

```mermaid
flowchart TD
    START([Is this DP?]) --> Q1{Optimal Substructure?}
    Q1 -->|No| NOT_DP[Not DP]
    Q1 -->|Yes| INPUT{What is INPUT?}
    
    INPUT -->|Single Array| Q2{Constraint?}
    Q2 -->|Cant pick adjacent| HOUSE_ROBBER[House Robber]
    Q2 -->|Contiguous| KADANE[Kadane]
    Q2 -->|Count ways| FIB[1D Linear]
    Q2 -->|Unlimited items| UNBOUNDED[Unbounded]
    Q2 -->|Multiple states| STATE_MACHINE[State Machine]
    Q2 -->|Palindrome| INTERVAL[Interval DP]
    Q2 -->|Split anywhere| ADV_INTERVAL[Matrix Chain]
    
    INPUT -->|Two Strings| Q3{Goal?}
    Q3 -->|Longest common|LCS[LCS]
    Q3 -->|Edit ops| EDIT[Edit Distance]
    Q3 -->|Pattern match| REGEX[Regex]
    
    INPUT -->|Grid| Q4{Movement?}
    Q4 -->|Down Right| GRID_BASIC[2D Grid]
    Q4 -->|directions 3| FALLING[Falling Path]
    Q4 -->|Diagonal| SQUARE[Maximal Square]
    
    INPUT -->|Items Capacity| Q5{Usage?}
    Q5 -->|Once| K01[0 1 Knapsack]
    Q5 -->|Multiple| KUNBOUND[Unbounded]
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
