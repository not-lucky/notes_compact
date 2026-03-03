# HLD Fundamentals

Before designing a system, you must understand the core metrics and principles that govern distributed systems.

> **Prerequisites:** [Chapter 19 README](./README.md)

---

## 1. Scalability

The ability of a system to handle increased load **without degrading performance**.

### How to Recognize Scalability Needs
- **Traffic Spikes**: User base expected to grow or has seasonal peaks (e.g., Black Friday).
- **Data Growth**: Storing logs, user posts, or videos that accumulate indefinitely.
- **Compute Heavy**: Video encoding, ML inference, or complex analytics.

### Vertical vs. Horizontal Scaling

| Aspect | Vertical (Scale Up) | Horizontal (Scale Out) |
|--------|---------------------|------------------------|
| **What** | Add more CPU/RAM/disk to one machine | Add more machines to the pool |
| **Limit** | Hardware ceiling (you can't buy a 1TB RAM server forever) | Theoretically unlimited |
| **Complexity** | Simple — no code changes needed | Requires load balancers, stateless design |
| **Downtime** | Usually requires restart | Zero-downtime with rolling deploys |
| **Cost** | Exponentially more expensive at high end | Linearly scales with commodity hardware |
| **SPOF** | Yes — one machine fails, everything fails | No — traffic reroutes to surviving nodes |

> **Key Insight**: Most real-world systems use **both**. Start vertical (simple), then go
> horizontal when you hit limits. Horizontal scaling requires your application to be
> **stateless** — session state must live in an external store (Redis, DB), not in-memory.

---

## 2. Availability vs. Reliability

These are related but distinct:
- **Availability**: The fraction of time a system is operational and accepting requests. Measured as a percentage (e.g., 99.9%).
- **Reliability**: The probability that the system performs its **intended function correctly** for a given period. A system can be "available" but unreliable (e.g., returns wrong data).

### How to Recognize Availability Needs
- **Mission Critical**: Downtime costs money or lives (payments, medical, aviation).
- **Global User Base**: Users in every timezone — no "off-peak" maintenance window.
- **SLA Obligations**: Contractual uptime guarantees with penalties for breach.

### "Nines" of Availability

| Availability % | Allowed Downtime / Year | Allowed Downtime / Month |
|----------------|-------------------------|--------------------------|
| **99% (Two Nines)** | 3.65 days | 7.31 hours |
| **99.9% (Three Nines)** | 8.77 hours | 43.83 minutes |
| **99.99% (Four Nines)** | 52.60 minutes | 4.38 minutes |
| **99.999% (Five Nines)** | 5.26 minutes | 26.30 seconds |

> **Reality Check**: Going from 99.9% to 99.99% is a **10x reduction** in allowed downtime,
> and typically requires **10x+ the engineering investment** (redundancy, failover, monitoring,
> multi-region deployment). Most consumer apps target Three Nines; critical infrastructure
> targets Four or Five Nines.

### Achieving High Availability
- **Redundancy**: No single point of failure (replicated DBs, multiple app servers).
- **Failover**: Automatic detection and rerouting (active-passive or active-active).
- **Health Checks**: Heartbeat monitoring to detect failures fast.
- **Graceful Degradation**: Serve partial results rather than failing completely.

---

## 3. Failure Models

How do distributed system nodes fail?

| Model | Behavior | Detection | Difficulty |
|-------|----------|-----------|------------|
| **Fail-stop** | Node stops completely and other nodes can detect it | Easy (heartbeat timeout) | Low |
| **Fail-recovery** | Node stops but eventually recovers (possibly with stale state) | Medium | Medium |
| **Byzantine (Arbitrary)** | Node behaves unpredictably — may send malicious, contradictory, or corrupted data | Hard (need BFT protocols) | Highest |

> **Interview Tip**: Most system design questions assume fail-stop or fail-recovery models.
> Byzantine fault tolerance is relevant for blockchain/cryptocurrency systems.

### Consensus Algorithms

To maintain consistency across replicas despite failures, distributed systems use consensus algorithms. These ensure all non-faulty nodes agree on the same value:

- **Paxos**: The original consensus protocol (Lamport, 1989). Provably correct but notoriously difficult to implement and understand.
- **Raft**: Designed as an understandable alternative to Paxos (2014). Separates leader election, log replication, and safety. Used by **etcd** (Kubernetes) and **Consul**.
- **ZAB (Zookeeper Atomic Broadcast)**: Similar to Paxos but optimized for primary-backup replication. Used by **ZooKeeper**.

---

## 4. CAP Theorem

In a **distributed** data store, when a **network partition** occurs, you must choose between:

1. **Consistency (C)**: Every read receives the most recent write or an error. All nodes see the same data at the same time.
2. **Availability (A)**: Every request receives a (non-error) response, though it may not contain the most recent write.
3. **Partition Tolerance (P)**: The system continues to operate despite network partitions (messages lost or delayed between nodes).

### Why P Is Non-Negotiable

In any distributed system, network partitions **will** happen (hardware failures, network congestion, misconfigured firewalls). You cannot choose to "not have" partitions. So the real choice is:

- **CP (Consistency + Partition Tolerance)**: During a partition, some requests may be rejected (unavailable) to prevent inconsistent data. *Example*: HBase, MongoDB (with majority write concern), ZooKeeper.
- **AP (Availability + Partition Tolerance)**: During a partition, all requests succeed but may return stale data. *Example*: Cassandra, DynamoDB, CouchDB.

### The Decision Tree

| Requirement | Choose | Reasoning | Examples |
|-------------|--------|-----------|----------|
| Financial transactions, inventory | **CP** | Incorrect data = money loss, overselling | Banking, stock trading, booking systems |
| Social media, recommendations | **AP** | Stale data is acceptable; downtime is not | Twitter feed, YouTube recommendations |
| Configuration/coordination | **CP** | All nodes must agree on state | Service discovery (ZooKeeper, etcd) |

> **Common Misconception**: CAP does not mean you "give up" one property entirely. It means
> during a partition you must **prioritize** one over the other. When the network is healthy,
> a well-designed system can provide all three.

---

## 5. PACELC Theorem

An extension of CAP that addresses behavior **when there is no partition** (the common case):

> **P**artition → trade off **A**vailability vs. **C**onsistency
> **E**lse (no partition) → trade off **L**atency vs. **C**onsistency

| System | During Partition (PAC) | Normal Operation (ELC) | Classification |
|--------|------------------------|------------------------|----------------|
| **DynamoDB** | Availability (A) | Latency (L) | PA/EL |
| **Cassandra** | Availability (A) | Latency (L) | PA/EL |
| **MongoDB** | Consistency (C) | Consistency (C) | PC/EC |
| **HBase** | Consistency (C) | Consistency (C) | PC/EC |
| **Cosmos DB** | Configurable | Configurable | Tunable |

> **Why This Matters**: CAP only describes partition scenarios (rare). PACELC captures the
> **everyday** trade-off between latency and consistency, which is what you optimize for
> in practice.

---

## 6. Latency vs. Throughput

- **Latency**: Time for a single request to complete (measured in ms). "How fast is one request?"
- **Throughput**: Number of requests processed per unit time (measured in QPS or RPS). "How many requests at once?"

These are often in tension: optimizing one can hurt the other (e.g., batching increases throughput but adds latency per individual request).

### How to Optimize

| Goal | Techniques |
|------|------------|
| **Reduce Latency** | Caching, CDNs, edge computing, connection pooling, async I/O |
| **Increase Throughput** | Horizontal scaling, load balancing, message queues, batch processing |
| **Both** | Data locality, efficient serialization (Protobuf > JSON), database indexing |

### Latency Numbers Every Engineer Should Know

These are approximate orders of magnitude (useful for back-of-the-envelope calculations):

| Operation | Latency | Notes |
|-----------|---------|-------|
| L1 cache reference | ~1 ns | |
| L2 cache reference | ~4 ns | |
| RAM reference | ~100 ns | |
| SSD random read | ~100 μs | |
| HDD random read | ~4 ms | ~40x slower than SSD |
| Round trip within same datacenter | ~0.5 ms | |
| Send 1 MB over 1 Gbps network | ~10 ms | |
| Round trip CA → Netherlands | ~150 ms | |
| HDD sequential read (1 MB) | ~4 ms | ~100-200 MB/s throughput |
| SSD sequential read (1 MB) | ~0.5 ms | SATA ~500 MB/s, NVMe faster |

> **Key Takeaway**: Memory is ~1000x faster than SSD, SSD is ~40x faster than HDD for random reads,
> intra-datacenter is ~300x faster than cross-continent. These ratios drive caching,
> CDN placement, and data replication strategies.

---

## 7. Back-of-the-Envelope Estimation

A critical skill for HLD interviews: quickly estimating system requirements.

### Common Reference Numbers

| Metric | Value |
|--------|-------|
| Seconds in a day | ~86,400 ≈ ~10^5 |
| Seconds in a month | ~2.6M ≈ ~2.5 × 10^6 |
| Seconds in a year | ~31.5M ≈ ~3 × 10^7 |
| 1 Million requests/day | ~12 QPS |
| 1 Billion requests/day | ~12,000 QPS |
| 1 character (ASCII) | 1 byte |
| 1 character (UTF-8, avg) | ~2-3 bytes |
| Average tweet/message | ~200 bytes |
| Average web page | ~2 MB |
| Average photo | ~200 KB |
| Average short video (1 min) | ~5 MB |
| 1 TB | 10^12 bytes |

### Estimation Example: Twitter-Like System

```python
# Back-of-the-envelope: How much storage for tweets in 1 year?

daily_active_users = 200_000_000       # 200M DAU
tweets_per_user_per_day = 2            # avg
avg_tweet_size_bytes = 280             # text only (280 chars × ~1 byte)
media_fraction = 0.10                  # 10% of tweets have media
avg_media_size_bytes = 200_000         # 200 KB average image

# Text storage per day
text_per_day = daily_active_users * tweets_per_user_per_day * avg_tweet_size_bytes
print(f"Text per day: {text_per_day / 1e9:.1f} GB")
# ~112 GB/day

# Media storage per day
tweets_per_day = daily_active_users * tweets_per_user_per_day
media_per_day = tweets_per_day * media_fraction * avg_media_size_bytes
print(f"Media per day: {media_per_day / 1e12:.1f} TB")
# ~8 TB/day

# Per year
text_per_year = text_per_day * 365
media_per_year = media_per_day * 365
print(f"Text per year: {text_per_year / 1e12:.1f} TB")   # ~41 TB
print(f"Media per year: {media_per_year / 1e15:.1f} PB")  # ~2.9 PB

# QPS
total_tweets_per_day = tweets_per_day  # 400M
qps = total_tweets_per_day / 86400
peak_qps = qps * 3  # assume 3x peak-to-average ratio
print(f"Avg QPS: {qps:,.0f}")          # ~4,630
print(f"Peak QPS: {peak_qps:,.0f}")    # ~13,890
```

---

## 8. Consistent Hashing

A technique for distributing data across a cluster of nodes so that **adding or removing
a node only requires redistributing a minimal amount of data** (not all of it).

### The Problem with Simple Hashing

```python
# Simple modular hashing: server = hash(key) % num_servers
# Problem: adding/removing a server changes MOST key assignments

def simple_hash(key: str, num_servers: int) -> int:
    """Assign key to a server using modular hashing."""
    return hash(key) % num_servers

# With 3 servers
for key in ["user:1", "user:2", "user:3", "user:4", "user:5"]:
    print(f"{key} -> server {simple_hash(key, 3)}")

print("--- Add a 4th server ---")

# With 4 servers: almost ALL keys move to different servers!
for key in ["user:1", "user:2", "user:3", "user:4", "user:5"]:
    print(f"{key} -> server {simple_hash(key, 4)}")
```

### How Consistent Hashing Works

1. Imagine a **hash ring** (0 to 2^32 - 1, wrapping around).
2. Each **server** is hashed to a position on the ring.
3. Each **key** is hashed to a position and assigned to the **next server clockwise**.
4. When a server is added/removed, only keys between it and the previous server are reassigned.

```python
import hashlib
from bisect import bisect_right

class ConsistentHashRing:
    """
    Consistent hash ring with virtual nodes.
    
    Virtual nodes (replicas) improve load distribution — each physical
    server is placed at multiple positions on the ring.
    """
    
    def __init__(self, num_virtual_nodes: int = 150):
        self.num_virtual_nodes = num_virtual_nodes
        self.ring: list[int] = []          # sorted hash positions
        self.ring_map: dict[int, str] = {} # hash position -> server name
    
    def _hash(self, key: str) -> int:
        """Compute a consistent hash (MD5-based, not Python's built-in)."""
        digest = hashlib.md5(key.encode()).hexdigest()
        return int(digest, 16)
    
    def add_server(self, server: str) -> None:
        """Add a server with its virtual nodes to the ring."""
        for i in range(self.num_virtual_nodes):
            virtual_key = f"{server}#vn{i}"
            h = self._hash(virtual_key)
            self.ring.append(h)
            self.ring_map[h] = server
        self.ring.sort()
    
    def remove_server(self, server: str) -> None:
        """Remove a server and all its virtual nodes from the ring."""
        for i in range(self.num_virtual_nodes):
            virtual_key = f"{server}#vn{i}"
            h = self._hash(virtual_key)
            # Note: list.remove() is O(n) per call, making this O(n * num_virtual_nodes).
            # For production use, consider rebuilding the ring or using a SortedList.
            self.ring.remove(h)
            del self.ring_map[h]
    
    def get_server(self, key: str) -> str:
        """Find which server a given key maps to."""
        if not self.ring:
            raise ValueError("No servers in the ring")
        h = self._hash(key)
        # Find the first server position clockwise from the key's hash
        idx = bisect_right(self.ring, h)
        if idx == len(self.ring):
            idx = 0  # wrap around
        return self.ring_map[self.ring[idx]]


# Demo
ring = ConsistentHashRing(num_virtual_nodes=150)
for server in ["server-A", "server-B", "server-C"]:
    ring.add_server(server)

keys = ["user:100", "user:200", "user:300", "user:400", "user:500"]

print("=== Before adding server-D ===")
assignments_before = {k: ring.get_server(k) for k in keys}
for k, s in assignments_before.items():
    print(f"  {k} -> {s}")

ring.add_server("server-D")

print("\n=== After adding server-D ===")
moved = 0
for k in keys:
    new_server = ring.get_server(k)
    marker = " (MOVED)" if new_server != assignments_before[k] else ""
    print(f"  {k} -> {new_server}{marker}")
    if marker:
        moved += 1

print(f"\nOnly {moved}/{len(keys)} keys moved — minimal disruption!")
```

> **Used By**: DynamoDB, Cassandra, Akamai CDN, Memcached (client-side).

---

## 9. Rate Limiting

Controlling the rate of requests a user/client can make. Protects against abuse, DDoS, and ensures fair usage.

### Common Algorithms

| Algorithm | How It Works | Pros | Cons |
|-----------|-------------|------|------|
| **Token Bucket** | Tokens added at fixed rate; each request consumes a token | Allows bursts, smooth | Needs tuning of bucket size |
| **Leaky Bucket** | Requests queued and processed at fixed rate | Smooth output rate | No burst handling |
| **Fixed Window** | Count requests in fixed time windows (e.g., per minute) | Simple | Burst at window edges |
| **Sliding Window Log** | Track timestamp of each request, count in rolling window | Accurate | Memory-heavy (stores all timestamps) |
| **Sliding Window Counter** | Hybrid: weighted count from current + previous window | Memory-efficient, accurate | Approximate |

### Token Bucket Implementation

```python
import time

class TokenBucketRateLimiter:
    """
    Token Bucket rate limiter.
    
    Tokens are added at a fixed rate (refill_rate per second).
    Each request consumes one token. Requests are rejected when
    the bucket is empty. Allows controlled bursts up to max_tokens.
    """
    
    def __init__(self, max_tokens: int, refill_rate: float):
        self.max_tokens = max_tokens        # bucket capacity (max burst size)
        self.refill_rate = refill_rate      # tokens added per second
        self.tokens = max_tokens            # start full
        self.last_refill_time = time.monotonic()
    
    def _refill(self) -> None:
        """Add tokens based on elapsed time since last refill."""
        now = time.monotonic()
        elapsed = now - self.last_refill_time
        new_tokens = elapsed * self.refill_rate
        self.tokens = min(self.max_tokens, self.tokens + new_tokens)
        self.last_refill_time = now
    
    def allow_request(self) -> bool:
        """Return True if the request is allowed, False if rate-limited."""
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


# Demo: 5 tokens max, refill 1 token/second
limiter = TokenBucketRateLimiter(max_tokens=5, refill_rate=1.0)

# Burst of 7 requests
for i in range(7):
    allowed = limiter.allow_request()
    print(f"Request {i+1}: {'ALLOWED' if allowed else 'REJECTED'}")

# Output:
# Request 1: ALLOWED   (5 -> 4 tokens)
# Request 2: ALLOWED   (4 -> 3 tokens)
# Request 3: ALLOWED   (3 -> 2 tokens)
# Request 4: ALLOWED   (2 -> 1 tokens)
# Request 5: ALLOWED   (1 -> 0 tokens)
# Request 6: REJECTED  (0 tokens, bucket empty)
# Request 7: REJECTED
```

---

## 10. Proxies

An intermediary server between client and backend.

### Forward Proxy vs. Reverse Proxy

```text
Forward Proxy (client-side):

  Client ──> [Forward Proxy] ──> Internet ──> Server
              (hides client)

  Use cases: corporate firewalls, privacy/anonymity, access control

Reverse Proxy (server-side):

  Client ──> Internet ──> [Reverse Proxy] ──> Server(s)
                           (hides servers)

  Use cases: load balancing, SSL termination, caching, DDoS protection
```

| Aspect | Forward Proxy | Reverse Proxy |
|--------|---------------|---------------|
| **Who uses it** | Client | Server |
| **Hides** | Client identity | Server identity/topology |
| **Examples** | Squid, corporate VPN | Nginx, HAProxy, Cloudflare |
| **Common in HLD?** | Rarely discussed | Very common (load balancer = reverse proxy) |

---

## 11. DNS (Domain Name System)

Translates human-readable domain names to IP addresses. The "phone book" of the internet.

### DNS Resolution Flow

```text
Browser ──> Local DNS Cache
              │ miss
              ▼
         DNS Resolver (ISP)
              │ miss
              ▼
         Root Name Server ──> TLD Server (.com) ──> Authoritative NS
              │                                          │
              └──────────── IP address ◄─────────────────┘
```

### DNS in System Design
- **DNS-based load balancing**: Return different IPs for the same domain (Round-Robin DNS).
- **GeoDNS**: Return IP of the nearest datacenter based on client location.
- **TTL (Time-To-Live)**: How long DNS results are cached. Low TTL = faster failover, more DNS queries.

---

## 12. Content Delivery Networks (CDNs)

A geographically distributed network of proxy servers that cache content close to users.

### How CDNs Work
```text
User (Tokyo) ──> CDN Edge Server (Tokyo) ──[cache hit]──> Response (fast!)
                         │
                    [cache miss]
                         │
                         ▼
                  Origin Server (US-East)
```

### Push vs. Pull CDN

| Type | How It Works | Best For |
|------|-------------|----------|
| **Push CDN** | You upload content to CDN proactively | Small sites, content that rarely changes |
| **Pull CDN** | CDN fetches from origin on first request, then caches | High-traffic sites, dynamic content mix |

### CDN in System Design
- Serve **static assets** (images, CSS, JS, videos) from CDN — offloads origin server.
- Reduces latency for global users by serving from nearby edge servers.
- Can also cache **API responses** with appropriate cache headers.

---

## 13. Summary of Trade-offs

| Choice | Pro | Con | When to use |
|--------|-----|-----|-------------|
| **Vertical Scale** | Simple, no code changes | Hardware limit, SPOF | Early-stage startups, internal tools |
| **Horizontal Scale** | Resilient, cost-effective | Complex, requires stateless design | Large-scale consumer apps |
| **Consistency (CP)** | Data accuracy guaranteed | Higher latency, potential downtime | Finance, inventory, auth |
| **Availability (AP)** | Always online | Stale data possible | Social media, recommendations |
| **Strong Consistency** | No stale reads | High latency (synchronous replication) | SQL primary-replica, single-leader |
| **Eventual Consistency** | High availability, low latency | Stale reads during convergence | NoSQL, multi-leader, leaderless |
| **Caching** | Dramatically reduces latency | Cache invalidation complexity, stale data | Read-heavy workloads |
| **CDN** | Low latency for global users | Cost, cache invalidation | Static assets, media-heavy apps |
| **Rate Limiting** | Protects against abuse/DDoS | May reject legitimate traffic | All public-facing APIs |

---

## Practice Problems

### Problem 1: Availability Calculator (Easy)

**Problem**: Given a list of component availabilities in a **serial** (all must work) system,
calculate the overall system availability. Then do the same for **parallel** (redundant) components.

**Formulas**:
- Serial: `A_total = A1 × A2 × ... × An` (all must work)
- Parallel: `A_total = 1 - (1-A1) × (1-A2) × ... × (1-An)` (at least one must work)

<details>
<summary><strong>Hint</strong></summary>

For serial systems, multiply all availabilities. For parallel systems, calculate the
probability that ALL components fail simultaneously, then subtract from 1.

</details>

<details>
<summary><strong>Solution</strong></summary>

```python
from functools import reduce

def serial_availability(components: list[float]) -> float:
    """
    Calculate availability of a serial system.
    All components must be operational for the system to work.
    
    Example: Web server (99.9%) -> Database (99.9%)
    Overall = 0.999 * 0.999 = 99.8%
    """
    return reduce(lambda a, b: a * b, components)


def parallel_availability(components: list[float]) -> float:
    """
    Calculate availability of a parallel (redundant) system.
    At least one component must be operational.
    
    Example: Two database replicas, each 99.9%
    P(both fail) = 0.001 * 0.001 = 0.000001
    Overall = 1 - 0.000001 = 99.9999%
    """
    prob_all_fail = reduce(lambda a, b: a * (1 - b), components, 1.0)
    return 1.0 - prob_all_fail


# --- Test Cases ---

# Serial: LB (99.99%) -> App Server (99.9%) -> DB (99.9%)
serial = serial_availability([0.9999, 0.999, 0.999])
print(f"Serial availability: {serial * 100:.4f}%")
# 99.8801% — the weakest link drags the whole system down

# Parallel: Two DB replicas, each 99.9%
parallel = parallel_availability([0.999, 0.999])
print(f"Parallel (2 DBs) availability: {parallel * 100:.6f}%")
# 99.999900% — redundancy massively improves availability

# Combined: Serial system where the DB layer has parallel redundancy
db_layer = parallel_availability([0.999, 0.999])
overall = serial_availability([0.9999, 0.999, db_layer])
print(f"Combined availability: {overall * 100:.6f}%")
# Much better than having a single DB
```

</details>

---

### Problem 2: QPS and Storage Estimator (Easy)

**Problem**: Design a function that takes system parameters and produces back-of-the-envelope
estimates for QPS, storage, and bandwidth.

A URL shortening service has:
- 100M new URLs per month
- 10:1 read-to-write ratio
- Each URL mapping is ~500 bytes
- Service should run for 5 years

Estimate: write QPS, read QPS, total storage, and bandwidth.

<details>
<summary><strong>Hint</strong></summary>

Convert monthly numbers to per-second. Multiply by duration for storage.
Bandwidth = QPS × size per request.

</details>

<details>
<summary><strong>Solution</strong></summary>

```python
def estimate_system(
    new_entries_per_month: int,
    read_write_ratio: int,
    entry_size_bytes: int,
    duration_years: int,
    peak_multiplier: float = 3.0,
) -> dict:
    """
    Back-of-the-envelope system estimation.
    
    Returns QPS, storage, and bandwidth estimates.
    """
    seconds_per_month = 30 * 24 * 3600  # ~2.6M

    write_qps = new_entries_per_month / seconds_per_month
    read_qps = write_qps * read_write_ratio

    peak_write_qps = write_qps * peak_multiplier
    peak_read_qps = read_qps * peak_multiplier

    total_entries = new_entries_per_month * 12 * duration_years
    total_storage_bytes = total_entries * entry_size_bytes

    write_bandwidth_bps = write_qps * entry_size_bytes
    read_bandwidth_bps = read_qps * entry_size_bytes

    return {
        "write_qps": write_qps,
        "read_qps": read_qps,
        "peak_write_qps": peak_write_qps,
        "peak_read_qps": peak_read_qps,
        "total_storage_tb": total_storage_bytes / 1e12,
        "write_bandwidth_mbps": write_bandwidth_bps * 8 / 1e6,
        "read_bandwidth_mbps": read_bandwidth_bps * 8 / 1e6,
    }


# URL Shortener estimates
result = estimate_system(
    new_entries_per_month=100_000_000,
    read_write_ratio=10,
    entry_size_bytes=500,
    duration_years=5,
)

for metric, value in result.items():
    print(f"  {metric}: {value:,.2f}")

# Expected output (approx):
#   write_qps: 38.58
#   read_qps: 385.80
#   peak_write_qps: 115.74
#   peak_read_qps: 1,157.41
#   total_storage_tb: 3.00
#   write_bandwidth_mbps: 0.15
#   read_bandwidth_mbps: 1.54
```

</details>

---

### Problem 3: CAP Theorem Decision Engine (Medium)

**Problem**: Build a function that takes system requirements and recommends whether the system
should be CP or AP. Given a list of system characteristics (e.g., "financial transactions",
"global users", "strong consistency needed", "high availability needed"), analyze the trade-offs
and return a recommendation with justification.

Then implement a `SystemDesignAdvisor` class that also considers PACELC — recommending the
normal-operation trade-off (latency vs consistency) in addition to the partition behavior.

<details>
<summary><strong>Hint</strong></summary>

Define sets of keywords/characteristics that map to CP vs AP. For PACELC, also consider
whether the system is latency-sensitive (user-facing, real-time) or consistency-sensitive
(transactions, coordination). Return a structured result with the classification and reasoning.

</details>

<details>
<summary><strong>Solution</strong></summary>

```python
from dataclasses import dataclass


# Characteristics that strongly suggest CP or AP
CP_INDICATORS = {
    "financial_transactions", "inventory_management", "booking_system",
    "strong_consistency", "coordination", "service_discovery",
    "leader_election", "distributed_locks", "payment_processing",
}

AP_INDICATORS = {
    "social_media", "recommendations", "user_feed", "content_delivery",
    "high_availability", "global_users", "analytics", "logging",
    "eventual_consistency_ok", "shopping_cart",
}

LATENCY_SENSITIVE = {
    "user_facing", "real_time", "gaming", "search", "social_media",
    "content_delivery", "recommendations", "user_feed", "shopping_cart",
}

CONSISTENCY_SENSITIVE = {
    "financial_transactions", "inventory_management", "booking_system",
    "payment_processing", "coordination", "distributed_locks",
    "leader_election", "service_discovery", "strong_consistency",
}


@dataclass
class DesignRecommendation:
    partition_choice: str  # "CP" or "AP"
    normal_choice: str     # "EL" (favor latency) or "EC" (favor consistency)
    pacelc: str            # e.g., "PA/EL" or "PC/EC"
    reasoning: list[str]
    example_systems: list[str]


PACELC_EXAMPLES = {
    "PA/EL": ["DynamoDB", "Cassandra"],
    "PA/EC": ["PNUTS (Yahoo)"],
    "PC/EL": ["Cosmos DB (bounded staleness)"],
    "PC/EC": ["MongoDB (majority)", "HBase", "ZooKeeper"],
}


def recommend_design(characteristics: set[str]) -> DesignRecommendation:
    """
    Analyze system characteristics and recommend CAP/PACELC trade-offs.
    """
    reasoning = []

    # --- Partition behavior (CP vs AP) ---
    cp_matches = characteristics & CP_INDICATORS
    ap_matches = characteristics & AP_INDICATORS

    if len(cp_matches) >= len(ap_matches):
        partition_choice = "CP"
        reasoning.append(
            f"CP recommended: data correctness is critical "
            f"(matched: {', '.join(sorted(cp_matches)) or 'default'})"
        )
    else:
        partition_choice = "AP"
        reasoning.append(
            f"AP recommended: availability is prioritized "
            f"(matched: {', '.join(sorted(ap_matches))})"
        )

    # --- Normal operation (Latency vs Consistency) ---
    lat_matches = characteristics & LATENCY_SENSITIVE
    con_matches = characteristics & CONSISTENCY_SENSITIVE

    if len(lat_matches) > len(con_matches):
        normal_choice = "EL"
        reasoning.append(
            f"Favor latency in normal operation "
            f"(matched: {', '.join(sorted(lat_matches))})"
        )
    else:
        normal_choice = "EC"
        reasoning.append(
            f"Favor consistency in normal operation "
            f"(matched: {', '.join(sorted(con_matches)) or 'default'})"
        )

    # --- Combine into PACELC ---
    p_label = "PA" if partition_choice == "AP" else "PC"
    pacelc = f"{p_label}/{normal_choice}"
    examples = PACELC_EXAMPLES.get(pacelc, [])

    reasoning.append(f"PACELC classification: {pacelc}")

    return DesignRecommendation(
        partition_choice=partition_choice,
        normal_choice=normal_choice,
        pacelc=pacelc,
        reasoning=reasoning,
        example_systems=examples,
    )


# --- Test Cases ---

# Case 1: Payment system — should be PC/EC
payment = recommend_design({"financial_transactions", "payment_processing", "strong_consistency"})
print(f"Payment System: {payment.pacelc}")
for r in payment.reasoning:
    print(f"  - {r}")
print(f"  Similar to: {', '.join(payment.example_systems)}")

print()

# Case 2: Social media feed — should be PA/EL
social = recommend_design({"social_media", "user_feed", "global_users", "user_facing"})
print(f"Social Feed: {social.pacelc}")
for r in social.reasoning:
    print(f"  - {r}")
print(f"  Similar to: {', '.join(social.example_systems)}")

print()

# Case 3: E-commerce cart — mixed signals
cart = recommend_design({"shopping_cart", "user_facing", "eventual_consistency_ok"})
print(f"Shopping Cart: {cart.pacelc}")
for r in cart.reasoning:
    print(f"  - {r}")

# Expected:
#   Payment System: PC/EC (consistency everywhere)
#   Social Feed: PA/EL (availability + low latency)
#   Shopping Cart: PA/EL (available + responsive)
```

</details>

---

### Problem 4: Consistent Hash Ring Simulation (Medium)

**Problem**: Implement a consistent hash ring that supports:
1. Adding and removing servers
2. Mapping keys to servers
3. **Measuring load distribution** across servers for N random keys

Test: add 3 servers with 100 virtual nodes each, hash 10,000 random keys, and print the
distribution. Then add a 4th server and show how many keys moved.

<details>
<summary><strong>Hint</strong></summary>

Reuse the `ConsistentHashRing` class from Section 8. Generate random keys, count assignments
per server before and after adding a node, and compare.

</details>

<details>
<summary><strong>Solution</strong></summary>

```python
import hashlib
from bisect import bisect_right
from collections import Counter

class ConsistentHashRing:
    def __init__(self, num_virtual_nodes: int = 100):
        self.num_virtual_nodes = num_virtual_nodes
        self.ring: list[int] = []
        self.ring_map: dict[int, str] = {}
    
    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_server(self, server: str) -> None:
        for i in range(self.num_virtual_nodes):
            h = self._hash(f"{server}#vn{i}")
            self.ring.append(h)
            self.ring_map[h] = server
        self.ring.sort()
    
    def remove_server(self, server: str) -> None:
        self.ring = [h for h in self.ring if self.ring_map.get(h) != server]
        self.ring_map = {h: s for h, s in self.ring_map.items() if s != server}
    
    def get_server(self, key: str) -> str:
        if not self.ring:
            raise ValueError("Empty ring")
        h = self._hash(key)
        idx = bisect_right(self.ring, h) % len(self.ring)
        return self.ring_map[self.ring[idx]]


def measure_distribution(ring: ConsistentHashRing, keys: list[str]) -> Counter:
    """Count how many keys are assigned to each server."""
    return Counter(ring.get_server(k) for k in keys)


# --- Simulation ---
ring = ConsistentHashRing(num_virtual_nodes=100)
for s in ["server-A", "server-B", "server-C"]:
    ring.add_server(s)

# Generate 10,000 random keys
keys = [f"key:{i}" for i in range(10_000)]

# Measure distribution before
dist_before = measure_distribution(ring, keys)
assignments_before = {k: ring.get_server(k) for k in keys}

print("Distribution with 3 servers:")
for server, count in sorted(dist_before.items()):
    pct = count / len(keys) * 100
    print(f"  {server}: {count} keys ({pct:.1f}%)")
# Expect roughly ~33% each (with some variance)

# Add a 4th server
ring.add_server("server-D")
dist_after = measure_distribution(ring, keys)

print("\nDistribution with 4 servers:")
for server, count in sorted(dist_after.items()):
    pct = count / len(keys) * 100
    print(f"  {server}: {count} keys ({pct:.1f}%)")

# Count how many keys moved
moved = sum(1 for k in keys if ring.get_server(k) != assignments_before[k])
print(f"\nKeys moved: {moved}/{len(keys)} ({moved/len(keys)*100:.1f}%)")
# Expect roughly ~25% moved (1/4 of keys, since we went from 3 to 4 servers)
```

</details>

---

### Problem 5: Design a Rate Limiter with Multiple Strategies (Hard)

**Problem**: Implement a rate limiter that supports three strategies via a common interface:
1. **Token Bucket** — allows bursts up to bucket capacity
2. **Fixed Window** — counts requests per fixed time window
3. **Sliding Window Log** — tracks exact timestamps in a rolling window

Requirements:
- Common `allow_request(user_id: str) -> bool` interface
- Support per-user rate limiting
- Write tests that verify each strategy handles edge cases

<details>
<summary><strong>Hint</strong></summary>

Use an abstract base class (ABC). For sliding window log, store timestamps in a deque
and prune expired ones on each call. For fixed window, compute the current window key
from `int(time / window_size)`.

</details>

<details>
<summary><strong>Solution</strong></summary>

```python
import time
from abc import ABC, abstractmethod
from collections import defaultdict, deque

class RateLimiter(ABC):
    """Abstract rate limiter interface."""
    
    @abstractmethod
    def allow_request(self, user_id: str) -> bool:
        """Return True if the request is allowed for this user."""
        ...


class TokenBucketLimiter(RateLimiter):
    """
    Token Bucket: tokens refill at a fixed rate.
    Allows short bursts up to max_tokens.
    """
    
    def __init__(self, max_tokens: int, refill_rate: float):
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate  # tokens per second
        self.buckets: dict[str, list[float]] = {}  # user -> [tokens, last_time]
    
    def allow_request(self, user_id: str) -> bool:
        now = time.monotonic()
        
        if user_id not in self.buckets:
            self.buckets[user_id] = [self.max_tokens, now]
        
        tokens, last_time = self.buckets[user_id]
        elapsed = now - last_time
        tokens = min(self.max_tokens, tokens + elapsed * self.refill_rate)
        
        if tokens >= 1:
            self.buckets[user_id] = [tokens - 1, now]
            return True
        
        self.buckets[user_id] = [tokens, now]
        return False


class FixedWindowLimiter(RateLimiter):
    """
    Fixed Window: count requests per discrete time window.
    Simple but allows up to 2x the limit at window boundaries.
    """
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # user -> {window_key: count}
        self.windows: dict[str, dict[int, int]] = defaultdict(dict)
    
    def allow_request(self, user_id: str) -> bool:
        now = time.monotonic()
        window_key = int(now // self.window_seconds)
        
        user_windows = self.windows[user_id]
        current_count = user_windows.get(window_key, 0)
        
        if current_count < self.max_requests:
            user_windows[window_key] = current_count + 1
            # Clean up old windows to prevent memory leak
            old_keys = [k for k in user_windows if k < window_key]
            for k in old_keys:
                del user_windows[k]
            return True
        return False


class SlidingWindowLogLimiter(RateLimiter):
    """
    Sliding Window Log: track exact timestamps of each request.
    Most accurate but uses more memory (O(max_requests) per user).
    """
    
    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.logs: dict[str, deque[float]] = defaultdict(deque)
    
    def allow_request(self, user_id: str) -> bool:
        now = time.monotonic()
        log = self.logs[user_id]
        
        # Remove timestamps outside the sliding window
        cutoff = now - self.window_seconds
        while log and log[0] <= cutoff:
            log.popleft()
        
        if len(log) < self.max_requests:
            log.append(now)
            return True
        return False


# --- Test all three strategies ---
def test_limiter(name: str, limiter: RateLimiter) -> None:
    print(f"\n--- {name} ---")
    user = "user:alice"
    
    # Burst of 7 requests (limit is 5)
    results = []
    for i in range(7):
        allowed = limiter.allow_request(user)
        results.append("OK" if allowed else "REJECT")
    
    print(f"  Burst of 7: {results}")
    # First 5 should be OK, last 2 rejected
    
    # Different user should have independent limits
    other_allowed = limiter.allow_request("user:bob")
    print(f"  Different user (bob): {'OK' if other_allowed else 'REJECT'}")
    # Should be OK — independent bucket


test_limiter("Token Bucket", TokenBucketLimiter(max_tokens=5, refill_rate=1.0))
test_limiter("Fixed Window", FixedWindowLimiter(max_requests=5, window_seconds=60))
test_limiter("Sliding Window Log", SlidingWindowLogLimiter(max_requests=5, window_seconds=60.0))

# Expected output for all three:
#   Burst of 7: ['OK', 'OK', 'OK', 'OK', 'OK', 'REJECT', 'REJECT']
#   Different user (bob): OK
```

</details>

---

## Next Steps

Continue to [Architectural Patterns](./02-architectural-patterns.md) to learn about load
balancers, caching strategies, message queues, and communication protocols.
