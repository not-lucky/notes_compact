# Chapter 18: Low-Level Design (LLD)

Low-Level Design (LLD) or Object-Oriented Design (OOD) is a critical part of technical interviews for SDE-1, SDE-2, and Senior roles. While DSA focuses on algorithms, LLD focuses on **class structure, code quality, and maintainability**.

## Building Intuition

### What is LLD?

If High-Level Design (HLD) is about drawing the blueprints of a city (where the power plant goes, how traffic flows), Low-Level Design is about **the architecture of a single building** (where the rooms are, how the plumbing works, and ensuring the structure can be easily renovated).

In an LLD interview, you are expected to:
1.  **Gather Requirements**: Clarify the scope of the problem.
2.  **Define Entities**: Identify the main objects and their attributes.
3.  **Establish Relationships**: How do these objects interact? (Composition, Inheritance, etc.)
4.  **Apply Principles**: Use SOLID, DRY, and Design Patterns to make the code flexible.
5.  **Schema Design**: Define how these entities map to a database.

### The Mental Model: Class Diagram First

Don't start coding immediately. Think in terms of a Class Diagram.

```text
┌─────────────────┐          ┌─────────────────┐
│     ParkingLot  │          │      Level      │
├─────────────────┤          ├─────────────────┤
│ - levels: List  │ 1      * │ - spots: List   │
├─────────────────┤ <>─────> ├─────────────────┤
│ + park(Vehicle) │          │ + findSpot()    │
└─────────────────┘          └─────────────────┘
```

## Important Trade-offs

When working on Low-Level Design, consider these trade-offs:

1.  **Flexibility vs. Simplicity:** Applying many design patterns makes the code extensible but can also make it harder to read and understand (over-engineering).
2.  **Inheritance vs. Composition:** Inheritance creates tight coupling, while composition offers more flexibility at runtime. Prefer composition over inheritance.
3.  **Performance vs. Clean Code:** Sometimes highly optimized code violates clean code principles. In LLD interviews, prioritize clean, modular code unless performance is explicitly a constraint.

## Why This Matters for Interviews

1.  **Code Quality**: Interviewers want to see if you can write "production-ready" code.
2.  **Extensibility**: Can you add a new feature (e.g., "Add Electric Vehicle charging") without rewriting the whole system?
3.  **Communication**: LLD tests how you translate vague requirements into concrete structures.
4.  **Standardization**: Knowledge of Design Patterns shows you speak the same language as experienced engineers.

---

## Core Topics

| Topic | Interview Relevance | Key Concepts |
|-------|-------------------|--------------|
| SOLID Principles | Fundamental | SRP, OCP, LSP, ISP, DIP |
| Design Patterns | Very Common | Singleton, Factory, Strategy, Observer |
| Schema Design | Common | Normalization, ER Diagrams, indexing |
| Case Studies | Practical | Parking Lot, ATM, BookMyShow |

---

## Chapter Contents

| # | Topic | Key Concepts |
|---|-------|--------------|
| 01 | [SOLID Principles](./01-solid-principles.md) | The foundation of clean OOD |
| 02 | [Design Patterns](./02-design-patterns.md) | Creational, Structural, and Behavioral patterns |
| 03 | [Case Studies](./03-case-studies.md) | Applying LLD to real-world problems |

---

## The LLD Interview Framework (4 Steps)

### 1. Requirement Gathering (5-10 mins)
- Define the scope (What is in? What is out?).
- Example: "Does the Parking Lot support multiple floors?" "Are there different vehicle types?"

### 2. Class Identification & Diagramming (10-15 mins)
- Identify the **Nouns** (Entities: Vehicle, ParkingSpot, Level).
- Identify the **Verbs** (Methods: parkVehicle, unparkVehicle, calculateFee).
- Define relationships (Is-a vs. Has-a).

### 3. Design Principles & Patterns (5-10 mins)
- Apply SOLID.
- Choose appropriate patterns (e.g., Strategy for pricing, Factory for vehicle creation).

### 4. Implementation (15-20 mins)
- Write clean, modular code.
- Focus on interfaces and abstract classes.

```python
from abc import ABC, abstractmethod
from typing import List

# Example: Strategy Pattern for Pricing in a Parking Lot
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, hours: int) -> float:
        pass

class HourlyPricing(PricingStrategy):
    def calculate_price(self, hours: int) -> float:
        return hours * 10.0

class DailyPricing(PricingStrategy):
    def calculate_price(self, hours: int) -> float:
        days = (hours + 23) // 24
        return days * 100.0

class Ticket:
    def __init__(self, hours: int, pricing_strategy: PricingStrategy):
        self.hours = hours
        self.pricing_strategy = pricing_strategy

    def get_price(self) -> float:
        return self.pricing_strategy.calculate_price(self.hours)

# Example usage
ticket1 = Ticket(5, HourlyPricing())
print(f"Hourly price: ${ticket1.get_price()}") # $50.0

ticket2 = Ticket(26, DailyPricing())
print(f"Daily price: ${ticket2.get_price()}")   # $200.0
```

---

## Next Steps

Start with the [SOLID Principles](./01-solid-principles.md) to understand the "Why" behind good design.
