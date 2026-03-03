# LLD Case Studies

In LLD interviews, you will often be asked to design a specific system. Here are the most common ones with complete, runnable implementations. Each case study highlights the key design patterns and decisions that interviewers are looking for.

> **Prerequisites:** [Design Patterns](./02-design-patterns.md)

## 1. Parking Lot Design
A classic interview question that tests your ability to model hierarchy, state, and extensibility.

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

### Implementation (Python)
```python
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from typing import Optional

# --- Enums ---
class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    BUS = 3

class SpotSize(Enum):
    SMALL = 1   # fits motorcycle
    MEDIUM = 2  # fits car
    LARGE = 3   # fits bus

# Map vehicle types to minimum required spot size
VEHICLE_TO_SPOT: dict[VehicleType, SpotSize] = {
    VehicleType.MOTORCYCLE: SpotSize.SMALL,
    VehicleType.CAR: SpotSize.MEDIUM,
    VehicleType.BUS: SpotSize.LARGE,
}

# --- Vehicle Hierarchy (Abstraction) ---
class Vehicle(ABC):
    """Abstract base for all vehicle types."""
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.type = vehicle_type

    def __repr__(self) -> str:
        return f"{self.type.name}({self.license_plate})"

class Motorcycle(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.MOTORCYCLE)

class Car(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.CAR)

class Bus(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.BUS)

# --- Parking Spot ---
class ParkingSpot:
    def __init__(self, spot_id: int, size: SpotSize):
        self.spot_id = spot_id
        self.size = size
        self.vehicle: Optional[Vehicle] = None

    @property
    def is_available(self) -> bool:
        return self.vehicle is None

    def can_fit(self, vehicle_type: VehicleType) -> bool:
        """A spot can fit a vehicle if the spot size >= required size."""
        return self.size.value >= VEHICLE_TO_SPOT[vehicle_type].value

    def park(self, vehicle: Vehicle) -> None:
        if not self.is_available:
            raise ValueError(f"Spot {self.spot_id} is already occupied")
        if not self.can_fit(vehicle.type):
            raise ValueError(f"Spot {self.spot_id} too small for {vehicle.type.name}")
        self.vehicle = vehicle

    def remove_vehicle(self) -> Optional[Vehicle]:
        v = self.vehicle
        self.vehicle = None
        return v

# --- Ticket ---
class Ticket:
    _counter = 0

    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        Ticket._counter += 1
        self.ticket_id = Ticket._counter
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.now()
        self.exit_time: Optional[datetime] = None

    def close(self) -> float:
        """Close ticket and return hours parked."""
        self.exit_time = datetime.now()
        delta = (self.exit_time - self.entry_time).total_seconds()
        return max(delta / 3600, 0.1)  # minimum 0.1 hr

# --- Level ---
class Level:
    def __init__(self, floor: int, num_spots: int):
        self.floor = floor
        # Mix of spot sizes: 20% small, 60% medium, 20% large
        self.spots: list[ParkingSpot] = []
        for i in range(num_spots):
            if i < num_spots * 0.2:
                size = SpotSize.SMALL
            elif i < num_spots * 0.8:
                size = SpotSize.MEDIUM
            else:
                size = SpotSize.LARGE
            self.spots.append(ParkingSpot(spot_id=floor * 100 + i, size=size))

    def available_spots(self) -> int:
        return sum(1 for s in self.spots if s.is_available)

# --- Strategy Pattern for spot finding ---
class ParkingStrategy(ABC):
    @abstractmethod
    def find_spot(self, vehicle_type: VehicleType,
                  levels: list[Level]) -> Optional[ParkingSpot]:
        pass

class NearestFirstStrategy(ParkingStrategy):
    """Find the first available spot starting from the lowest level."""
    def find_spot(self, vehicle_type: VehicleType,
                  levels: list[Level]) -> Optional[ParkingSpot]:
        for level in levels:
            for spot in level.spots:
                if spot.is_available and spot.can_fit(vehicle_type):
                    return spot
        return None

# --- Parking Lot (Singleton) ---
class ParkingLot:
    """
    Singleton parking lot that delegates spot-finding to a strategy.
    Design patterns used: Singleton, Strategy.
    """
    _instance: Optional["ParkingLot"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, num_levels: int = 3, spots_per_level: int = 20,
                 strategy: Optional[ParkingStrategy] = None):
        # Guard against re-initialization — __init__ runs every time
        # __new__ returns the existing instance
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        self.levels = [Level(i, spots_per_level) for i in range(num_levels)]
        self.strategy = strategy or NearestFirstStrategy()
        self.active_tickets: dict[int, Ticket] = {}
        self.hourly_rate: float = 5.0

    def park_vehicle(self, vehicle: Vehicle) -> Optional[Ticket]:
        spot = self.strategy.find_spot(vehicle.type, self.levels)
        if spot is None:
            return None  # lot full for this vehicle type
        spot.park(vehicle)
        ticket = Ticket(vehicle, spot)
        self.active_tickets[ticket.ticket_id] = ticket
        return ticket

    def checkout(self, ticket_id: int) -> float:
        """Remove vehicle and return amount owed."""
        ticket = self.active_tickets.pop(ticket_id, None)
        if ticket is None:
            raise ValueError(f"Ticket {ticket_id} not found")
        hours = ticket.close()
        ticket.spot.remove_vehicle()
        return round(hours * self.hourly_rate, 2)

# --- Usage ---
# lot = ParkingLot(num_levels=3, spots_per_level=20)
# ticket = lot.park_vehicle(Car("ABC-123"))
# amount = lot.checkout(ticket.ticket_id)
```

### Schema Design (Relational)
- **Vehicles**: `id, license_plate, type_id`
- **ParkingSpots**: `id, level_id, size_id, is_occupied, current_vehicle_id`
- **Tickets**: `id, vehicle_id, spot_id, entry_time, exit_time, amount`

---

## 2. ATM Machine
Tests state management and transactional logic. A great example of how the State pattern eliminates complex `if/else` chains.

### Key Patterns
- **State Pattern**: ATM behavior changes based on its internal state (idle, card inserted, PIN verified). Each state class defines valid/invalid operations — invalid ones raise errors instead of silently failing.
- **Chain of Responsibility**: The cash dispenser chain breaks a withdrawal into denominations. Each handler processes what it can and passes the remainder to the next.

```text
IdleState ──> HasCardState ──> PinVerifiedState ──> (Withdraw) ──> IdleState
  ^                                                                   │
  └───────────────────── (Eject Card) ────────────────────────────────┘
```

### Implementation (Python)
```python
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

# --- State Pattern: ATM States ---
class ATMState(ABC):
    """
    Each state defines what actions are valid. Invalid actions raise errors.
    Design patterns used: State, Chain of Responsibility.
    """
    def __init__(self, atm: "ATM"):
        self.atm = atm

    @abstractmethod
    def insert_card(self, card_number: str) -> None: pass
    @abstractmethod
    def enter_pin(self, pin: str) -> None: pass
    @abstractmethod
    def withdraw_cash(self, amount: int) -> None: pass
    @abstractmethod
    def eject_card(self) -> None: pass

class IdleState(ATMState):
    """Waiting for a card to be inserted."""
    def insert_card(self, card_number: str) -> None:
        print(f"Card {card_number} inserted.")
        self.atm.current_card = card_number
        self.atm.set_state(HasCardState(self.atm))

    def enter_pin(self, pin: str) -> None:
        raise RuntimeError("Insert a card first.")

    def withdraw_cash(self, amount: int) -> None:
        raise RuntimeError("Insert a card first.")

    def eject_card(self) -> None:
        raise RuntimeError("No card inserted.")

class HasCardState(ATMState):
    """Card is inserted, waiting for PIN."""
    def insert_card(self, card_number: str) -> None:
        raise RuntimeError("Card already inserted.")

    def enter_pin(self, pin: str) -> None:
        if self.atm.bank.verify_pin(self.atm.current_card, pin):
            print("PIN verified.")
            self.atm.set_state(PinVerifiedState(self.atm))
        else:
            print("Incorrect PIN. Ejecting card.")
            self.atm.eject_card()

    def withdraw_cash(self, amount: int) -> None:
        raise RuntimeError("Enter PIN first.")

    def eject_card(self) -> None:
        print("Card ejected.")
        self.atm.current_card = None
        self.atm.set_state(IdleState(self.atm))

class PinVerifiedState(ATMState):
    """PIN verified, user can perform transactions."""
    def insert_card(self, card_number: str) -> None:
        raise RuntimeError("Card already inserted.")

    def enter_pin(self, pin: str) -> None:
        raise RuntimeError("PIN already entered.")

    def withdraw_cash(self, amount: int) -> None:
        if self.atm.bank.has_sufficient_funds(self.atm.current_card, amount):
            if self.atm.cash_available >= amount:
                self.atm.bank.debit(self.atm.current_card, amount)
                self.atm.dispenser.dispense(amount)
                self.atm.cash_available -= amount
                print(f"Withdrew ${amount}. Please take your cash.")
            else:
                print("ATM has insufficient cash.")
        else:
            print("Insufficient funds in account.")
        # Return to idle after transaction
        self.atm.eject_card()

    def eject_card(self) -> None:
        print("Card ejected.")
        self.atm.current_card = None
        self.atm.set_state(IdleState(self.atm))

# --- Chain of Responsibility: Cash Dispensing ---
class CashDispenser:
    """Each handler tries to dispense its denomination, then passes remainder to next."""
    def __init__(self, denomination: int, next_handler: Optional["CashDispenser"] = None):
        self.denomination = denomination
        self.next_handler = next_handler

    def dispense(self, amount: int) -> None:
        num_bills = amount // self.denomination
        remainder = amount % self.denomination
        if num_bills > 0:
            print(f"  Dispensing {num_bills} x ${self.denomination}")
        if remainder > 0 and self.next_handler:
            self.next_handler.dispense(remainder)
        elif remainder > 0:
            print(f"  Cannot dispense remaining ${remainder}")

# --- Stub Bank Service ---
class BankService:
    """Simulates bank account operations (stub for demo)."""
    def __init__(self):
        self.accounts: dict[str, dict] = {
            "1234-5678": {"pin": "1111", "balance": 5000},
        }

    def verify_pin(self, card: str, pin: str) -> bool:
        return self.accounts.get(card, {}).get("pin") == pin

    def has_sufficient_funds(self, card: str, amount: int) -> bool:
        return self.accounts.get(card, {}).get("balance", 0) >= amount

    def debit(self, card: str, amount: int) -> None:
        self.accounts[card]["balance"] -= amount

# --- ATM Machine ---
class ATM:
    """Main ATM class — delegates behavior to current state."""
    def __init__(self, cash: int = 10000):
        self.bank = BankService()
        self.cash_available = cash
        self.current_card: Optional[str] = None
        # Build dispenser chain: $100 -> $50 -> $20 -> $10
        self.dispenser = CashDispenser(100,
            CashDispenser(50,
                CashDispenser(20,
                    CashDispenser(10))))
        self._state: ATMState = IdleState(self)

    def set_state(self, state: ATMState) -> None:
        self._state = state

    def insert_card(self, card_number: str) -> None:
        self._state.insert_card(card_number)

    def enter_pin(self, pin: str) -> None:
        self._state.enter_pin(pin)

    def withdraw_cash(self, amount: int) -> None:
        self._state.withdraw_cash(amount)

    def eject_card(self) -> None:
        self._state.eject_card()

# --- Usage ---
# atm = ATM(cash=10000)
# atm.insert_card("1234-5678")
# atm.enter_pin("1111")
# atm.withdraw_cash(270)  # Dispenses 2x$100 + 1x$50 + 1x$20
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
How do you prevent two users from booking the same seat? This is the core challenge.
- **Optimistic Locking**: Use a version column in the DB. If the version changed between read and write, retry. Best when conflicts are rare.
- **Pessimistic Locking**: Lock the row in the DB during the transaction (`SELECT ... FOR UPDATE`). Best when conflicts are frequent.
- **Distributed Lock**: Use Redis with a TTL (e.g., lock seat for 10 mins during checkout). Best for microservice architectures.

### Implementation (Python)
```python
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import threading

class SeatType(Enum):
    REGULAR = 1
    PREMIUM = 2
    VIP = 3

class SeatStatus(Enum):
    AVAILABLE = 1
    TEMPORARILY_HELD = 2  # user is in checkout
    BOOKED = 3

class BookingStatus(Enum):
    PENDING = 1
    CONFIRMED = 2
    CANCELLED = 3

@dataclass
class Movie:
    movie_id: int
    title: str
    duration_mins: int
    genre: str

@dataclass
class Seat:
    seat_id: str          # e.g. "A1", "B5"
    seat_type: SeatType
    price: float
    status: SeatStatus = SeatStatus.AVAILABLE
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def hold(self) -> bool:
        """Attempt to temporarily hold seat (thread-safe)."""
        with self._lock:
            if self.status == SeatStatus.AVAILABLE:
                self.status = SeatStatus.TEMPORARILY_HELD
                return True
            return False

    def confirm(self) -> None:
        """Transition from HELD to BOOKED (only valid from HELD state)."""
        with self._lock:
            if self.status != SeatStatus.TEMPORARILY_HELD:
                raise ValueError(f"Cannot confirm seat {self.seat_id} in {self.status.name} state")
            self.status = SeatStatus.BOOKED

    def release(self) -> None:
        """Release a held seat back to available."""
        with self._lock:
            if self.status == SeatStatus.TEMPORARILY_HELD:
                self.status = SeatStatus.AVAILABLE

@dataclass
class Screen:
    screen_id: int
    name: str
    seats: list[Seat]

@dataclass
class Show:
    show_id: int
    movie: Movie
    screen: Screen
    start_time: datetime
    price_multiplier: float = 1.0  # weekends/holidays cost more

    def get_available_seats(self) -> list[Seat]:
        return [s for s in self.screen.seats if s.status == SeatStatus.AVAILABLE]

@dataclass
class Cinema:
    cinema_id: int
    name: str
    city: str
    screens: list[Screen]

class Booking:
    _counter = 0

    def __init__(self, user_id: int, show: Show, seats: list[Seat]):
        Booking._counter += 1
        self.booking_id = Booking._counter
        self.user_id = user_id
        self.show = show
        self.seats = seats
        self.status = BookingStatus.PENDING
        self.total_amount = sum(
            s.price * show.price_multiplier for s in seats
        )
        self.created_at = datetime.now()

    def confirm_payment(self) -> None:
        for seat in self.seats:
            seat.confirm()
        self.status = BookingStatus.CONFIRMED

    def cancel(self) -> None:
        for seat in self.seats:
            seat.release()
        self.status = BookingStatus.CANCELLED

# --- Booking Service (handles concurrency) ---
class BookingService:
    """
    Central service that coordinates seat selection and booking.
    Uses per-seat locking to handle concurrent booking attempts.
    Design patterns: Facade (simple API), per-seat Lock (concurrency).
    """
    def __init__(self):
        self.bookings: dict[int, Booking] = {}

    def book_seats(self, user_id: int, show: Show,
                   seat_ids: list[str]) -> Optional[Booking]:
        """
        Attempt to book specific seats. Returns Booking if all seats
        are available, None if any seat is taken.
        """
        target_seats = [s for s in show.screen.seats if s.seat_id in seat_ids]
        if len(target_seats) != len(seat_ids):
            raise ValueError("One or more seat IDs not found")

        # Try to hold all requested seats. Per-seat locks ensure each
        # hold() is thread-safe. If any seat is taken, we rollback all
        # previously held seats. Note: this is not globally atomic —
        # in production, use a DB transaction or distributed lock.
        held: list[Seat] = []
        for seat in target_seats:
            if seat.hold():
                held.append(seat)
            else:
                # Rollback: release any seats we already held
                for s in held:
                    s.release()
                return None  # seat was taken by another user

        booking = Booking(user_id, show, held)
        self.bookings[booking.booking_id] = booking
        return booking

# --- Usage ---
# movie = Movie(1, "Inception", 148, "Sci-Fi")
# seats = [Seat(f"A{i}", SeatType.REGULAR, 12.0) for i in range(1, 11)]
# screen = Screen(1, "Screen 1", seats)
# show = Show(1, movie, screen, datetime(2026, 3, 1, 19, 0))
# service = BookingService()
# booking = service.book_seats(user_id=42, show=show, seat_ids=["A1", "A2"])
# booking.confirm_payment()
```

---

## 4. Design a Vending Machine
Tests state management and handling of inventory/money. Similar to ATM but with inventory tracking and change calculation.

### Key Considerations
- **Concurrency**: What if two people try to buy the last soda simultaneously?
- **Payment**: Support for coins, bills, and card.
- **Dispensing**: Handling out-of-stock or mechanical failure.

### State Transitions
- `Idle`: Waiting for money.
- `HasMoney`: Money inserted, waiting for selection.
- `Dispensing`: Releasing the product.
- `OutOfOrder`: Technical fault or empty.

### Implementation (Python)
```python
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class Product(Enum):
    COLA = "Cola"
    CHIPS = "Chips"
    WATER = "Water"
    CANDY = "Candy"

@dataclass
class Item:
    product: Product
    price: float
    quantity: int

# --- State Pattern ---
class VendingState(ABC):
    """
    Each state controls what operations are valid.
    Design patterns used: State, Singleton (machine instance).
    """
    def __init__(self, machine: "VendingMachine"):
        self.machine = machine

    @abstractmethod
    def insert_money(self, amount: float) -> None: pass
    @abstractmethod
    def select_product(self, product: Product) -> None: pass
    @abstractmethod
    def dispense(self) -> None: pass
    @abstractmethod
    def cancel(self) -> float: pass

class IdleState(VendingState):
    """No money inserted yet."""
    def insert_money(self, amount: float) -> None:
        self.machine.balance += amount
        print(f"Inserted ${amount:.2f}. Balance: ${self.machine.balance:.2f}")
        self.machine.set_state(HasMoneyState(self.machine))

    def select_product(self, product: Product) -> None:
        raise RuntimeError("Insert money first.")

    def dispense(self) -> None:
        raise RuntimeError("Insert money first.")

    def cancel(self) -> float:
        print("Nothing to cancel.")
        return 0.0

class HasMoneyState(VendingState):
    """Money inserted, waiting for product selection."""
    def insert_money(self, amount: float) -> None:
        self.machine.balance += amount
        print(f"Added ${amount:.2f}. Balance: ${self.machine.balance:.2f}")

    def select_product(self, product: Product) -> None:
        item = self.machine.inventory.get(product)
        if item is None or item.quantity == 0:
            print(f"{product.value} is out of stock.")
            return
        if self.machine.balance < item.price:
            print(f"Insufficient funds. Need ${item.price:.2f}, "
                  f"have ${self.machine.balance:.2f}")
            return
        self.machine.selected = product
        self.machine.set_state(DispensingState(self.machine))
        self.machine.state.dispense()

    def dispense(self) -> None:
        raise RuntimeError("Select a product first.")

    def cancel(self) -> float:
        refund = self.machine.balance
        self.machine.balance = 0.0
        self.machine.set_state(IdleState(self.machine))
        print(f"Cancelled. Refunding ${refund:.2f}")
        return refund

class DispensingState(VendingState):
    """Dispensing selected product."""
    def insert_money(self, amount: float) -> None:
        raise RuntimeError("Currently dispensing. Please wait.")

    def select_product(self, product: Product) -> None:
        raise RuntimeError("Currently dispensing. Please wait.")

    def dispense(self) -> None:
        product = self.machine.selected
        item = self.machine.inventory[product]
        item.quantity -= 1
        self.machine.balance -= item.price
        change = self.machine.balance
        self.machine.balance = 0.0
        self.machine.selected = None
        print(f"Dispensed {product.value}. Change: ${change:.2f}")
        self.machine.set_state(IdleState(self.machine))

    def cancel(self) -> float:
        raise RuntimeError("Cannot cancel during dispensing.")

class OutOfOrderState(VendingState):
    """Machine is broken or completely empty."""
    def insert_money(self, amount: float) -> None:
        raise RuntimeError("Machine is out of order.")

    def select_product(self, product: Product) -> None:
        raise RuntimeError("Machine is out of order.")

    def dispense(self) -> None:
        raise RuntimeError("Machine is out of order.")

    def cancel(self) -> float:
        raise RuntimeError("Machine is out of order.")

# --- Vending Machine ---
class VendingMachine:
    def __init__(self):
        self.inventory: dict[Product, Item] = {}
        self.balance: float = 0.0
        self.selected: Optional[Product] = None
        self.state: VendingState = IdleState(self)

    def set_state(self, state: VendingState) -> None:
        self.state = state

    def stock(self, product: Product, price: float, quantity: int) -> None:
        self.inventory[product] = Item(product, price, quantity)

    def insert_money(self, amount: float) -> None:
        self.state.insert_money(amount)

    def select_product(self, product: Product) -> None:
        self.state.select_product(product)

    def cancel(self) -> float:
        return self.state.cancel()

# --- Usage ---
# vm = VendingMachine()
# vm.stock(Product.COLA, 1.50, 10)
# vm.stock(Product.CHIPS, 2.00, 5)
# vm.insert_money(2.00)
# vm.select_product(Product.COLA)  # Dispensed Cola. Change: $0.50
```

---

## 5. Design a Logging Library (like Log4j)
Tests Singleton, Factory, and Strategy patterns.

### Key Requirements
- Support multiple levels (INFO, DEBUG, WARN, ERROR).
- Support multiple destinations (Console, File, Remote Server).
- Custom formatting (JSON, Plaintext).

### How to Recognize What to Consider
- **Performance**: Logging shouldn't block the main application. In production, use an async queue between the logger and handlers. This implementation is synchronous for clarity.
- **Extensibility**: How easy is it to add a "Slack" logger? Just add a new `LogHandler` subclass — no existing code changes needed (Open/Closed Principle).

### Implementation (Python)
```python
from abc import ABC, abstractmethod
from enum import IntEnum
from datetime import datetime
from typing import Optional
import threading
import json

# --- Log Levels (IntEnum so levels are comparable) ---
class LogLevel(IntEnum):
    DEBUG = 10
    INFO = 20
    WARN = 30
    ERROR = 40

# --- Formatter Strategy ---
class LogFormatter(ABC):
    """Strategy pattern: swap formatting without changing handlers."""
    @abstractmethod
    def format(self, level: LogLevel, message: str,
               timestamp: datetime) -> str:
        pass

class PlainTextFormatter(LogFormatter):
    def format(self, level: LogLevel, message: str,
               timestamp: datetime) -> str:
        ts = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"[{ts}] [{level.name}] {message}"

class JsonFormatter(LogFormatter):
    def format(self, level: LogLevel, message: str,
               timestamp: datetime) -> str:
        return json.dumps({
            "timestamp": timestamp.isoformat(),
            "level": level.name,
            "message": message,
        })

# --- Handler (Observer-like: logger notifies handlers) ---
class LogHandler(ABC):
    """Each handler writes logs to a destination."""
    def __init__(self, min_level: LogLevel = LogLevel.DEBUG,
                 formatter: Optional[LogFormatter] = None):
        self.min_level = min_level
        self.formatter = formatter or PlainTextFormatter()

    def handle(self, level: LogLevel, message: str,
               timestamp: datetime) -> None:
        if level >= self.min_level:
            formatted = self.formatter.format(level, message, timestamp)
            self.emit(formatted)

    @abstractmethod
    def emit(self, formatted_message: str) -> None:
        pass

class ConsoleHandler(LogHandler):
    def emit(self, formatted_message: str) -> None:
        print(formatted_message)

class FileHandler(LogHandler):
    def __init__(self, filepath: str, **kwargs):
        super().__init__(**kwargs)
        self.filepath = filepath

    def emit(self, formatted_message: str) -> None:
        with open(self.filepath, "a") as f:
            f.write(formatted_message + "\n")

# Easy to extend: just add a new handler class (OCP)
# class SlackHandler(LogHandler):
#     def emit(self, formatted_message: str) -> None:
#         slack_client.post(channel, formatted_message)

# --- Logger (Singleton, thread-safe) ---
class Logger:
    """
    Singleton logger with pluggable handlers and formatters.
    Design patterns: Singleton, Strategy (formatters), Observer (handlers).
    """
    _instance: Optional["Logger"] = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # double-checked locking
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        self._handlers: list[LogHandler] = []

    def add_handler(self, handler: LogHandler) -> None:
        self._handlers.append(handler)

    def _log(self, level: LogLevel, message: str) -> None:
        now = datetime.now()
        for handler in self._handlers:
            handler.handle(level, message, now)

    def debug(self, message: str) -> None:
        self._log(LogLevel.DEBUG, message)

    def info(self, message: str) -> None:
        self._log(LogLevel.INFO, message)

    def warn(self, message: str) -> None:
        self._log(LogLevel.WARN, message)

    def error(self, message: str) -> None:
        self._log(LogLevel.ERROR, message)

# --- Usage ---
# logger = Logger()
# logger.add_handler(ConsoleHandler(min_level=LogLevel.DEBUG))
# logger.add_handler(FileHandler("app.log", min_level=LogLevel.ERROR,
#                                formatter=JsonFormatter()))
# logger.info("Server started")       # -> console only
# logger.error("Connection failed")   # -> console AND file (as JSON)
```

---

## 6. Design Splitwise (Expense Sharing)
Tests complex data relationships, strategy pattern, and balance tracking. The key challenge is correctly tracking who owes whom across many transactions.

### Key Entities
- `User`: Metadata and balance.
- `Group`: Collection of users.
- `Expense`: Amount, payer, and split strategy (Equal, Percentage, Exact).

### Implementation (Python)
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from collections import defaultdict

class SplitType(Enum):
    EQUAL = "equal"
    EXACT = "exact"
    PERCENTAGE = "percentage"

@dataclass
class User:
    user_id: int
    name: str
    email: str

# --- Strategy Pattern for split calculation ---
class SplitStrategy(ABC):
    @abstractmethod
    def calculate_split(self, amount: float,
                        users: list[User],
                        params: Optional[dict] = None) -> dict[int, float]:
        """Returns {user_id: amount_owed}."""
        pass

class EqualSplit(SplitStrategy):
    def calculate_split(self, amount: float, users: list[User],
                        params: Optional[dict] = None) -> dict[int, float]:
        per_person = round(amount / len(users), 2)
        return {u.user_id: per_person for u in users}

class ExactSplit(SplitStrategy):
    def calculate_split(self, amount: float, users: list[User],
                        params: Optional[dict] = None) -> dict[int, float]:
        """params = {user_id: exact_amount}"""
        if params is None:
            raise ValueError("ExactSplit requires exact amounts per user")
        total = sum(params.values())
        if abs(total - amount) > 0.01:
            raise ValueError(
                f"Exact amounts ({total}) don't sum to total ({amount})")
        return params

class PercentageSplit(SplitStrategy):
    def calculate_split(self, amount: float, users: list[User],
                        params: Optional[dict] = None) -> dict[int, float]:
        """params = {user_id: percentage}"""
        if params is None:
            raise ValueError("PercentageSplit requires percentages per user")
        total_pct = sum(params.values())
        if abs(total_pct - 100.0) > 0.01:
            raise ValueError(f"Percentages sum to {total_pct}, not 100")
        return {uid: round(amount * pct / 100, 2)
                for uid, pct in params.items()}

# Strategy factory
SPLIT_STRATEGIES: dict[SplitType, SplitStrategy] = {
    SplitType.EQUAL: EqualSplit(),
    SplitType.EXACT: ExactSplit(),
    SplitType.PERCENTAGE: PercentageSplit(),
}

@dataclass
class Expense:
    expense_id: int
    description: str
    amount: float
    paid_by: User
    split_type: SplitType
    participants: list[User]
    splits: dict[int, float] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

# --- Balance Sheet (tracks who owes whom) ---
class BalanceSheet:
    """
    Tracks net balances between pairs of users.
    Positive value means user_a is owed by user_b.
    """
    def __init__(self):
        # balances[a][b] > 0 means b owes a
        self.balances: dict[int, dict[int, float]] = defaultdict(
            lambda: defaultdict(float))

    def record(self, creditor_id: int, debtor_id: int, amount: float) -> None:
        self.balances[creditor_id][debtor_id] += amount
        self.balances[debtor_id][creditor_id] -= amount

    def get_balance(self, user_a: int, user_b: int) -> float:
        return self.balances[user_a][user_b]

    def get_user_summary(self, user_id: int) -> dict[int, float]:
        """Returns {other_user_id: net_amount}. Positive = they owe you."""
        return {
            other: amt
            for other, amt in self.balances[user_id].items()
            if abs(amt) > 0.01
        }

@dataclass
class Group:
    group_id: int
    name: str
    members: list[User]
    expenses: list[Expense] = field(default_factory=list)

# --- Expense Manager (central service) ---
class ExpenseManager:
    """
    Core service: adds expenses, computes splits, tracks balances.
    Design patterns: Strategy (split types), Facade (simple API).
    """
    def __init__(self):
        self.users: dict[int, User] = {}
        self.groups: dict[int, Group] = {}
        self.balance_sheet = BalanceSheet()
        self._expense_counter = 0

    def add_user(self, user: User) -> None:
        self.users[user.user_id] = user

    def create_group(self, group: Group) -> None:
        self.groups[group.group_id] = group

    def add_expense(self, group_id: int, description: str, amount: float,
                    paid_by: User, split_type: SplitType,
                    participants: list[User],
                    split_params: Optional[dict] = None) -> Expense:
        strategy = SPLIT_STRATEGIES[split_type]
        splits = strategy.calculate_split(amount, participants, split_params)

        self._expense_counter += 1
        expense = Expense(
            expense_id=self._expense_counter,
            description=description,
            amount=amount,
            paid_by=paid_by,
            split_type=split_type,
            participants=participants,
            splits=splits,
        )

        # Update balances — payer is owed by each participant
        for user_id, share in splits.items():
            if user_id != paid_by.user_id:
                self.balance_sheet.record(paid_by.user_id, user_id, share)

        if group_id in self.groups:
            self.groups[group_id].expenses.append(expense)
        return expense

    def show_balances(self, user_id: int) -> None:
        summary = self.balance_sheet.get_user_summary(user_id)
        user = self.users[user_id]
        for other_id, amount in summary.items():
            other = self.users[other_id]
            if amount > 0:
                print(f"  {other.name} owes {user.name}: ${amount:.2f}")
            else:
                print(f"  {user.name} owes {other.name}: ${-amount:.2f}")

# --- Usage ---
# alice = User(1, "Alice", "alice@mail.com")
# bob = User(2, "Bob", "bob@mail.com")
# carol = User(3, "Carol", "carol@mail.com")
# mgr = ExpenseManager()
# mgr.add_user(alice); mgr.add_user(bob); mgr.add_user(carol)
# group = Group(1, "Trip", [alice, bob, carol])
# mgr.create_group(group)
# mgr.add_expense(1, "Dinner", 90.0, alice, SplitType.EQUAL,
#                  [alice, bob, carol])
# mgr.show_balances(1)  # Bob owes Alice $30, Carol owes Alice $30
```

---

## Tips for Case Studies

### Pattern Recognition Table

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
| **Logging / DB Connection** | Single global instance | **Singleton Pattern** |
| **Multiple output formats** | Same data, different views | **Strategy / Factory** |
| **Seat/resource booking** | Concurrent access to shared resource | **Locking + State** |

### Interview Checklist

1. **Define the API first**: Write out the public methods clearly (e.g., `park_vehicle(v)`, `checkout(ticket)`). This grounds the discussion.
2. **Concurrency**: Always mention how you handle race conditions (e.g., row-level locking, Redis distributed locks, optimistic locking with version columns).
3. **Extensibility**: If the interviewer asks "How do we add EV charging?", show where you would add the `ChargingStation` class and how it interacts with `ParkingSpot`. The design should be open for extension, closed for modification.
4. **Identify the core pattern**: Most LLD problems map to 1-2 design patterns. State the pattern explicitly — interviewers are listening for it.
5. **Schema design**: Sketch the DB tables. This shows you think about persistence, not just in-memory objects.
6. **Error handling**: Mention edge cases — what happens when the lot is full, the ATM runs out of cash, or payment fails mid-booking?
7. **Testability**: Use dependency injection (e.g., strategy/handler constructors) so components can be tested in isolation with mocks.

---

## Practice Problems

### Easy: Design a Notification Service (15 min)
Design a notification service that sends messages through multiple channels (Email, SMS, Push). Use the Observer + Strategy patterns.

**Key insight**: Decouple notification delivery from the sender using the Observer pattern. Each channel is a handler that can be added/removed independently.

<details>
<summary>Solution</summary>

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class NotificationType(Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"

@dataclass
class Message:
    recipient_id: str
    subject: str
    body: str
    created_at: datetime

# --- Observer pattern: each channel is a handler ---
class NotificationChannel(ABC):
    """Each channel knows how to deliver a message its way."""
    @abstractmethod
    def send(self, message: Message) -> bool:
        pass

class EmailChannel(NotificationChannel):
    def send(self, message: Message) -> bool:
        print(f"Email to {message.recipient_id}: {message.subject}")
        return True

class SMSChannel(NotificationChannel):
    def send(self, message: Message) -> bool:
        print(f"SMS to {message.recipient_id}: {message.body[:160]}")
        return True

class PushChannel(NotificationChannel):
    def send(self, message: Message) -> bool:
        print(f"Push to {message.recipient_id}: {message.subject}")
        return True

# --- Strategy: controls which channels a user prefers ---
class NotificationService:
    """
    Central service: registers channels, dispatches messages.
    Design patterns: Observer (channels), Strategy (per-user preferences).
    """
    def __init__(self):
        self._channels: dict[NotificationType, NotificationChannel] = {}
        # user_id -> set of preferred channel types
        self._preferences: dict[str, set[NotificationType]] = {}

    def register_channel(self, ntype: NotificationType,
                         channel: NotificationChannel) -> None:
        self._channels[ntype] = channel

    def set_user_preferences(self, user_id: str,
                             prefs: set[NotificationType]) -> None:
        self._preferences[user_id] = prefs

    def notify(self, recipient_id: str, subject: str, body: str) -> list[NotificationType]:
        """Send notification through user's preferred channels. Returns channels used."""
        message = Message(recipient_id, subject, body, datetime.now())
        prefs = self._preferences.get(recipient_id, {NotificationType.EMAIL})
        sent: list[NotificationType] = []
        for ntype in prefs:
            channel = self._channels.get(ntype)
            if channel and channel.send(message):
                sent.append(ntype)
        return sent

# Test
# service = NotificationService()
# service.register_channel(NotificationType.EMAIL, EmailChannel())
# service.register_channel(NotificationType.SMS, SMSChannel())
# service.register_channel(NotificationType.PUSH, PushChannel())
# service.set_user_preferences("user1", {NotificationType.EMAIL, NotificationType.PUSH})
# sent = service.notify("user1", "Welcome!", "Thanks for signing up.")
# assert NotificationType.EMAIL in sent
```

</details>

### Medium: Design a Rate Limiter (25 min)
Implement a rate limiter that allows at most `max_requests` within a sliding `window_seconds` window per user. Support multiple strategies (fixed window, sliding window).

**Key patterns**: Strategy pattern for the algorithm, Singleton for the global limiter.

<details>
<summary>Solution</summary>

```python
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from time import time
from typing import Optional

class RateLimitStrategy(ABC):
    @abstractmethod
    def is_allowed(self, user_id: str, max_requests: int,
                   window_seconds: float) -> bool:
        pass

class SlidingWindowStrategy(RateLimitStrategy):
    """Tracks exact timestamps; evicts expired entries."""
    def __init__(self):
        self.requests: dict[str, deque[float]] = defaultdict(deque)

    def is_allowed(self, user_id: str, max_requests: int,
                   window_seconds: float) -> bool:
        now = time()
        user_requests = self.requests[user_id]

        # Evict timestamps outside the window
        while user_requests and user_requests[0] <= now - window_seconds:
            user_requests.popleft()

        if len(user_requests) < max_requests:
            user_requests.append(now)
            return True
        return False

class FixedWindowStrategy(RateLimitStrategy):
    """Buckets time into fixed intervals; simpler but less precise."""
    def __init__(self):
        self.windows: dict[str, tuple[int, int]] = {}  # user -> (window_key, count)

    def is_allowed(self, user_id: str, max_requests: int,
                   window_seconds: float) -> bool:
        now = time()
        window_key = int(now // window_seconds)
        entry = self.windows.get(user_id)

        if entry is None or entry[0] != window_key:
            self.windows[user_id] = (window_key, 1)
            return True

        if entry[1] < max_requests:
            self.windows[user_id] = (window_key, entry[1] + 1)
            return True
        return False

class RateLimiter:
    """
    Configurable rate limiter with pluggable strategy.
    Design patterns: Strategy, Singleton (if needed globally).
    """
    def __init__(self, max_requests: int = 10,
                 window_seconds: float = 60.0,
                 strategy: Optional[RateLimitStrategy] = None):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.strategy = strategy or SlidingWindowStrategy()

    def allow_request(self, user_id: str) -> bool:
        return self.strategy.is_allowed(
            user_id, self.max_requests, self.window_seconds)

# Test
# limiter = RateLimiter(max_requests=3, window_seconds=1.0)
# assert limiter.allow_request("user1") == True   # 1/3
# assert limiter.allow_request("user1") == True   # 2/3
# assert limiter.allow_request("user1") == True   # 3/3
# assert limiter.allow_request("user1") == False  # blocked
```

</details>

### Hard: Design a Task Scheduler with Dependencies (40 min)
Design a task scheduler that executes tasks respecting dependency ordering (topological sort). Support adding tasks with dependencies, detecting cycles, and executing in valid order.

**Key patterns**: Observer (task completion notifications), Template Method (task execution), topological sort algorithm.

<details>
<summary>Solution</summary>

```python
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    task_id: str
    name: str
    action: Callable[[], None]  # the work to execute
    dependencies: list[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING

class CyclicDependencyError(Exception):
    pass

class TaskScheduler:
    """
    Schedules tasks respecting dependencies via topological sort (Kahn's).
    Design patterns: Observer (completion triggers dependents),
    Template Method (execute wraps action with status tracking).
    """
    def __init__(self):
        self.tasks: dict[str, Task] = {}
        self.graph: dict[str, list[str]] = defaultdict(list)  # task -> dependents
        self.in_degree: dict[str, int] = defaultdict(int)

    def add_task(self, task: Task) -> None:
        self.tasks[task.task_id] = task
        if task.task_id not in self.in_degree:
            self.in_degree[task.task_id] = 0
        for dep in task.dependencies:
            self.graph[dep].append(task.task_id)
            self.in_degree[task.task_id] += 1

    def _topological_order(self) -> list[str]:
        """Kahn's algorithm. Raises on cycle. Uses a copy of in_degree
        so the scheduler can be called multiple times."""
        in_deg = dict(self.in_degree)  # work on a copy
        queue: deque[str] = deque()
        for tid, deg in in_deg.items():
            if deg == 0:
                queue.append(tid)

        order: list[str] = []
        while queue:
            current = queue.popleft()
            order.append(current)
            for dependent in self.graph[current]:
                in_deg[dependent] -= 1
                if in_deg[dependent] == 0:
                    queue.append(dependent)

        if len(order) != len(self.tasks):
            raise CyclicDependencyError(
                "Cycle detected — cannot schedule all tasks")
        return order

    def execute_all(self) -> list[str]:
        """Execute tasks in dependency order. Returns execution order.
        Skips tasks whose dependencies failed."""
        order = self._topological_order()
        executed: list[str] = []
        failed: set[str] = set()

        for task_id in order:
            task = self.tasks[task_id]
            # Skip if any dependency failed
            if any(dep in failed for dep in task.dependencies):
                task.status = TaskStatus.FAILED
                failed.add(task_id)
                print(f"Task {task.name} skipped: dependency failed")
                continue
            task.status = TaskStatus.RUNNING
            try:
                task.action()
                task.status = TaskStatus.COMPLETED
                executed.append(task_id)
            except Exception as e:
                task.status = TaskStatus.FAILED
                failed.add(task_id)
                print(f"Task {task.name} failed: {e}")

        return executed

# Test
# scheduler = TaskScheduler()
# scheduler.add_task(Task("A", "Compile", lambda: print("Compiling...")))
# scheduler.add_task(Task("B", "Test", lambda: print("Testing..."),
#                         dependencies=["A"]))
# scheduler.add_task(Task("C", "Deploy", lambda: print("Deploying..."),
#                         dependencies=["A", "B"]))
# order = scheduler.execute_all()  # A -> B -> C
# assert order == ["A", "B", "C"]
```

</details>
