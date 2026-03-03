# HLD Case Studies

Applying the components and fundamentals to real-world problems. Each case study
follows the interview framework: Requirements → Estimation → API → Architecture → Deep Dive → Scaling.

> **Prerequisites:** [Databases](./03-databases.md)

---

## 1. URL Shortener (TinyURL)

### Requirements
- **Functional**: Given a long URL, return a short alias. Given a short alias, redirect to the original URL. Optional: custom aliases, expiration, analytics.
- **Non-Functional**: Very high availability, low latency redirects, short URLs should not be guessable (no sequential IDs exposed).

### Back-of-the-Envelope Estimation
- 100M URLs created/day → ~1,160 writes/sec.
- Read:Write ratio ~100:1 → ~116,000 reads/sec (read-heavy).
- 7-character alias using Base62 (a-z, A-Z, 0-9) → 62^7 ≈ 3.5 trillion unique URLs.
- Storage: 100M/day × 365 days × 5 years × 500 bytes/record ≈ 91 TB.

### API Design
```python
# POST /api/v1/shorten
# Request:  {"long_url": "https://example.com/very/long/path", "expiry": "2027-01-01"}
# Response: {"short_url": "https://tiny.url/aB3x7Kq", "expires_at": "2027-01-01"}

# GET /:alias  → HTTP 301 (permanent) or 302 (temporary) redirect
# 301 = browser caches the redirect (less load, but no analytics)
# 302 = browser always hits our server (more load, but enables click tracking)
```

### High-Level Architecture
```text
Client ──> LB ──> App Server ──> Cache (Redis)
                      │               │ (miss)
                      │               ▼
                      │          Database (SQL)
                      │
                      ▼
              ID Generator Service
```

### Key Design Decisions

**Approach 1 — Counter + Base62 Encoding (Preferred)**
- Use a distributed counter (e.g., Snowflake ID or a dedicated ID service with pre-allocated ranges).
- Convert the numeric ID to a Base62 string.
- No collisions by design since every ID is unique.

```python
import string

BASE62_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase  # 62 chars

def base62_encode(num: int) -> str:
    """Convert a positive integer to a Base62 string."""
    if num == 0:
        return BASE62_CHARS[0]
    
    result = []
    while num > 0:
        num, remainder = divmod(num, 62)
        result.append(BASE62_CHARS[remainder])
    return ''.join(reversed(result))

def base62_decode(short_str: str) -> int:
    """Convert a Base62 string back to an integer."""
    num = 0
    for char in short_str:
        num = num * 62 + BASE62_CHARS.index(char)
    return num

# Example: ID 1_000_000_000 → "15FTGg" (6 chars, fits in 7-char alias)
print(base62_encode(1_000_000_000))  # "15FTGg"
print(base62_decode("15FTGg"))       # 1000000000
```

**Approach 2 — Hashing (MD5/SHA-256) + Collision Handling**
- Hash the long URL, take the first 7 characters.
- On collision: append a timestamp or counter to the URL, re-hash.
- Drawback: must check the DB on every write for collisions.

### Scaling Considerations
- **Caching**: Redis/Memcached for hot URLs. A small percentage of URLs get the vast majority of reads.
- **Database Sharding**: Shard by the first character(s) of the alias for even distribution. Alternatively, use consistent hashing on the alias.
- **Read Replicas**: Since reads dominate, add many read replicas.
- **Rate Limiting**: Prevent abuse (mass URL creation for spam).

---

## 2. News Feed / Timeline (Facebook / Twitter)

### Requirements
- **Functional**: Users can create posts. Users see a feed of posts from people they follow, sorted by relevance/time. Support likes, comments, shares.
- **Non-Functional**: Feed generation must be fast (<500ms). High availability. Eventual consistency is acceptable (seeing a post 2-3 seconds late is fine).

### Back-of-the-Envelope Estimation
- 300M DAU, each user checks feed ~10 times/day → 3B feed requests/day → ~35K reads/sec.
- Each user follows ~200 people on average.
- Average post size: 1 KB text + metadata.

### API Design
```python
# POST /api/v1/posts
# Request:  {"content": "Hello world!", "media_ids": ["img_123"]}
# Response: {"post_id": "post_456", "created_at": "2026-03-01T12:00:00Z"}

# GET /api/v1/feed?page_token=xyz&page_size=20
# Response: {"posts": [...], "next_page_token": "abc"}
```

### High-Level Architecture
```text
              ┌──────────────┐
              │  Post Service │──> Post DB (Write)
              └──────┬───────┘
                     │ (new post event)
                     ▼
              ┌──────────────┐
              │   Fan-out    │──> Feed Cache (per-user feed in Redis)
              │   Service    │
              └──────────────┘
                     ▲
                     │ (follower list)
              ┌──────────────┐
              │  Social Graph│
              │   Service    │
              └──────────────┘

User reads feed:
  Client ──> LB ──> Feed Service ──> Feed Cache (Redis)
                                         │ (miss)
                                         ▼
                                     Post DB (fallback)
```

### Fan-out Models (Critical Decision)

| Model | How it works | Pros | Cons |
|-------|-------------|------|------|
| **Push (Fan-out on Write)** | On post creation, write to every follower's feed cache | Fast reads (pre-computed) | Slow writes for users with millions of followers; wastes storage for inactive users |
| **Pull (Fan-out on Read)** | On feed request, query all followed users' posts and merge | Fast writes, no wasted storage | Slow reads (must merge N timelines on the fly) |
| **Hybrid** | Push for normal users, Pull for celebrities (>100K followers) | Balances both | More complex to implement |

**Twitter uses the Hybrid approach.** When a celebrity posts, their post is not fanned out to millions of feeds. Instead, when a user requests their feed, the system merges their pre-computed feed (from Push) with the latest posts from celebrities they follow (Pull).

### Scaling Considerations
- **Feed Cache**: Redis sorted sets keyed by `user_id`, scored by timestamp. Limit to last ~800 posts per user.
- **Sharding Social Graph**: Shard by `user_id`. The follower list is the hottest data.
- **Ranking Service**: ML model that re-ranks posts by engagement probability (not just chronological).

---

## 3. Chat / Messaging System (WhatsApp / Slack)

### Requirements
- **Functional**: 1-on-1 messaging, group messaging (up to 500 members), online/offline status, read receipts, media sharing.
- **Non-Functional**: Real-time delivery (<100ms when both online), message ordering guaranteed per conversation, no message loss, end-to-end encryption.

### Back-of-the-Envelope Estimation
- 500M DAU, each sends ~40 messages/day → 20B messages/day → ~230K writes/sec.
- Average message size: 200 bytes → 20B × 200B = 4 TB/day raw storage.
- Peak QPS: ~3x average → ~700K messages/sec.

### API Design (WebSocket-Based)
```python
# WebSocket connection: wss://chat.example.com/ws?token=<auth_token>

# Client sends:
# {"action": "send", "to": "user_456", "msg_id": "uuid-1", "body": "Hello!"}

# Server pushes to recipient:
# {"action": "receive", "from": "user_123", "msg_id": "uuid-1", "body": "Hello!", "ts": 1709280000}

# Acknowledgement (client → server):
# {"action": "ack", "msg_id": "uuid-1"}

# REST fallback for offline sync:
# GET /api/v1/messages?conversation_id=conv_789&since=1709270000
```

### High-Level Architecture
```text
Sender ──WebSocket──> Chat Server A
                          │
                          ▼
                    Message Queue (Kafka)
                          │
                          ▼
                    Chat Server B ──WebSocket──> Recipient (if online)
                          │
                          ▼ (if offline)
                    Push Notification Service ──> APNs / FCM

Service Discovery (ZooKeeper/Consul):
  Tracks which Chat Server each user is connected to.

Storage:
  Message DB (Cassandra) ─── wide-column, partitioned by conversation_id
```

### Key Design Decisions
- **WebSockets** for persistent, bi-directional, low-latency communication. HTTP polling would waste bandwidth and add latency.
- **Service Discovery**: When User A sends a message to User B, the system must know which chat server User B is connected to. ZooKeeper or Consul maintains a mapping of `user_id → server_id`.
- **Message Ordering**: Use a monotonically increasing sequence number per conversation. The sender's clock cannot be trusted (clock skew). The server assigns the sequence number.
- **Offline Messages**: Messages are persisted to the database. When the user comes online, a sync process fetches undelivered messages.
- **Group Messaging**: For a group of N members, the chat server fans out the message to N-1 recipients via their respective chat servers. For large groups, this is done asynchronously through the message queue.

### Scaling Considerations
- **Database Choice**: Cassandra or HBase — optimized for high write throughput. Partition key = `conversation_id`, clustering key = `message_timestamp`. This keeps all messages in a conversation co-located on the same node for efficient range queries.
- **Horizontal Scaling**: Add more chat servers behind a load balancer. WebSocket connections are stateful, so use consistent hashing to route reconnections to the same server when possible.
- **Message Queue**: Kafka decouples the sender's chat server from the recipient's. Provides durability if a chat server crashes.

---

## 4. Video Streaming Platform (YouTube / Netflix)

### Requirements
- **Functional**: Upload videos, stream videos in multiple resolutions (adaptive bitrate), search, recommendations, comments, likes.
- **Non-Functional**: High availability, low startup latency for playback (<2s), support for global audience, handle large files (up to several GB).

### Back-of-the-Envelope Estimation
- 5M video uploads/day, average raw size 500 MB → 2.5 PB/day of raw uploads.
- After transcoding to multiple resolutions + codecs: ~5x raw size → 12.5 PB/day total storage.
- 1B video views/day → ~11,500 reads/sec (but served from CDN, not origin).

### High-Level Architecture

```text
Upload Flow:
  User ──> LB ──> Upload Service ──> Object Store (S3 - raw video)
                       │
                       ▼
                  Message Queue (SQS/Kafka)
                       │
                       ▼
              Transcoding Workers (parallel)
              ├── 1080p encode
              ├── 720p encode
              ├── 480p encode
              └── 360p encode
                       │
                       ▼
              Object Store (S3 - transcoded) ──> CDN (CloudFront)
                       │
                       ▼
              Metadata DB (update status: "ready")

Viewing Flow:
  User ──> CDN (edge cache) ──> Origin (S3) if cache miss
              │
              ▼
         Adaptive Bitrate Streaming (HLS/DASH manifest)
```

### Key Design Decisions
- **Transcoding Pipeline**: Raw video is split into small chunks (e.g., 10-second segments) and transcoded in parallel. Each chunk is encoded into multiple resolutions and codecs (H.264, VP9, AV1). This enables adaptive bitrate streaming where the player switches quality based on network conditions.
- **CDN**: The single most important component. Popular videos are cached at edge locations worldwide. Without a CDN, origin servers would be overwhelmed.
- **Object Storage (S3)**: Videos are large binary blobs — relational databases are not suited for this. Object storage provides durability (11 nines), cheap at-rest storage, and integrates with CDNs.
- **Metadata vs. Video Data**: Metadata (title, description, uploader, view count) is stored in a database (SQL or NoSQL). The actual video files are in object storage. Never mix these.

### Scaling Considerations
- **Upload Processing**: Use a message queue to buffer uploads and process them asynchronously. Transcoding is CPU-intensive; use auto-scaling worker pools.
- **Hot Videos**: A tiny fraction of videos get the vast majority of views. CDN handles this naturally — popular content stays in edge cache.
- **Cost Optimization**: Move infrequently accessed (cold) videos to cheaper storage tiers (S3 Glacier). Keep only popular videos in CDN.

---

## 5. Ride-Sharing Service (Uber / Lyft)

### Requirements
- **Functional**: Rider requests a ride, system matches with a nearby available driver, real-time tracking of driver location, fare estimation, trip history.
- **Non-Functional**: Low latency matching (<10s), high availability (people depend on it for transportation), driver location updates every 3-5 seconds.

### Back-of-the-Envelope Estimation
- 20M daily rides, 5M concurrent drivers sending location every 4 seconds.
- Location updates: 5M / 4 = 1.25M writes/sec (extremely write-heavy).
- Each location update: ~50 bytes (lat, lng, timestamp, driver_id) → ~5.4 TB/day of location data.

### High-Level Architecture

```text
Driver App ──(location updates every 4s)──> LB ──> Location Service
                                                        │
                                                        ▼
                                                  Location Index
                                                  (Geohash in Redis
                                                   or QuadTree)

Rider App ──(request ride)──> LB ──> Ride Matching Service
                                          │
                                 ┌────────┴────────┐
                                 ▼                  ▼
                          Location Index      Driver Status DB
                          (find nearby)       (available?)
                                 │
                                 ▼
                          Notification Service ──> Push to Driver
                          (ride offer)
```

### Key Design Decisions

**Spatial Indexing — How to find nearby drivers efficiently:**

| Approach | How it works | Pros | Cons |
|----------|-------------|------|------|
| **Geohash** | Encodes lat/lng into a string prefix. Nearby locations share prefixes. | Simple, works with Redis/DB indexes | Edge cases at geohash boundaries (two nearby points can have different prefixes) |
| **QuadTree** | Recursively divides 2D space into 4 quadrants. Subdivides further in dense areas. | Adapts to density (more detail in cities) | In-memory, harder to distribute |
| **S2 Geometry (Google)** | Projects Earth onto a cube, then uses a Hilbert curve for 1D indexing. | Handles sphere geometry correctly, good for global scale | More complex to implement |

```python
# Simplified geohash concept: encoding latitude/longitude into a grid cell
def simple_geohash(lat: float, lng: float, precision: int = 6) -> str:
    """
    Simplified geohash: divide the world into a grid.
    Real geohash interleaves bits of lat/lng and encodes in base32.
    This demonstrates the core idea: nearby points → same prefix.
    """
    # Normalize to [0, 1) range
    norm_lat = (lat + 90.0) / 180.0
    norm_lng = (lng + 180.0) / 360.0

    chars = "0123456789bcdefghjkmnpqrstuvwxyz"  # base32 (no a, i, l, o)
    result = []
    lat_range = [0.0, 1.0]
    lng_range = [0.0, 1.0]
    is_lng = True  # alternate between longitude and latitude bits

    for _ in range(precision * 5):  # 5 bits per character
        if is_lng:
            mid = (lng_range[0] + lng_range[1]) / 2
            if norm_lng >= mid:
                lng_range[0] = mid
                result.append(1)
            else:
                lng_range[1] = mid
                result.append(0)
        else:
            mid = (lat_range[0] + lat_range[1]) / 2
            if norm_lat >= mid:
                lat_range[0] = mid
                result.append(1)
            else:
                lat_range[1] = mid
                result.append(0)
        is_lng = not is_lng

    # Convert every 5 bits to a base32 character
    hash_str = []
    for i in range(0, len(result), 5):
        chunk = result[i:i+5]
        index = sum(bit << (4 - j) for j, bit in enumerate(chunk))
        hash_str.append(chars[index])

    return ''.join(hash_str)

# Two nearby points produce similar geohashes
print(simple_geohash(37.7749, -122.4194))  # San Francisco
print(simple_geohash(37.7750, -122.4195))  # ~10 meters away — same prefix
```

- **Driver Location Updates**: Drivers send GPS coordinates every 3-5 seconds. The Location Service updates the driver's position in a geospatial index (e.g., Redis with geohash-based sorted sets, or an in-memory QuadTree).
- **Matching Algorithm**: When a rider requests a ride, query the spatial index for available drivers within a radius (e.g., 5 km). Rank by ETA (not just distance — account for traffic). Send ride offer to the closest driver first; if they decline, try the next.
- **Stale Location Tolerance**: A driver's position from 3-4 seconds ago is acceptable. This makes eventual consistency viable for the location data.

### Scaling Considerations
- **Partitioning Location Data**: Partition by geographic region (city/geohash prefix). Each partition handles a manageable number of drivers.
- **Separation of Read/Write Paths**: Location updates (writes) go to a fast in-memory store. Ride matching (reads) queries this store. Different scaling needs.
- **Trip History**: Store completed trips in a relational database sharded by `user_id`. This data is write-once, read-occasionally.

---

## 6. Notification System

### Requirements
- **Functional**: Send push notifications (iOS APNs, Android FCM), SMS, and email. Support scheduled notifications, user preferences (opt-out), rate limiting.
- **Non-Functional**: At-least-once delivery (never lose a notification), soft real-time (deliver within seconds, not milliseconds), high throughput (millions of notifications per event).

### High-Level Architecture

```text
Trigger Sources                    Notification Service
(Microservices, Cron) ──> LB ──> Validation & Rate Limiter
                                       │
                                       ▼
                                 Message Queue (Kafka)
                                       │
                         ┌─────────────┼─────────────┐
                         ▼             ▼             ▼
                    Push Worker    SMS Worker    Email Worker
                         │             │             │
                         ▼             ▼             ▼
                    APNs / FCM    Twilio API    SendGrid API

  User Preferences DB ← checked before sending (opt-out, quiet hours)
  Notification Log DB ← record every sent notification (deduplication, analytics)
```

### Key Design Decisions
- **Decoupling with Message Queues**: Producing services should not directly call APNs/FCM/Twilio. A queue absorbs bursts (e.g., "new episode released" triggers millions of notifications simultaneously) and provides retry semantics.
- **Deduplication**: Each notification gets a unique `notification_id`. Workers check the Notification Log before sending to prevent duplicates on retry.
- **Priority Queues**: Urgent notifications (security alerts, OTPs) go to a high-priority queue processed first. Marketing notifications go to a low-priority queue.
- **Rate Limiting**: Per-user rate limits prevent notification fatigue. Per-provider rate limits respect third-party API quotas (APNs throttles abusive senders).
- **Template System**: Notifications use templates with variable substitution to support localization (i18n) and A/B testing.

```python
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional

class Channel(Enum):
    PUSH = "push"
    SMS = "sms"
    EMAIL = "email"

class Priority(Enum):
    HIGH = 1     # OTP, security alerts
    MEDIUM = 2   # social interactions
    LOW = 3      # marketing, digest

@dataclass
class Notification:
    notification_id: str
    user_id: str
    channel: Channel
    priority: Priority
    template_id: str
    params: dict = field(default_factory=dict)     # e.g., {"name": "Alice", "item": "shoes"}
    scheduled_at: Optional[str] = None             # ISO timestamp for delayed delivery

class NotificationService:
    """
    Validates, deduplicates, and enqueues notifications.
    
    Note: preferences_db, log_db, and queue are interface stubs — in production,
    these would be backed by Redis, a database, and Kafka/SQS respectively.
    """

    def __init__(self, queue, preferences_db, log_db):
        self.queue = queue
        self.preferences_db = preferences_db
        self.log_db = log_db

    def send(self, notification: Notification) -> bool:
        # 1. Check user preferences (opted out? quiet hours?)
        prefs = self.preferences_db.get(notification.user_id)
        if not prefs.allows(notification.channel):  # stub: returns False if user opted out of this channel
            return False

        # 2. Deduplication — skip if already sent
        if self.log_db.exists(notification.notification_id):  # stub: checks if notification_id is in the log
            return False

        # 3. Rate limiting
        if self.log_db.count_recent(notification.user_id) > 50:  # stub: counts notifications in last 24h
            return False  # too many notifications today

        # 4. Enqueue for async processing
        self.queue.publish(
            topic=f"notifications.{notification.channel.value}",
            message=notification,
            priority=notification.priority.value,
        )

        # 5. Log for deduplication and analytics
        self.log_db.record(notification)
        return True
```

---

## 7. Web Crawler (Googlebot)

### Requirements
- **Functional**: Discover and download billions of web pages. Extract links to discover new pages. Store page content for indexing.
- **Non-Functional**: Politeness (don't overwhelm any single website), freshness (re-crawl important pages frequently), scalability (billions of pages), handle duplicates.

### High-Level Architecture

```text
Seed URLs ──> URL Frontier (Priority Queue)
                    │
                    ▼
              URL Scheduler (politeness: 1 request/domain/second)
                    │
                    ▼
              DNS Resolver (local cache) ──> Fetcher Workers (HTTP GET)
                                                    │
                                                    ▼
                                              Content Parser
                                              (extract text + links)
                                                    │
                                    ┌───────────────┼───────────────┐
                                    ▼               ▼               ▼
                            URL Filter       Content Store     Link Extractor
                          (seen before?       (S3 / HDFS)         │
                           Bloom Filter)                          ▼
                                │                          URL Frontier
                                ▼                         (new URLs added)
                          Dedup Store
                         (content hash)
```

### Key Design Decisions
- **URL Frontier**: Not a simple FIFO queue. It is a priority queue that balances:
  - **Priority**: Important pages (high PageRank, news sites) are crawled first.
  - **Politeness**: Separate sub-queues per domain. A scheduler ensures at most one request per domain per time window (respects `robots.txt` crawl-delay).
- **DNS Resolution**: A major bottleneck. Each domain requires a DNS lookup. Use a local DNS cache to avoid redundant lookups. DNS responses are cached with TTL.
- **Deduplication**:
  - **URL Dedup**: Bloom filter to check if a URL has been seen before (space-efficient, allows small false positive rate).
  - **Content Dedup**: Hash the page content (e.g., SimHash for near-duplicate detection). Avoids storing mirror sites multiple times.
- **Trap Avoidance**: Some sites generate infinite URLs (e.g., calendar pages: `/2026/01/01`, `/2026/01/02`, ...). Set a maximum depth and detect URL patterns that grow indefinitely.

### Scaling Considerations
- **Distributed Crawling**: Partition domains across crawler nodes using consistent hashing. Each node is responsible for a set of domains (also enforces per-domain politeness naturally).
- **Freshness**: Maintain a re-crawl schedule. High-priority pages (news) are re-crawled every few minutes. Static pages are re-crawled every few weeks.
- **Storage**: Raw HTML is stored in distributed file systems (HDFS) or object storage (S3). Metadata (URL, last crawl time, content hash) is stored in a database.

---

## 8. Ad Click Aggregator

### Requirements
- **Functional**: Count ad clicks in real-time for billing and analytics. Support queries like "how many clicks did ad X get in the last 5 minutes?" and "what is the click-through rate by region?"
- **Non-Functional**: Exactly-once counting (clicks tied to billing — overcounting costs advertisers money, undercounting costs the platform revenue). Low-latency aggregation. Handle billions of events/day.

### High-Level Architecture

```text
Ad Click ──> LB ──> Click Receiver ──> Kafka (raw click events)
                        │                      │
                        ▼                      ▼
                   Click Log DB         Stream Processor
                  (raw events,          (Flink / Spark)
                   append-only)               │
                                              ▼
                                      Aggregation DB
                                      (ad_id, time_window, count)
                                              │
                                              ▼
                                      Query Service ──> Dashboard / Billing API
```

### Key Design Decisions
- **Stream Processing**: Apache Flink or Spark Streaming consumes from Kafka and performs windowed aggregation (e.g., count clicks per ad per minute). Flink provides exactly-once semantics via checkpointing.
- **Idempotency & Deduplication**: Each click event has a unique `click_id`. The stream processor uses a dedup window (e.g., Redis with TTL or Flink's built-in dedup) to discard duplicate events caused by retries.
- **Exactly-Once Semantics**: Achieved by combining Kafka's idempotent producer, Flink's checkpointing, and transactional writes to the aggregation DB. This is an end-to-end guarantee, not just within one component.
- **Lambda vs. Kappa Architecture**:
  - **Lambda**: Separate batch layer (reprocesses all historical data for accuracy) and speed layer (real-time approximation). Results are merged. Complex to maintain.
  - **Kappa**: Single stream processing layer handles both real-time and reprocessing (replay Kafka topics). Simpler but requires Kafka to retain data long enough.

### Scaling Considerations
- **Kafka Partitioning**: Partition by `ad_id` so all clicks for one ad go to the same partition (enables per-ad aggregation without shuffling).
- **Hot Ads**: A viral ad might get billions of clicks. Pre-aggregate at the Click Receiver level (local counters flushed periodically) before sending to Kafka to reduce event volume.
- **Time-Series Storage**: Use a time-series database (InfluxDB, TimescaleDB) or pre-aggregate into time buckets (1-minute, 1-hour, 1-day) for fast range queries.

---

## 9. Distributed Search Engine (Elasticsearch-like)

### Requirements
- **Functional**: Full-text search across billions of documents. Return results ranked by relevance. Support filters, facets, autocomplete.
- **Non-Functional**: Low search latency (<200ms), near-real-time indexing (new documents searchable within seconds), high availability.

### High-Level Architecture

```text
Documents ──> Indexing Service ──> Index Builder ──> Inverted Index Shards
                                                          │
                                                    (distributed across nodes)

Search Query ──> Query Service ──> Scatter to Index Shards (parallel)
                                          │
                                   Gather & Merge Results
                                   (top-K ranked by relevance)
                                          │
                                          ▼
                                   Response to Client
```

### Key Design Decisions

**Inverted Index — The core data structure for full-text search:**

```python
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Posting:
    doc_id: int
    term_frequency: int    # how many times the term appears in this doc
    positions: list[int]   # positions of the term in the doc (for phrase queries)


class InvertedIndex:
    """
    Maps each term to a list of documents containing that term.
    This is the fundamental data structure behind search engines.
    """

    def __init__(self):
        # term → [Posting, Posting, ...]
        self.index: dict[str, list[Posting]] = defaultdict(list)
        self.doc_count = 0
        self.doc_lengths: dict[int, int] = {}  # doc_id → number of terms

    def add_document(self, doc_id: int, text: str) -> None:
        """Tokenize text and add to the index."""
        tokens = self._tokenize(text)
        self.doc_count += 1
        self.doc_lengths[doc_id] = len(tokens)

        # Count term frequencies and positions
        term_positions: dict[str, list[int]] = defaultdict(list)
        for pos, token in enumerate(tokens):
            term_positions[token].append(pos)

        for term, positions in term_positions.items():
            self.index[term].append(Posting(
                doc_id=doc_id,
                term_frequency=len(positions),
                positions=positions,
            ))

    def search(self, query: str) -> list[int]:
        """Return doc_ids containing ALL query terms, sorted by simple TF score."""
        terms = self._tokenize(query)
        if not terms:
            return []

        # Find docs containing all terms (AND query)
        posting_lists = [self.index.get(term, []) for term in terms]
        if any(not pl for pl in posting_lists):
            return []

        # Intersect posting lists
        doc_sets = [set(p.doc_id for p in pl) for pl in posting_lists]
        common_docs = doc_sets[0]
        for ds in doc_sets[1:]:
            common_docs &= ds

        # Score by sum of term frequencies
        scores: dict[int, float] = defaultdict(float)
        for pl in posting_lists:
            for posting in pl:
                if posting.doc_id in common_docs:
                    scores[posting.doc_id] += posting.term_frequency

        return sorted(common_docs, key=lambda d: scores[d], reverse=True)

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Simple whitespace + lowercase tokenizer."""
        return text.lower().split()


# Example usage
idx = InvertedIndex()
idx.add_document(1, "the quick brown fox")
idx.add_document(2, "the lazy brown dog")
idx.add_document(3, "the quick fox jumps")

print(idx.search("quick fox"))   # [1, 3] — both contain "quick" AND "fox"
print(idx.search("brown"))       # [1, 2] — both contain "brown"
# Note: docs with equal TF scores may appear in any order.
# A production engine would use BM25 or TF-IDF for better ranking.
```

- **Scatter-Gather**: The index is sharded across multiple nodes. A search query is broadcast to all shards in parallel. Each shard returns its top-K results. A coordinator merges and re-ranks the results.
- **Relevance Ranking**: BM25 (an improvement over TF-IDF) is the standard ranking function. It considers term frequency, inverse document frequency, and document length normalization.
- **Near-Real-Time Indexing**: New documents are first written to an in-memory buffer. Periodically (every 1 second in Elasticsearch), the buffer is flushed to a new immutable segment. This segment is immediately searchable.

### Scaling Considerations
- **Index Sharding**: Shard by document ID (each shard holds a subset of documents). Replicate each shard for availability and read throughput.
- **Query Routing**: Common queries can be cached. Use a query cache to avoid re-computing results for identical queries.
- **Autocomplete**: Use a prefix tree (trie) or edge n-grams at index time to support fast prefix matching.

---

## The "How to Recognize What to Consider" Framework

When presented with a problem, ask these questions to identify the core design challenges:

| If the problem involves... | You must consider... | Component to use |
|---------------------------|----------------------|------------------|
| **Real-time updates** (Chat, Gaming) | Latency, Bi-directional comms | **WebSockets** |
| **Heavy Reads** (Search, Profiles) | Read latency, DB load | **Redis Cache, CDN** |
| **Heavy Writes** (Logging, Clicks) | Write throughput, Durability | **LSM-Tree DB (Cassandra), Kafka** |
| **Asset Delivery** (Videos, Images) | Global latency, Bandwidth | **CDN, Object Storage (S3)** |
| **Celebrities/Hot Keys** (Twitter) | Fan-out bottlenecks, Thundering herd | **Hybrid Push/Pull, Request coalescing** |
| **Money/Transactions** (Payments) | ACID, Strong consistency, Idempotency | **SQL, 2PC/Sagas, Idempotency keys** |
| **Search/Discovery** (Maps, Yelp) | Spatial indexing, Full-text search | **Geohash, QuadTree, Inverted Index** |
| **Unreliable Networks** | Consensus, Failover, Split-brain | **Raft/Paxos, Gossip Protocol** |
| **Event Counting** (Analytics, Billing) | Exactly-once, Deduplication | **Kafka + Flink, Bloom Filter** |
| **Notifications** (Alerts, Marketing) | Delivery guarantee, Rate limiting | **Message Queue, Priority Queue** |

---

## The "Back-of-the-Envelope" Calculation Template

You should be able to estimate these quickly in an interview:

### Key Formulas
```python
# QPS (Queries Per Second)
dau = 10_000_000           # 10M daily active users
avg_requests_per_user = 20
seconds_per_day = 86_400

qps = dau * avg_requests_per_user / seconds_per_day
# = 10M * 20 / 86400 ≈ 2,315 QPS

peak_qps = qps * 3  # peak is typically 2-5x average
# ≈ 6,944 QPS

# Storage
daily_new_records = 1_000_000          # 1M new records/day
avg_record_size_bytes = 500            # 500 bytes each
retention_years = 5

total_storage_bytes = (
    daily_new_records
    * avg_record_size_bytes
    * 365
    * retention_years
)
# = 1M * 500 * 365 * 5 ≈ 912.5 GB ≈ ~1 TB

# Bandwidth
bandwidth_bps = qps * avg_record_size_bytes * 8  # bits per second
# = 2315 * 500 * 8 ≈ 9.26 Mbps
```

### Useful Powers of 2
| Power | Exact Value | Approx. Metric | Common Name |
|-------|-------------|----------------|-------------|
| 2^10 | 1,024 | ~1 Thousand | 1 KB |
| 2^20 | 1,048,576 | ~1 Million | 1 MB |
| 2^30 | 1,073,741,824 | ~1 Billion | 1 GB |
| 2^40 | 1,099,511,627,776 | ~1 Trillion | 1 TB |

> **Note**: These are approximations. 1 KB = 1,024 bytes (not exactly 1,000). The ~2.4%
> difference is negligible for back-of-the-envelope estimates, but be aware that storage
> vendors use metric prefixes (1 TB = 10^12 bytes) while operating systems often use
> binary prefixes (1 TiB = 2^40 bytes). For interviews, treating 2^10 ≈ 10^3 is fine.

### Latency Numbers Every Engineer Should Know

> **Note**: These are order-of-magnitude approximations from various sources (Jeff Dean,
> Peter Norvig). Exact values vary by hardware generation. What matters for interviews is
> the **relative order**: L1 ≪ L2 ≪ RAM ≪ SSD ≪ HDD, and intra-DC ≪ cross-continent.
> See also [Fundamentals — Latency Numbers](./01-fundamentals.md#latency-numbers-every-engineer-should-know).

| Operation | Latency | Order of Magnitude |
|-----------|---------|-------------------|
| L1 cache reference | ~1 ns | nanoseconds |
| L2 cache reference | ~4 ns | nanoseconds |
| Main memory reference | ~100 ns | nanoseconds |
| SSD random read | ~100 μs | microseconds |
| Send 1 KB over 1 Gbps network | ~10 μs | microseconds |
| Round trip within same datacenter | ~0.5 ms | sub-millisecond |
| HDD random read | ~4 ms | milliseconds |
| Send 1 MB over 1 Gbps network | ~10 ms | milliseconds |
| Round trip CA → Netherlands | ~150 ms | hundred milliseconds |

---

## Practice Problems (Progressive Difficulty)

### Easy — Component Selection

**1. Rate Limiter**: Design a rate limiter that allows 100 requests per user per minute. Which data structure would you use?

<details>
<summary><strong>Hint</strong></summary>

Think about what needs to be tracked per user and how to expire old data. Redis has built-in TTL support that makes this straightforward.

</details>

<details>
<summary><strong>Solution</strong></summary>

Use a **sliding window counter in Redis with TTL**. For each user, maintain a Redis key like `rate:{user_id}:{minute_window}` with an integer count. Increment on each request, set TTL to 60 seconds. If the count exceeds 100, reject.

Alternatively, use a Redis sorted set where each member is a request timestamp. On each request, remove entries older than 60 seconds, count remaining entries, and add the new timestamp if under the limit.

```python
import time

def is_allowed_sliding_window(redis_client, user_id: str, limit: int = 100, window_secs: int = 60) -> bool:
    """Sliding window rate limiter using a sorted set."""
    key = f"rate:{user_id}"
    now = time.time()
    cutoff = now - window_secs

    pipe = redis_client.pipeline()
    pipe.zremrangebyscore(key, 0, cutoff)  # remove expired entries
    pipe.zcard(key)                         # count current entries
    pipe.zadd(key, {str(now): now})         # add current request
    pipe.expire(key, window_secs)           # auto-cleanup
    results = pipe.execute()

    current_count = results[1]
    return current_count < limit
```

</details>

---

**2. Paste Service (Pastebin)**: Design a system like Pastebin. How does it differ from a URL shortener?

<details>
<summary><strong>Hint</strong></summary>

The key difference is what gets stored. A URL shortener stores a mapping (short → long URL). A paste service stores actual content that can be large (up to several MB).

</details>

<details>
<summary><strong>Solution</strong></summary>

Similar architecture to a URL shortener, but with key differences:
- **Storage**: Content is stored in **object storage (S3)** instead of a database field, because pastes can be large (up to ~10 MB). The database stores metadata (paste_id, title, expiry, language, author).
- **Reads return content**: Instead of a 301/302 redirect, the API returns the paste content directly (or a pre-signed URL to S3).
- **Content-type awareness**: Pastes have syntax highlighting, so the system stores the language/format.
- **Expiration**: More prominent than in URL shorteners — many pastes are meant to be temporary.

```text
Client ──> LB ──> App Server ──> Metadata DB (paste_id, title, expiry)
                      │
                      ▼
               Object Store (S3) ── stores actual paste content
                      │
                      ▼
                  CDN (cache popular pastes)
```

</details>

---

**3. Unique ID Generator**: Design a system that generates unique IDs across multiple servers without coordination.

<details>
<summary><strong>Hint</strong></summary>

Think about how to embed enough information in the ID itself (timestamp, machine identity, sequence) to guarantee uniqueness without a central coordinator.

</details>

<details>
<summary><strong>Solution</strong></summary>

Use **Twitter's Snowflake ID** scheme — a 64-bit ID composed of:

| Bits | Field | Purpose |
|------|-------|---------|
| 1 | Sign | Always 0 (positive) |
| 41 | Timestamp | Milliseconds since custom epoch (~69 years) |
| 10 | Machine ID | Supports 1,024 machines |
| 12 | Sequence | 4,096 IDs per millisecond per machine |

```python
import time

class SnowflakeGenerator:
    """Generates unique 64-bit IDs without coordination."""

    EPOCH = 1609459200000  # 2021-01-01 00:00:00 UTC in ms

    def __init__(self, machine_id: int):
        if not (0 <= machine_id < 1024):
            raise ValueError("machine_id must be 0-1023")
        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = -1

    def generate(self) -> int:
        timestamp = int(time.time() * 1000) - self.EPOCH

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 0xFFF  # 12-bit wrap
            if self.sequence == 0:
                # Exhausted sequence in this ms — wait for next ms
                while timestamp == self.last_timestamp:
                    timestamp = int(time.time() * 1000) - self.EPOCH
        else:
            self.sequence = 0

        self.last_timestamp = timestamp
        return (timestamp << 22) | (self.machine_id << 12) | self.sequence

gen = SnowflakeGenerator(machine_id=1)
ids = [gen.generate() for _ in range(5)]
print("Generated IDs:", ids)
print("All unique:", len(set(ids)) == len(ids))
```

Key properties: IDs are **time-sortable** (newer IDs are larger), **unique** (no coordination needed), and **compact** (64-bit integer).

</details>

### Medium — Full System Design

**4. Instagram/Photo Sharing**: Design a photo-sharing service. Key questions: How do you store and serve billions of images? How do you generate the news feed?

<details>
<summary><strong>Hint</strong></summary>

This combines three case studies: URL shortener-like ID generation for photo IDs, CDN + object storage for images (like the video streaming section), and news feed fan-out. Focus on the image pipeline: upload → resize/thumbnail → store → serve via CDN.

</details>

<details>
<summary><strong>Solution</strong></summary>

**Architecture overview:**
```text
Upload: Client ──> LB ──> Upload Service ──> S3 (original)
                               │
                               ▼
                         Image Processing Queue
                               │
                               ▼
                         Resize Workers (thumbnail, medium, full)
                               │
                               ▼
                         S3 (processed) ──> CDN

Feed:   Client ──> LB ──> Feed Service ──> Feed Cache (Redis)
                                               │ (miss)
                                               ▼
                                           Post DB + Social Graph
```

**Key decisions:**
- **Storage**: Original images in S3. Generate multiple sizes (150×150 thumbnail, 640×640 feed, original). Total ~3-4x the original storage.
- **Feed**: Hybrid fan-out (same as Twitter). Push for normal users, pull for celebrity accounts.
- **Image IDs**: Snowflake IDs — time-sortable, which is useful for chronological feeds.
- **CDN**: Critical for serving images. Most reads hit the CDN, not origin. Hot images (recent posts from popular accounts) stay cached.
- **Metadata DB**: Sharded by user_id. Stores post metadata, likes, comments. Separate from image storage.

</details>

---

**5. Typeahead / Autocomplete**: Design a search autocomplete system. Key questions: How do you serve suggestions in <100ms? How do you update suggestions as new data comes in?

<details>
<summary><strong>Hint</strong></summary>

The core data structure is a **trie** (prefix tree). Think about how to rank suggestions (by frequency/popularity) and how to update the trie without affecting read latency. Consider the update frequency — do you need real-time updates or is batch rebuilding acceptable?

</details>

<details>
<summary><strong>Solution</strong></summary>

**Architecture:**
```text
User types "how t" ──> LB ──> Autocomplete Service ──> Trie (in-memory)
                                                             │
                                                       Top-K suggestions
                                                       for prefix "how t"

Offline Pipeline (every few hours):
  Query Logs ──> MapReduce ──> Aggregate frequencies ──> Build new Trie ──> Swap in
```

**Key decisions:**
- **Trie data structure**: Each node stores a character. Leaf/internal nodes annotated with top-K suggestions for that prefix (precomputed). This makes lookups O(prefix_length) regardless of corpus size.
- **Precomputed top-K**: Don't traverse the entire subtree at query time. Store the top 10-15 suggestions at each trie node during build time.
- **Sharding**: Shard the trie by prefix range (a-m on shard 1, n-z on shard 2). The first character determines the shard.
- **Updates**: Rebuild the trie offline from aggregated query logs (hourly/daily). Swap the new trie in atomically. Real-time trending queries can be handled by a separate small index merged at query time.
- **Caching**: Browser-side caching + CDN caching for popular prefixes. "how to" is queried millions of times — cache it aggressively.

</details>

---

**6. Distributed Cache (Memcached)**: Design a distributed caching system. Key questions: How do you partition keys across nodes? What happens when a node dies?

<details>
<summary><strong>Hint</strong></summary>

This is a direct application of consistent hashing (Section 8 of fundamentals). The interesting part is handling node failures — what happens to the keys that were on the dead node? Consider the cold-start problem and thundering herd.

</details>

<details>
<summary><strong>Solution</strong></summary>

**Architecture:**
```text
Client Library (with consistent hash ring)
       │
       ├──> Cache Node A (keys: x, y)
       ├──> Cache Node B (keys: z, w)
       └──> Cache Node C (keys: v, u)
```

**Key decisions:**
- **Consistent hashing**: Client library maintains a hash ring. Keys are mapped to nodes via the ring. Adding/removing a node only moves ~1/N of the keys.
- **Virtual nodes**: Each physical node has 100-200 virtual nodes on the ring for even distribution.
- **Node failure**: Keys on the dead node become cache misses. Requests fall through to the database. The ring is updated to redistribute those keys to surviving nodes. **Thundering herd risk**: many cache misses simultaneously hitting the DB.
- **Thundering herd mitigation**: Use **request coalescing** (only one request fetches from DB, others wait for the result) and **staggered expiry** (add random jitter to TTLs).
- **Replication**: For high availability, replicate each key to the next N nodes on the ring. On a cache miss from the primary, check replicas before hitting the DB.

</details>

### Hard — Complex Trade-offs

**7. Google Maps / Navigation**: Design a navigation service. Key questions: How do you store the road network? How do you compute shortest paths at scale?

<details>
<summary><strong>Hint</strong></summary>

The road network is a weighted graph (intersections = nodes, road segments = edges, weights = travel time). Dijkstra's algorithm is too slow for continent-scale routing. Research **Contraction Hierarchies** — a preprocessing technique that adds shortcut edges to speed up queries by orders of magnitude.

</details>

<details>
<summary><strong>Solution</strong></summary>

**Key decisions:**
- **Graph representation**: Road network as an adjacency list. Node = intersection (lat, lng, ID). Edge = road segment (distance, speed limit, current traffic, road type). The full US road network has ~24M nodes and ~58M edges.
- **Contraction Hierarchies (CH)**: Preprocess the graph by iteratively removing "unimportant" nodes and adding shortcut edges. Query time drops from seconds (Dijkstra) to milliseconds. Preprocessing takes hours but only needs to happen once (or when the road network changes).
- **Live traffic**: CH works for static weights. For real-time traffic, use **time-dependent CH** or a hybrid: CH for the macro route + Dijkstra for the local start/end segments with live traffic data.
- **Tile-based storage**: Partition the map into geographic tiles. Load only the tiles needed for the route. Store tiles in object storage, cache popular tiles (urban areas) aggressively.
- **ETA updates**: Once a route is computed, the driver's position is tracked. If they deviate or traffic changes, re-route from the current position (not from scratch — reuse parts of the original route).

</details>

---

**8. Distributed Message Queue (Kafka)**: Design a distributed message queue from scratch. Key questions: How do you guarantee ordering? How do you handle consumer failures?

<details>
<summary><strong>Hint</strong></summary>

Think about the core abstraction: a **partitioned, append-only log**. Ordering is guaranteed within a partition. Consumers track their position (offset) in each partition. Replication provides durability. The key design tension is between ordering guarantees and parallelism.

</details>

<details>
<summary><strong>Solution</strong></summary>

**Architecture:**
```text
Producers ──> Broker Cluster (partitioned topics)
                  │
           ┌──────┼──────┐
           ▼      ▼      ▼
        Part 0  Part 1  Part 2   (append-only logs, replicated)
           │      │      │
           ▼      ▼      ▼
        Consumer Group (each partition assigned to one consumer)
```

**Key decisions:**
- **Partitioning**: Each topic is split into N partitions. Messages with the same key go to the same partition (hash(key) % N). This guarantees ordering per key.
- **Replication**: Each partition has a leader and R-1 followers (replication factor R). Writes go to the leader, which replicates to followers. ISR (In-Sync Replicas) tracks which followers are caught up.
- **Consumer offsets**: Each consumer tracks its offset (position) per partition. On failure, the consumer resumes from the last committed offset. At-least-once delivery by default; exactly-once requires idempotent consumers.
- **Consumer groups**: Each partition is assigned to exactly one consumer within a group. Adding consumers triggers rebalancing. Max parallelism = number of partitions.
- **Retention**: Messages are retained for a configurable period (e.g., 7 days) regardless of consumption. This enables replay for reprocessing.

</details>

---

**9. Real-Time Gaming Leaderboard**: Design a global leaderboard that updates in real-time for 100M players. Key questions: How do you efficiently insert scores and query rank?

<details>
<summary><strong>Hint</strong></summary>

Redis Sorted Sets give you O(log N) insert and O(log N) rank lookup. But 100M entries in a single Redis instance may hit memory limits (~1.6 GB for 100M entries with small values). Think about sharding by score range and how to compute global rank from shard-local ranks.

</details>

<details>
<summary><strong>Solution</strong></summary>

**Approach 1: Redis Sorted Set (up to ~10M players)**
```python
# Redis commands:
# ZADD leaderboard <score> <user_id>     — O(log N) insert
# ZREVRANK leaderboard <user_id>          — O(log N) rank query (0-indexed)
# ZREVRANGE leaderboard 0 9 WITHSCORES   — top 10
```

**Approach 2: Sharded by score range (100M+ players)**
- Divide the score range into S shards (e.g., 0-999 → shard 0, 1000-1999 → shard 1, ...).
- Each shard is a Redis sorted set.
- To get a user's global rank: rank within shard + sum of counts from all higher shards.
- Trade-off: rank queries require cross-shard aggregation, but writes are distributed.

**Approach 3: Approximate ranking (for users outside top N)**
- Maintain an exact leaderboard for the top 10,000 players.
- For other players, report approximate rank using percentile buckets (e.g., "top 5%").
- Most users only care about their approximate position; exact rank matters only near the top.

</details>

---

### Mini-Implementation Problems

These hands-on problems let you practice implementing pieces of the systems discussed above.

**10. Bloom Filter for URL Deduplication (Easy-Medium)**

A web crawler needs to track billions of URLs it has already visited. Implement a Bloom filter — a space-efficient probabilistic data structure that can tell you "definitely not seen" or "probably seen."

<details>
<summary><strong>Hint</strong></summary>

A Bloom filter is a bit array of size `m` with `k` hash functions. To add an element, hash it with each function and set those bit positions to 1. To check membership, hash with all functions — if any bit is 0, the element is definitely not in the set. If all bits are 1, it's *probably* in the set (false positive possible, but false negative is impossible).

</details>

<details>
<summary><strong>Solution</strong></summary>

```python
import hashlib
import math


class BloomFilter:
    """
    Space-efficient probabilistic set membership test.
    
    Used in web crawlers (URL dedup), databases (skip disk reads for absent keys),
    and caches (avoid caching items that were never requested).
    
    Properties:
    - False positives possible (says "yes" but element was never added)
    - False negatives impossible (never says "no" for an added element)
    - Cannot delete elements (use Counting Bloom Filter for that)
    """

    def __init__(self, expected_items: int, false_positive_rate: float = 0.01):
        # Optimal bit array size: m = -(n * ln(p)) / (ln(2)^2)
        self.size = self._optimal_size(expected_items, false_positive_rate)
        # Optimal number of hash functions: k = (m / n) * ln(2)
        self.num_hashes = self._optimal_hashes(self.size, expected_items)
        self.bit_array = [False] * self.size
        self.count = 0

    @staticmethod
    def _optimal_size(n: int, p: float) -> int:
        """Calculate optimal bit array size for n items and false positive rate p."""
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m) + 1

    @staticmethod
    def _optimal_hashes(m: int, n: int) -> int:
        """Calculate optimal number of hash functions."""
        k = (m / n) * math.log(2)
        return max(1, int(k))

    def _get_hash_positions(self, item: str) -> list[int]:
        """Generate k hash positions using double hashing technique."""
        # Use two independent hashes to simulate k hash functions:
        # h_i(x) = (h1(x) + i * h2(x)) % m
        h1 = int(hashlib.md5(item.encode()).hexdigest(), 16)
        h2 = int(hashlib.sha256(item.encode()).hexdigest(), 16)
        return [(h1 + i * h2) % self.size for i in range(self.num_hashes)]

    def add(self, item: str) -> None:
        """Add an item to the filter."""
        for pos in self._get_hash_positions(item):
            self.bit_array[pos] = True
        self.count += 1

    def might_contain(self, item: str) -> bool:
        """
        Check if item might be in the set.
        Returns False = DEFINITELY not in set.
        Returns True  = PROBABLY in set (small chance of false positive).
        """
        return all(self.bit_array[pos] for pos in self._get_hash_positions(item))


# --- Demo: URL deduplication for a web crawler ---
bf = BloomFilter(expected_items=1_000_000, false_positive_rate=0.01)

# Simulate crawling
crawled_urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
]

for url in crawled_urls:
    bf.add(url)

# Check membership
print(bf.might_contain("https://example.com/page1"))  # True (correctly identified)
print(bf.might_contain("https://example.com/page4"))  # False (correctly rejected)
print(bf.might_contain("https://example.com/page2"))  # True (correctly identified)

# Space efficiency
bits_per_item = bf.size / bf.count
print(f"\nFilter size: {bf.size:,} bits ({bf.size // 8:,} bytes)")
print(f"Hash functions: {bf.num_hashes}")
print(f"Items added: {bf.count}")
print(f"Bits per item: {bits_per_item:.1f}")
# For 1M items at 1% FP rate: ~1.2 MB (vs. storing actual URLs: ~50+ MB)

# Measure actual false positive rate with random URLs
false_positives = sum(
    1 for i in range(10_000)
    if bf.might_contain(f"https://random-site.com/not-crawled-{i}")
)
print(f"Measured false positive rate: {false_positives / 10_000:.4f} (target: 0.01)")
```

</details>

---

**11. Fan-Out Service Simulator (Medium)**

Implement a simplified fan-out service for a social media news feed. Given a user's post and their follower list, simulate both **push (fan-out on write)** and **pull (fan-out on read)** strategies. Measure the trade-offs in write cost vs. read cost.

<details>
<summary><strong>Hint</strong></summary>

For push: when a user posts, iterate over all followers and write the post to each follower's feed cache. For pull: when a user reads their feed, iterate over all accounts they follow and fetch their latest posts, then merge and sort. Track the number of operations for each strategy.

</details>

<details>
<summary><strong>Solution</strong></summary>

```python
from collections import defaultdict
from dataclasses import dataclass, field
import time as time_module


@dataclass
class Post:
    post_id: str
    author_id: str
    content: str
    timestamp: float = field(default_factory=time_module.time)


class SocialGraph:
    """Tracks who follows whom."""

    def __init__(self):
        self.followers: dict[str, set[str]] = defaultdict(set)   # user → set of followers
        self.following: dict[str, set[str]] = defaultdict(set)   # user → set of users they follow

    def follow(self, follower: str, followee: str) -> None:
        self.followers[followee].add(follower)
        self.following[follower].add(followee)

    def get_followers(self, user: str) -> set[str]:
        return self.followers[user]

    def get_following(self, user: str) -> set[str]:
        return self.following[user]


class PushFanOut:
    """
    Fan-out on WRITE: when a user posts, write to every follower's feed cache.
    Fast reads (pre-computed), slow writes for popular users.
    """

    def __init__(self, graph: SocialGraph):
        self.graph = graph
        self.feed_cache: dict[str, list[Post]] = defaultdict(list)  # user → their feed
        self.write_ops = 0
        self.read_ops = 0

    def publish(self, post: Post) -> int:
        """Fan-out a post to all followers' feed caches. Returns number of writes."""
        followers = self.graph.get_followers(post.author_id)
        for follower in followers:
            self.feed_cache[follower].append(post)
            self.write_ops += 1
        return len(followers)

    def get_feed(self, user_id: str, limit: int = 10) -> list[Post]:
        """Read pre-computed feed — O(1) lookup, just sort and truncate."""
        self.read_ops += 1
        feed = sorted(self.feed_cache[user_id], key=lambda p: p.timestamp, reverse=True)
        return feed[:limit]


class PullFanOut:
    """
    Fan-out on READ: when a user reads their feed, fetch posts from all followed users.
    Fast writes (just store the post), slow reads for users following many accounts.
    """

    def __init__(self, graph: SocialGraph):
        self.graph = graph
        self.user_posts: dict[str, list[Post]] = defaultdict(list)  # user → their posts
        self.write_ops = 0
        self.read_ops = 0

    def publish(self, post: Post) -> int:
        """Just store the post under the author. O(1) write."""
        self.user_posts[post.author_id].append(post)
        self.write_ops += 1
        return 1

    def get_feed(self, user_id: str, limit: int = 10) -> list[Post]:
        """Fetch and merge posts from all followed users at read time."""
        following = self.graph.get_following(user_id)
        all_posts: list[Post] = []
        for followee in following:
            all_posts.extend(self.user_posts[followee])
            self.read_ops += 1
        all_posts.sort(key=lambda p: p.timestamp, reverse=True)
        return all_posts[:limit]


# --- Simulation ---
graph = SocialGraph()

# Create a "celebrity" with 1000 followers
for i in range(1000):
    graph.follow(f"user_{i}", "celebrity")

# Create a "normal user" with 5 followers
for i in range(5):
    graph.follow(f"fan_{i}", "normal_user")

# Each follower also follows 50 other users (for pull cost)
for i in range(1000):
    for j in range(50):
        graph.follow(f"user_{i}", f"content_creator_{j}")

# --- Test Push ---
push = PushFanOut(graph)
celebrity_post = Post("p1", "celebrity", "Hello from celebrity!")
writes = push.publish(celebrity_post)
print(f"PUSH — Celebrity post: {writes} write operations (1 per follower)")

normal_post = Post("p2", "normal_user", "Hello from normal user!")
writes = push.publish(normal_post)
print(f"PUSH — Normal user post: {writes} write operations")

feed = push.get_feed("user_0")
print(f"PUSH — Read feed: 1 operation, got {len(feed)} posts")
print(f"PUSH — Total: {push.write_ops} writes, {push.read_ops} reads")

# --- Test Pull ---
pull = PullFanOut(graph)
pull.publish(celebrity_post)
print(f"\nPULL — Celebrity post: 1 write operation (just store it)")
pull.publish(normal_post)
print(f"PULL — Normal user post: 1 write operation")

feed = pull.get_feed("user_0")
print(f"PULL — Read feed: {pull.read_ops} read operations (1 per followed user)")
print(f"PULL — Total: {pull.write_ops} writes, {pull.read_ops} reads")

print(f"\n--- Summary ---")
print(f"Push: O(num_followers) writes, O(1) reads — best when followers << reads")
print(f"Pull: O(1) writes, O(num_following) reads — best when following << writes")
print(f"Hybrid: Push for normal users, Pull for celebrities (>100K followers)")
```

</details>

---

**12. Simple Base62 Encoder/Decoder (Easy)**

Implement a Base62 encoder and decoder for a URL shortener. Verify that encoding and decoding are inverses of each other for a range of inputs.

<details>
<summary><strong>Hint</strong></summary>

Base62 uses characters `0-9`, `a-z`, `A-Z` (62 characters). Encoding is like converting a base-10 number to base-62. Use repeated division (`divmod`) for encoding and positional multiplication for decoding.

</details>

<details>
<summary><strong>Solution</strong></summary>

```python
import string


BASE62_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase

def base62_encode(num: int) -> str:
    """Convert a non-negative integer to a Base62 string."""
    if num < 0:
        raise ValueError("Only non-negative integers are supported")
    if num == 0:
        return BASE62_CHARS[0]

    result = []
    while num > 0:
        num, remainder = divmod(num, 62)
        result.append(BASE62_CHARS[remainder])
    return ''.join(reversed(result))


def base62_decode(encoded: str) -> int:
    """Convert a Base62 string back to an integer."""
    num = 0
    for char in encoded:
        num = num * 62 + BASE62_CHARS.index(char)
    return num


# --- Verification ---

# Test specific values
test_cases = [0, 1, 61, 62, 1000, 1_000_000, 1_000_000_000, 3_500_000_000_000]
for n in test_cases:
    encoded = base62_encode(n)
    decoded = base62_decode(encoded)
    status = "OK" if decoded == n else "FAIL"
    print(f"  {n:>15,} -> {encoded:>8} -> {decoded:>15,}  [{status}]")

# Verify 7-char capacity: 62^7 = 3,521,614,606,208 ≈ 3.5 trillion
max_7char = 62**7 - 1
encoded_max = base62_encode(max_7char)
print(f"\n  Max 7-char value: {max_7char:,} -> \"{encoded_max}\"")
print(f"  Length: {len(encoded_max)} chars")
print(f"  This means 7 chars can represent ~3.5 trillion unique URLs.")
```

</details>

---

## Interview Tip: The "Why"

Whenever you add a component (like a Cache or a Queue), always state **why**:

> "I'm adding a Redis cache here to reduce the read latency on the profile service from ~100ms (database) to ~5ms (cache), because profiles are read 1000x more than they are updated."

> "I'm using Kafka between the Order Service and the Email Service to decouple them. If the Email Service goes down, orders are not lost — they queue up and are processed when the service recovers."

> "I'm choosing Cassandra over PostgreSQL for the chat message store because we need to handle 230K writes/sec. Cassandra's LSM-tree storage engine is optimized for high write throughput, and we can partition by conversation_id to keep related messages co-located."

The interviewer is testing whether you understand trade-offs, not whether you can memorize architectures.
