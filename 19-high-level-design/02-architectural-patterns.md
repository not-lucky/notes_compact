# Architectural Patterns

Core building blocks and design patterns for system design interviews.

> **Prerequisites:** [HLD Fundamentals](./01-fundamentals.md)

---

## 1. Monolith vs. Microservices

The most fundamental architectural decision. Understand the trade-offs deeply.

### Monolithic Architecture
All components run in a **single process** and are deployed as a single unit.

```text
┌──────────────────────────────────────┐
│            Monolith App              │
│  ┌──────┐ ┌──────┐ ┌──────────────┐ │
│  │ Auth │ │Orders│ │  Payments    │ │
│  └──┬───┘ └──┬───┘ └──────┬───────┘ │
│     └────────┴─────────────┘         │
│            Shared Database           │
└──────────────────────────────────────┘
```

- **Pros**: Simple to develop, test, deploy, and debug. Low latency (in-process calls).
- **Cons**: Tight coupling. One bug can crash everything. Hard to scale individual components. Long deploy cycles as codebase grows.
- **When to use**: Early-stage startups, small teams, MVPs, internal tools.

### Microservices Architecture
Each service is an **independent process** that owns its own data and communicates over the network.

```text
┌────────┐   ┌──────────┐   ┌──────────┐
│  Auth  │   │  Orders  │   │ Payments │
│Service │   │ Service  │   │ Service  │
│  [DB]  │   │   [DB]   │   │   [DB]   │
└───┬────┘   └────┬─────┘   └────┬─────┘
    │             │              │
────┴─────────────┴──────────────┴──── Network
```

- **Pros**: Independent deployments, independent scaling, team autonomy, technology diversity.
- **Cons**: Network latency, distributed system complexity (partial failures, data consistency), operational overhead (monitoring, tracing, deployment).
- **When to use**: Large teams (Conway's Law), services with very different scaling profiles, organizations needing independent deploy cycles.

### Decision Framework

| Factor | Monolith | Microservices |
|--------|----------|---------------|
| **Team size** | < 10 engineers | Multiple teams (> 10) |
| **Deploy cadence** | Weekly/monthly | Multiple per day |
| **Scale needs** | Uniform | Component-specific |
| **Data model** | Highly relational | Bounded contexts |
| **Latency tolerance** | Low (in-process) | Higher (network hops) |
| **Operational maturity** | Low | High (CI/CD, observability) |

> **Interview Tip**: Don't say "microservices are always better." State the trade-offs and justify your choice based on the problem's constraints. Many successful systems start as monoliths and migrate.

---

## 2. API Gateway

A **single entry point** for all client requests. Routes requests to the appropriate microservice.

```text
             ┌─────────────┐
 Clients ──> │ API Gateway │
             └──┬───┬───┬──┘
                │   │   │
           ┌────┘   │   └────┐
           v        v        v
        Auth    Orders   Payments
```

### Responsibilities
- **Routing**: Forward requests to the correct backend service.
- **Authentication/Authorization**: Validate tokens/API keys at the edge.
- **Rate Limiting**: Protect backend services from abuse.
- **Request/Response Transformation**: Aggregate responses from multiple services (BFF pattern).
- **SSL Termination**: Decrypt HTTPS at the gateway, use plain HTTP internally.
- **Caching**: Cache responses for repeated requests.

### Tools
- **Cloud-native**: AWS API Gateway, Google Cloud Endpoints.
- **Self-hosted**: Kong, NGINX, Envoy, Traefik.

```python
# Conceptual API Gateway routing logic
from dataclasses import dataclass

@dataclass
class Route:
    path_prefix: str
    target_service: str
    rate_limit_rps: int  # requests per second

class APIGateway:
    def __init__(self):
        self.routes: list[Route] = [
            Route("/api/auth",     "auth-service:8001",     rate_limit_rps=100),
            Route("/api/orders",   "orders-service:8002",   rate_limit_rps=500),
            Route("/api/payments", "payments-service:8003",  rate_limit_rps=200),
        ]

    def resolve(self, request_path: str) -> str | None:
        """Find the target service for a given request path."""
        for route in self.routes:
            if request_path.startswith(route.path_prefix):
                return route.target_service
        return None
```

> **When to use**: Almost always in a microservices architecture. Avoids clients needing to know about every service.

---

## 3. Load Balancers

Distributes incoming network traffic across multiple servers to ensure no single server is overwhelmed.

- **Algorithms**: Round Robin, Weighted Round Robin, Least Connections, IP Hash, Consistent Hashing.
- **Placement**: Client → LB → Web Server → LB → Internal Service.

### Layer 4 vs. Layer 7 Load Balancing

| Feature | L4 (Transport Layer) | L7 (Application Layer) |
|---------|-----------------------|-------------------------|
| **Inspects** | IP address, TCP/UDP port | HTTP headers, cookies, URL path, body |
| **Routing logic** | Packet-level (fast) | Content-aware (smart) |
| **Performance** | Higher throughput, lower latency | Lower throughput (parses HTTP, terminates SSL) |
| **Use case** | High-speed TCP/UDP balancing, non-HTTP protocols | Microservices routing, A/B testing, sticky sessions |
| **Examples** | AWS NLB, HAProxy (TCP mode) | AWS ALB, NGINX, Envoy |

### Health Checks
Load balancers must detect unhealthy servers to stop routing traffic to them:
- **Active**: LB periodically pings a health endpoint (e.g., `GET /health`).
- **Passive**: LB monitors error rates on real traffic and removes servers exceeding a threshold.

```python
# Simplified Round Robin Load Balancer
class RoundRobinLB:
    def __init__(self, servers: list[str]):
        self.servers = servers
        self._index = 0

    def next_server(self) -> str:
        """Return the next healthy server in round-robin order."""
        server = self.servers[self._index % len(self.servers)]
        self._index += 1
        return server

# Usage
lb = RoundRobinLB(["server-1:8080", "server-2:8080", "server-3:8080"])
for _ in range(5):
    print(lb.next_server())
# Output: server-1, server-2, server-3, server-1, server-2
```

---

## 4. Caching

Storing copies of data in a **high-speed storage layer** to reduce latency and database load.

- **CDN (Content Delivery Network)**: Caches static assets (images, videos, JS/CSS) at edge locations near users. (CloudFront, Cloudflare, Akamai).
- **Application Cache**: Caches database query results, API responses, session data. (Redis, Memcached).
- **Browser Cache**: Client-side caching via HTTP headers (`Cache-Control`, `ETag`).

### Caching Patterns

#### Cache-Aside (Lazy Loading) — Most Common
Application manages both cache and DB. On read miss, app fetches from DB and populates cache.

```text
Read:  App ──check──> Cache (HIT? return)
                       │ (MISS)
       App ──query──> DB ──result──> App ──populate──> Cache

Write: App ──write──> DB, then invalidate/delete from Cache
```

- **Pros**: Only caches what's actually requested. Cache failure doesn't break reads (falls back to DB).
- **Cons**: Cache miss = 3 round trips (check cache, query DB, populate cache). Potential for stale data if DB is updated without invalidating cache.

#### Read-Through
Cache sits **in the data path**. On miss, the cache itself fetches from DB (not the application).

- **Pros**: Simpler application code. Cache handles data loading.
- **Cons**: Cache library/provider must support it. First request for each key is slow.

#### Write-Through
Data is written to **cache and DB synchronously** (in the same operation).

```text
Client ──> Cache ──(sync write)──> DB
  ^          │
  └──────────┘  (response after both succeed)
```

- **Pros**: Cache is always consistent with DB. No stale reads.
- **Cons**: Higher write latency (writes wait for both cache + DB). Every write goes to cache, even data that may never be read.

#### Write-Back (Write-Behind)
Data is written to **cache only**, and the cache asynchronously flushes to DB in batches.

```text
Client ──> Cache ──(async, batched)──> DB
  ^          │
  └──────────┘  (fast response)
```

- **Pros**: Very low write latency. Batching reduces DB load.
- **Cons**: **Risk of data loss** if cache node fails before flushing. More complex to implement. Eventual consistency.

### Cache Eviction Policies
- **LRU (Least Recently Used)**: Evicts the least recently accessed item. Best general-purpose policy.
- **LFU (Least Frequently Used)**: Evicts the least frequently accessed item. Good for skewed access patterns.
- **FIFO (First In, First Out)**: Evicts the oldest item. Simple but not access-aware.
- **TTL (Time To Live)**: Items expire after a fixed duration. Good for data with known staleness tolerance.

### Cache Invalidation — The Hard Problem
> "There are only two hard things in Computer Science: cache invalidation and naming things." — Phil Karlton

Strategies:
- **TTL-based**: Set expiration time. Simple but can serve stale data until expiry.
- **Event-based**: Invalidate cache when the source data changes (via pub/sub, DB triggers, CDC).
- **Versioning**: Append version number to cache keys. New version = new key = automatic miss.

---

## 5. Communication Protocols

How services talk to each other. The choice depends on latency, direction, and data requirements.

| Protocol | Mechanism | Direction | Latency | Best For |
|----------|-----------|-----------|---------|----------|
| **REST (HTTP/1.1)** | Request/Response, JSON | Client → Server | Medium | Public APIs, CRUD services |
| **gRPC** | Request/Response, Protobuf over HTTP/2 | Bidirectional + streaming | Low | Internal microservice-to-microservice |
| **GraphQL** | Single endpoint, client-defined queries | Client → Server | Medium | Mobile apps, aggregation of multiple data sources |
| **WebSockets** | Persistent full-duplex TCP connection | Bidirectional | Very Low | Chat, gaming, collaborative editing |
| **SSE (Server-Sent Events)** | Persistent HTTP connection | Server → Client only | Low | Live feeds, stock tickers, notifications |
| **Long Polling** | Repeated HTTP requests, server holds response | Server → Client (simulated) | High | Simple real-time when WebSockets unavailable |

### Choosing the Right Protocol

```text
Need real-time bidirectional?
  ├── Yes → WebSockets
  └── No
      ├── Server push only? → SSE
      └── Request/Response?
          ├── Internal service-to-service, high perf? → gRPC
          ├── Public API, simple CRUD? → REST
          └── Clients need flexible queries? → GraphQL
```

### REST vs gRPC — Key Differences

| Aspect | REST | gRPC |
|--------|------|------|
| **Serialization** | JSON (text, human-readable) | Protobuf (binary, compact) |
| **Contract** | OpenAPI/Swagger (optional) | `.proto` file (required, strict) |
| **Streaming** | Not native (workarounds exist) | Native bidirectional streaming |
| **Browser support** | Full | Limited (needs grpc-web proxy) |
| **Performance** | ~2-10x slower than gRPC | Baseline |

---

## 6. Message Queues & Event Streaming

Asynchronous communication decouples producers from consumers.

### Point-to-Point (Message Queue)
A message is consumed by **exactly one consumer**. Once processed, the message is removed.

```text
Producer ──> [ Queue ] ──> Consumer
                           (one consumer gets each message)
```

- **Tools**: RabbitMQ, Amazon SQS, ActiveMQ.
- **Use cases**: Task distribution, background job processing (sending emails, resizing images).

### Pub/Sub (Publish-Subscribe)
A message is broadcast to **all subscribers** of a topic. Each subscriber gets its own copy.

```text
Publisher ──> [ Topic ] ──> Subscriber A
                       ──> Subscriber B
                       ──> Subscriber C
```

- **Tools**: Redis Pub/Sub, Google Pub/Sub, SNS.
- **Use cases**: Notifications, event broadcasting, fan-out.

### Event Streaming
Like pub/sub, but messages are **persisted in an ordered, immutable log**. Consumers can replay from any offset.

```text
Producer ──> [ Topic Partition 0 ] ──> Consumer Group A
             [ Topic Partition 1 ] ──> Consumer Group B
             (messages persisted, replayable)
```

- **Tools**: Apache Kafka, Amazon Kinesis, Redpanda.
- **Use cases**: Event sourcing, real-time analytics, change data capture (CDC), audit logs.

### Message Queue vs Event Streaming

| Feature | Message Queue (RabbitMQ/SQS) | Event Streaming (Kafka) |
|---------|------------------------------|--------------------------|
| **Message lifetime** | Deleted after consumption | Retained (configurable, days/forever) |
| **Replay** | No | Yes (consumers track their offset) |
| **Ordering** | Per-queue (best effort) | Per-partition (guaranteed) |
| **Consumer model** | Competing consumers | Consumer groups (parallel) |
| **Throughput** | Moderate (thousands/sec) | Very high (millions/sec) |
| **Use case** | Task queues, work distribution | Event sourcing, analytics, CDC |

### Delivery Guarantees
- **At-most-once**: Message may be lost, never duplicated. (Fastest, least reliable.)
- **At-least-once**: Message is never lost, but may be duplicated. (Consumer must be **idempotent**.)
- **Exactly-once**: Message delivered exactly once. (Hardest to achieve. Kafka supports this with transactions.)

> **Interview Tip**: "At-least-once + idempotent consumers" is the most practical design for real systems. True exactly-once is expensive and rarely needed.

---

## 7. Event-Driven Architecture (EDA)

Services communicate by **producing and reacting to events** rather than direct API calls.

```text
Order Service ──publishes──> "OrderPlaced" event
                                    │
                    ┌───────────────┼───────────────┐
                    v               v               v
             Payment Service  Inventory Service  Notification Service
             (charges card)   (reserves stock)   (sends email)
```

### Benefits
- **Loose coupling**: Services don't know about each other—they only know about events.
- **Scalability**: Each consumer scales independently.
- **Extensibility**: Add new consumers without modifying existing services.

### Challenges
- **Eventual consistency**: No immediate confirmation that all downstream work is done.
- **Debugging**: Hard to trace a request across many asynchronous services. Requires **distributed tracing** (Jaeger, Zipkin).
- **Event ordering**: Must handle out-of-order events or use partitioning keys for ordering.

### Event Sourcing
Instead of storing **current state**, store an **immutable log of all events** that led to the current state.

```python
# Traditional: Store current state
# account.balance = 500  (we lost history of how we got here)

# Event Sourcing: Store the events
events = [
    {"type": "AccountCreated", "balance": 0,    "timestamp": "2025-01-01T00:00:00Z"},
    {"type": "Deposit",        "amount": 1000,  "timestamp": "2025-01-02T10:00:00Z"},
    {"type": "Withdrawal",     "amount": 200,   "timestamp": "2025-01-03T14:30:00Z"},
    {"type": "Withdrawal",     "amount": 300,   "timestamp": "2025-01-04T09:15:00Z"},
]

def replay_events(events: list[dict]) -> int:
    """Rebuild current state by replaying all events (requires Python 3.10+)."""
    balance = 0
    for event in events:
        match event["type"]:
            case "AccountCreated":
                balance = event["balance"]
            case "Deposit":
                balance += event["amount"]
            case "Withdrawal":
                balance -= event["amount"]
            case _:
                raise ValueError(f"Unknown event type: {event['type']}")
    return balance

print(replay_events(events))  # 500
```

- **Pros**: Complete audit trail, can reconstruct state at any point in time, natural fit for event-driven systems.
- **Cons**: Event store grows indefinitely (use **snapshots** to mitigate), replaying can be slow, schema evolution of events is hard.

---

## 8. CQRS (Command Query Responsibility Segregation)

Separate the **write model** (commands) from the **read model** (queries). Each is optimized independently.

```text
                  ┌───────────────────────────┐
   Write ────>    │   Command Service         │
   (Commands)     │   (normalized, validated)  │──> Write DB (e.g., PostgreSQL)
                  └────────────┬──────────────┘
                               │ events
                               v
                  ┌───────────────────────────┐
   Read  ────>    │   Query Service           │
   (Queries)      │   (denormalized, fast)    │<── Read DB (e.g., Elasticsearch, Redis)
                  └───────────────────────────┘
```

### Why CQRS?
- **Different optimization needs**: Writes need ACID transactions, validation, normalization. Reads need speed, denormalization, search.
- **Independent scaling**: Scale read replicas independently of write nodes.
- **Pairs well with Event Sourcing**: Events from the write side project into optimized read models.

### When to Use
- Read and write workloads have very different characteristics (e.g., 100:1 read:write ratio).
- Complex query requirements (full-text search, aggregations) that don't fit the write model.
- Need to present the same data in multiple views/formats.

### When NOT to Use
- Simple CRUD applications where read/write models are nearly identical.
- Small scale where the complexity of maintaining two models isn't justified.

---

## 9. Saga Pattern

Manages **distributed transactions** across multiple microservices without a central 2PC coordinator. Each service executes a local transaction and publishes an event to trigger the next step. If a step fails, **compensating transactions** undo the previous steps.

### Choreography (Event-based)
Each service listens for events and decides what to do. No central controller.

```text
Order Service ──"OrderCreated"──> Payment Service
                                       │
                              "PaymentCompleted"
                                       │
                                       v
                               Inventory Service
                                       │
                              "StockReserved"
                                       │
                                       v
                               Shipping Service

If Payment fails:
Payment Service ──"PaymentFailed"──> Order Service (cancels order)
```

- **Pros**: Fully decoupled, no single point of failure.
- **Cons**: Hard to track the overall transaction, risk of cyclic dependencies, difficult to debug.

### Orchestration (Coordinator-based)
A central **Saga Orchestrator** directs each step and handles failures.

```text
                  Saga Orchestrator
                   /      |      \
                  v       v       v
              Payment  Inventory  Shipping
              Service  Service    Service
```

- **Pros**: Clear transaction flow, easier to debug and monitor, centralized error handling.
- **Cons**: Orchestrator is a single point of failure (must be highly available), tighter coupling to orchestrator.

```python
# Simplified Saga Orchestrator
from enum import Enum
from dataclasses import dataclass, field

class StepStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATED = "compensated"

@dataclass
class SagaStep:
    name: str
    action: str            # e.g., "charge_payment"
    compensation: str      # e.g., "refund_payment"
    status: StepStatus = StepStatus.PENDING

@dataclass
class SagaOrchestrator:
    order_id: str
    steps: list[SagaStep] = field(default_factory=list)

    def execute(self) -> bool:
        """Execute all steps. If any fails, compensate completed steps."""
        for i, step in enumerate(self.steps):
            print(f"  Executing: {step.action}")
            success = self._run_action(step.action)
            if success:
                step.status = StepStatus.COMPLETED
            else:
                step.status = StepStatus.FAILED
                print(f"  FAILED at step: {step.name}. Starting compensation...")
                self._compensate(i)
                return False
        return True

    def _compensate(self, failed_index: int) -> None:
        """Compensate all completed steps in reverse order."""
        for j in range(failed_index - 1, -1, -1):
            step = self.steps[j]
            if step.status == StepStatus.COMPLETED:
                print(f"  Compensating: {step.compensation}")
                self._run_action(step.compensation)
                step.status = StepStatus.COMPENSATED

    def _run_action(self, action: str) -> bool:
        """Simulate calling a service. Replace with real HTTP/gRPC calls."""
        # Simulate a failure for demonstration
        if action == "reserve_stock":
            return False  # Stock unavailable
        return True

# Usage
saga = SagaOrchestrator(
    order_id="order-123",
    steps=[
        SagaStep("Payment",   "charge_payment",  "refund_payment"),
        SagaStep("Inventory", "reserve_stock",    "release_stock"),
        SagaStep("Shipping",  "schedule_pickup",  "cancel_pickup"),
    ],
)
print(f"Saga result: {saga.execute()}")
# Output:
#   Executing: charge_payment
#   Executing: reserve_stock
#   FAILED at step: Inventory. Starting compensation...
#   Compensating: refund_payment
#   Saga result: False
```

---

## 10. Circuit Breaker Pattern

Prevents a service from **repeatedly calling a failing downstream service**, which would waste resources and cascade failures.

### States
```text
         ┌──────────────────────────────────────┐
         │              CLOSED                   │
         │  (normal operation, requests go       │
         │   through, failures counted)          │
         └──────────────┬───────────────────────┘
                        │ failure threshold exceeded
                        v
         ┌──────────────────────────────────────┐
         │               OPEN                    │
         │  (requests immediately fail-fast,     │
         │   no calls to downstream service)     │
         └──────────────┬───────────────────────┘
                        │ timeout expires
                        v
         ┌──────────────────────────────────────┐
         │           HALF-OPEN                   │
         │  (allow a few test requests through)  │
         │  success → CLOSED, failure → OPEN     │
         └──────────────────────────────────────┘
```

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 10.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: float = 0.0

    def call(self, func, *args, **kwargs):
        """Execute func through the circuit breaker."""
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit is OPEN — failing fast")

        try:
            result = func(*args, **kwargs)
            # Success: reset to CLOSED
            self.failure_count = 0
            self.state = CircuitState.CLOSED
            return result
        except Exception:
            self.failure_count += 1
            self.last_failure_time = time.monotonic()
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            raise
```

> **Tools**: Hystrix (deprecated, but influential), Resilience4j (Java), Polly (.NET), or implement in Python with `tenacity` + custom logic.

---

## 11. Service Mesh

A **dedicated infrastructure layer** for managing service-to-service communication. Implements networking concerns (retries, load balancing, mTLS, observability) **outside** of application code via sidecar proxies.

```text
┌──────────────────────┐     ┌──────────────────────┐
│  Service A           │     │  Service B           │
│  ┌────────────────┐  │     │  ┌────────────────┐  │
│  │  App Container  │  │     │  │  App Container  │  │
│  └───────┬────────┘  │     │  └───────▲────────┘  │
│          │           │     │          │           │
│  ┌───────▼────────┐  │     │  ┌───────┴────────┐  │
│  │ Sidecar Proxy  │──┼─────┼──│ Sidecar Proxy  │  │
│  │  (e.g. Envoy)  │  │     │  │  (e.g. Envoy)  │  │
│  └────────────────┘  │     │  └────────────────┘  │
└──────────────────────┘     └──────────────────────┘
              │                         │
              └────── Control Plane ────┘
                    (e.g., Istio, Linkerd)
```

### What It Handles
- **mTLS**: Automatic mutual TLS encryption between all services.
- **Traffic management**: Canary deployments, A/B testing, traffic splitting.
- **Observability**: Distributed tracing, metrics, logging — without app code changes.
- **Retries & Timeouts**: Configurable per-route retry policies.
- **Circuit breaking**: Built-in circuit breaker support at the proxy level.

### When to Use
- Large microservices deployments (50+ services) where managing cross-cutting concerns in each service is impractical.
- When you need consistent security (mTLS) across all services.

### When NOT to Use
- Small number of services. The operational overhead of a service mesh isn't justified.
- Monoliths or simple architectures.

---

## 12. Strangler Fig Pattern

A **migration pattern** for incrementally replacing a legacy monolith with microservices, without a risky big-bang rewrite.

```text
Phase 1:  All traffic → Monolith

Phase 2:  Traffic → Proxy/Gateway
                     ├── /users  → New User Service
                     └── /* else → Monolith (legacy)

Phase 3:  Traffic → Proxy/Gateway
                     ├── /users    → User Service
                     ├── /orders   → Order Service
                     ├── /payments → Payment Service
                     └── /reports  → Monolith (shrinking)

Phase 4:  All traffic → Microservices (Monolith decommissioned)
```

- **How it works**: Place a routing layer (API Gateway) in front of the monolith. For each feature you migrate, route that path to the new service. The monolith "shrinks" over time.
- **Named after**: The strangler fig tree, which grows around and eventually replaces its host tree.
- **Benefit**: Zero big-bang risk. Each migration is small, testable, and reversible.

---

## 13. Backpressure & Rate Limiting

### Backpressure
When a downstream service can't keep up, the upstream service **slows down** instead of overwhelming it.

- **Buffering**: Queue messages and let the consumer process at its own pace.
- **Dropping**: Drop excess messages (acceptable for metrics, telemetry).
- **Signaling**: Downstream tells upstream to slow down (e.g., TCP flow control, HTTP 429).

### Rate Limiting
Controls the **rate of incoming requests** to protect services.

#### Common Algorithms

> **Note**: See [HLD Fundamentals § Rate Limiting](./01-fundamentals.md) for detailed implementations of each algorithm. The table below is included here for quick reference in the context of backpressure.

| Algorithm | How it works | Pros | Cons |
|-----------|-------------|------|------|
| **Token Bucket** | Tokens added at fixed rate; each request costs a token | Allows bursts up to bucket size | Slightly complex |
| **Leaky Bucket** | Requests processed at fixed rate; excess queued or dropped | Smooth output rate | No burst allowance |
| **Fixed Window** | Count requests in fixed time windows (e.g., 100/minute) | Simple | Burst at window boundaries |
| **Sliding Window Log** | Track timestamp of each request in a sliding window | Accurate | Memory-heavy |
| **Sliding Window Counter** | Hybrid: weighted count from current + previous window | Accurate + memory efficient | Slightly complex |

```python
import time

class TokenBucket:
    """Rate limiter using the Token Bucket algorithm."""

    def __init__(self, capacity: int, refill_rate: float):
        """
        Args:
            capacity: Maximum tokens the bucket can hold.
            refill_rate: Tokens added per second.
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.monotonic()

    def _refill(self) -> None:
        """Add tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill = now

    def allow_request(self) -> bool:
        """Return True if the request is allowed, False otherwise."""
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

# Allow 5 requests per second, burst up to 10
limiter = TokenBucket(capacity=10, refill_rate=5)
```

---

## Summary: Choosing the Right Pattern

| Pattern | Problem it Solves | Key Trade-off |
|---------|-------------------|---------------|
| **Monolith** | Simple deployment, low latency | Doesn't scale with team size |
| **Microservices** | Team autonomy, independent scaling | Operational complexity |
| **API Gateway** | Single entry point, cross-cutting concerns | Additional network hop |
| **Load Balancer** | Distribute traffic, avoid SPOF | L4 (fast, dumb) vs L7 (smart, slower) |
| **Caching** | Reduce latency and DB load | Cache invalidation, stale data |
| **Message Queue** | Decouple producers/consumers | Added latency, at-least-once complexity |
| **Event Streaming** | Event replay, audit, real-time analytics | Operational complexity (Kafka) |
| **Event-Driven (EDA)** | Loose coupling, extensibility | Eventual consistency, hard to debug |
| **CQRS** | Optimize reads/writes independently | Two data models to maintain |
| **Saga** | Distributed transactions | Compensating transactions are complex |
| **Circuit Breaker** | Prevent cascade failures | Requests fail-fast when open |
| **Service Mesh** | Cross-cutting concerns (mTLS, tracing) | Significant operational overhead |
| **Strangler Fig** | Incremental monolith migration | Dual-system maintenance during migration |
| **Rate Limiting** | Protect from abuse/overload | Legitimate traffic may be throttled |

---

## Practice Problems

### Problem 1 (Easy): Design a Notification Router

**Problem**: Design a system that routes notifications to users via their preferred channel (email, SMS, push). Given a list of notification requests, each with a user ID, message, and preferred channel, route each notification to the correct sender.

**Requirements**:
- Support email, SMS, and push notification channels.
- Each channel has a different sender implementation.
- Make it easy to add new channels without modifying existing code.

<details>
<summary>Hint</summary>

Use the **Strategy pattern** combined with a simple routing map. Think about how an API Gateway routes requests to different services.

</details>

<details>
<summary>Solution</summary>

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

# --- Channel senders (Strategy pattern) ---
class NotificationSender(ABC):
    @abstractmethod
    def send(self, user_id: str, message: str) -> None:
        pass

class EmailSender(NotificationSender):
    def send(self, user_id: str, message: str) -> None:
        print(f"[EMAIL] To user {user_id}: {message}")

class SMSSender(NotificationSender):
    def send(self, user_id: str, message: str) -> None:
        print(f"[SMS] To user {user_id}: {message}")

class PushSender(NotificationSender):
    def send(self, user_id: str, message: str) -> None:
        print(f"[PUSH] To user {user_id}: {message}")

# --- Router ---
@dataclass
class NotificationRequest:
    user_id: str
    message: str
    channel: str  # "email", "sms", "push"

class NotificationRouter:
    def __init__(self):
        self.senders: dict[str, NotificationSender] = {
            "email": EmailSender(),
            "sms": SMSSender(),
            "push": PushSender(),
        }

    def register_channel(self, name: str, sender: NotificationSender) -> None:
        """Add a new channel without modifying existing code."""
        self.senders[name] = sender

    def route(self, request: NotificationRequest) -> None:
        sender = self.senders.get(request.channel)
        if not sender:
            print(f"[WARN] Unknown channel '{request.channel}' for user {request.user_id}")
            return
        sender.send(request.user_id, request.message)

# --- Usage ---
router = NotificationRouter()
requests = [
    NotificationRequest("user-1", "Your order shipped!", "email"),
    NotificationRequest("user-2", "OTP: 482910", "sms"),
    NotificationRequest("user-3", "New message from Alice", "push"),
]
for req in requests:
    router.route(req)
# [EMAIL] To user user-1: Your order shipped!
# [SMS] To user user-2: OTP: 482910
# [PUSH] To user user-3: New message from Alice
```

**Key takeaways**: This mirrors how an **API Gateway** routes to different services and how **event-driven architectures** route events to handlers. The `register_channel` method demonstrates the Open/Closed Principle.

</details>

---

### Problem 2 (Medium): Implement Event-Driven Order Processing

**Problem**: Implement a simplified event-driven order processing system. When an order is placed, the system should:
1. Process payment
2. Reserve inventory
3. Send a confirmation notification

Each step is a separate "service" that reacts to events. If payment fails, no further steps should execute and the order should be marked as failed.

<details>
<summary>Hint</summary>

Build a simple pub/sub event bus. Services subscribe to specific event types. When an event is published, all subscribers for that event type are notified.

</details>

<details>
<summary>Solution</summary>

```python
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Callable

# --- Event Bus (Pub/Sub) ---
@dataclass
class Event:
    event_type: str
    data: dict

class EventBus:
    """Simple in-process pub/sub event bus."""

    def __init__(self):
        self._subscribers: dict[str, list[Callable[[Event], None]]] = defaultdict(list)
        self.event_log: list[Event] = []  # For debugging/tracing

    def subscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        self._subscribers[event_type].append(handler)

    def publish(self, event: Event) -> None:
        self.event_log.append(event)
        print(f"  [BUS] Published: {event.event_type}")
        for handler in self._subscribers.get(event.event_type, []):
            handler(event)

# --- Services ---
class PaymentService:
    def __init__(self, bus: EventBus, should_fail: bool = False):
        self.bus = bus
        self.should_fail = should_fail
        bus.subscribe("OrderPlaced", self.handle_order)

    def handle_order(self, event: Event) -> None:
        order_id = event.data["order_id"]
        if self.should_fail:
            print(f"  [Payment] FAILED for order {order_id}")
            self.bus.publish(Event("PaymentFailed", {"order_id": order_id}))
        else:
            print(f"  [Payment] Charged ${ event.data['amount']} for order {order_id}")
            self.bus.publish(Event("PaymentCompleted", {"order_id": order_id}))

class InventoryService:
    def __init__(self, bus: EventBus):
        self.bus = bus
        bus.subscribe("PaymentCompleted", self.reserve_stock)

    def reserve_stock(self, event: Event) -> None:
        order_id = event.data["order_id"]
        print(f"  [Inventory] Stock reserved for order {order_id}")
        self.bus.publish(Event("StockReserved", {"order_id": order_id}))

class NotificationService:
    def __init__(self, bus: EventBus):
        bus.subscribe("StockReserved", self.send_confirmation)
        bus.subscribe("PaymentFailed", self.send_failure_notice)

    def send_confirmation(self, event: Event) -> None:
        print(f"  [Notification] Order {event.data['order_id']} confirmed! Email sent.")

    def send_failure_notice(self, event: Event) -> None:
        print(f"  [Notification] Order {event.data['order_id']} failed. User notified.")

# --- Simulation ---
print("=== Successful Order ===")
bus = EventBus()
PaymentService(bus)
InventoryService(bus)
NotificationService(bus)
bus.publish(Event("OrderPlaced", {"order_id": "ORD-001", "amount": 99.99}))

print("\n=== Failed Order ===")
bus2 = EventBus()
PaymentService(bus2, should_fail=True)
InventoryService(bus2)
NotificationService(bus2)
bus2.publish(Event("OrderPlaced", {"order_id": "ORD-002", "amount": 49.99}))

# Output:
# === Successful Order ===
#   [BUS] Published: OrderPlaced
#   [Payment] Charged $99.99 for order ORD-001
#   [BUS] Published: PaymentCompleted
#   [Inventory] Stock reserved for order ORD-001
#   [BUS] Published: StockReserved
#   [Notification] Order ORD-001 confirmed! Email sent.
#
# === Failed Order ===
#   [BUS] Published: OrderPlaced
#   [Payment] FAILED for order ORD-002
#   [BUS] Published: PaymentFailed
#   [Notification] Order ORD-002 failed. User notified.
```

**Key takeaways**: Services are **loosely coupled** — they communicate only through events. Adding a new service (e.g., Analytics) requires zero changes to existing services. The event log enables debugging and could support **event replay**.

</details>

---

### Problem 3 (Medium-Hard): Resilient Cache with Circuit Breaker

**Problem**: Implement a `ResilientCache` that wraps a remote cache (e.g., Redis) with a circuit breaker. The system should:
1. Attempt to read/write from the remote cache.
2. If the remote cache fails repeatedly (e.g., 3 consecutive failures), the circuit breaker trips **OPEN** and the system falls back to an in-memory local cache.
3. After a recovery timeout, the circuit breaker moves to **HALF-OPEN** and tests the remote cache with the next request.
4. If the test succeeds, the circuit resets to **CLOSED**. If it fails, the circuit goes back to **OPEN**.

Track and print the circuit breaker state transitions and cache source (remote vs. local fallback).

<details>
<summary>Hint</summary>

Combine the **Cache-Aside** pattern with the **Circuit Breaker** pattern. The circuit breaker wraps the remote cache calls. When the circuit is open, use a local `dict` as a fallback cache. Use `time.monotonic()` for timing.

</details>

<details>
<summary>Solution</summary>

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class RemoteCacheError(Exception):
    """Simulates a remote cache failure (e.g., Redis timeout)."""
    pass

class SimulatedRemoteCache:
    """Simulates a remote cache that can be toggled to fail."""

    def __init__(self):
        self._store: dict[str, str] = {}
        self.is_down = False

    def get(self, key: str) -> str | None:
        if self.is_down:
            raise RemoteCacheError("Remote cache unreachable")
        return self._store.get(key)

    def set(self, key: str, value: str) -> None:
        if self.is_down:
            raise RemoteCacheError("Remote cache unreachable")
        self._store[key] = value

class ResilientCache:
    """Cache-aside with circuit breaker fallback to local cache."""

    def __init__(
        self,
        remote: SimulatedRemoteCache,
        failure_threshold: int = 3,
        recovery_timeout: float = 5.0,
    ):
        self.remote = remote
        self.local: dict[str, str] = {}  # Fallback cache

        # Circuit breaker state
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time: float = 0.0

    def _trip_open(self) -> None:
        self.state = CircuitState.OPEN
        self.last_failure_time = time.monotonic()
        print(f"    [CIRCUIT] State → OPEN (falling back to local cache)")

    def _reset_closed(self) -> None:
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        print(f"    [CIRCUIT] State → CLOSED (remote cache recovered)")

    def _record_failure(self) -> None:
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self._trip_open()

    def _should_try_remote(self) -> bool:
        """Determine if we should attempt a remote cache call."""
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.OPEN:
            elapsed = time.monotonic() - self.last_failure_time
            if elapsed >= self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                print(f"    [CIRCUIT] State → HALF_OPEN (testing remote cache)")
                return True
            return False
        # HALF_OPEN: allow the test request through
        return True

    def get(self, key: str) -> str | None:
        """Read-through with circuit breaker."""
        if self._should_try_remote():
            try:
                value = self.remote.get(key)
                if self.state == CircuitState.HALF_OPEN:
                    self._reset_closed()
                print(f"    [GET] key='{key}' → remote cache (value={value!r})")
                # Sync to local cache for fallback
                if value is not None:
                    self.local[key] = value
                return value
            except RemoteCacheError:
                self._record_failure()
                if self.state == CircuitState.HALF_OPEN:
                    self._trip_open()

        # Fallback to local cache
        value = self.local.get(key)
        print(f"    [GET] key='{key}' → local fallback (value={value!r})")
        return value

    def set(self, key: str, value: str) -> None:
        """Write-through with circuit breaker."""
        # Always write to local cache so fallback is fresh
        self.local[key] = value

        if self._should_try_remote():
            try:
                self.remote.set(key, value)
                if self.state == CircuitState.HALF_OPEN:
                    self._reset_closed()
                print(f"    [SET] key='{key}' → remote cache + local")
                return
            except RemoteCacheError:
                self._record_failure()
                if self.state == CircuitState.HALF_OPEN:
                    self._trip_open()

        print(f"    [SET] key='{key}' → local only (remote unavailable)")

# --- Simulation ---
remote = SimulatedRemoteCache()
cache = ResilientCache(remote, failure_threshold=3, recovery_timeout=0.5)

print("=== Phase 1: Normal operation (remote cache healthy) ===")
cache.set("user:1", "Alice")
cache.set("user:2", "Bob")
print(f"  Result: {cache.get('user:1')}")

print("\n=== Phase 2: Remote cache goes down ===")
remote.is_down = True
# These failures will trip the circuit breaker
cache.get("user:1")  # failure 1
cache.get("user:2")  # failure 2
cache.get("user:1")  # failure 3 → circuit opens
# Now circuit is OPEN, uses local fallback
cache.get("user:1")
cache.set("user:3", "Charlie")

print("\n=== Phase 3: Wait for recovery timeout, remote recovers ===")
time.sleep(0.6)  # Wait past recovery_timeout
remote.is_down = False
cache.get("user:1")  # HALF_OPEN → test succeeds → CLOSED

print("\n=== Phase 4: Back to normal ===")
cache.get("user:2")

# Output:
# === Phase 1: Normal operation (remote cache healthy) ===
#     [SET] key='user:1' → remote cache + local
#     [SET] key='user:2' → remote cache + local
#     [GET] key='user:1' → remote cache (value='Alice')
#   Result: Alice
#
# === Phase 2: Remote cache goes down ===
#     [GET] key='user:1' → local fallback (value='Alice')
#     [GET] key='user:2' → local fallback (value='Bob')
#     [CIRCUIT] State → OPEN (falling back to local cache)
#     [GET] key='user:1' → local fallback (value='Alice')
#     [GET] key='user:1' → local fallback (value='Alice')
#     [SET] key='user:3' → local only (remote unavailable)
#
# === Phase 3: Wait for recovery timeout, remote recovers ===
#     [CIRCUIT] State → HALF_OPEN (testing remote cache)
#     [CIRCUIT] State → CLOSED (remote cache recovered)
#     [GET] key='user:1' → remote cache (value='Alice')
#
# === Phase 4: Back to normal ===
#     [GET] key='user:2' → remote cache (value='Bob')
```

**Key takeaways**:
1. **Circuit breaker + caching** is a very common production combination — Redis outages shouldn't take down your whole application.
2. The local cache acts as a **graceful degradation** layer, serving stale data over no data.
3. In production, you'd also add TTLs to the local cache to prevent serving indefinitely stale data, and metrics/alerts on circuit state transitions.

</details>

---

### Problem 4 (Hard): Implement a Saga with Compensating Transactions

**Problem**: Implement a saga orchestrator for a travel booking system. The saga must:
1. **Book flight** → if fails, stop.
2. **Book hotel** → if fails, cancel flight.
3. **Book rental car** → if fails, cancel hotel and cancel flight.
4. **Charge payment** → if fails, cancel rental car, cancel hotel, and cancel flight.

Each step can succeed or fail (simulate with a parameter). On failure, all previously completed steps must be compensated **in reverse order**.

Track the state of each step and print a clear audit trail.

<details>
<summary>Hint</summary>

Model each step as a pair of (action, compensation). Execute steps sequentially. On failure, iterate backwards through completed steps and execute their compensations. This is the **Orchestration Saga** pattern.

</details>

<details>
<summary>Solution</summary>

```python
from dataclasses import dataclass, field
from enum import Enum

class Status(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    COMPENSATED = "COMPENSATED"

@dataclass
class SagaStep:
    name: str
    status: Status = Status.PENDING

@dataclass
class TravelBookingSaga:
    booking_id: str
    steps: list[SagaStep] = field(default_factory=list)
    fail_at_step: int = -1  # -1 means no failure (all succeed)

    def __post_init__(self):
        self.steps = [
            SagaStep("Book Flight"),
            SagaStep("Book Hotel"),
            SagaStep("Book Rental Car"),
            SagaStep("Charge Payment"),
        ]

    def execute(self) -> bool:
        """Run the saga. Returns True if all steps succeeded."""
        print(f"\n{'='*50}")
        print(f"Starting saga for booking: {self.booking_id}")
        print(f"{'='*50}")

        for i, step in enumerate(self.steps):
            success = self._do_action(step, i)
            if not success:
                step.status = Status.FAILED
                print(f"  STEP FAILED: {step.name}")
                print(f"\n  --- Starting Compensation (reverse order) ---")
                self._compensate(i)
                self._print_summary()
                return False
            step.status = Status.COMPLETED

        self._print_summary()
        return True

    def _do_action(self, step: SagaStep, index: int) -> bool:
        """Simulate executing a step. Fails if index == fail_at_step."""
        if index == self.fail_at_step:
            print(f"  [{index + 1}] {step.name}... FAILED")
            return False
        print(f"  [{index + 1}] {step.name}... OK")
        return True

    def _compensate(self, failed_index: int) -> None:
        """Compensate all completed steps in reverse order."""
        for j in range(failed_index - 1, -1, -1):
            step = self.steps[j]
            if step.status == Status.COMPLETED:
                compensation_name = f"Cancel {step.name.split(' ', 1)[1]}"
                print(f"  [UNDO] {compensation_name}... OK")
                step.status = Status.COMPENSATED

    def _print_summary(self) -> None:
        """Print the final status of all steps."""
        print(f"\n  Final Status:")
        for step in self.steps:
            indicator = {
                Status.COMPLETED: "+",
                Status.FAILED: "X",
                Status.COMPENSATED: "~",
                Status.PENDING: "-",
            }[step.status]
            print(f"    [{indicator}] {step.name}: {step.status.value}")

# --- Test all scenarios ---

# All steps succeed
saga1 = TravelBookingSaga("TRIP-001", fail_at_step=-1)
saga1.execute()

# Fail at hotel booking (step index 1) → compensate flight
saga2 = TravelBookingSaga("TRIP-002", fail_at_step=1)
saga2.execute()

# Fail at payment (step index 3) → compensate car, hotel, flight
saga3 = TravelBookingSaga("TRIP-003", fail_at_step=3)
saga3.execute()

# Output:
# ==================================================
# Starting saga for booking: TRIP-001
# ==================================================
#   [1] Book Flight... OK
#   [2] Book Hotel... OK
#   [3] Book Rental Car... OK
#   [4] Charge Payment... OK
#
#   Final Status:
#     [+] Book Flight: COMPLETED
#     [+] Book Hotel: COMPLETED
#     [+] Book Rental Car: COMPLETED
#     [+] Charge Payment: COMPLETED
#
# ==================================================
# Starting saga for booking: TRIP-002
# ==================================================
#   [1] Book Flight... OK
#   [2] Book Hotel... FAILED
#   STEP FAILED: Book Hotel
#
#   --- Starting Compensation (reverse order) ---
#   [UNDO] Cancel Flight... OK
#
#   Final Status:
#     [~] Book Flight: COMPENSATED
#     [X] Book Hotel: FAILED
#     [-] Book Rental Car: PENDING
#     [-] Charge Payment: PENDING
#
# ==================================================
# Starting saga for booking: TRIP-003
# ==================================================
#   [1] Book Flight... OK
#   [2] Book Hotel... OK
#   [3] Book Rental Car... OK
#   [4] Charge Payment... FAILED
#   STEP FAILED: Charge Payment
#
#   --- Starting Compensation (reverse order) ---
#   [UNDO] Cancel Rental Car... OK
#   [UNDO] Cancel Hotel... OK
#   [UNDO] Cancel Flight... OK
#
#   Final Status:
#     [~] Book Flight: COMPENSATED
#     [~] Book Hotel: COMPENSATED
#     [~] Book Rental Car: COMPENSATED
#     [X] Charge Payment: FAILED
```

**Key takeaways**:
1. **Compensating transactions** are the core of the Saga pattern — every action must have an undo.
2. Compensation runs in **reverse order** to maintain consistency.
3. In production, each step would be an **HTTP/gRPC call** to a different microservice, and step states would be **persisted** (in a database) so the saga can resume after a crash.
4. Idempotency is critical: compensations might be retried, so they must be safe to re-execute.

</details>
