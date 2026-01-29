# Architectural Patterns

These are the core components you will use to build your system diagrams.

> **Prerequisites:** [HLD Fundamentals](./01-fundamentals.md)

## 1. Load Balancers
Distributes incoming network traffic across multiple servers.
- **Algorithms**: Round Robin, Least Connections, IP Hash.
- **Placement**: Client-LB, LB-Web Server, Web Server-Internal Service.

### Layer 4 vs. Layer 7 Load Balancing
| Feature | L4 (Transport Layer) | L7 (Application Layer) |
|---------|-----------------------|-------------------------|
| **Data** | IP, TCP/UDP Port | HTTP Headers, Cookies, URL |
| **Logic** | Packet-level routing | Content-aware routing |
| **Performance**| Faster (Less CPU) | Slower (SSL Decryption) |
| **Use Case** | High-speed TCP balancing | Microservices, Sticky sessions |

## 2. Caching
Storing copies of data in a high-speed storage layer (like Redis or Memcached).
- **CDN (Content Delivery Network)**: For static assets (Images, Videos, JS).
- **Application Cache**: For database query results.

### Caching Patterns
- **Cache-Aside**: Application checks cache. If miss, reads from DB and updates cache. (Most common).
- **Read-Through**: Cache sits in the data path. If miss, cache fetches from DB and returns to app.
- **Write-Through**: Data is written to cache and DB simultaneously.
- **Write-Back**: Data is written to cache only, DB update happens asynchronously.

### Cache Eviction Policies
- **LRU (Least Recently Used)**: Discards the least recently accessed items first.
- **LFU (Least Frequently Used)**: Discards items used least often.
- **FIFO (First In First Out)**: Discards the oldest items first.
- **Random**: Randomly selects items to discard.

### Caching Strategies (Sequence Diagrams)

#### Write-Through Cache
Data is written to the cache and the database at the same time.
```text
Client ───> Cache ───> Database
  ^           │           │
  └───────────┴───────────┘
     (Success response)
```

#### Write-Back Cache
Data is written to the cache only. The write to the database is done later.
```text
Client ───> Cache ───> (Later) ───> Database
  ^           │
  └───────────┘
     (Fast response)
```

## 3. Message Queues (Asynchronous Communication)
Decouples producers from consumers.
- **Tools**: Kafka, RabbitMQ, Amazon SQS.
- **Use cases**: Sending emails, processing videos, handling high-burst traffic.

---

## 4. Communication Protocols

| Protocol | Pros | Cons | Use Case |
|----------|------|------|----------|
| **REST (HTTP)** | Universal, Simple | Verbose (JSON) | Standard APIs |
| **gRPC** | Fast (Protobuf), Typed | Requires HTTP/2 | Microservices |
| **Long Polling** | Real-time-ish | Server overhead | Simple updates |
| **SSE (Server-Sent Events)** | Server -> Client push | Uni-directional | Stock tickers, News |
| **WebSockets** | Real-time, Bi-directional | Stateful connection | Chat, Gaming |
| **GraphQL** | Precise data fetching | Complex to implement | Mobile apps |

---

## 5. Microservices vs. Monolith
- **Monolith**: All code in one codebase. Easy to start, hard to scale teams.
- **Microservices**: Each service does one thing. Scales teams and tech stacks, but increases operational complexity.
