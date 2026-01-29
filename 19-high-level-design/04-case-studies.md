# HLD Case Studies

Applying the components and fundamentals to real-world problems.

> **Prerequisites:** [Databases](./03-databases.md)

## 1. URL Shortener (TinyURL)
- **Goal**: Take a long URL and return a short 7-character string.
- **Key Concepts**:
    - **Base62 Encoding**: To convert an auto-incrementing ID to a string.
    - **Collision Handling**: If using a hashing approach (like MD5) instead of a counter, you must handle collisions by appending a salt and re-hashing.
    - **Read-Heavy Caching**: Most URLs are read far more than they are created.
    - **Sharding**: By `alias` or `original_url`.

## 2. Messaging App (WhatsApp)
- **Goal**: One-on-one and group messaging.
- **Key Concepts**:
    - **WebSockets**: For real-time delivery.
    - **Service Discovery**: Using **Zookeeper** or **Consul** to keep track of which WebSocket server a user is connected to.
    - **Message Queue**: To handle offline users.
    - **Consistency**: High availability is more important than perfect consistency (if a message arrives 1s late, it's okay).

## 3. News Feed (Facebook/Twitter)
- **Goal**: Display a list of posts from people the user follows.
- **Fan-out Models**:
    - **Push Model (Fan-out on Write)**: When a user posts, it's pushed to all followers' feeds. (Fast reads, slow writes for celebrities).
    - **Pull Model (Fan-out on Read)**: Feeds are generated when the user opens the app. (Slow reads, fast writes).
    - **Hybrid**: Use Push for regular users and Pull for celebrities (Kim Kardashian).

## 4. Ad Click Aggregator
- **Goal**: Count billions of ad clicks for billing and analytics.
- **Key Concepts**:
    - **Stream Processing**: Using **Apache Flink** or **Spark Streaming** to process clicks in real-time.
    - **Idempotency & Deduplication**: Use **Redis** with a TTL or Bloom Filters to ensure a click isn't counted twice. Use a `request_id` or `click_id` as the key.
    - **Exactly-once Processing**: Ensuring each click is processed exactly once despite network failures.

## 5. Video Streaming (YouTube/Netflix)
- **Goal**: Uploading and viewing high-resolution videos.
- **Key Concepts**:
### Video Processing Flow (YouTube)

```text
User ──> LB ──> Upload Srv ──> Object Store (Raw)
                                    │
                                    ▼
       Metadata DB <─── Transcoder Worker ───> Message Queue
                                    │
                                    ▼
User <── CDN <── S3 (Transcoded) <──┘
```

- **Transcoding**: Takes the raw file and generates multiple resolutions (1080p, 720p, etc.).
- **CDN**: Distributes these files globally to minimize latency.

## 6. Uber/Lyft (Proximity Service)
- **Goal**: Match riders with nearby drivers in real-time.
- **Key Concepts**:
    - **Geohashing/S2 Cells**: To divide the map into small regions for efficient spatial indexing.
    - **QuadTree**: A data structure to manage 2D spatial data.
    - **Pub/Sub**: Drivers publish their location every few seconds; riders subscribe to nearby driver updates.
    - **Consistency**: High availability is crucial, but stale driver locations (by a few seconds) are acceptable.

## 7. Web Crawler (Googlebot)
- **Goal**: Discover and index billions of web pages.
- **Key Concepts**:
    - **URL Frontier**: A prioritized queue of URLs to visit.
    - **DNS Resolver**: A bottleneck; needs a custom, high-performance local cache.
    - **Politeness**: Ensuring the crawler doesn't DoS a single website (Wait time between requests).
    - **Deduplication**: Bloom Filters or Hashsets to avoid crawling the same content twice.

---

## The "How to Recognize What to Consider" Framework

When presented with a problem, ask these questions to identify the core design challenges:

| If the problem involves... | You must consider... | Component to use |
|---------------------------|----------------------|------------------|
| **Real-time updates** (Chat, Gaming) | Latency, Bi-directional comms | **WebSockets** |
| **Heavy Reads** (Search, Profiles) | Read latency, DB load | **Redis Cache, CDN** |
| **Heavy Writes** (Logging, Clicks) | Write throughput, Durability | **LSM-Tree DB, Kafka** |
| **Asset Delivery** (Videos, Images) | Global latency, Bandwidth | **CDN** |
| **Celebrities/Hot Keys** (Twitter) | Fan-out bottlenecks, Sharding | **Hybrid Push/Pull** |
| **Money/Transactions** (Payments) | ACID, Strong consistency | **SQL, 2PC/Sagas** |
| **Search/Discovery** (Maps, Yelp) | Spatial indexing | **Geohash, QuadTree** |
| **Unreliable Networks** | Consensus, Failover | **Raft/Paxos, Gossip** |

---

## The "Back-of-the-envelope" Calculation Template
You should be able to estimate:
- **DAU (Daily Active Users)**: e.g., 10 Million.
- **QPS (Queries Per Second)**: `DAU * avg_requests / 86400`.
- **Storage**: `Daily_Uploads * avg_size * retention_period`.

---

## Interview Tip: The "Why"
Whenever you add a component (like a Cache or a Queue), always state **why**:
- "I'm adding a Redis cache here to reduce the read latency on the profile service from 100ms to 5ms."
- "I'm using Kafka to decouple the Order service from the Email service so that if the Email service is down, orders aren't lost."
