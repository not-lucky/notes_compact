# Google Interview Patterns

> **Prerequisites:** [README.md](./README.md)

Google's interview process is known for its algorithmic rigor. They want to see structured thinking, optimal solutions, and clear complexity analysis. This guide covers what to expect and how to prepare.

---

## Building Intuition

### Why Google Interviews Feel Different

Google pioneered the modern tech interview. Their style—deep algorithmic problems, emphasis on complexity analysis, structured communication—has become the industry standard, but Google does it more intensely than anyone else.

**The key insight**: Google optimizes for avoiding false positives (hiring someone who can't do the job) over false negatives (rejecting someone who could). This means they'd rather pass on a good candidate than hire a mediocre one. You need to be obviously good, not just adequate.

### What Interviewers Actually Evaluate

Google interviewers score you on:
1. **Analytical skills**: How you break down problems
2. **Coding skills**: Clean, working code
3. **Communication**: Can they understand your thinking?
4. **Googleyness**: Would you be good to work with?

The first three are table stakes. Googleyness is the differentiator—it's why two candidates with similar technical skills get different outcomes.

### Mental Model: The Collaborative Colleague Test

Interviewers ask themselves: "Would I want to work with this person?"

This means:
- When you explain your approach, they imagine hearing this in a design discussion
- When you take feedback, they imagine giving you a code review
- When you handle a hard problem, they imagine you on-call at 2 AM

Your goal is to demonstrate that working with you would be pleasant and productive.

### Why Optimal Solutions Matter at Google

Google systems serve billions of users. An O(n²) solution that works fine in an interview could cost millions at scale. When interviewers push for optimal solutions, they're testing whether you think about scalability instinctively.

---

## When NOT to Use Google-Specific Strategies

### Don't Over-Optimize for Google's Style

1. **Don't be too slow**: Spending 15 minutes on clarification is too much. 3-5 minutes, then get buy-in and code.

2. **Don't ignore partial credit**: If you can't find the optimal solution, a working brute-force solution with clear analysis is still valuable. Don't freeze trying to find the perfect approach.

3. **Don't be robotic**: "I'll now state my assumptions" repeated for each problem sounds rehearsed. Be natural in your communication.

4. **Don't hide confusion**: If you don't understand the problem, asking clarifying questions is better than solving the wrong problem optimally.

### Common Google Interview Mistakes

- **Silent thinking**: Google wants to hear your thought process. Thinking silently for 5 minutes is a red flag.
- **Giving up on optimization**: Even if you can't find O(n), discussing why O(n²) is suboptimal shows understanding.
- **Defensive about feedback**: When an interviewer hints that something is wrong, thank them and adapt.
- **Skipping complexity analysis**: Always state time AND space complexity before and after coding.

---

## Interview Structure

### Typical Process
1. **Recruiter screen** (30 min) - Background, role fit
2. **Technical phone screen** (45 min) - 1-2 coding problems
3. **Onsite/Virtual** (4-5 hours) - 4-5 interviews
   - 3-4 coding/algorithm rounds
   - 1 behavioral (Googleyness and Leadership)
   - 1 system design (for senior roles)

### Round Breakdown

| Round | Duration | Focus | What They Evaluate |
|-------|----------|-------|-------------------|
| Coding 1-3 | 45 min each | DSA problems | Problem-solving, code quality |
| Behavioral | 45 min | Past experience | Googliness, leadership |
| System Design | 45 min | Large-scale systems | Architecture, tradeoffs |

---

## What Makes Google Different

### 1. Emphasis on Optimal Solutions
Google interviewers often push for the best possible solution:
- Expect follow-ups: "Can you do better than O(n²)?"
- Partial credit for brute force, but optimal is the target
- They want to see your optimization thought process

### 2. Communication Is Scored
- Think out loud continuously
- Explain why you're considering each approach
- State your assumptions explicitly
- Summarize complexity at the end

### 3. Googliness (GCA - General Cognitive Ability)
Interviewers assess:
- How you handle ambiguity
- Willingness to take feedback
- Collaborative attitude
- Intellectual humility

---

## Common Problem Categories

### High-Frequency Topics

| Category | Frequency | Example Patterns |
|----------|-----------|------------------|
| Arrays/Strings | Very High | Two pointers, sliding window |
| Trees | High | Traversals, LCA, path problems |
| Graphs | High | BFS/DFS, topological sort |
| Dynamic Programming | Medium-High | 1D/2D DP, state machine |
| Design (Senior) | High | Distributed systems |

### Google's Favorite Problem Types

1. **Graph problems with clever BFS/DFS**
   - Multi-source BFS
   - Cycle detection in various contexts
   - Shortest path variations

2. **String manipulation with constraints**
   - Substring with conditions
   - Pattern matching
   - Parsing problems

3. **Tree problems requiring recursion insight**
   - Path sums with conditions
   - Tree construction
   - Serialize/deserialize

4. **Array problems requiring multiple passes or clever data structures**
   - Prefix sums with HashMap
   - Monotonic stack/queue
   - Interval problems

---

## The Google Interview Framework

### Phase 1: Clarify (3-5 minutes)
```
1. Repeat the problem in your own words
2. Ask about input constraints:
   - Size of input (n)
   - Range of values
   - Sorted? Unique?
3. Ask about edge cases:
   - Empty input
   - Single element
   - All same values
4. Confirm expected output format
```

### Phase 2: Approach (5-7 minutes)
```
1. Start with brute force: "The naive approach would be..."
2. Identify inefficiency
3. Propose optimization with reasoning
4. State complexity before coding
5. Get interviewer buy-in: "Does this approach sound reasonable?"
```

### Phase 3: Code (15-20 minutes)
```
1. Write clean, readable code
2. Use meaningful variable names
3. Handle edge cases explicitly
4. Talk through your code as you write
5. Leave room for modifications (don't pack code tightly)
```

### Phase 4: Test (5-7 minutes)
```
1. Trace through a simple example by hand
2. Test edge cases:
   - Empty/null input
   - Single element
   - Large input (verbally)
3. Look for off-by-one errors
4. Verify complexity claims
```

---

## Google-Specific Tips

### Do's
- **Ask clarifying questions first** - Shows thoroughness
- **State assumptions explicitly** - "I'm assuming the input is 0-indexed"
- **Analyze complexity before and after** - Time AND space
- **Consider follow-ups proactively** - "If we needed to handle streaming data..."
- **Be comfortable with silence** - Take time to think

### Don'ts
- Don't start coding immediately
- Don't give up after one approach fails
- Don't be defensive about mistakes
- Don't forget to test your code
- Don't optimize prematurely—get correct solution first

---

## Googliness Signals

What interviewers look for in the behavioral/GCA assessment:

### Positive Signals
```
+ Taking feedback gracefully
+ Asking for clarification rather than assuming
+ Admitting when you don't know something
+ Showing curiosity about the problem
+ Collaborative rather than defensive
+ Explaining failures and what you learned
```

### Negative Signals
```
- Arrogance or dismissing hints
- Giving up too easily
- Not listening to interviewer guidance
- Claiming to know everything
- Blaming others for failures
- Not showing enthusiasm for learning
```

---

## Sample Problems by Difficulty

### Phone Screen Level (Medium)

| Problem | Pattern | Key Insight |
|---------|---------|-------------|
| LRU Cache | Design + HashMap + DLL | O(1) get/put with ordered eviction |
| Word Search | DFS + Backtracking | Mark visited, restore after |
| Group Anagrams | HashMap | Sorted string as key |
| Find K Closest Points | Heap | Min-heap of size k |

### Onsite Level (Medium-Hard)

| Problem | Pattern | Key Insight |
|---------|---------|-------------|
| Median from Data Stream | Two Heaps | Balance max-heap and min-heap |
| Serialize/Deserialize Binary Tree | BFS/DFS | Null markers for structure |
| Word Ladder | BFS | Word transformation as graph |
| Longest Increasing Path in Matrix | DFS + Memo | Cache path length from each cell |

### Hard (Occasional)

| Problem | Pattern | Key Insight |
|---------|---------|-------------|
| Sliding Window Maximum | Monotonic Deque | Maintain decreasing order |
| Trapping Rain Water | Two Pointers | Max from left and right |
| Word Break II | DP + Backtracking | Build all valid sentences |
| Regular Expression Matching | DP | Handle '.' and '*' cases |

---

## Time Management

### 45-Minute Round
```
0:00-0:03  Problem understanding, clarify
0:03-0:08  Discuss approach, complexity
0:08-0:30  Code solution
0:30-0:38  Test, debug
0:38-0:43  Optimization discussion
0:43-0:45  Candidate questions
```

### What to Do If Stuck

1. **State where you're stuck** - "I'm trying to figure out how to handle..."
2. **Think about simpler cases** - "What if the input was just 2 elements?"
3. **Consider related problems** - "This reminds me of..."
4. **Ask for a hint** - "Could you point me in the right direction?"
   - Taking hints is OK; not taking them when offered is worse

---

## Common Mistakes at Google

| Mistake | Impact | Fix |
|---------|--------|-----|
| Starting to code too fast | Miss cases, wrong approach | Spend 5+ min planning |
| Silent problem solving | Can't assess your thinking | Think out loud always |
| Ignoring space complexity | Incomplete analysis | Always state both time/space |
| Not testing code | Bugs left in solution | Trace through example |
| Giving up on optimization | Miss chance to improve | Always discuss how to optimize |

---

## Mock Interview Checklist

Before your Google interview, practice until you can:

- [ ] Explain any solution in under 3 minutes
- [ ] Code a medium problem in 15 minutes
- [ ] Identify the pattern within 2 minutes
- [ ] Handle follow-up questions smoothly
- [ ] Test your code systematically
- [ ] Discuss tradeoffs clearly

---

## Next: [02-meta-patterns.md](./02-meta-patterns.md)
