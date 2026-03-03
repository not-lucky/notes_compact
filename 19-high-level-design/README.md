# Chapter 19: High-Level Design (HLD)

High-Level Design (HLD), also called System Design, is the art of designing large-scale distributed systems that can handle millions of users and petabytes of data. While [LLD (Chapter 18)](../18-low-level-design/) focuses on code-level architecture within a single service, HLD focuses on the **infrastructure, communication, and data flow between services** — and how the system stays up when things inevitably fail.

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

## What You'll Learn

By the end of this chapter, you will be able to:

- Reason about **scalability**, **availability**, and **reliability** as measurable properties of a system
- Apply the **CAP** and **PACELC** theorems to make informed database and consistency decisions
- Use core architectural building blocks: **load balancers**, **caches**, **message queues**, and **communication protocols**
- Choose between **SQL and NoSQL** databases and understand **sharding**, **replication**, and **indexing**
- Design real-world systems (URL shorteners, messaging apps, video streaming, etc.) end-to-end
- Navigate an HLD interview with a structured 4-step framework

---

## Chapter Contents

| # | Topic | Description | Key Concepts |
|---|-------|-------------|--------------|
| 01 | [Fundamentals](./01-fundamentals.md) | Core metrics and principles of distributed systems: how to measure and reason about system quality | Scalability (vertical vs. horizontal), Availability ("Nines"), Reliability, Failure Models, CAP & PACELC Theorems, Latency vs. Throughput |
| 02 | [Architectural Patterns](./02-architectural-patterns.md) | The building blocks you combine to construct system diagrams | Load Balancers (L4 vs. L7), Caching Patterns (Cache-Aside, Write-Through, Write-Back), Message Queues, Communication Protocols (REST, gRPC, WebSockets, SSE), Microservices vs. Monolith |
| 03 | [Databases](./03-databases.md) | Choosing, scaling, and tuning the data layer — often the most critical part of an HLD interview | SQL vs. NoSQL, Replication & Sharding, Transaction Isolation Levels, Distributed Transactions (2PC, Saga), Storage Engines (B-Trees vs. LSM), Indexing, Storage Types (Key-Value, Document, Wide-Column, Graph, Vector) |
| 04 | [Case Studies](./04-case-studies.md) | Applying fundamentals and patterns to real-world problems, with a recognition framework for interviews | TinyURL, WhatsApp, News Feed, Ad Click Aggregator, YouTube/Netflix, Uber/Lyft, Web Crawler, Back-of-the-envelope Estimation |

---

## Recommended Learning Path

Follow the files in order — each builds on the previous:

```text
01-Fundamentals ──> 02-Architectural Patterns ──> 03-Databases ──> 04-Case Studies
   (Theory)            (Building Blocks)           (Data Layer)      (Put It All Together)
```

1. **Start with [Fundamentals](./01-fundamentals.md)** — understand the core metrics (scalability, availability, CAP theorem) that every design decision references.
2. **Move to [Architectural Patterns](./02-architectural-patterns.md)** — learn the components (load balancers, caches, queues, protocols) you'll draw in every diagram.
3. **Then [Databases](./03-databases.md)** — the data layer is the heart of most systems; learn how to choose, scale, and protect it.
4. **Finish with [Case Studies](./04-case-studies.md)** — apply everything to real interview problems and practice the recognition framework.

> **Prerequisite**: Familiarity with [Chapter 17: System Design Basics](../17-system-design-basics/) (data structure choices, caching concepts, rate limiting) and [Chapter 18: Low-Level Design](../18-low-level-design/) (OOD, SOLID principles) will strengthen your foundation.

---

## Important Trade-offs

When working on High-Level Design, these fundamental trade-offs appear in every decision:

1. **CAP Theorem**: In distributed systems, Partition Tolerance is a given, so you trade off Consistency vs. Availability. Banking apps choose CP; social media chooses AP.
2. **Latency vs. Throughput**: You can optimize for fast individual responses (low latency) or processing many requests overall (high throughput), but pushing one often costs the other.
3. **SQL vs. NoSQL**: Relational databases provide ACID guarantees and powerful joins but are harder to scale horizontally. NoSQL databases scale easily but often relax consistency.
4. **Consistency vs. Performance**: Strong consistency requires locking and synchronous replication, hurting performance. Eventual consistency improves performance but users might see stale data.

---

## Why This Matters for Interviews

1. **Scalability**: Can your system handle 10x or 100x more traffic?
2. **Availability**: What happens if a server dies? (SLA, 99.999% "Five Nines")
3. **Reliability**: Does the system do what it's supposed to do correctly?
4. **Trade-offs**: Can you justify why you chose NoSQL over SQL for a specific use case?

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

### Example: Load Balancer Simulation

The code below illustrates two common load balancing strategies — Round Robin and Least Connections — that you would reference in Step 2 of the framework:

```python
from enum import Enum

# A conceptual simulation of a load balancer routing requests
class Server:
    def __init__(self, id: str):
        self.id = id
        self.load = 0

    def handle_request(self) -> str:
        self.load += 1
        return f"Server {self.id} handled request. Current load: {self.load}"

class LoadBalancerStrategy(Enum):
    ROUND_ROBIN = 1
    LEAST_CONNECTIONS = 2

class LoadBalancer:
    def __init__(self, strategy: LoadBalancerStrategy):
        self.servers: list[Server] = []
        self.strategy = strategy
        self._current_index = 0

    def add_server(self, server: Server) -> None:
        self.servers.append(server)

    def get_server(self) -> Server:
        if not self.servers:
            raise RuntimeError("No available servers")

        if self.strategy == LoadBalancerStrategy.ROUND_ROBIN:
            server = self.servers[self._current_index]
            self._current_index = (self._current_index + 1) % len(self.servers)
            return server
        elif self.strategy == LoadBalancerStrategy.LEAST_CONNECTIONS:
            return min(self.servers, key=lambda s: s.load)
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

# Example Usage:
lb = LoadBalancer(LoadBalancerStrategy.ROUND_ROBIN)
lb.add_server(Server("A"))
lb.add_server(Server("B"))
lb.add_server(Server("C"))

print(lb.get_server().handle_request()) # Server A
print(lb.get_server().handle_request()) # Server B
print(lb.get_server().handle_request()) # Server C
print(lb.get_server().handle_request()) # Server A
```

---

## Key Takeaways

| Principle | Remember |
|-----------|----------|
| **No perfect design** | Every decision is a trade-off; state your reasoning |
| **Partition Tolerance is non-negotiable** | In distributed systems, choose CP or AP — never sacrifice P |
| **Start simple, then scale** | Monolith → Microservices; Vertical → Horizontal |
| **Always justify components** | "I'm adding a cache here to reduce read latency from 100ms to 5ms" |
| **Back-of-the-envelope math** | Estimate DAU, QPS, and storage to validate your design |
| **The data layer is the hard part** | Sharding strategy, replication model, and consistency level drive most decisions |

---

## Next Steps

Start with the [Fundamentals](./01-fundamentals.md) to understand the core metrics of system design, then work through the chapter in order.
