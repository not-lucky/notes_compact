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

## Important Trade-offs

When working on High-Level Design, consider these fundamental trade-offs:

1.  **CAP Theorem:** You can only guarantee two out of three: Consistency, Availability, and Partition Tolerance. In distributed systems, P is a given, so you trade off C vs. A.
2.  **Latency vs. Throughput:** You can optimize for fast individual responses (low latency) or processing many requests overall (high throughput).
3.  **SQL vs. NoSQL:** Relational databases provide ACID guarantees and structured data (SQL) but are harder to scale horizontally. NoSQL databases scale easily but often relax consistency.
4.  **Consistency vs. Performance:** Strong consistency requires locking and synchronous replication, hurting performance. Eventual consistency improves performance but users might see stale data.

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

```python
from enum import Enum
from typing import Dict, List
from collections import defaultdict

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
        self.servers: List[Server] = []
        self.strategy = strategy
        self._current_index = 0

    def add_server(self, server: Server) -> None:
        self.servers.append(server)

    def get_server(self) -> Server:
        if not self.servers:
            raise Exception("No available servers")

        if self.strategy == LoadBalancerStrategy.ROUND_ROBIN:
            server = self.servers[self._current_index]
            self._current_index = (self._current_index + 1) % len(self.servers)
            return server
        elif self.strategy == LoadBalancerStrategy.LEAST_CONNECTIONS:
            return min(self.servers, key=lambda s: s.load)

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

## Next Steps

Start with the [Fundamentals](./01-fundamentals.md) to understand the core metrics of system design.
