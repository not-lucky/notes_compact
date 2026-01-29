# Databases

Choosing the right database and scaling it is the most important part of any HLD interview.

> **Prerequisites:** [Architectural Patterns](./02-architectural-patterns.md)

## 1. SQL vs. NoSQL

| Feature | SQL (PostgreSQL, MySQL) | NoSQL (MongoDB, Cassandra) |
|---------|-------------------------|---------------------------|
| **Schema** | Rigid, Predefined | Flexible, Dynamic |
| **Scaling** | Vertical (Mostly) | Horizontal (Built-in) |
| **Joins** | Powerful | Poor or None |
| **ACID** | Strong support | Base (Basically Available) |

## 2. Scaling Databases
- **Replication**: Copying data across multiple servers (Leader-Follower). Used for Read Scaling.
- **Sharding (Partitioning)**: Splitting a large dataset into smaller chunks across different servers. Used for Write Scaling.
    - **Sharding Key**: Critical choice. Good keys (like `user_id`) ensure even distribution.

---

## 3. Transaction Isolation Levels
Defines how a transaction is isolated from others. Prevents anomalies.
- **Read Uncommitted**: Can see uncommitted changes (Dirty Reads).
- **Read Committed**: Only sees committed changes. (Prevents Dirty Reads).
- **Repeatable Read**: Ensures that if you read a row once, reading it again returns the same data. (Prevents Non-repeatable Reads).
- **Serializable**: Highest level. Transactions appear to run sequentially. (Prevents Phantom Reads).

---

## 4. Distributed Transactions
When a transaction spans multiple services/databases.
- **Two-Phase Commit (2PC)**: Coordinator asks all nodes to "Prepare", then "Commit". (Synchronous, blocking, risk of coordinator failure).
- **Saga Pattern**: Sequence of local transactions.
    - **Choreography**: Each service produces and listens to events (Decentralized).
    - **Orchestration**: A central orchestrator tells services what to do (Centralized).

---

## 5. Storage Engines
How data is actually stored on disk.
- **B-Trees**: Optimized for reads and range queries. (Used in most RDBMS like MySQL/PostgreSQL).
- **LSM Trees (Log-Structured Merge-Trees)**: Optimized for high write throughput. (Used in NoSQL like Cassandra, RocksDB).

---

## 6. Indexing
Speeds up reads by creating a data structure (B-Trees or Hash Indexes) that allows faster lookups.
- **Trade-off**: Faster reads, slower writes (because index must be updated).

---

## 7. Consistency Models
- **Eventual Consistency**: Data will eventually be consistent across all nodes (e.g., DNS, Cassandra).
- **Strong Consistency**: Data is consistent immediately after a write (e.g., SQL with transactions).

---

## 8. Storage Types
- **Key-Value**: Redis, Riak.
- **Document**: MongoDB, CouchDB.
- **Wide-Column**: Cassandra, Hbase.
- **Graph**: Neo4j (for social networks, fraud detection).
- **Vector**: Pinecone, Milvus, Weaviate (optimized for high-dimensional vector embeddings, critical for **LLM/RAG** applications).
