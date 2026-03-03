# Databases

Choosing the right database and scaling it is the most important part of any HLD interview. This section covers the fundamentals of databases, how they scale, and when to use which type.

> **Prerequisites:** [Architectural Patterns](./02-architectural-patterns.md)

## 1. SQL vs. NoSQL

| Feature | SQL (PostgreSQL, MySQL) | NoSQL (MongoDB, Cassandra, Redis) |
|---------|-------------------------|-----------------------------------|
| **Schema** | Rigid, predefined (tables, columns, types) | Flexible, dynamic (schema-on-read) |
| **Scaling** | Primarily vertical; horizontal possible but harder (read replicas, sharding via Citus/Vitess) | Horizontal by design (built-in sharding) |
| **Joins** | Powerful multi-table joins | Poor or none; data is typically denormalized |
| **Transactions** | Strong ACID support | Varies: MongoDB supports ACID (since v4.0), Cassandra offers tunable consistency |
| **Query Language** | SQL (standardized) | Database-specific APIs or query languages |
| **Best For** | Complex relationships, transactions, strong consistency | High throughput, flexible schemas, horizontal scale |

### When to Choose SQL
- Complex relationships between entities (e.g., e-commerce: users, orders, products, payments).
- Strong consistency is required (e.g., banking, inventory management).
- You need complex queries with joins, aggregations, and GROUP BY.
- Data schema is well-defined and unlikely to change frequently.

### When to Choose NoSQL
- Massive write throughput (e.g., IoT sensor data, logging).
- Data is naturally hierarchical or document-shaped (e.g., user profiles, product catalogs).
- Schema evolves rapidly (early-stage startups iterating fast).
- You need horizontal scaling with minimal operational overhead.

---

## 2. ACID Properties

Every relational database transaction guarantees these four properties:

| Property | Definition | Example |
|----------|-----------|---------|
| **Atomicity** | All operations in a transaction succeed or all fail. No partial commits. | Transferring $100: debit and credit both happen, or neither does. |
| **Consistency** | A transaction moves the database from one valid state to another. All database invariants and constraints (foreign keys, unique, check constraints, triggers) must hold before and after the transaction. | A transfer cannot create or destroy money — if Account A is debited $100, Account B must be credited $100. A foreign key referencing a non-existent user is rejected. |
| **Isolation** | Concurrent transactions don't interfere with each other. The result is as if they ran sequentially. | Two people buying the last item: only one succeeds. |
| **Durability** | Once committed, data survives crashes (written to disk/WAL). | After a commit, even a power failure won't lose the data. |

### BASE (NoSQL Alternative)
NoSQL databases often follow BASE instead of ACID:
- **Basically Available**: The system guarantees availability (every request gets a response).
- **Soft State**: The state of the system may change over time, even without input (due to async replication).
- **Eventually Consistent**: The system will eventually become consistent (given enough time without new writes).

---

## 3. Transaction Isolation Levels

Defines how a transaction is isolated from others. Higher isolation = fewer anomalies but worse performance.

| Level | Dirty Reads | Non-Repeatable Reads | Phantom Reads | Performance |
|-------|:-----------:|:--------------------:|:-------------:|:-----------:|
| **Read Uncommitted** | Possible | Possible | Possible | Fastest |
| **Read Committed** | Prevented | Possible | Possible | Fast |
| **Repeatable Read** | Prevented | Prevented | Possible | Moderate |
| **Serializable** | Prevented | Prevented | Prevented | Slowest |

**Anomaly Definitions:**
- **Dirty Read**: Reading data written by an uncommitted transaction. If that transaction rolls back, you read data that never existed.
- **Non-Repeatable Read**: Reading the same row twice within a transaction yields different results because another transaction modified or deleted that row and committed in between.
- **Phantom Read**: Re-executing a range query within a transaction returns a different set of rows because another committed transaction inserted, deleted, or updated rows that now match (or no longer match) the query predicate.

> **Default Levels:** PostgreSQL defaults to **Read Committed**. MySQL (InnoDB) defaults to **Repeatable Read**.

---

## 4. Indexing

An index is a data structure (typically a B-Tree or hash table) that speeds up reads at the cost of slower writes and additional storage.

### How Indexes Work
Without an index, the database performs a **full table scan** (O(n)). With a B-Tree index, lookups become **O(log n)**.

### Types of Indexes
- **Primary Index**: Automatically created on the primary key. Determines physical row order in some engines (clustered index).
- **Secondary Index**: Created on non-primary columns you frequently query or filter on.
- **Composite Index**: An index on multiple columns. Column order matters — follows the **leftmost prefix rule**.
- **Covering Index**: An index that contains all columns needed by a query, so the database never reads the actual table.
- **Unique Index**: Enforces uniqueness on a column (or combination of columns).

### Composite Index Example
```sql
-- Index on (country, city, zip_code)
-- This index speeds up queries that filter by:
--   (country)                          ✅ uses index
--   (country, city)                    ✅ uses index
--   (country, city, zip_code)          ✅ uses index
--   (city)                             ❌ skips leftmost prefix, no index
--   (zip_code)                         ❌ skips leftmost prefix, no index

CREATE INDEX idx_location ON addresses (country, city, zip_code);
```

### Trade-offs
| Pro | Con |
|-----|-----|
| Faster reads (O(log n) vs O(n)) | Slower writes (index must be updated on INSERT/UPDATE/DELETE) |
| Supports range queries efficiently | Uses additional disk space |
| Can eliminate full table scans | Too many indexes degrade write performance |

> **Rule of Thumb:** Index columns that appear in WHERE, JOIN, and ORDER BY clauses. Don't create standalone indexes on low-cardinality columns (e.g., a boolean `is_active` with only two values) — but they can be effective as part of composite indexes or as partial index predicates (e.g., `CREATE INDEX ... WHERE is_active = TRUE`).

---

## 5. Replication

Copying data across multiple database servers for fault tolerance and read scalability.

### Leader-Follower (Master-Slave)
- **One leader** accepts all writes. **Multiple followers** replicate the leader's data and serve reads.
- **Use case:** Read-heavy workloads (most web applications). Scale reads by adding followers.
- **Failure:** If the leader fails, a follower is promoted (failover). Risk of data loss if replication was asynchronous.

```text
               ┌──────────┐
  Writes ────> │  Leader   │
               └────┬──┬───┘
            Repl.   │  │   Repl.
           ┌────────┘  └────────┐
           v                    v
     ┌──────────┐         ┌──────────┐
     │ Follower │         │ Follower │    <──── Reads
     └──────────┘         └──────────┘
```

### Multi-Leader (Master-Master)
- **Multiple leaders** accept writes. Each replicates to the others.
- **Use case:** Multi-datacenter setups (each datacenter has its own leader).
- **Challenge:** Write conflicts. If two leaders modify the same row, you need conflict resolution (last-write-wins, merge, or custom logic).

### Leaderless (Dynamo-Style)
- **Any node** can accept reads and writes. Uses **quorum** for consistency.
- **Quorum formula:** For `N` replicas, write to `W` nodes and read from `R` nodes. If `W + R > N`, you're guaranteed to read the latest write.
- **Use case:** Cassandra, Amazon DynamoDB. High availability, tunable consistency.
- **Example:** N=3, W=2, R=2. Every read overlaps with at least one node that has the latest write.

### Synchronous vs. Asynchronous Replication
| Type | Behavior | Pro | Con |
|------|----------|-----|-----|
| **Synchronous** | Leader waits for follower ACK before confirming write | No data loss on failover | Higher write latency |
| **Asynchronous** | Leader confirms write immediately, replicates later | Lower write latency | Possible data loss on failover |
| **Semi-Synchronous** | At least one follower is synchronous, rest are async | Balance of safety and speed | Slightly higher latency than async |

---

## 6. Sharding (Horizontal Partitioning)

Splitting a large dataset across multiple database servers (shards). Each shard holds a subset of the data. Essential for **write scaling** — unlike replication, which only scales reads.

### Sharding Strategies

| Strategy | How It Works | Pro | Con |
|----------|-------------|-----|-----|
| **Range-Based** | Rows with keys A-M go to Shard 1, N-Z to Shard 2 | Simple, good for range queries | Hot spots if data is skewed |
| **Hash-Based** | `hash(shard_key) % num_shards` determines the shard | Even distribution | Range queries require scatter-gather |
| **Directory-Based** | A lookup service maps each key to a shard | Flexible | Lookup service is a single point of failure |

### Consistent Hashing
A technique to minimize data movement when adding or removing shards. Instead of `hash % N` (which remaps almost everything when N changes), keys and nodes are placed on a virtual ring. Only keys between the old and new node positions are remapped.

```text
        Node A
       /      \
      /   Ring  \
  Node D        Node B
      \        /
       \      /
        Node C

Adding Node E between A and B only moves keys
in the arc from A to E — all other keys stay put.
```

### Choosing a Shard Key
The shard key is the **most critical decision** in a sharded architecture.

**Good shard key properties:**
- High cardinality (many distinct values) — e.g., `user_id`
- Even distribution — no single value dominates
- Aligns with query patterns — most queries include the shard key

**Bad shard key examples:**
- `country_code` — a few countries dominate traffic (hot shards)
- `created_date` — all new writes go to one shard
- `status` — very few distinct values

### Challenges of Sharding
- **Cross-shard joins**: Queries spanning multiple shards are expensive (scatter-gather).
- **Rebalancing**: Adding/removing shards requires data migration.
- **Distributed transactions**: ACID across shards is hard (requires 2PC or Sagas).
- **Application complexity**: The application or middleware must be shard-aware.

> **When to Shard:** Shard only when you've exhausted vertical scaling, read replicas, caching, and query optimization. Sharding adds significant operational complexity.

---

## 7. Denormalization

Intentionally adding redundant data to avoid expensive joins at read time.

| Aspect | Normalized | Denormalized |
|--------|-----------|-------------|
| **Data redundancy** | Minimal | Intentional duplication |
| **Read performance** | Slower (joins required) | Faster (pre-joined data) |
| **Write performance** | Faster (single update) | Slower (must update all copies) |
| **Consistency** | Easy (single source of truth) | Harder (duplicates can drift) |
| **Use case** | OLTP, write-heavy | OLAP, read-heavy, NoSQL |

**Example:** In a normalized schema, a `posts` table references `users` via `user_id`. Every time you display a post, you JOIN with `users` to get the author's name. In a denormalized schema, you store `author_name` directly in the `posts` document — faster reads, but you must update every post if the author changes their name.

---

## 8. Distributed Transactions

When a transaction spans multiple services or databases.

### Two-Phase Commit (2PC)
A coordinator ensures all participants either commit or abort together.

```text
Phase 1 (Prepare):
  Coordinator ──> "Can you commit?" ──> Node A ──> "Yes"
  Coordinator ──> "Can you commit?" ──> Node B ──> "Yes"

Phase 2 (Commit):
  Coordinator ──> "Commit!" ──> Node A ──> Done
  Coordinator ──> "Commit!" ──> Node B ──> Done
```

- **Pros:** Strong consistency across nodes.
- **Cons:** Synchronous and blocking. If the coordinator crashes after Phase 1, participants are stuck holding locks (blocking problem). Poor performance and availability.

### Saga Pattern
A sequence of local transactions, each with a compensating transaction to undo its work if a later step fails.

- **Choreography**: Each service emits events. Other services react. Decentralized. Simple for small chains, hard to debug in large ones.
- **Orchestration**: A central orchestrator coordinates the steps. Centralized. Easier to reason about and monitor.

```text
Saga (Orchestration):
  Order Service ──> Payment Service ──> Inventory Service
       │                  │                    │
       │            (if fails)                 │
       │                  │                    │
       └──── Compensate <─┘                    │
                          └── Compensate <─────┘
```

> **2PC vs. Saga:** Use 2PC when you need strong consistency and can tolerate latency (rare in microservices). Use Sagas for eventual consistency with better availability and performance.

---

## 9. Storage Engines

How data is physically stored on disk. The storage engine choice determines read/write performance characteristics.

### B-Trees
- **How:** Balanced tree structure. Data is stored in sorted order across pages on disk. Updates are done in-place.
- **Read performance:** Excellent — O(log n) lookups, range queries follow sorted leaf pages.
- **Write performance:** Moderate — each write requires finding the page, updating it, and possibly splitting pages.
- **Used by:** PostgreSQL, MySQL (InnoDB), most RDBMS.

### LSM Trees (Log-Structured Merge-Trees)
- **How:** Writes go to an in-memory buffer (memtable). When full, it's flushed to disk as a sorted file (SSTable). Background compaction merges SSTables.
- **Read performance:** Moderate — may need to check memtable + multiple SSTables (mitigated by Bloom filters).
- **Write performance:** Excellent — sequential disk writes (append-only), no random I/O.
- **Used by:** Cassandra, RocksDB, LevelDB, HBase.

| Feature | B-Trees | LSM Trees |
|---------|---------|-----------|
| **Read** | Fast (O(log n), in-place) | Slower (check multiple levels, mitigated by Bloom filters) |
| **Write** | Moderate (random I/O, in-place updates) | Fast (sequential I/O, append-only) |
| **Space** | Some internal fragmentation | Temporary space amplification (duplicate keys across levels until compaction) |
| **Write amplification** | Lower (single in-place update per write) | Higher (data rewritten during compaction) |
| **Best for** | Read-heavy OLTP | Write-heavy workloads |

---

## 10. Consistency Models (Database Context)

How and when updates become visible across replicas. See also [CAP Theorem in Fundamentals](./01-fundamentals.md#4-cap-theorem).

| Model | Guarantee | Example |
|-------|----------|---------|
| **Strong Consistency** | After a write completes, every subsequent read sees that write. | PostgreSQL with synchronous replication, Google Spanner. |
| **Eventual Consistency** | After a write, replicas will converge to the same value *eventually*. Reads may return stale data. | Cassandra (default), DynamoDB, DNS. |
| **Causal Consistency** | Operations that are causally related are seen in the same order by all nodes. Unrelated operations may be seen in any order. | MongoDB (causal consistency sessions). |
| **Read-Your-Writes** | A client always sees its own writes, but may not see others' writes immediately. | Common in leader-follower setups when reading from the leader after writing. |

---

## 11. Storage Types & When to Use Each

### Decision Framework

| Type | Best For | Examples | When to Use |
|------|----------|----------|-------------|
| **Relational (SQL)** | Structured data, transactions, complex queries | PostgreSQL, MySQL, CockroachDB | E-commerce, banking, ERP, any system needing strong consistency and joins |
| **Key-Value** | Simple lookups, caching, sessions | Redis, Memcached, DynamoDB | Session stores, caching layers, leaderboards, rate limiting |
| **Document** | Semi-structured data, flexible schema | MongoDB, CouchDB, Firestore | Product catalogs, user profiles, CMS, event logging |
| **Wide-Column** | High write throughput, time-series | Cassandra, HBase, ScyllaDB | IoT, metrics, messaging apps, activity feeds |
| **Graph** | Highly connected data, relationship queries | Neo4j, Amazon Neptune, ArangoDB | Social networks, fraud detection, recommendation engines |
| **Vector** | Similarity search, embeddings | Pinecone, Milvus, Weaviate, pgvector | LLM/RAG applications, image search, recommendation by similarity |
| **Time-Series** | Ordered time-stamped data | InfluxDB, TimescaleDB, Prometheus | Monitoring, IoT sensors, financial tick data |
| **Search Engine** | Full-text search, analytics | Elasticsearch, OpenSearch | Log aggregation, product search, analytics dashboards |
| **Message Queue / Log** | Event streaming, decoupling services | Kafka, Pulsar, RabbitMQ | Event sourcing, async processing, log aggregation |

### Common Database Choices in HLD Interviews

| Scenario | Recommended DB | Why |
|----------|---------------|-----|
| User accounts, orders, payments | **PostgreSQL** | ACID transactions, complex joins, mature ecosystem |
| Caching layer, session store | **Redis** | In-memory, sub-millisecond latency, built-in data structures |
| Chat message storage (high write throughput) | **Cassandra** | Distributed, handles massive write volumes, tunable consistency |
| Product catalog (flexible schema) | **MongoDB** | Document model fits nested product attributes, flexible schema |
| Social graph (friends, followers) | **Neo4j** | Traversing relationships is O(1) per hop vs expensive SQL joins |
| Real-time analytics dashboard | **Elasticsearch** (search) + **ClickHouse** (analytics) | Full-text search + columnar analytics |
| URL shortener (simple key-value) | **Redis** or **DynamoDB** | Fast key-value lookups, scales horizontally |
| Notification system | **Kafka** (queue) + **Cassandra** (storage) | High throughput ingestion + write-optimized storage |

---

## 12. Database Scaling Strategy (Decision Tree)

Follow this order before jumping to more complex solutions:

```text
1. Optimize Queries & Add Indexes
   │
   ├── Still slow? ──> 2. Add Caching Layer (Redis)
   │                       │
   │                       ├── Still bottlenecked? ──> 3. Read Replicas
   │                       │                              │
   │                       │                              ├── Writes are the bottleneck?
   │                       │                              │   ──> 4. Vertical Scaling (bigger machine)
   │                       │                              │        │
   │                       │                              │        ├── Still not enough?
   │                       │                              │        │   ──> 5. Sharding
   │                       │                              │        │
   │                       │                              │        └── Consider switching to
   │                       │                              │            a write-optimized DB
   │                       │                              │
   │                       │                              └── Reads still slow?
   │                       │                                  ──> Add more replicas or
   │                       │                                      denormalize hot queries
   │                       │
   │                       └── Cache invalidation too complex?
   │                           ──> Reconsider data model
   │
   └── Already fast? ──> Don't over-engineer. Ship it.
```

---

## 13. Connection Pooling

Opening a new database connection for every request is expensive (TCP handshake, authentication, memory allocation). A **connection pool** maintains a set of reusable connections.

```python
# Python 3 — Connection pooling with psycopg2 (PostgreSQL)
import psycopg2
from psycopg2 import pool

# Create a connection pool (min 2, max 10 connections)
connection_pool = pool.SimpleConnectionPool(
    minconn=2,
    maxconn=10,
    host="localhost",
    database="mydb",
    user="admin",
    password="secret",
)

# Get a connection from the pool
conn = connection_pool.getconn()
try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (42,))  # Example user ID
    user = cursor.fetchone()
    cursor.close()
finally:
    # Return the connection to the pool (don't close it)
    connection_pool.putconn(conn)
```

> **In HLD interviews:** Mention connection pooling when discussing how your application servers talk to the database. Tools like **PgBouncer** (PostgreSQL) are dedicated connection poolers that sit between the app and the database.

---

## 14. N+1 Query Problem

A common performance anti-pattern where fetching a list of N items triggers N additional queries to fetch related data.

```python
# Python 3 — N+1 Problem Example
# NOTE: `db.execute()` below is pseudo-code / conceptual. It is not from a
# specific library — it represents any DB interface (e.g., SQLAlchemy, psycopg2,
# Django ORM raw queries). The pattern itself is the important takeaway.

# BAD: N+1 queries (1 query for orders + N queries for users)
orders = db.execute("SELECT * FROM orders").fetchall()  # 1 query
for order in orders:
    # This runs once PER order — if there are 1000 orders, that's 1000 queries!
    user = db.execute(
        "SELECT * FROM users WHERE id = %s", (order["user_id"],)
    ).fetchone()
    print(f"Order {order['id']} by {user['name']}")

# GOOD: Single query with JOIN (1 query total)
results = db.execute("""
    SELECT orders.id AS order_id, users.name AS user_name
    FROM orders
    JOIN users ON orders.user_id = users.id
""").fetchall()  # 1 query

for row in results:
    print(f"Order {row['order_id']} by {row['user_name']}")
```

> **In HLD interviews:** If you're designing a system that displays lists with related data (e.g., a feed with author info), mention that you'll use JOINs, batch queries, or denormalization to avoid the N+1 problem.

---

## 15. Write-Ahead Log (WAL)

A durability mechanism used by most databases. Every change is first written to an append-only log file before being applied to the actual data pages.

- **Purpose:** If the database crashes mid-write, it can replay the WAL to recover to a consistent state.
- **Used by:** PostgreSQL (WAL), MySQL (redo log), SQLite (WAL mode).
- **Bonus:** WAL is also used for replication — followers can replay the leader's WAL to stay in sync.

---

## Practice Problems

### Problem 1 (Easy): Choose the Right Database

**Problem:** You're designing a system for a food delivery app. For each component below, choose the most appropriate database type and justify your choice.

1. User profiles and restaurant info
2. Real-time driver location tracking
3. Order history and payment records
4. Restaurant search by name and cuisine

<details>
<summary>Hints</summary>

- Think about the access patterns for each component.
- Which components need ACID? Which need fast writes? Which need search capabilities?
</details>

<details>
<summary>Solution</summary>

1. **User profiles & restaurant info → MongoDB (Document DB)**
   - Semi-structured data (menus have varying fields per restaurant).
   - Flexible schema for different restaurant types.
   - Read-heavy with occasional updates.

2. **Real-time driver location → Redis (Key-Value with Geo)**
   - Redis has built-in geospatial commands (`GEOADD`, `GEORADIUS`).
   - Sub-millisecond latency for real-time location updates.
   - Ephemeral data (only current location matters).

3. **Order history & payments → PostgreSQL (Relational)**
   - ACID transactions are critical for payments.
   - Complex queries (order totals, revenue reports, refunds).
   - Strong consistency required — a payment must never be lost or duplicated.

4. **Restaurant search → Elasticsearch (Search Engine)**
   - Full-text search with fuzzy matching ("Pizzza" → "Pizza").
   - Faceted search (filter by cuisine, rating, distance).
   - Optimized for read-heavy search workloads.
</details>

---

### Problem 2 (Easy-Medium): Indexing Strategy & Replication Topology

**Problem:** You're building a social media platform. The `posts` table has the following schema:

```sql
CREATE TABLE posts (
    id          BIGSERIAL PRIMARY KEY,
    user_id     BIGINT NOT NULL,
    content     TEXT NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    likes_count INT NOT NULL DEFAULT 0,
    is_deleted  BOOLEAN NOT NULL DEFAULT FALSE
);
```

The main query patterns are:
1. Get all posts by a specific user, ordered by most recent first (user profile page).
2. Get the global feed: most recent non-deleted posts across all users.
3. Get "trending" posts: non-deleted posts from the last 24 hours with the most likes.

**Part A:** Design the indexes for these three query patterns. Explain which columns you'd index, the index type, and why.

**Part B:** The platform grows to 50M users and 2B posts. Reads outnumber writes 20:1. Design a replication topology. How many replicas? Sync or async? How do you handle the case where a user creates a post and immediately refreshes their profile?

<details>
<summary>Hints</summary>

- For Part A, think about composite indexes and the leftmost prefix rule.
- For the "trending" query, consider a partial index (an index with a WHERE clause).
- For Part B, think about the "read-your-writes" consistency problem.
- Low-cardinality columns (like `is_deleted`) are poor index candidates on their own, but useful in composite or partial indexes.
</details>

<details>
<summary>Solution</summary>

**Part A: Indexes**

```sql
-- Query 1: Posts by user, newest first
-- Composite index on (user_id, created_at DESC)
-- Covers the WHERE (user_id = ?) and ORDER BY (created_at DESC) in one index scan.
CREATE INDEX idx_posts_user_timeline ON posts (user_id, created_at DESC);

-- Query 2: Global feed of recent non-deleted posts
-- Partial index: only indexes non-deleted posts, keeping the index small.
-- Sorted by created_at DESC for the feed ordering.
CREATE INDEX idx_posts_global_feed ON posts (created_at DESC)
    WHERE is_deleted = FALSE;

-- Query 3: Trending posts (last 24h, most likes)
-- This is a time-windowed query. A partial index won't work well here because
-- the 24h window shifts constantly. Instead, use a composite index:
CREATE INDEX idx_posts_trending ON posts (created_at DESC, likes_count DESC)
    WHERE is_deleted = FALSE;
-- The query planner uses the partial index to skip deleted posts, scans
-- created_at DESC to find posts within the last 24h, then sorts by likes_count.
```

**Why not index `is_deleted` as a standalone column?**
It has only 2 values (TRUE/FALSE) — extremely low cardinality. A standalone index would select ~50% of rows (assuming most posts are not deleted), which is worse than a full table scan. Instead, we use it as a partial index predicate (`WHERE is_deleted = FALSE`), which makes the index itself smaller and faster.

**Part B: Replication Topology**

```text
              ┌──────────────┐
  Writes ───> │    Leader     │
              └──┬──┬──┬──┬──┘
                 │  │  │  │
        Sync     │  │  │  │  Async
       ┌─────────┘  │  │  └─────────┐
       v            v  v            v
  ┌─────────┐  ┌─────────┐   ┌─────────┐
  │Replica 1│  │Replica 2│   │Replica 3│   <── Reads
  │ (sync)  │  │ (async) │   │ (async) │
  └─────────┘  └─────────┘   └─────────┘
```

- **1 leader + 3 read replicas** (20:1 read-to-write ratio warrants multiple replicas).
- **Semi-synchronous replication**: 1 replica is synchronous (guarantees no data loss on leader failure), the other 2 are asynchronous (lower latency for the leader).
- **Read-your-writes consistency**: After a user creates a post and immediately loads their profile, route that specific user's read to the **leader** (or the synchronous replica) for a short window (~5 seconds). All other reads go to any replica. This avoids the user seeing a stale profile without their new post.

```python
# Python 3 — Simplified read routing logic (pseudo-code)
import time

# In-memory cache of recent writers (in production, use Redis)
recent_writers: dict[str, float] = {}  # user_id -> timestamp of last write
LEADER_READ_WINDOW = 5.0  # seconds

def route_read(user_id: str) -> str:
    """Decide whether to read from leader or replica."""
    last_write = recent_writers.get(user_id)
    if last_write and (time.time() - last_write) < LEADER_READ_WINDOW:
        return "leader"  # Read-your-writes: route to leader
    return "replica"  # Safe to read from any replica

def on_write(user_id: str) -> None:
    """Record that this user just performed a write."""
    recent_writers[user_id] = time.time()
```
</details>

---

### Problem 3 (Medium): Design a Sharding Strategy

**Problem:** You're building a multi-tenant SaaS application (like Slack). Each tenant (company) has many users, and each user sends many messages. The system has:
- 10,000 tenants
- Average 500 users per tenant
- 1 billion messages total, growing by 10M/day

Design a sharding strategy. What is your shard key? How do you handle the following query patterns?
1. Get all messages in a channel (within a tenant)
2. Get all channels for a user
3. Search messages by keyword within a tenant

<details>
<summary>Hints</summary>

- Think about data locality — which queries should be single-shard?
- Consider a composite shard key.
- What happens if one tenant is much larger than others (e.g., a company with 50,000 users)?
</details>

<details>
<summary>Solution</summary>

**Shard key: `tenant_id`**

**Rationale:**
- Almost all queries are scoped to a single tenant (get messages in a channel, get channels for a user).
- Using `tenant_id` as the shard key ensures all data for one tenant lives on one shard — no cross-shard queries for the common case.
- 10,000 tenants provides good cardinality for even distribution.

**Handling the queries:**
1. **Messages in a channel:** Single-shard query. All messages for tenant X are on the same shard. Filter by `channel_id` within the shard (with a local index on `channel_id`).
2. **Channels for a user:** Single-shard query. User belongs to a tenant, so all their channels are on the same shard.
3. **Search by keyword:** Use Elasticsearch as a secondary index, also partitioned by `tenant_id`. The search hits one ES shard, returns message IDs, which are fetched from one DB shard.

**Handling large tenants (hot shards):**
- For very large tenants (>50,000 users), use a secondary sharding level: `tenant_id + channel_id` hash. This splits a single large tenant across multiple shards.
- Alternatively, give large tenants their own dedicated shard(s).

```python
# Python 3 — Simple shard routing logic
import hashlib

NUM_SHARDS = 16

def get_shard(tenant_id: str) -> int:
    """Route a tenant to a specific shard using hash-based partitioning."""
    hash_value = int(hashlib.sha256(tenant_id.encode()).hexdigest(), 16)
    return hash_value % NUM_SHARDS

# Examples
print(get_shard("acme-corp"))     # e.g., 7
print(get_shard("globex-inc"))    # e.g., 12
print(get_shard("initech"))       # e.g., 3
```
</details>

---

### Problem 4 (Hard): Database Design for a Global Payment System

**Problem:** You're designing the database layer for a global payment processing system (like Stripe). Requirements:
- Process 50,000 transactions per second globally.
- Each transaction must be ACID-compliant (no double charges, no lost payments).
- Users are distributed across 5 geographic regions (US, EU, APAC, LATAM, Africa).
- Must support idempotent payment processing (retries don't cause duplicate charges).
- 99.999% availability requirement.
- Must support refunds, chargebacks, and audit trails.

Design the database architecture. Address:
1. Which database(s) would you use and why?
2. How do you handle multi-region deployment?
3. How do you achieve idempotency?
4. What is your replication and consistency strategy?
5. How do you handle a scenario where a user in the US pays a merchant in the EU?

<details>
<summary>Hints</summary>

- Consider using different databases for different parts of the system (polyglot persistence).
- Think about idempotency keys and how to implement them.
- CockroachDB and Google Spanner are designed for globally distributed ACID transactions.
- Consider the PACELC theorem — what trade-offs are you making during normal operation vs. during a partition?
</details>

<details>
<summary>Solution</summary>

**Architecture Overview:**

**1. Database Choices (Polyglot Persistence):**
- **Primary transaction DB: CockroachDB (or Google Spanner)**
  - Globally distributed SQL database with strong consistency (serializable isolation).
  - Survives region-level failures while maintaining ACID.
  - Automatic sharding and rebalancing.
- **Idempotency store: Redis (with persistence)**
  - Store idempotency keys with TTL for fast deduplication.
- **Audit log: Cassandra**
  - Append-only, high write throughput for immutable audit trail.
  - Time-series partitioning by date for efficient historical queries.
- **Analytics: ClickHouse**
  - Columnar storage for aggregate queries (daily revenue, fraud detection).

**2. Multi-Region Deployment:**
- CockroachDB with region-pinned data: user accounts are pinned to their home region (data locality). US user data lives primarily in US nodes.
- Reads are served locally for low latency.
- Cross-region writes use consensus (Raft) — higher latency but strong consistency.

**3. Idempotency:**
```python
# Python 3 — Idempotent payment processing
# Requires: pip install redis
import redis
import uuid

redis_client = redis.Redis(host="localhost", port=6379, db=0)

def process_payment(idempotency_key: str, amount: float, currency: str) -> dict:
    """
    Process a payment idempotently.
    If the same idempotency_key is sent twice, return the original result.
    """
    # Check if this payment was already processed
    # NOTE: In production, use Redis SET with NX (set-if-not-exists) to
    # atomically claim the idempotency key and prevent race conditions
    # between concurrent requests with the same key.
    existing_result = redis_client.get(f"payment:{idempotency_key}")
    if existing_result is not None:
        # Return the cached result — no double charge
        return {"status": "already_processed", "original_result": existing_result.decode()}

    # Process the payment (simplified)
    transaction_id = str(uuid.uuid4())

    # BEGIN TRANSACTION in CockroachDB
    #   1. Debit the payer's account
    #   2. Credit the payee's account
    #   3. Insert transaction record
    # COMMIT

    # Cache the result with a 24-hour TTL
    redis_client.setex(
        name=f"payment:{idempotency_key}",
        time=86400,  # 24 hours
        value=transaction_id,
    )

    return {"status": "success", "transaction_id": transaction_id}
```

**4. Replication & Consistency:**
- CockroachDB uses Raft consensus — every write is replicated to a majority of nodes before ACK.
- PACELC classification: **PC/EC** — prioritizes consistency both during partitions and normal operation. Accepts higher latency as a trade-off.
- Replication factor of 5 (one per region). A write needs 3/5 ACKs.

**5. Cross-Region Transaction (US user → EU merchant):**
- The transaction coordinator is in the region closest to the user (US).
- CockroachDB handles the distributed transaction across the US (payer account) and EU (payee account) nodes via Raft.
- Latency: ~150-300ms due to cross-region consensus, which is acceptable for payment processing.
- The idempotency key ensures retries (due to network timeouts) don't cause double charges.
</details>
