# Chapter 19: High-Level Design (HLD)

High-Level Design (HLD) or System Design is the art of designing large-scale distributed systems that can handle millions of users and petabytes of data.

## Building Intuition

### What is HLD?

If LLD is about the internal code structure, HLD is about the **infrastructure and communication** between services. It's about how data flows through a system and how to ensure the system stays up when things fail.

> **Key Insight**: There is no "perfect" design. Every choice is a **trade-off**.

```text
┌──────────┐      ┌──────────────┐      ┌──────────┐
│  Client  │ ───> │ Load Balancer│ ───> │ API Nodes│
└──────────┘      └──────────────┘      └────┬─────┘
                                             │
                       ┌─────────────────────┴───┐
                       ▼                         ▼
                ┌────────────┐            ┌────────────┐
                │   Cache    │            │  Database  │
                └────────────┘            └────────────┘
```

## Why This Matters for Interviews

1.  **Scalability**: Can your system handle 10x or 100x more traffic?
2.  **Availability**: What happens if a server dies? (SLA, 99.999% "Five Nines")
3.  **Reliability**: Does the system do what it's supposed to do correctly?
4.  **Trade-offs**: Can you justify why you chose NoSQL over SQL for a specific use case?

---

## Core Topics

| Topic | Interview Relevance | Key Concepts |
|-------|-------------------|--------------|
| Fundamentals | Basic | Scalability, Availability, CAP Theorem |
| Architectural Patterns | Essential | Microservices, Load Balancers, Caching |
| Databases | Critical | SQL vs NoSQL, Sharding, Replication |
| Case Studies | Practical | TinyURL, WhatsApp, YouTube |

---

## Chapter Contents

| # | Topic | Key Concepts |
|---|-------|--------------|
| 01 | [Fundamentals](./01-fundamentals.md) | Scalability, Availability, Reliability |
| 02 | [Architectural Patterns](./02-architectural-patterns.md) | Load Balancers, Caching, Message Queues |
| 03 | [Databases](./03-databases.md) | SQL vs NoSQL, Sharding, CAP/PACELC |
| 04 | [Case Studies](./04-case-studies.md) | Designing real-world systems at scale |

---

## The HLD Interview Framework (4 Steps)

### 1. Requirements & Scope (5 mins)
- **Functional**: What should the system do? (e.g., "User can post a tweet").
- **Non-Functional**: Scalability (100M users), Availability, Latency.
- **Constraints**: Throughput (QPS), Storage capacity.

### 2. High-Level Diagram (10-15 mins)
- Draw the main components (DNS, LB, App Servers, DB, Cache).
- Describe the data flow for the main use cases.

### 3. Component Deep Dive (10-15 mins)
- Database schema and scaling (Sharding, Partitioning).
- Caching strategy (Write-through vs Write-back).
- Handling bottlenecks and Single Points of Failure (SPOF).

### 4. Advanced Topics/Refinement (5 mins)
- Monitoring, Logging, Service Discovery.
- Security (HTTPS, Auth).

---

## Next Steps

Start with the [Fundamentals](./01-fundamentals.md) to understand the core metrics of system design.
