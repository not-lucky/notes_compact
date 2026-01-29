# HLD Fundamentals

Before designing a system, you must understand the core metrics and principles that govern distributed systems.

> **Prerequisites:** [Chapter 19 README](./README.md)

## 1. Scalability
The ability of a system to handle increased load.

### How to Recognize Scalability Needs
- **Traffic Spikes**: If the user base is expected to grow or has seasonal peaks (e.g., Black Friday).
- **Data Growth**: If you are storing logs, user posts, or videos that never get deleted.
- **Compute Heavy**: If you are doing video encoding or complex analytics.

- **Vertical Scaling (Scaling Up)**: Adding more power (CPU, RAM) to an existing server. (Limited, expensive).
- **Horizontal Scaling (Scaling Out)**: Adding more servers to the pool. (Infinite potential, requires Load Balancers).

## 2. Availability vs. Reliability
- **Availability**: The percentage of time the system is operational (e.g., 99.9%).
- **Reliability**: The probability that the system will perform its intended function without failure for a specified period.

### How to Recognize Availability Needs
- **Mission Critical**: If downtime costs money or lives (e.g., Payments, Medical systems).
- **Global User Base**: If users are in every timezone, there is no "off-peak" for maintenance.

### "Nines" of Availability
| Availability % | Allowed Downtime / Year | Allowed Downtime / Month |
|----------------|-------------------------|--------------------------|
| **99% (Two Nines)** | 3.65 days | 7.31 hours |
| **99.9% (Three Nines)** | 8.77 hours | 43.83 minutes |
| **99.99% (Four Nines)** | 52.60 minutes | 4.38 minutes |
| **99.999% (Five Nines)** | 5.26 minutes | 26.30 seconds |

---

## 3. Failure Models
How do systems fail?
- **Fail-stop**: A node stops and other nodes can detect it.
- **Fail-recovery**: A node stops, but eventually recovers.
- **Byzantine (Arbitrary)**: A node behaves arbitrarily, including sending malicious or contradictory data. (Hardest to handle).

### Consensus Algorithms
To handle failures and maintain consistency (especially in CP systems), distributed systems use consensus algorithms:
- **Paxos**: The original, complex consensus protocol.
- **Raft**: Designed to be more understandable than Paxos. Used by **Etcd** (Kubernetes) and **Consul**.
- **ZAB (Zookeeper Atomic Broadcast)**: Used by **Zookeeper**.

---

## 4. CAP Theorem
In a distributed system, you can only provide two of the following three guarantees:
1.  **Consistency**: Every read receives the most recent write or an error.
2.  **Availability**: Every request receives a (non-error) response.
3.  **Partition Tolerance**: The system continues to operate despite an arbitrary number of messages being dropped by the network between nodes.

### How to Choose (The "Decision Tree")
- **Is it a Banking App?** Choose **CP**. Data must be correct. If the network is split, stop the transaction to prevent double spending.
- **Is it a Social Media Feed?** Choose **AP**. It's okay if a user sees a post 2 seconds late, as long as the site is "up".
- **Is it a Stock Exchange?** Choose **CP** + **Low Latency**. Hardest problem.

> **Note**: In a real distributed network, **Partition Tolerance (P) is a must**. So you usually choose between CP (Consistency/Partition) or AP (Availability/Partition).

## 5. PACELC Theorem
An extension of CAP. If there is a Partition (P), how does the system trade off Availability (A) and Consistency (C)? Else (E), how does it trade off Latency (L) and Consistency (C)?

- **Example (Amazon Dynamo)**: PA/EL. Prioritizes Availability during partition and Latency during normal operation.

---

## 6. Latency vs. Throughput
- **Latency**: The time it takes for a single request to be fulfilled (measured in ms).
- **Throughput**: The number of requests a system can handle in a given time period (measured in QPS - Queries Per Second).

### How to Optimize
- **Reduce Latency**: Use Caching, CDN, or Geographically distributed servers (Edge computing).
- **Increase Throughput**: Use Horizontal Scaling, Load Balancers, or Message Queues (to handle bursts).

---

## 7. Summary of Trade-offs

| Choice | Pro | Con | When to use? |
|--------|-----|-----|--------------|
| **Vertical Scale** | Simple | Hardware limit, SPOF | Small startups, internal tools |
| **Horizontal Scale** | Resilient | Complex, Network overhead | Large scale consumer apps |
| **Consistency (CP)** | Data accuracy | Slower, potential downtime | Finance, Inventory, Auth |
| **Availability (AP)** | Always online | Stale data possible | Social Media, Recommendations |
| **Strong Consistency** | No stale data | High Latency | SQL, Single-leader replication |
| **Eventual Consistency** | High Availability | Stale data | NoSQL, Multi-leader/Leaderless |
