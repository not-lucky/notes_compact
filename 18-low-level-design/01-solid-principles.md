# SOLID Principles

SOLID is a mnemonic acronym for five design principles intended to make software designs more understandable, flexible, and maintainable. They were introduced by Robert C. Martin (Uncle Bob) and are foundational to good object-oriented design.

| Letter | Principle | Core Idea |
|--------|-----------|-----------|
| **S** | Single Responsibility | One class, one reason to change |
| **O** | Open/Closed | Extend behavior without modifying existing code |
| **L** | Liskov Substitution | Subtypes must be substitutable for their base types |
| **I** | Interface Segregation | Prefer small, focused interfaces over fat ones |
| **D** | Dependency Inversion | Depend on abstractions, not concretions |

> **Note**: Python examples use `ABC` and `@abstractmethod` from the `abc` module for defining abstract interfaces where applicable. BAD and GOOD examples are in separate code blocks to avoid class name conflicts. Every example is runnable Python 3.10+.

> **Prerequisites:** [Chapter 18 README](./README.md)

---

## 1. S: Single Responsibility Principle (SRP)

**Definition**: A class should have one, and only one, reason to change. Each class encapsulates a single concern.

**Why it matters**: When a class has multiple responsibilities, changes to one responsibility risk breaking the other. SRP reduces coupling, makes classes easier to test, and makes the codebase easier to navigate.

### How to Recognize Violation
- **The "And" Test**: If you describe what a class does and use the word "and", it's likely violating SRP. ("It calculates salary *and* formats the report *and* sends it via email").
- **Fat Class**: Too many imports from unrelated modules (e.g., `import sqlalchemy` and `import matplotlib` and `import smtplib` in one class).
- **Frequent Changes**: If multiple unrelated feature requests lead to changes in the same file.
- **Hard to Name**: If you struggle to give the class a concise name without using "Manager" or "Handler", it may be doing too much.

### Building Intuition
Imagine a Swiss Army Knife. It's great for camping, but if the screwdriver part breaks, you might have to replace the whole knife. In software, if a class handles "Calculating Salary" AND "Saving to Database", a change in the database schema might break the salary calculation logic. Each "axis of change" should live in its own class.

### Python Example

**❌ BAD:** Employee class has THREE responsibilities — business logic, persistence, and formatting. A DB schema change or report format change forces you to modify this class.
```python
class Employee:
    def __init__(self, name: str, hours: float, rate: float) -> None:
        self.name = name
        self.hours = hours
        self.rate = rate

    def calculate_salary(self) -> float:
        return self.hours * self.rate

    def save_to_db(self) -> None:
        # Persistence logic mixed into domain object
        print(f"INSERT INTO employees VALUES ('{self.name}', {self.calculate_salary()})")

    def generate_report(self) -> str:
        # Formatting logic mixed into domain object
        return f"Report: {self.name} earned ${self.calculate_salary():.2f}"
```

**✅ GOOD:** Each class has exactly ONE reason to change.
```python
from dataclasses import dataclass

@dataclass
class Employee:
    """Domain object — only responsible for employee data and salary logic."""
    name: str
    hours: float
    rate: float

    def calculate_salary(self) -> float:
        """Business rule: salary = hours * rate."""
        return self.hours * self.rate


class EmployeeRepository:
    """Handles persistence — changes only when DB schema changes."""
    def save(self, employee: Employee) -> None:
        salary = employee.calculate_salary()
        print(f"INSERT INTO employees VALUES ('{employee.name}', {salary})")


class SalaryReportFormatter:
    """Handles formatting — changes only when report format changes."""
    def format(self, employee: Employee) -> str:
        return f"Report: {employee.name} earned ${employee.calculate_salary():.2f}"
```

---

## 2. O: Open/Closed Principle (OCP)

**Definition**: Software entities (classes, modules, functions) should be open for extension, but closed for modification.

**Why it matters**: Every time you modify existing, tested code to add a new feature, you risk introducing regressions. OCP encourages designs where new behavior is added by writing *new* code rather than changing *old* code. The key mechanism is **polymorphism** — define an abstract interface, then extend it with new implementations.

### How to Recognize Violation
- **Giant If/Else or Switch Blocks**: If you find yourself adding a new `elif` every time a new business requirement comes in (e.g., `if type == 'CREDIT_CARD'`, `elif type == 'CRYPTO'`).
- **Fear of Breaking Things**: If adding a new feature requires you to change code that has been working for months.
- **Shotgun Surgery**: Adding one new "type" requires changes in multiple places across the codebase.

### Building Intuition
Think of a USB port. The USB specification is *closed* — you don't redesign the port for each new device. But it's *open* — any device that implements the USB interface can plug in. Your code should work the same way: define stable interfaces, then extend by plugging in new implementations.

### Python Example

**❌ BAD:** Every new discount type requires modifying this class. Adding "STUDENT" means touching working code — risk of regression.
```python
class DiscountCalculator:
    def apply(self, price: float, discount_type: str) -> float:
        if discount_type == "VIP":
            return price * 0.8
        elif discount_type == "SALE":
            return price * 0.9
        elif discount_type == "STUDENT":
            return price * 0.85
        # ... grows forever
        else:
            return price
```

**✅ GOOD:** New discounts are added by creating new classes — existing code never changes. The `DiscountCalculator` is closed for modification but open for extension via new `Discount` subclasses.
```python
from abc import ABC, abstractmethod

class Discount(ABC):
    """Abstract discount strategy. Subclass to add new discount types."""
    @abstractmethod
    def apply(self, price: float) -> float:
        """Apply this discount to the given price."""
        ...

class VIPDiscount(Discount):
    def apply(self, price: float) -> float:
        return price * 0.8  # 20% off

class SaleDiscount(Discount):
    def apply(self, price: float) -> float:
        return price * 0.9  # 10% off

class StudentDiscount(Discount):
    """Added later — no existing code was modified."""
    def apply(self, price: float) -> float:
        return price * 0.85  # 15% off

# Usage — works with ANY discount, present or future:
def checkout(price: float, discount: Discount) -> float:
    """Apply a discount at checkout. Works with any Discount subclass."""
    return discount.apply(price)

# checkout(100.0, StudentDiscount())  -> 85.0
```

---

## 3. L: Liskov Substitution Principle (LSP)

**Definition**: Objects of a superclass should be replaceable with objects of its subclasses without breaking the application. Formally: if `S` is a subtype of `T`, then objects of type `T` may be replaced with objects of type `S` without altering any desirable property of the program.

**Why it matters**: LSP ensures that inheritance hierarchies are semantically correct, not just syntactically correct. A subclass that violates LSP creates landmines — code that works with the base class will crash or behave incorrectly with the subclass.

### How to Recognize Violation
- **`isinstance()` checks**: If calling code needs `if isinstance(obj, Ostrich): raise Error()`, the hierarchy is wrong — the caller shouldn't need to know about specific subtypes.
- **Empty Method Overrides**: If a subclass implements a method from an interface with `pass` or `raise NotImplementedError`, it can't truly substitute for the parent.
- **Strengthening Pre-conditions**: If a subclass requires more strict input than the parent (e.g., parent accepts any int, subclass only accepts positive ints).
- **Weakening Post-conditions**: If a subclass returns something weaker than what the parent promises (e.g., parent guarantees sorted output, subclass doesn't).

### Building Intuition
If `Ostrich` is a subclass of `Bird`, but `Bird` has a `fly()` method, you can't substitute `Bird` with `Ostrich` everywhere without potential crashes. The fix isn't to make `Ostrich.fly()` raise an error — it's to redesign the hierarchy so that `fly()` only exists on birds that can actually fly. **Model behavior, not taxonomy.**

Another classic example: `Square` as a subclass of `Rectangle`. A `Rectangle` lets you set width and height independently, but a `Square` must keep them equal. If a caller sets `rect.width = 5` and expects `rect.height` to remain unchanged, a `Square` violates that expectation. The hierarchy is taxonomically correct ("a square is a rectangle") but behaviorally wrong.

### Python Example

**❌ BAD:** Subclass breaks superclass contract. Any code that calls `bird.fly()` will crash when given an Ostrich. The hierarchy models taxonomy ("is-a bird") instead of behavior ("can fly").
```python
from abc import ABC, abstractmethod

class Bird(ABC):
    @abstractmethod
    def fly(self) -> str:
        ...

class Sparrow(Bird):
    def fly(self) -> str:
        return "Sparrow flying high!"

class Ostrich(Bird):
    def fly(self) -> str:
        # Violates LSP — callers expect fly() to work, not explode
        raise Exception("Can't fly!")

def make_bird_fly(bird: Bird) -> str:
    return bird.fly()  # Crashes with Ostrich — LSP violated

# make_bird_fly(Ostrich())  -> Exception!
```

**✅ GOOD:** Hierarchy models capabilities, not taxonomy. Code that needs a flying bird asks for `FlyingBird`. Ostrich is still a Bird but never promises to fly — so no contract is broken.
```python
from abc import ABC, abstractmethod

class Bird(ABC):
    """Base class for all birds — only includes universal bird behavior."""
    @abstractmethod
    def eat(self) -> str:
        ...

class FlyingBird(Bird):
    """Birds that can fly. Only use this type when flight is required."""
    @abstractmethod
    def fly(self) -> str:
        ...

class Sparrow(FlyingBird):
    def eat(self) -> str:
        return "Sparrow pecking seeds"

    def fly(self) -> str:
        return "Sparrow flying high!"

class Ostrich(Bird):
    """Ostrich is a Bird but NOT a FlyingBird — no broken contracts."""
    def eat(self) -> str:
        return "Ostrich grazing on plants"

def make_bird_fly(bird: FlyingBird) -> str:
    """Type system now prevents passing an Ostrich here."""
    return bird.fly()  # Safe — only FlyingBird subtypes accepted
```

---

## 4. I: Interface Segregation Principle (ISP)

**Definition**: No client should be forced to depend on methods it does not use. Prefer many small, specific interfaces over one large, general-purpose interface.

**Why it matters**: Fat interfaces create unnecessary coupling. When a class is forced to implement methods it doesn't need, you get dummy implementations (`raise NotImplementedError`) that violate LSP, and changes to unused methods can force recompilation or retesting of unrelated code.

### How to Recognize Violation
- **"Polluted" Interfaces**: An interface has 20 methods, but most implementations only care about 3.
- **Throwing `NotImplementedError`**: If you're forced to implement a method just to satisfy an interface and your only option is to throw an error, the interface is too broad.
- **"God Interface"**: One interface tries to serve multiple very different clients.

### Building Intuition
Instead of one "Fat Interface", create many small, specific ones. A `SimplePrinter` shouldn't be forced to implement `scan()` or `fax()`. Think about it from the **client's perspective** — what does each client actually need? Each client should see an interface tailored to its needs.

### Python Example

**❌ BAD:** Fat interface forces `BasicPrinter` to implement `fax()` and `scan()` even though it can't do either. This also violates LSP — passing a `BasicPrinter` to code that calls `fax()` will crash.
```python
from abc import ABC, abstractmethod

class SmartDevice(ABC):
    @abstractmethod
    def print_document(self, doc: str) -> None: ...

    @abstractmethod
    def fax(self, doc: str, number: str) -> None: ...

    @abstractmethod
    def scan(self) -> str: ...

class BasicPrinter(SmartDevice):
    def print_document(self, doc: str) -> None:
        print(f"Printing: {doc}")

    def fax(self, doc: str, number: str) -> None:
        raise NotImplementedError("BasicPrinter can't fax!")  # Forced stub

    def scan(self) -> str:
        raise NotImplementedError("BasicPrinter can't scan!")  # Forced stub
```

**✅ GOOD:** Segregated interfaces — each class only implements what it actually supports. Clients depend only on the capability they need.
```python
from abc import ABC, abstractmethod

class Printable(ABC):
    """Interface for devices that can print."""
    @abstractmethod
    def print_document(self, doc: str) -> None: ...

class Faxable(ABC):
    """Interface for devices that can fax."""
    @abstractmethod
    def fax(self, doc: str, number: str) -> None: ...

class Scannable(ABC):
    """Interface for devices that can scan."""
    @abstractmethod
    def scan(self) -> str: ...

class BasicPrinter(Printable):
    """Only implements Printable — no dummy methods needed."""
    def print_document(self, doc: str) -> None:
        print(f"Printing: {doc}")

class MultiFunctionPrinter(Printable, Faxable, Scannable):
    """Implements all interfaces because it actually supports all features."""
    def print_document(self, doc: str) -> None:
        print(f"Printing: {doc}")

    def fax(self, doc: str, number: str) -> None:
        print(f"Faxing '{doc}' to {number}")

    def scan(self) -> str:
        return "Scanned document content"

# Client code depends only on the interface it needs:
def print_job(printer: Printable, doc: str) -> None:
    """Works with BasicPrinter or MultiFunctionPrinter — doesn't care about fax/scan."""
    printer.print_document(doc)
```

---

## 5. D: Dependency Inversion Principle (DIP)

**Definition**: High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details. Details should depend on abstractions.

**Why it matters**: Without DIP, high-level business logic is tightly coupled to low-level implementation details (specific databases, APIs, file formats). This makes the code hard to test (you need a real database for unit tests) and hard to change (swapping MySQL for PostgreSQL requires rewriting business logic).

### How to Recognize Violation
- **Direct instantiation**: `self.db = MySQLDB()` inside a class — this hardcodes the dependency so you can't swap or mock it.
- **Hard to Test**: If you can't unit test a class without setting up a real database, network connection, or external service.
- **Import of concrete classes in high-level modules**: High-level policy code importing low-level infrastructure details.

### Building Intuition
Your laptop doesn't care if you plug in a Dell monitor or an LG monitor, because both use the **HDMI interface**. The laptop (high-level) doesn't depend on the specific monitor (low-level), but on the HDMI standard (abstraction). DIP applies the same idea: define an abstract interface, then both the high-level module and the low-level module depend on that interface.

### Python Example

**❌ BAD:** `UserService` (high-level business logic) directly depends on `MySQLDatabase` (low-level detail). You can't test `UserService` without a real MySQL connection, and switching to PostgreSQL means rewriting `UserService`.
```python
class MySQLDatabase:
    def save(self, table: str, data: dict) -> None:
        print(f"MySQL: INSERT INTO {table} VALUES {data}")

class UserService:
    def __init__(self) -> None:
        self.db = MySQLDatabase()  # Hardcoded dependency — violation

    def create_user(self, name: str, email: str) -> None:
        self.db.save("users", {"name": name, "email": email})
```

**✅ GOOD:** Both `UserService` and `MySQLDatabase` depend on the `Database` abstraction. `UserService` doesn't know or care which DB it's using. You can easily swap databases or inject a mock for testing.
```python
from abc import ABC, abstractmethod

class Database(ABC):
    """Abstraction that both high-level and low-level code depend on."""
    @abstractmethod
    def save(self, table: str, data: dict) -> None: ...

class MySQLDatabase(Database):
    """Low-level detail — implements the Database abstraction."""
    def save(self, table: str, data: dict) -> None:
        print(f"MySQL: INSERT INTO {table} VALUES {data}")

class PostgreSQLDatabase(Database):
    """Another low-level detail — swappable without changing UserService."""
    def save(self, table: str, data: dict) -> None:
        print(f"PostgreSQL: INSERT INTO {table} VALUES {data}")

class InMemoryDatabase(Database):
    """Useful for unit testing — no real DB needed."""
    def __init__(self) -> None:
        self.store: list[dict] = []

    def save(self, table: str, data: dict) -> None:
        self.store.append({"table": table, **data})

class UserService:
    """High-level module — depends on abstraction, not concrete DB."""
    def __init__(self, db: Database) -> None:
        self.db = db  # Injected — easy to swap or mock

    def create_user(self, name: str, email: str) -> None:
        self.db.save("users", {"name": name, "email": email})

# Production:   UserService(MySQLDatabase())
# Testing:      UserService(InMemoryDatabase())
# Migration:    UserService(PostgreSQLDatabase())  — zero changes to UserService
```

---

## Common Misconceptions

| Misconception | Reality |
|--------------|---------|
| "Every class must have only one method" | SRP is about one *reason to change*, not one method. A class can have multiple methods if they all serve the same responsibility. |
| "OCP means never modify any code" | OCP means design so that *common* extensions don't require modification. Bug fixes and refactors still modify existing code. |
| "LSP is just about inheritance" | LSP applies to any subtype relationship, including interface implementations. The key question: can a caller use the subtype without knowing it's a subtype? |
| "ISP means every interface has one method" | ISP means interfaces should be *cohesive* — all methods serve the same client need. A `Repository` with `save()`, `find()`, `delete()` is fine if clients typically need all three. |
| "DIP means use dependency injection frameworks" | DIP is a *design principle*, not a framework. Simple constructor injection (passing dependencies as arguments) is the most common and often sufficient approach. |

---

## Practice Problems

### Problem 1 (Easy): Design a Notification System

Apply SOLID to design a system that supports Email and SMS notifications, and can easily add Push notifications later.

**Think about**: Which principles apply? How would you structure the classes so that adding a new notification channel requires zero changes to existing code?

<details>
<summary><strong>Solution</strong></summary>

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

# --- SRP: Each class has exactly one responsibility ---

@dataclass
class Message:
    """Data class — only holds message data (SRP)."""
    recipient: str
    subject: str
    body: str


# --- OCP + DIP: NotificationChannel is the abstraction that both
# high-level (NotificationService) and low-level (Email, SMS) depend on.
# Adding Push later means creating a new class — no existing code changes. ---

class NotificationChannel(ABC):
    """Abstraction for all notification channels (DIP).
    New channels extend this — existing code stays closed (OCP)."""

    @abstractmethod
    def send(self, message: Message) -> bool:
        """Send a message. Returns True if successful."""
        ...


class EmailChannel(NotificationChannel):
    """Concrete implementation for email delivery."""

    def __init__(self, smtp_host: str = "smtp.example.com") -> None:
        self.smtp_host = smtp_host

    def send(self, message: Message) -> bool:
        print(f"Email to {message.recipient} via {self.smtp_host}: "
              f"[{message.subject}] {message.body}")
        return True


class SMSChannel(NotificationChannel):
    """Concrete implementation for SMS delivery."""

    def __init__(self, api_key: str = "sms-api-key") -> None:
        self.api_key = api_key

    def send(self, message: Message) -> bool:
        print(f"SMS to {message.recipient}: {message.body}")
        return True


class PushChannel(NotificationChannel):
    """Added later — no existing code was modified (OCP)."""

    def send(self, message: Message) -> bool:
        print(f"Push to {message.recipient}: {message.subject}")
        return True


# --- LSP: Every channel is fully substitutable. No channel raises
# NotImplementedError or silently skips — they all honor the contract. ---

# --- ISP: NotificationChannel has exactly ONE method (send). Channels
# don't need to implement irrelevant methods like retry() or format(). ---

# If we later need retry logic, we add a separate Retryable interface
# rather than bloating NotificationChannel:
class Retryable(ABC):
    """Separate interface for channels that support retries (ISP)."""
    @abstractmethod
    def retry(self, message: Message, attempts: int) -> bool: ...


class EmailChannelWithRetry(NotificationChannel, Retryable):
    """Implements both interfaces — only if the channel actually supports retry."""

    def __init__(self, smtp_host: str = "smtp.example.com") -> None:
        self.smtp_host = smtp_host

    def send(self, message: Message) -> bool:
        print(f"Email to {message.recipient}: [{message.subject}] {message.body}")
        return True

    def retry(self, message: Message, attempts: int) -> bool:
        for i in range(attempts):
            print(f"  Retry {i + 1}/{attempts}...")
            if self.send(message):
                return True
        return False


# --- SRP: NotificationService only orchestrates sending. It doesn't
# know HOW to send — that's the channel's job. ---

class NotificationService:
    """High-level orchestrator. Depends on abstractions (DIP), not
    concrete channels. Adding a new channel requires zero changes here."""

    def __init__(self, channels: list[NotificationChannel]) -> None:
        self.channels = channels

    def notify(self, message: Message) -> dict[str, bool]:
        """Send message via all configured channels. Returns per-channel results."""
        results: dict[str, bool] = {}
        for channel in self.channels:
            channel_name = type(channel).__name__
            results[channel_name] = channel.send(message)
        return results


# --- Usage ---
if __name__ == "__main__":
    service = NotificationService([
        EmailChannel(),
        SMSChannel(),
        PushChannel(),  # Added with zero changes to existing code
    ])

    msg = Message(
        recipient="user@example.com",
        subject="Welcome!",
        body="Thanks for signing up.",
    )
    results = service.notify(msg)
    print(f"Results: {results}")
```

**SOLID Scorecard:**

| Principle | How it's applied |
|-----------|-----------------|
| **SRP** | `Message` holds data, each channel handles one delivery method, `NotificationService` only orchestrates |
| **OCP** | New channels (e.g., `PushChannel`) are added without modifying existing code |
| **LSP** | Every `NotificationChannel` subclass is fully substitutable — no dummy methods |
| **ISP** | `NotificationChannel` has one method; retry is a separate `Retryable` interface |
| **DIP** | `NotificationService` depends on `NotificationChannel` (abstraction), not on `EmailChannel` (concrete) |

</details>

---

### Problem 2 (Medium): Design a Payment Processing System

Design a system that processes payments via CreditCard, PayPal, and BankTransfer. Each payment method has different validation rules and processing steps. The system should:
- Validate payment details before processing
- Log every transaction
- Support adding new payment methods without modifying existing code

**Think about**: Where does validation logic live? How do you avoid a god class that does validation + processing + logging? How do you make the logger swappable for testing?

<details>
<summary><strong>Solution</strong></summary>

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


# --- Data classes (SRP: only hold data) ---

@dataclass
class PaymentRequest:
    """Immutable payment request data."""
    amount: float
    currency: str
    payer_id: str
    metadata: dict[str, str] = field(default_factory=dict)

@dataclass
class PaymentResult:
    """Result of a payment attempt."""
    success: bool
    transaction_id: str
    message: str


# --- ISP: Separate interfaces for validation and processing.
# Some systems might only need to validate (e.g., a preview/dry-run mode)
# without actually processing. ---

class PaymentValidator(ABC):
    """Interface for validating a payment before processing (ISP)."""
    @abstractmethod
    def validate(self, request: PaymentRequest) -> tuple[bool, str]:
        """Returns (is_valid, error_message). Empty string if valid."""
        ...

class PaymentProcessor(ABC):
    """Interface for processing a validated payment (ISP)."""
    @abstractmethod
    def process(self, request: PaymentRequest) -> PaymentResult:
        """Process the payment and return result."""
        ...


# --- Concrete payment methods (OCP: add new ones without touching existing) ---

class CreditCardPayment(PaymentValidator, PaymentProcessor):
    """Handles credit card validation and processing."""

    def validate(self, request: PaymentRequest) -> tuple[bool, str]:
        if request.amount <= 0:
            return False, "Amount must be positive"
        if request.amount > 10_000:
            return False, "Credit card limit exceeded"
        if "card_number" not in request.metadata:
            return False, "Card number required"
        return True, ""

    def process(self, request: PaymentRequest) -> PaymentResult:
        card = request.metadata["card_number"]
        return PaymentResult(
            success=True,
            transaction_id=f"CC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            message=f"Charged ${request.amount:.2f} to card ending {card[-4:]}",
        )


class PayPalPayment(PaymentValidator, PaymentProcessor):
    """Handles PayPal validation and processing."""

    def validate(self, request: PaymentRequest) -> tuple[bool, str]:
        if request.amount <= 0:
            return False, "Amount must be positive"
        if "paypal_email" not in request.metadata:
            return False, "PayPal email required"
        return True, ""

    def process(self, request: PaymentRequest) -> PaymentResult:
        email = request.metadata["paypal_email"]
        return PaymentResult(
            success=True,
            transaction_id=f"PP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            message=f"Charged ${request.amount:.2f} to PayPal account {email}",
        )


class BankTransferPayment(PaymentValidator, PaymentProcessor):
    """Handles bank transfer validation and processing."""

    def validate(self, request: PaymentRequest) -> tuple[bool, str]:
        if request.amount <= 0:
            return False, "Amount must be positive"
        if "routing_number" not in request.metadata:
            return False, "Routing number required"
        if "account_number" not in request.metadata:
            return False, "Account number required"
        return True, ""

    def process(self, request: PaymentRequest) -> PaymentResult:
        return PaymentResult(
            success=True,
            transaction_id=f"BT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            message=f"Transferred ${request.amount:.2f} via bank transfer",
        )


# --- DIP: Logger abstraction — swappable for testing ---

class TransactionLogger(ABC):
    """Abstraction for logging (DIP). Swap with InMemoryLogger for tests."""
    @abstractmethod
    def log(self, result: PaymentResult) -> None: ...

class ConsoleLogger(TransactionLogger):
    def log(self, result: PaymentResult) -> None:
        status = "SUCCESS" if result.success else "FAILED"
        print(f"[{status}] {result.transaction_id}: {result.message}")

class InMemoryLogger(TransactionLogger):
    """For testing — captures logs without side effects."""
    def __init__(self) -> None:
        self.logs: list[PaymentResult] = []

    def log(self, result: PaymentResult) -> None:
        self.logs.append(result)


# --- SRP: PaymentService only orchestrates. It doesn't validate,
# process, or log — it delegates each to the appropriate collaborator. ---

class PaymentService:
    """Orchestrates validation, processing, and logging.
    Depends entirely on abstractions (DIP)."""

    def __init__(
        self,
        validator: PaymentValidator,
        processor: PaymentProcessor,
        logger: TransactionLogger,
    ) -> None:
        self.validator = validator
        self.processor = processor
        self.logger = logger

    def handle_payment(self, request: PaymentRequest) -> PaymentResult:
        """Validate, process, and log a payment."""
        is_valid, error = self.validator.validate(request)
        if not is_valid:
            result = PaymentResult(
                success=False,
                transaction_id="N/A",
                message=f"Validation failed: {error}",
            )
            self.logger.log(result)
            return result

        result = self.processor.process(request)
        self.logger.log(result)
        return result


# --- Usage ---
if __name__ == "__main__":
    # Production setup
    cc = CreditCardPayment()
    service = PaymentService(
        validator=cc,       # Same object acts as both validator and processor
        processor=cc,
        logger=ConsoleLogger(),
    )

    request = PaymentRequest(
        amount=49.99,
        currency="USD",
        payer_id="user-123",
        metadata={"card_number": "4111111111111234"},
    )
    result = service.handle_payment(request)

    # Test setup — no real DB, no real payment gateway
    test_logger = InMemoryLogger()
    paypal = PayPalPayment()
    test_service = PaymentService(
        validator=paypal,
        processor=paypal,
        logger=test_logger,
    )
    test_service.handle_payment(PaymentRequest(
        amount=25.00, currency="USD", payer_id="test",
        metadata={"paypal_email": "test@example.com"},
    ))
    assert len(test_logger.logs) == 1
    assert test_logger.logs[0].success is True
```

**SOLID Scorecard:**

| Principle | How it's applied |
|-----------|-----------------|
| **SRP** | `PaymentRequest`/`PaymentResult` hold data, each payment class handles one method's rules, `PaymentService` only orchestrates |
| **OCP** | New payment methods (e.g., `CryptoPayment`) are added without modifying existing code |
| **LSP** | Every `PaymentValidator`/`PaymentProcessor` implementation is fully substitutable |
| **ISP** | Validation and processing are separate interfaces — a dry-run mode could use only `PaymentValidator` |
| **DIP** | `PaymentService` depends on abstractions (`PaymentValidator`, `PaymentProcessor`, `TransactionLogger`), not concrete classes |

</details>

---

### Problem 3 (Hard): Design a Report Generation System

Design a system that generates reports in multiple formats (PDF, CSV, HTML) from multiple data sources (Database, API, FileSystem). The system should:
- Fetch data from any source
- Apply optional transformations (filtering, sorting, aggregation)
- Render the final report in the chosen format
- Support adding new data sources, transformations, and formats independently

**Think about**: This problem has three independent axes of variation (source, transform, format). How do you avoid a combinatorial explosion of classes? How do you compose transformations?

<details>
<summary><strong>Solution</strong></summary>

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

# --- Core data types ---

@dataclass
class Record:
    """A single row of report data."""
    fields: dict[str, str | int | float]

@dataclass
class ReportData:
    """Collection of records with column metadata."""
    columns: list[str]
    records: list[Record]

    def __len__(self) -> int:
        return len(self.records)


# --- ISP: Three small interfaces for three independent concerns.
# Each axis of variation gets its own interface. ---

class DataSource(ABC):
    """Interface for fetching raw data (ISP)."""
    @abstractmethod
    def fetch(self) -> ReportData: ...

class DataTransformer(ABC):
    """Interface for transforming data (ISP).
    Transformers are composable — chain them together."""
    @abstractmethod
    def transform(self, data: ReportData) -> ReportData: ...

class ReportRenderer(ABC):
    """Interface for rendering data into a final format (ISP)."""
    @abstractmethod
    def render(self, data: ReportData) -> str: ...


# --- Data sources (OCP: add new sources without touching existing) ---

class DatabaseSource(DataSource):
    """Fetches data from a database."""
    def __init__(self, query: str) -> None:
        self.query = query

    def fetch(self) -> ReportData:
        # Simulated DB fetch
        print(f"Executing query: {self.query}")
        return ReportData(
            columns=["name", "department", "salary"],
            records=[
                Record({"name": "Alice", "department": "Engineering", "salary": 120000}),
                Record({"name": "Bob", "department": "Marketing", "salary": 90000}),
                Record({"name": "Charlie", "department": "Engineering", "salary": 110000}),
                Record({"name": "Diana", "department": "Marketing", "salary": 95000}),
            ],
        )

class APISource(DataSource):
    """Fetches data from an external API."""
    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint

    def fetch(self) -> ReportData:
        print(f"Fetching from API: {self.endpoint}")
        return ReportData(
            columns=["product", "revenue"],
            records=[
                Record({"product": "Widget A", "revenue": 50000}),
                Record({"product": "Widget B", "revenue": 75000}),
            ],
        )


# --- Transformers (OCP: composable, add new ones freely) ---

class FilterTransformer(DataTransformer):
    """Filters records where a field matches a value."""
    def __init__(self, field: str, value: str | int | float) -> None:
        self.field = field
        self.value = value

    def transform(self, data: ReportData) -> ReportData:
        filtered = [r for r in data.records if r.fields.get(self.field) == self.value]
        return ReportData(columns=data.columns, records=filtered)

class SortTransformer(DataTransformer):
    """Sorts records by a field."""
    def __init__(self, field: str, reverse: bool = False) -> None:
        self.field = field
        self.reverse = reverse

    def transform(self, data: ReportData) -> ReportData:
        sorted_records = sorted(
            data.records,
            key=lambda r: r.fields.get(self.field, ""),
            reverse=self.reverse,
        )
        return ReportData(columns=data.columns, records=sorted_records)

class TransformPipeline(DataTransformer):
    """Composes multiple transformers into a sequential pipeline.
    This avoids combinatorial explosion — mix and match freely."""
    def __init__(self, transformers: list[DataTransformer]) -> None:
        self.transformers = transformers

    def transform(self, data: ReportData) -> ReportData:
        result = data
        for transformer in self.transformers:
            result = transformer.transform(result)
        return result


# --- Renderers (OCP: add new formats without touching existing) ---

class CSVRenderer(ReportRenderer):
    """Renders report data as CSV."""
    def render(self, data: ReportData) -> str:
        lines: list[str] = [",".join(data.columns)]
        for record in data.records:
            row = ",".join(str(record.fields.get(col, "")) for col in data.columns)
            lines.append(row)
        return "\n".join(lines)

class HTMLRenderer(ReportRenderer):
    """Renders report data as an HTML table."""
    def render(self, data: ReportData) -> str:
        header = "".join(f"<th>{col}</th>" for col in data.columns)
        rows = ""
        for record in data.records:
            cells = "".join(
                f"<td>{record.fields.get(col, '')}</td>" for col in data.columns
            )
            rows += f"<tr>{cells}</tr>\n"
        return f"<table>\n<tr>{header}</tr>\n{rows}</table>"

class PlainTextRenderer(ReportRenderer):
    """Renders report data as formatted plain text."""
    def render(self, data: ReportData) -> str:
        col_widths = {col: len(col) for col in data.columns}
        for record in data.records:
            for col in data.columns:
                col_widths[col] = max(col_widths[col], len(str(record.fields.get(col, ""))))

        header = " | ".join(col.ljust(col_widths[col]) for col in data.columns)
        separator = "-+-".join("-" * col_widths[col] for col in data.columns)
        lines = [header, separator]
        for record in data.records:
            row = " | ".join(
                str(record.fields.get(col, "")).ljust(col_widths[col])
                for col in data.columns
            )
            lines.append(row)
        return "\n".join(lines)


# --- SRP: ReportGenerator only orchestrates. It delegates fetching,
# transforming, and rendering to injected collaborators (DIP). ---

class ReportGenerator:
    """Orchestrates report generation.
    Depends on abstractions (DIP) — any source, any transform, any renderer."""

    def __init__(
        self,
        source: DataSource,
        renderer: ReportRenderer,
        transformer: DataTransformer | None = None,
    ) -> None:
        self.source = source
        self.renderer = renderer
        self.transformer = transformer

    def generate(self) -> str:
        """Fetch, optionally transform, then render."""
        data = self.source.fetch()
        if self.transformer:
            data = self.transformer.transform(data)
        return self.renderer.render(data)


# --- LSP: Every DataSource, DataTransformer, and ReportRenderer is fully
# substitutable. The ReportGenerator doesn't need isinstance() checks
# or special-case handling for any implementation. ---


# --- Usage ---
if __name__ == "__main__":
    # Generate a CSV of Engineering employees, sorted by salary (high to low)
    pipeline = TransformPipeline([
        FilterTransformer("department", "Engineering"),
        SortTransformer("salary", reverse=True),
    ])

    report = ReportGenerator(
        source=DatabaseSource("SELECT * FROM employees"),
        transformer=pipeline,
        renderer=CSVRenderer(),
    )
    print(report.generate())
    print()

    # Same data, different format — swap renderer, nothing else changes
    text_report = ReportGenerator(
        source=DatabaseSource("SELECT * FROM employees"),
        transformer=pipeline,
        renderer=PlainTextRenderer(),
    )
    print(text_report.generate())
```

**Key design decisions:**
- **Three independent interfaces** (`DataSource`, `DataTransformer`, `ReportRenderer`) avoid combinatorial explosion. You don't need `DatabaseCSVReport`, `DatabaseHTMLReport`, `APICSVReport`, etc. — just compose the pieces.
- **`TransformPipeline`** composes transformers without inheritance. New transforms slot in freely.
- **`ReportGenerator`** depends only on abstractions. You can swap any component independently.
- All five SOLID principles are applied, with ISP being especially visible in the clean separation of the three concerns into three interfaces.

</details>
