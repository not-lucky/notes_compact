# Meta Interview Patterns

> **Prerequisites:** [README.md](./README.md)

Meta (Facebook) interviews emphasize velocity and working solutions. Their "move fast" culture is reflected in how they evaluate candidates—they want to see you iterate quickly and ship code that works.

---

## Interview Structure

### Typical Process
1. **Recruiter screen** (30 min) - Background, role alignment
2. **Technical screen** (45 min) - 2 coding problems
3. **Onsite/Virtual** (4-5 hours)
   - 2 coding rounds (45 min each, 2 problems per round)
   - 1 system design (45-60 min, senior+)
   - 1 behavioral (45 min)

### Round Breakdown

| Round | Duration | Focus | What They Evaluate |
|-------|----------|-------|-------------------|
| Coding 1-2 | 45 min × 2 | 2 problems each | Speed + correctness |
| System Design | 45-60 min | Large-scale system | Scale, product sense |
| Behavioral | 45 min | Past experience | Impact, collaboration |

---

## What Makes Meta Different

### 1. Two Problems Per Round
Unlike Google (often 1 deep problem), Meta does 2 problems per 45-min slot:
- ~20 min per problem
- First is usually easier, second harder
- Speed matters—if you're slow on #1, less time for #2

### 2. Working Code First, Optimize Later
Meta values:
- Getting to a working solution quickly
- Then improving if time permits
- Brute force that works > elegant solution that doesn't compile

### 3. Product Sense in System Design
Meta heavily weights:
- Understanding user needs
- Product tradeoffs
- How features affect user experience
- Scale at Meta (billions of users)

---

## Common Problem Categories

### High-Frequency Topics

| Category | Frequency | Example Patterns |
|----------|-----------|------------------|
| Arrays/Strings | Very High | Two pointers, sliding window |
| Trees | High | Traversals, BST operations |
| Graphs | Medium-High | BFS, DFS, grid problems |
| Dynamic Programming | Medium | 1D DP, classic problems |
| Design | High (Senior) | News Feed, Messenger, Instagram |

### Meta's Favorite Problem Types

1. **String problems with specific constraints**
   - Substring problems
   - String parsing
   - Character frequency

2. **Tree problems (especially traversal variations)**
   - Level order variations
   - Binary tree to linked list
   - Path problems

3. **Graph problems (especially grids)**
   - Islands counting
   - Shortest path in grid
   - Flood fill

4. **Array manipulation**
   - Intervals
   - Subarray sums
   - Two-pointer problems

---

## The Meta Interview Framework

### Problem 1 Approach (~20 min)
```
0:00-0:02  Read, clarify quickly
0:02-0:03  State approach in 30 seconds
0:03-0:15  Code solution
0:15-0:18  Quick test
0:18-0:20  Buffer/optimization
```

### Problem 2 Approach (~22 min)
```
0:00-0:02  Read, clarify
0:02-0:04  State approach
0:04-0:18  Code solution
0:18-0:22  Test and debug
```

### Key Differences from Google
- Less time for clarification
- Move to code faster
- Less emphasis on optimal first pass
- More focus on bug-free working code

---

## Meta-Specific Tips

### Do's
- **Start coding earlier** - Don't over-plan
- **Get working solution first** - Optimize later if time
- **Practice speed** - 2 problems in 45 min is demanding
- **Know your language well** - No time to look things up
- **Handle both problems** - Struggling on #2 because #1 took too long is bad

### Don'ts
- Don't spend 10 minutes discussing approach
- Don't aim for optimal immediately if it risks not finishing
- Don't forget to test (but keep it quick)
- Don't panic if problem 1 is easy—2 might be harder
- Don't skip communication entirely

---

## Behavioral: Impact Focus

Meta behavioral interviews assess:

### Core Themes
1. **Impact** - What results did you drive?
2. **Move Fast** - How quickly did you deliver?
3. **Be Bold** - Did you take calculated risks?
4. **Focus on Long-Term** - Did you build sustainable solutions?
5. **Be Open** - How did you collaborate?

### Sample Questions
- "Tell me about a time you shipped something quickly"
- "Describe a project where you had significant impact"
- "Tell me about a time you disagreed with your manager"
- "How do you prioritize when everything is urgent?"

### STAR Format Tips
```
S - Situation: Brief context (2 sentences max)
T - Task: Your specific responsibility
A - Action: What YOU did (be specific)
R - Result: Quantified impact if possible
```

---

## System Design at Meta

### Common Topics

| Topic | Focus Areas |
|-------|-------------|
| News Feed | Ranking, caching, real-time updates |
| Messenger | Real-time communication, message storage |
| Instagram Feed | Photo storage, CDN, ranking |
| Notifications | Push system, delivery guarantees |
| Search | Type-ahead, ranking, freshness |

### Meta-Specific Considerations

1. **Scale**: Design for billions of users
2. **Product Sense**: How does feature affect UX?
3. **Privacy**: Consider data privacy implications
4. **Real-time**: Many Meta products need low latency
5. **Mobile**: Heavy mobile usage patterns

### What They Look For
```
+ Clear requirements gathering
+ Reasonable high-level design
+ Identifying bottlenecks
+ Making reasonable tradeoffs
+ Knowing when to deep-dive vs. move on
+ Understanding caching, databases, scaling
```

---

## Sample Problems by Round

### Technical Screen / Round 1

| Problem | Pattern | Time Target |
|---------|---------|-------------|
| Valid Parentheses | Stack | 8 min |
| Merge Intervals | Sort + iteration | 10 min |
| Binary Tree Level Order | BFS | 12 min |
| Product of Array Except Self | Prefix/suffix | 10 min |

### Round 2 (Harder)

| Problem | Pattern | Time Target |
|---------|---------|-------------|
| LRU Cache | HashMap + DLL | 18 min |
| Word Break | DP | 15 min |
| Clone Graph | BFS/DFS + HashMap | 15 min |
| Alien Dictionary | Topological sort | 18 min |

---

## Time Management: Two-Problem Strategy

### When Problem 1 Is Easy
```
Solve quickly (~12-15 min)
Leave 25+ min for problem 2
Use extra time for thorough testing on #2
```

### When Problem 1 Is Hard
```
Get working solution (even suboptimal)
Don't get stuck perfecting
Move to problem 2
A working solution on both > perfect on one
```

### When Stuck
1. State your best approach so far
2. Implement what you have
3. Ask: "I have X approach in O(n²), is there a better way?"
4. Take hints—they're given to help you

---

## Coding Style at Meta

### What They Want to See

```python
# Good: Clear, readable, handles edge cases
def merge_intervals(intervals):
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged
```

### Code Quality Checklist
- [ ] Handles empty input
- [ ] Uses meaningful variable names
- [ ] Has clear structure
- [ ] Is reasonably concise
- [ ] Would compile/run

---

## Common Mistakes at Meta

| Mistake | Impact | Fix |
|---------|--------|-----|
| Spending too long on problem 1 | Not enough time for #2 | Time-box at 20 min |
| Over-optimizing early | Risk not finishing | Get working first |
| Not practicing speed | Run out of time | Do timed practice |
| Skipping testing | Bugs in solution | Quick trace-through |
| Ignoring problem 2 difficulty | Underestimate time | Check problem first |

---

## Mock Interview Checklist

Before your Meta interview, practice until you can:

- [ ] Solve 2 medium problems in 45 minutes
- [ ] Code without looking up syntax
- [ ] Test quickly but thoroughly
- [ ] Switch gears between problems smoothly
- [ ] Explain your approach in under 1 minute
- [ ] Handle interruptions/hints gracefully

---

## Practice Problems (Meta Favorites)

### Must-Know Problems

| Problem | Why It's Asked |
|---------|----------------|
| LRU Cache | Tests design + implementation |
| Binary Tree Level Order | Classic BFS |
| Clone Graph | Graph traversal + copying |
| Word Break | DP pattern recognition |
| Merge Intervals | Real-world applicability |
| Valid Parentheses | Stack fundamentals |
| Product Except Self | Clever array manipulation |
| Number of Islands | Grid DFS/BFS |

---

## Next: [03-amazon-patterns.md](./03-amazon-patterns.md)
