# LLD Case Studies

In LLD interviews, you will often be asked to design a specific system. Here are the most common ones.

> **Prerequisites:** [Design Patterns](./02-design-patterns.md)

## 1. Parking Lot Design
A classic interview question that tests your ability to handle hierarchy and state.

### Key Requirements
- Multiple levels, multiple spots per level.
- Support for different vehicle types (Motorcycle, Car, Bus).
- Parking spot sizes matching vehicle types.
- Payment calculation based on time.

### Class Diagram Sketch

```text
┌─────────────────┐          ┌─────────────────┐
│   ParkingLot    │          │      Level      │
├─────────────────┤          ├─────────────────┤
│ - levels: List  │ 1      * │ - floor: int    │
├─────────────────┤ <>─────> │ - spots: List   │
│ + park(Vehicle) │          └────────┬────────┘
└─────────────────┘                   │
                                      │ *
                                      ▼
┌─────────────────┐          ┌─────────────────┐
│     Vehicle     │          │   ParkingSpot   │
├─────────────────┤          ├─────────────────┤
│ - plate: string │          │ - spotId: int   │
│ - type: Enum    │ <──────> │ - size: Enum    │
└─────────────────┘          └─────────────────┘
```

- `ParkingLot` (Singleton): Central entry point.
- `Level`: Manages a collection of spots on a specific floor.
- `ParkingSpot`: Stores vehicle info and size constraints.
- `Vehicle` (Abstract): Base for `Car`, `Bus`, `Motorcycle`.
- `Ticket`: Tracks entry time and vehicle for payment.

### Implementation Logic (Python)
```python
class ParkingStrategy(ABC):
    @abstractmethod
    def find_spot(self, vehicle_type, levels): pass

class NearestFirstStrategy(ParkingStrategy):
    def find_spot(self, vehicle_type, levels):
        for level in levels:
            for spot in level.spots:
                if spot.is_available and spot.can_fit(vehicle_type):
                    return spot
        return None

class ParkingLot:
    def __init__(self, strategy: ParkingStrategy):
        self.levels = []
        self.strategy = strategy

    def find_and_park(self, vehicle):
        spot = self.strategy.find_spot(vehicle.type, self.levels)
        if spot:
            spot.park(vehicle)
            return Ticket(vehicle, spot)
        return None
```

### Schema Design (Relational)
- **Vehicles**: `id, license_plate, type_id`
- **ParkingSpots**: `id, level_id, size_id, is_occupied, current_vehicle_id`
- **Tickets**: `id, vehicle_id, spot_id, entry_time, exit_time, amount`

---

## 2. ATM Machine
Tests state management and transactional logic.

### Key Patterns
- **State Pattern**: The ATM behavior changes based on its internal state.
- **Chain of Responsibility**: For the bill dispenser.

```text
IdleState ──> HasCardState ──> PinEnteredState ──> TransactionState
  ^                                                    │
  └────────────────────────────────────────────────────┘
```

### Implementation Logic (Python)
```python
class ATMState(ABC):
    @abstractmethod
    def insert_card(self): pass
    @abstractmethod
    def enter_pin(self, pin): pass
    @abstractmethod
    def withdraw_cash(self, amount): pass

class CashDispenser(ABC):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    @abstractmethod
    def dispense(self, amount): pass

class Dollar100Dispenser(CashDispenser):
    def dispense(self, amount):
        num_bills = amount // 100
        remainder = amount % 100
        if num_bills > 0: print(f"Dispensing {num_bills} $100 bills")
        if remainder > 0 and self.next_handler:
            self.next_handler.dispense(remainder)
```

### Schema Design (Relational)
- **Accounts**: `id, account_number, balance, pin_hash, status`
- **Transactions**: `id, account_id, type (Withdraw/Deposit), amount, timestamp`
- **ATMMachine**: `id, location, status, current_cash_balance`

### Chain of Responsibility (Dispenser)
```text
[100$ Handler] ───> [50$ Handler] ───> [20$ Handler] ───> [10$ Handler]
      │                   │                  │                 │
 (Dispense X)        (Dispense Y)       (Dispense Z)      (Dispense W)
```

---

## 3. Movie Booking System (BookMyShow)
Tests handling of concurrency and seat selection.

### Key Entities
- `Cinema`: Represents the theater complex.
- `Movie`: Metadata about the film.
- `Show`: A specific movie at a specific time in a specific hall.
- `Booking`: Ties user, show, and seats together.

### Concurrency Challenge
How do you prevent two users from booking the same seat?
- **Optimistic Locking**: Use a version column in the DB.
- **Pessimistic Locking**: Lock the row in the DB during the transaction.
- **Distributed Lock**: Use Redis with a TTL (e.g., lock for 10 mins during checkout).

---

## Tips for Case Studies

## 4. Design a Vending Machine
Tests state management and handling of inventory/money.

### Key Considerations
- **Concurrency**: What if two people try to buy the last soda simultaneously?
- **Payment**: Support for coins, bills, and card.
- **Dispensing**: Handling out-of-stock or mechanical failure.

### State Transitions
- `Idle`: Waiting for money.
- `HasMoney`: Money inserted, waiting for selection.
- `Dispensing`: Releasing the product.
- `OutofOrder`: Technical fault or empty.

---

## 5. Design a Logging Library (like Log4j)
Tests Singleton, Factory, and Decorator patterns.

### Key Requirements
- Support multiple levels (INFO, DEBUG, ERROR).
- Support multiple destinations (Console, File, Remote Server).
- Custom formatting (JSON, Plaintext).

### How to Recognize What to Consider
- **Performance**: Logging shouldn't block the main application (Asynchronous logging using a Queue).
- **Extensibility**: How easy is it to add a "Slack" logger? (OCP).

---

## 6. Design a Splitwise (Expense Sharing)
Tests complex data relationships and transaction history.

### Key Entities
- `User`: Metadata and balance.
- `Group`: Collection of users.
- `Expense`: Amount, payer, and split strategy (Equal, Percentage, Exact).

### Strategy Pattern for Splitting
```python
class SplitStrategy(ABC):
    @abstractmethod
    def calculate_split(self, amount, users): pass

class EqualSplit(SplitStrategy):
    def calculate_split(self, amount, users):
        return {u: amount/len(users) for u in users}
```

---

## Tips for Case Studies: How to Recognize Considerations

| Question | Hidden Consideration | Pattern to Use |
|----------|----------------------|----------------|
| **Any "Machine" (ATM, Vending)** | Behavior changes by state | **State Pattern** |
| **Pricing/Discount/Splitting** | Algorithms change | **Strategy Pattern** |
| **Undo/Redo/Transactional** | Reverting actions | **Command Pattern** |
| **Notification/Feeds** | One-to-many updates | **Observer Pattern** |
| **Building complex objects** | Many optional fields | **Builder Pattern** |
| **Legacy Integration** | Incompatible APIs | **Adapter Pattern** |
| **Heavy Resource Loading** | Delaying execution | **Proxy Pattern** |
| **Workflow with variations** | Fixed steps, custom logic | **Template Method** |

1.  **Don't forget the API**: Define the public methods clearly (e.g., `park_vehicle(v)`, `checkout(ticket)`).
2.  **Concurrency**: Mention how you would handle two people trying to book the same seat (e.g., Row-level locking in DB, or Redis for distributed locking).
3.  **Extensibility**: If the interviewer asks "How do we add EV charging?", show where you would add the `ChargingStation` class and how it interacts with `ParkingSpot`.
