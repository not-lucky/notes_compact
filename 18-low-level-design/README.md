# Chapter 18: Low-Level Design (LLD)

Low-Level Design (LLD), also called Object-Oriented Design (OOD), is a critical part of technical interviews for SDE-1, SDE-2, and Senior roles. While DSA tests your ability to solve algorithmic problems efficiently, LLD tests your ability to **model real-world systems as clean, extensible, and maintainable code**. The focus is on class-level architecture — not distributed systems or infrastructure.

## Building Intuition

### What is LLD?

If High-Level Design (HLD) is about drawing the blueprints of a city (where the power plant goes, how traffic flows), Low-Level Design is about **the architecture of a single building** — where the rooms are, how the plumbing works, and ensuring the structure can be easily renovated without tearing down walls.

**Key distinction:** HLD answers *"which services exist and how do they communicate?"* — LLD answers *"inside one service, how are the classes structured and how do they collaborate?"*

In an LLD interview, you are expected to:
1.  **Gather Requirements**: Clarify the scope — what's in, what's out.
2.  **Define Entities**: Identify the main objects (nouns) and their attributes.
3.  **Establish Relationships**: How do these objects interact? (Composition, Inheritance, Association, etc.)
4.  **Apply Principles**: Use SOLID, DRY, KISS, and Design Patterns to make the code flexible and clean.
5.  **Write Code**: Translate the design into clean, modular, production-quality code.
6.  **Schema Design** *(if asked)*: Define how these entities map to database tables.

### The Mental Model: Class Diagram First

Don't start coding immediately. Sketch a Class Diagram to map out entities, their attributes, methods, and relationships. This is your blueprint.

**UML Relationship Notation Refresher:**
| Notation | Relationship | Meaning |
|----------|-------------|---------|
| `──────>` | Association | Uses / knows about |
| `<>────>` | Aggregation | Has, but can exist independently |
| `◆─────>` | Composition | Owns, lifecycle is tied together |
| `─ ─ ─ >` | Dependency | Uses temporarily (e.g., method parameter) |
| `───▷` | Inheritance | Is-a (solid line = extends) |
| `─ ─ ▷` | Realization | Implements an interface (dashed line) |

```text
┌─────────────────┐   composition   ┌─────────────────┐
│    ParkingLot    │                 │      Level      │
├─────────────────┤                 ├─────────────────┤
│ - name: str     │  1           *  │ - floor: int    │
│ - levels: List  │ ◆────────────>  │ - spots: List   │
├─────────────────┤                 ├─────────────────┤
│ + park(Vehicle) │                 │ + find_spot()   │
│ + unpark(ticket)│                 │ + available()   │
└─────────────────┘                 └─────────────────┘
                                           │
                                           │ 1     *
                                           ◆
                                    ┌──────┴──────────┐
                                    │   ParkingSpot   │
                                    ├─────────────────┤
                                    │ - id: int       │
                                    │ - size: SpotSize│
                                    │ - vehicle: Opt  │
                                    ├─────────────────┤
                                    │ + is_available()│
                                    │ + assign(v)     │
                                    └─────────────────┘
```

## Important Trade-offs

When working on Low-Level Design, consider these trade-offs:

1.  **Flexibility vs. Simplicity:** Applying many design patterns makes the code extensible but can also make it harder to read and understand (over-engineering). Use patterns to solve real problems, not to impress.
2.  **Inheritance vs. Composition:** Inheritance creates tight coupling and fragile hierarchies. Composition offers more flexibility at runtime. **Prefer composition over inheritance** — it's one of the most important OOD principles.
3.  **Performance vs. Clean Code:** Sometimes highly optimized code violates clean code principles. In LLD interviews, **prioritize clean, modular code** unless performance is explicitly a constraint.
4.  **Abstraction vs. Concreteness:** Too many interfaces/abstract classes add indirection; too few make the code rigid. Abstract where you expect variation (e.g., pricing strategies), keep things concrete where you don't.
5.  **DRY vs. Decoupling:** Merging similar code to avoid repetition can accidentally couple unrelated modules. It's okay to tolerate some duplication if it keeps modules independent.
6.  **Thread Safety vs. Complexity:** Adding locks and synchronization makes concurrent access safe but increases complexity and can hurt performance. Only introduce thread safety where shared mutable state is accessed concurrently — don't preemptively lock everything.

## Why This Matters for Interviews

1.  **Code Quality**: Interviewers want to see if you can write "production-ready" code — proper naming, separation of concerns, error handling.
2.  **Extensibility**: Can you add a new feature (e.g., "Add Electric Vehicle charging spots") without rewriting the whole system? This directly tests Open/Closed Principle.
3.  **Communication**: LLD tests how you translate vague, ambiguous requirements into concrete class structures. Asking clarifying questions is part of the evaluation.
4.  **Design Vocabulary**: Knowledge of Design Patterns shows you can communicate solutions using a shared vocabulary that experienced engineers understand.

---

## Core Topics

| Topic | Interview Relevance | Key Concepts |
|-------|-------------------|--------------|
| SOLID Principles | Fundamental | SRP, OCP, LSP, ISP, DIP |
| Design Patterns | Very Common | Singleton, Factory, Strategy, Observer, Decorator |
| UML & Class Diagrams | Common | Relationships (Association, Composition, Inheritance), Multiplicity |
| Schema Design | Common | Normalization, ER Diagrams, Indexing |
| Enums & Constants | Foundational | Using `Enum` for fixed categories (vehicle types, spot sizes, etc.) |
| Case Studies | Practical | Parking Lot, ATM, BookMyShow, Elevator System |

---

## Chapter Contents

| # | Topic | Key Concepts |
|---|-------|--------------|
| 01 | [SOLID Principles](./01-solid-principles.md) | The foundation of clean OOD — SRP, OCP, LSP, ISP, DIP |
| 02 | [Design Patterns](./02-design-patterns.md) | Creational, Structural, and Behavioral patterns |
| 03 | [Case Studies](./03-case-studies.md) | Applying LLD to real-world interview problems |

---

## The LLD Interview Framework (4 Steps)

### 1. Requirement Gathering (~5 mins)
- Define the scope — what is in, what is out.
- Ask clarifying questions. This is expected and evaluated.
- Example: "Does the Parking Lot support multiple floors?" "Are there different vehicle types?" "Do we need to track entry/exit time?"

### 2. Class Identification & Diagramming (~10 mins)
- Identify the **Nouns** → Entities: `Vehicle`, `ParkingSpot`, `Level`, `Ticket`.
- Identify the **Verbs** → Methods: `park_vehicle()`, `unpark_vehicle()`, `calculate_fee()`.
- Define relationships: Is-a (inheritance) vs. Has-a (composition/aggregation).
- Sketch a quick class diagram showing attributes, methods, and cardinality.

### 3. Design Principles & Patterns (~5 mins)
- Apply SOLID — especially SRP (one responsibility per class) and OCP (open for extension).
- Choose appropriate patterns (e.g., Strategy for pricing, Factory for vehicle creation, Observer for notifications).
- Justify your choices briefly to the interviewer.

### 4. Implementation (~20 mins)
- Write clean, modular code with proper type hints.
- Focus on interfaces and abstract classes to define contracts.
- Handle edge cases (e.g., lot full, invalid ticket).
- Use `Enum` for fixed categories.

```python
from abc import ABC, abstractmethod
from enum import Enum


# --- Step 1: Define enums for fixed categories ---

class VehicleType(Enum):
    """Fixed set of vehicle types the system supports."""
    MOTORCYCLE = "motorcycle"
    CAR = "car"
    BUS = "bus"


# --- Step 2: Strategy Pattern for flexible pricing ---

class PricingStrategy(ABC):
    """Abstract base class for pricing strategies.

    Using the Strategy pattern allows us to swap pricing logic
    at runtime without modifying the Ticket class (Open/Closed Principle).
    """

    @abstractmethod
    def calculate_price(self, hours: int) -> float:
        """Calculate the parking fee for the given duration."""
        ...


class HourlyPricing(PricingStrategy):
    """Charges a flat rate per hour."""

    def __init__(self, rate_per_hour: float = 10.0) -> None:
        self.rate_per_hour = rate_per_hour

    def calculate_price(self, hours: int) -> float:
        return hours * self.rate_per_hour


class DailyPricing(PricingStrategy):
    """Charges a flat rate per day (any partial day counts as a full day)."""

    def __init__(self, rate_per_day: float = 100.0) -> None:
        self.rate_per_day = rate_per_day

    def calculate_price(self, hours: int) -> float:
        # Ceiling division: 25 hours → 2 days, 24 hours → 1 day
        days: int = (hours + 23) // 24
        return days * self.rate_per_day


# --- Step 3: Core entities ---

class Ticket:
    """Represents a parking ticket issued to a vehicle.

    The ticket holds the duration and delegates price calculation
    to a PricingStrategy (composition over inheritance).
    """

    def __init__(
        self,
        ticket_id: int,
        hours: int,
        vehicle_type: VehicleType,
        pricing_strategy: PricingStrategy,
    ) -> None:
        self.ticket_id = ticket_id
        self.hours = hours
        self.vehicle_type = vehicle_type
        self._pricing_strategy = pricing_strategy

    def get_price(self) -> float:
        """Delegate pricing to the strategy."""
        return self._pricing_strategy.calculate_price(self.hours)

    def __repr__(self) -> str:
        return (
            f"Ticket(id={self.ticket_id}, vehicle={self.vehicle_type.value}, "
            f"hours={self.hours}, price={self.get_price():.2f})"
        )


# --- Example usage ---

if __name__ == "__main__":
    ticket1 = Ticket(
        ticket_id=1, hours=5,
        vehicle_type=VehicleType.CAR,
        pricing_strategy=HourlyPricing(),
    )
    print(f"Hourly price: ${ticket1.get_price():.2f}")  # $50.00

    ticket2 = Ticket(
        ticket_id=2, hours=26,
        vehicle_type=VehicleType.CAR,
        pricing_strategy=DailyPricing(),
    )
    print(f"Daily price: ${ticket2.get_price():.2f}")   # $200.00

    # Easy to extend: add a new strategy without changing existing code
    ticket3 = Ticket(
        ticket_id=3, hours=3,
        vehicle_type=VehicleType.MOTORCYCLE,
        pricing_strategy=HourlyPricing(rate_per_hour=5.0),  # discounted rate
    )
    print(f"Motorcycle price: ${ticket3.get_price():.2f}")  # $15.00
```

> **Key takeaway:** Notice how adding a new pricing strategy (e.g., `WeekendPricing`) requires **zero changes** to the `Ticket` class. This is the Open/Closed Principle in action — open for extension, closed for modification.

---

## Common Mistakes in LLD Interviews

1.  **Jumping straight to code** without clarifying requirements or sketching a class diagram. Interviewers explicitly evaluate your design process, not just the final code.
2.  **Over-engineering:** Applying every design pattern you know. Use patterns to solve *actual* problems in the design, not to show off.
3.  **God classes:** Putting all logic in one class (e.g., a `ParkingLot` that handles parking, pricing, ticketing, and notifications). Violates SRP.
4.  **Ignoring edge cases:** Not handling scenarios like "lot is full," "invalid ticket," or "duplicate booking." Mentioning these shows production-level thinking.
5.  **Using inheritance where composition is better:** Creating deep class hierarchies instead of composing behavior via interfaces and delegation.
6.  **Hardcoding values:** Using magic numbers or strings instead of enums and constants. Makes the code fragile and hard to extend.

---

## Next Steps

Start with the [SOLID Principles](./01-solid-principles.md) to understand the **"Why"** behind good design — every pattern and practice in LLD traces back to these five principles.
