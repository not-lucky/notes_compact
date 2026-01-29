# Amazon Interview Patterns

> **Prerequisites:** [README.md](./README.md)

Amazon interviews are unique because they blend technical skills with Leadership Principles (LPs). Understanding how to naturally integrate LPs into your responses is just as important as solving the coding problems.

---

## Building Intuition

### Why Amazon Interviews Are Different

Amazon is the only FANG company that explicitly evaluates you against a defined set of behavioral principles in every round. While other companies assess culture fit implicitly, Amazon makes it explicit with their 16 Leadership Principles.

**The key insight**: At Amazon, how you frame your technical decisions matters as much as the decisions themselves. An engineer who says "I optimized this for scalability" is good; one who says "I thought about our customers who need fast page loads, so I optimized for scalability" is better.

### What Leadership Principles Really Test

LPs aren't arbitrary corporate values—they encode what Amazon believes makes effective employees:

- **Customer Obsession**: Do you think from the user's perspective?
- **Ownership**: Do you take responsibility beyond your job description?
- **Bias for Action**: Do you act decisively with incomplete information?
- **Dive Deep**: Do you understand your systems at a detailed level?

Interviewers evaluate whether you naturally think this way, not whether you can recite the principles.

### Mental Model: The LP Lens

Think of LPs as lenses for viewing any situation:

| Situation       | Without LP Lens             | With LP Lens                                                                                |
| --------------- | --------------------------- | ------------------------------------------------------------------------------------------- |
| Fixed a bug     | "I found and fixed the bug" | "I dove deep into the logs, found the root cause affecting customer checkout, and fixed it" |
| Made a decision | "I decided to use Redis"    | "I owned the caching decision, chose Redis for our customer latency requirements"           |
| Shipped fast    | "I delivered on time"       | "I had a bias for action—shipped MVP in 2 weeks despite incomplete specs"                   |

### Why the Bar Raiser Matters

The Bar Raiser is Amazon's quality control mechanism. They're from a different team, have no stake in hiring you, and can veto any hire. They exist to prevent "lowering the bar" during hiring surges. Expect deeper behavioral probing from them.

---

## When NOT to Use Amazon-Specific Strategies

### Don't Force LP Integration

1. **Don't shoehorn LPs**: If your answer doesn't naturally demonstrate an LP, don't force it. Interviewers can tell when you're artificially inserting "customer obsession" into every sentence.

2. **Don't forget the technical**: LP integration is important, but you still need to solve the coding problem. Don't spend so much time on behavioral framing that you run out of coding time.

3. **Don't use generic STAR stories**: "Tell me about a time you showed ownership" should get a specific, detailed story—not a vague answer that could apply to anyone.

4. **Don't memorize LP definitions**: Know the principles conceptually, but don't recite their definitions verbatim. That sounds rehearsed.

### Common Amazon Interview Mistakes

- **"We" instead of "I"**: Amazon wants to know what _you_ did, not what your team did. Use "I" throughout your STAR stories.
- **No quantified results**: "It was successful" is weak. "We reduced latency by 40%, improving customer satisfaction scores by 15%" is strong.
- **Ignoring the Bar Raiser**: Treating the Bar Raiser interview casually is dangerous. They often ask the hardest behavioral questions.
- **Separate tech and behavioral**: At Amazon, technical decisions should demonstrate LPs naturally.

---

## Interview Structure

### Typical Process

1. **Recruiter screen** (30 min) - Background, role fit
2. **Online Assessment (OA)** - 2-3 coding problems (70 min)
3. **Onsite/Virtual Loop** (4-5 hours)
   - 4-5 interviews (45-60 min each)
   - Mix of technical and behavioral
   - Each interview includes LP questions

### The Loop Breakdown

| Interview      | Format           | Focus                    |
| -------------- | ---------------- | ------------------------ |
| Technical 1    | Coding + LPs     | DSA + behavioral         |
| Technical 2    | Coding + LPs     | DSA + behavioral         |
| System Design  | Design + LPs     | Architecture + ownership |
| Hiring Manager | Behavioral       | Leadership, fit          |
| Bar Raiser     | Behavioral/Mixed | Raise the bar, LPs       |

---

## Leadership Principles (LPs)

### The 16 LPs You Must Know

| #   | Principle                                    | Key Phrase                  | What It Means                      |
| --- | -------------------------------------------- | --------------------------- | ---------------------------------- |
| 1   | Customer Obsession                           | Start with customer         | Think backward from customer needs |
| 2   | Ownership                                    | Think long-term             | Never say "that's not my job"      |
| 3   | Invent and Simplify                          | Seek simplicity             | Innovation + removing complexity   |
| 4   | Are Right, A Lot                             | Good judgment               | Make quality decisions             |
| 5   | Learn and Be Curious                         | Never stop learning         | Hunger for knowledge               |
| 6   | Hire and Develop the Best                    | Raise the bar               | Hire people better than you        |
| 7   | Insist on Highest Standards                  | Keep raising the bar        | Never settle for "good enough"     |
| 8   | Think Big                                    | Bold direction              | Think differently, broadly         |
| 9   | Bias for Action                              | Speed matters               | Take calculated risks              |
| 10  | Frugality                                    | Do more with less           | Constraints drive innovation       |
| 11  | Earn Trust                                   | Vocally self-critical       | Admit mistakes openly              |
| 12  | Dive Deep                                    | Stay connected to details   | Know your metrics                  |
| 13  | Have Backbone; Disagree and Commit           | Respectfully challenge      | Speak up, then commit              |
| 14  | Deliver Results                              | Focus on outputs            | Get things done                    |
| 15  | Strive to be Earth's Best Employer           | Create safety               | Work environment                   |
| 16  | Success and Scale Bring Broad Responsibility | Leave better than you found | Social responsibility              |

### Most Commonly Tested LPs

```
CRITICAL:
1. Customer Obsession
2. Ownership
3. Bias for Action
4. Deliver Results
5. Dive Deep
6. Earn Trust

FREQUENTLY:
7. Learn and Be Curious
8. Invent and Simplify
9. Have Backbone; Disagree and Commit
10. Insist on Highest Standards
```

---

## Behavioral Questions: STAR Method

### The STAR Format

```
S - SITUATION
    Brief context (2-3 sentences max)
    Set the scene quickly

T - TASK
    Your specific responsibility
    What was expected of you

A - ACTION
    What YOU did (not the team)
    Be specific and detailed
    This is the bulk of your answer (60%)

R - RESULT
    Quantified impact if possible
    What you learned
    What you'd do differently
```

### Sample LP Questions by Principle

#### Customer Obsession

- "Tell me about a time you had to make a decision that was unpopular with your team but right for the customer"
- "Describe a situation where you had to balance customer needs with business constraints"

#### Ownership

- "Tell me about a time you took on something outside your job description"
- "Describe a project where you saw it through from start to finish"

#### Bias for Action

- "Tell me about a time you made a decision without all the data"
- "Describe a situation where speed was more important than perfection"

#### Dive Deep

- "Tell me about a time you had to dig into the details to solve a problem"
- "Describe a situation where data analysis changed your approach"

#### Earn Trust

- "Tell me about a time you failed and how you handled it"
- "Describe a time you received critical feedback"

---

## Technical Interview: LP Integration

### How Technical Rounds Work

Each technical interview typically:

- 5-10 min: Behavioral question (LP-focused)
- 30-35 min: Coding problem
- 5-10 min: Your questions

### Connecting Coding to LPs

**During problem clarification:**

```
"I want to make sure I understand the customer use case here..."
(Customer Obsession)
```

**When discussing approach:**

```
"The simplest solution would be O(n²), but thinking long-term about
scale, I should optimize to O(n)..."
(Ownership, Think Big)
```

**When handling errors:**

```
"Let me trace through this carefully to make sure I haven't
missed anything..."
(Dive Deep, Insist on Highest Standards)
```

**When finishing:**

```
"If I had more time, I'd add error handling for these edge cases..."
(Ownership, Highest Standards)
```

---

## The Bar Raiser

### What Is a Bar Raiser?

- Specially trained interviewer from a different team
- Objective perspective—no vested interest
- Can veto a hire
- Focuses heavily on LPs
- Ensures hiring bar stays high

### How to Prepare

1. **Expect harder behavioral questions**
   - Follow-up questions that dig deeper
   - "Tell me more about X"
   - "What would you do differently?"

2. **Have 10-12 strong stories**
   - Each mapped to 2-3 LPs
   - Varied across your career
   - Include failures and what you learned

3. **Know your resume cold**
   - They will ask about anything on it
   - Be ready to dive deep on any project

---

## Common Problem Categories

### Online Assessment (OA)

| Category       | Frequency  | Notes                    |
| -------------- | ---------- | ------------------------ |
| Arrays/Strings | High       | Often 2-3 problems       |
| Trees          | Medium     | Usually one problem      |
| Graphs         | Medium     | Grid or network problems |
| DP             | Medium-Low | Usually easier DP        |

### Onsite Technical

| Category       | Frequency     | Difficulty  |
| -------------- | ------------- | ----------- |
| Arrays/Strings | High          | Medium      |
| Trees/Graphs   | High          | Medium-Hard |
| System Design  | High (Senior) | Medium-Hard |
| OOP Design     | Medium        | Medium      |

### Amazon Favorite Problems

1. **LRU Cache** - Tests design and implementation
2. **Number of Islands** - BFS/DFS on grids
3. **Merge K Sorted Lists** - Heap usage
4. **Word Ladder** - BFS for transformations
5. **Meeting Rooms II** - Interval/heap
6. **Design Problems** - Product delivery systems

---

## System Design at Amazon

### Common Topics

| Topic                 | Amazon Context          |
| --------------------- | ----------------------- |
| E-commerce platform   | Amazon's core business  |
| Delivery/logistics    | Prime delivery          |
| Recommendation system | Product recommendations |
| Inventory management  | Warehouse systems       |
| Rate limiting         | API management          |

### What They Look For

1. **Scalability** - Amazon scale is massive
2. **Reliability** - 99.99% uptime expectations
3. **Customer impact** - How does design affect UX?
4. **Cost efficiency** - Frugality LP applies here
5. **Operational excellence** - How do you monitor/maintain?

### Weave In LPs

```
"For customer obsession, I'd prioritize low latency for
the product page load..."

"Taking ownership of reliability, I'd implement circuit
breakers and fallbacks..."

"Thinking about frugality, we could use spot instances
for batch processing..."
```

---

## Time Management

### 45-60 Minute Round Structure

```
0:00-0:10   Behavioral question (LP-focused)
0:10-0:45   Technical problem
0:45-0:55   (If 60 min) Deeper discussion
0:55-0:60   Your questions
```

### Behavioral Time Breakdown

```
Situation: 20% (30-45 seconds)
Task: 10% (15-20 seconds)
Action: 60% (2-3 minutes)
Result: 10% (30-45 seconds)

Total: 3-4 minutes per story
```

---

## Prepare Your Story Bank

### Template for Each Story

```
Story Title: _______________
LPs Demonstrated: LP1, LP2, LP3

SITUATION:
[2-3 sentences]

TASK:
[1-2 sentences]

ACTION:
[4-6 bullet points of what YOU did]

RESULT:
[Quantified outcome]
[What you learned]
```

### Story Bank Requirements

| Category               | # of Stories |
| ---------------------- | ------------ |
| Technical challenges   | 2-3          |
| Conflict/disagreement  | 2-3          |
| Customer focus         | 2            |
| Failure/learning       | 2            |
| Leadership/influence   | 2            |
| Working under pressure | 1-2          |

---

## Common Mistakes at Amazon

| Mistake               | Impact                   | Fix                    |
| --------------------- | ------------------------ | ---------------------- |
| Not knowing LPs       | Can't connect stories    | Memorize all 16        |
| Weak STAR stories     | Vague, not compelling    | Prepare 10+ stories    |
| "We" not "I"          | Can't assess your role   | Use "I" throughout     |
| No quantified results | Impact unclear           | Add numbers            |
| Ignoring Bar Raiser   | Underestimate difficulty | Prepare for deep dives |
| Tech-only focus       | Miss LP connection       | Weave LPs naturally    |

---

## Mock Interview Checklist

Before your Amazon interview, ensure:

### Technical

- [ ] Solve medium problems in 25-30 minutes
- [ ] Can naturally mention LPs during coding
- [ ] Handle follow-up questions smoothly
- [ ] Know basic system design patterns

### Behavioral

- [ ] 10-12 prepared STAR stories
- [ ] Each story maps to 2-3 LPs
- [ ] Stories have quantified results
- [ ] Can handle "tell me more" follow-ups
- [ ] Know all 16 LPs by heart
- [ ] Can explain 2-3 stories per LP

---

## LP Quick Reference During Interview

When answering, mentally map to LPs:

```
"I made sure to understand the customer need first..."
→ Customer Obsession

"I took full ownership of the project..."
→ Ownership

"I knew we needed to move fast, so I made a decision with
80% of the information..."
→ Bias for Action

"I dug into the logs and found the root cause..."
→ Dive Deep

"When the project failed, I owned the mistake publicly..."
→ Earn Trust

"I pushed back on the initial design because I believed
there was a better way..."
→ Have Backbone; Disagree and Commit

"We delivered the project on time and under budget..."
→ Deliver Results
```

---

## Next: [04-microsoft-apple.md](./04-microsoft-apple.md)
