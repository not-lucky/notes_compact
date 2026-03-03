# Design Patterns

Design patterns are typical solutions to common problems in software design. They are like pre-made blueprints that you can customize to solve a recurring design problem in your code. The Gang of Four (GoF) categorized 23 patterns into three groups: Creational, Structural, and Behavioral.

**Key insight:** Patterns are about *intent*, not structure. Two patterns can look identical in code but solve different problems. Always ask "what problem does this solve?" before reaching for a pattern.

> **Prerequisites:** [SOLID Principles](./01-solid-principles.md)

## 1. Creational Patterns
How objects are created, abstracting the instantiation process. These patterns decouple the client code from the concrete classes it needs to instantiate.

### Singleton
Ensures a class has only one instance and provides a global point of access to it.
- **How to recognize**: When you need a single shared resource (e.g., a Database connection, a Logger, or a Configuration manager).
- **Interviewer favorite**: "How do you make it thread-safe?" (Double-checked locking).
- **Use case**: Database connection pool, Logging service, Application configuration.
- **Why use it**: Guarantees exactly one instance exists, providing coordinated access to a shared resource. Avoids the overhead of creating multiple instances of expensive objects.
- **When NOT to use**: When you're using it as a glorified global variable. If the singleton doesn't manage shared state or a scarce resource, prefer dependency injection instead. Singletons make unit testing harder because they carry state across tests.

> **Interview Tip: Thread-safe Singleton in Python**
> In a multi-threaded environment, a simple Singleton can fail if two threads enter `__new__` simultaneously. Use a lock to ensure only one instance is created:

```python
import threading


class DatabaseConnection:
    """Thread-safe Singleton for a database connection pool.

    Uses double-checked locking: the first check avoids acquiring the lock
    on every call, the second check (inside the lock) prevents race conditions.
    """

    _instance: "DatabaseConnection | None" = None
    _lock: threading.Lock = threading.Lock()
    _initialized: bool = False

    def __new__(cls) -> "DatabaseConnection":
        if cls._instance is None:          # First check (no lock)
            with cls._lock:
                if cls._instance is None:  # Second check (with lock)
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self.connection_string = "postgresql://localhost:5432/mydb"
        print(f"Connecting to {self.connection_string}")

    def query(self, sql: str) -> str:
        return f"Executing: {sql}"


# Usage
db1 = DatabaseConnection()  # Connecting to postgresql://localhost:5432/mydb
db2 = DatabaseConnection()  # No output — same instance reused
print(db1 is db2)           # True
print(db1.query("SELECT 1"))  # Executing: SELECT 1
```

### Factory Method
Provides an interface for creating objects in a superclass, but allows subclasses to alter the type of objects that will be created.
- **How to recognize**: When the exact type of the object isn't known until runtime (e.g., reading a file extension to decide which parser to use).
- **Use case**: A document reader that supports PDF, Docx, and TXT. A notification system that creates Email/SMS/Push notifications based on user preferences.
- **Why use it**: Decouples object creation from usage. Adding a new product type only requires a new subclass — existing code stays untouched (Open/Closed Principle).
- **When NOT to use**: If you only have one or two product types that are unlikely to change, a simple `if/else` is clearer. Don't introduce a factory for the sake of having a factory.

```python
from abc import ABC, abstractmethod


class Notification(ABC):
    """Abstract product."""

    @abstractmethod
    def send(self, message: str) -> str:
        ...


class EmailNotification(Notification):
    def send(self, message: str) -> str:
        return f"Email sent: {message}"


class SMSNotification(Notification):
    def send(self, message: str) -> str:
        return f"SMS sent: {message}"


class PushNotification(Notification):
    def send(self, message: str) -> str:
        return f"Push notification sent: {message}"


class NotificationFactory(ABC):
    """Creator — declares the factory method."""

    @abstractmethod
    def create_notification(self) -> Notification:
        ...

    def notify(self, message: str) -> str:
        """Uses the factory method. Client code calls this, not create_notification."""
        notification = self.create_notification()
        return notification.send(message)


class EmailFactory(NotificationFactory):
    def create_notification(self) -> Notification:
        return EmailNotification()


class SMSFactory(NotificationFactory):
    def create_notification(self) -> Notification:
        return SMSNotification()


class PushFactory(NotificationFactory):
    def create_notification(self) -> Notification:
        return PushNotification()


# Usage
factories: dict[str, NotificationFactory] = {
    "email": EmailFactory(),
    "sms": SMSFactory(),
    "push": PushFactory(),
}

user_pref = "sms"
result = factories[user_pref].notify("Your order shipped!")
print(result)  # SMS sent: Your order shipped!
```

### Abstract Factory
Provides an interface for creating families of related or dependent objects without specifying their concrete classes.
- **How to recognize**: When you have multiple families of products that should be used together (e.g., Windows buttons must go with Windows checkboxes, not Mac checkboxes).
- **Use case**: A UI toolkit that creates Windows-style vs Mac-style buttons and checkboxes. A database access layer that creates connections + queries for MySQL vs PostgreSQL.
- **Why use it**: Ensures product compatibility within a family. The client code never mixes incompatible products (e.g., a Windows button with a Mac checkbox).
- **When NOT to use**: If you only have one product family or products don't need to be used together. The pattern adds significant complexity — make sure you actually need the family constraint.
- **Factory Method vs Abstract Factory**: Factory Method creates *one* product type via inheritance (each subclass overrides a single creation method). Abstract Factory creates *families* of related products via composition (the factory object has multiple creation methods that produce compatible products).

```python
from abc import ABC, abstractmethod


# --- Abstract Products ---
class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        ...


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str:
        ...


# --- Concrete Products: Windows family ---
class WindowsButton(Button):
    def render(self) -> str:
        return "[Windows Button]"


class WindowsCheckbox(Checkbox):
    def render(self) -> str:
        return "[Windows ☑]"


# --- Concrete Products: Mac family ---
class MacButton(Button):
    def render(self) -> str:
        return "[Mac Button]"


class MacCheckbox(Checkbox):
    def render(self) -> str:
        return "[Mac ☑]"


# --- Abstract Factory ---
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        ...

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        ...


class WindowsUIFactory(UIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()


class MacUIFactory(UIFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()


# --- Client code: works with any factory ---
def render_ui(factory: UIFactory) -> None:
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    print(f"Button: {button.render()}, Checkbox: {checkbox.render()}")


# Usage
render_ui(WindowsUIFactory())  # Button: [Windows Button], Checkbox: [Windows ☑]
render_ui(MacUIFactory())      # Button: [Mac Button], Checkbox: [Mac ☑]
```

### Builder
Separates the construction of a complex object from its representation, allowing the same construction process to create different representations.
- **How to recognize**: When an object has many optional parameters or a complex construction process (the "Telescoping Constructor" problem — `__init__` with 10+ parameters).
- **Use case**: A `QueryBuilder` for SQL, an `HttpRequest` builder, or constructing complex configuration objects.
- **Why use it**: Makes complex object construction readable via method chaining. Each step is named and self-documenting, unlike a constructor with positional args.
- **When NOT to use**: If your object has 2-3 required fields and no optional ones. A simple constructor or dataclass is cleaner. Don't wrap a trivial object in a builder.

```python
from dataclasses import dataclass, field


@dataclass
class HttpRequest:
    """The product — a complex object with many optional parts."""
    method: str = "GET"
    url: str = ""
    headers: dict[str, str] = field(default_factory=dict)
    body: str | None = None
    timeout: int = 30
    retries: int = 0


class HttpRequestBuilder:
    """Builder with fluent interface (method chaining)."""

    def __init__(self, method: str, url: str) -> None:
        self._request = HttpRequest(method=method, url=url)

    def with_header(self, key: str, value: str) -> "HttpRequestBuilder":
        self._request.headers[key] = value
        return self

    def with_body(self, body: str) -> "HttpRequestBuilder":
        self._request.body = body
        return self

    def with_timeout(self, seconds: int) -> "HttpRequestBuilder":
        self._request.timeout = seconds
        return self

    def with_retries(self, count: int) -> "HttpRequestBuilder":
        self._request.retries = count
        return self

    def build(self) -> HttpRequest:
        if not self._request.url:
            raise ValueError("URL is required")
        return self._request


# Usage — reads like a sentence
request = (
    HttpRequestBuilder("POST", "https://api.example.com/users")
    .with_header("Content-Type", "application/json")
    .with_header("Authorization", "Bearer token123")
    .with_body('{"name": "Alice"}')
    .with_timeout(10)
    .with_retries(3)
    .build()
)
print(request)
# HttpRequest(method='POST', url='https://api.example.com/users',
#   headers={'Content-Type': 'application/json', 'Authorization': 'Bearer token123'},
#   body='{"name": "Alice"}', timeout=10, retries=3)
```

---

## 2. Structural Patterns
How classes and objects are composed to form larger structures. These patterns explain how to assemble objects and classes into larger structures while keeping these structures flexible and efficient.

### Adapter
Allows objects with incompatible interfaces to collaborate by wrapping one interface to match another.
- **How to recognize**: When you have an existing class but its interface doesn't match the one you need (e.g., a 3rd party API that returns XML while your app expects JSON).
- **Use case**: Integrating a 3rd party legacy library into your modern system. Wrapping a REST API to look like a local service.
- **Why use it**: Lets you reuse existing code without modification (Open/Closed Principle). The adapter translates calls between the client's expected interface and the adaptee's actual interface.
- **When NOT to use**: If you control both interfaces, refactor them to be compatible instead. Adapters are for code you *can't* change (3rd party, legacy).

```python
from abc import ABC, abstractmethod
import json


class PaymentProcessor(ABC):
    """Target interface — what our application expects."""

    @abstractmethod
    def pay(self, amount: float, currency: str) -> dict:
        ...


# --- Legacy 3rd-party library we can't modify ---
class LegacyPayPalSDK:
    """Adaptee — incompatible interface from a 3rd party."""

    def make_payment(self, amount_in_cents: int, currency_code: str) -> str:
        return json.dumps({
            "status": "OK",
            "charged": amount_in_cents,
            "currency": currency_code,
        })


# --- Adapter ---
class PayPalAdapter(PaymentProcessor):
    """Adapts LegacyPayPalSDK to our PaymentProcessor interface."""

    def __init__(self, paypal_sdk: LegacyPayPalSDK) -> None:
        self._sdk = paypal_sdk

    def pay(self, amount: float, currency: str) -> dict:
        # Translate: dollars -> cents, parse JSON string -> dict
        amount_cents = int(amount * 100)
        raw_response = self._sdk.make_payment(amount_cents, currency.upper())
        return json.loads(raw_response)


# Usage — client code only knows about PaymentProcessor
def checkout(processor: PaymentProcessor, amount: float) -> None:
    result = processor.pay(amount, "usd")
    print(f"Payment result: {result}")


adapter = PayPalAdapter(LegacyPayPalSDK())
checkout(adapter, 29.99)
# Payment result: {'status': 'OK', 'charged': 2999, 'currency': 'USD'}
```

### Proxy
Provides a surrogate or placeholder for another object to control access to it.
- **How to recognize**: When you need to control access to an object — lazy initialization, access control, caching, or logging — without the client knowing it's not talking to the real object.
- **Use case**: Lazy loading a heavy object (like an image), caching expensive results, or adding an auth layer to a service.
- **Why use it**: Controls access to the real object without the client knowing. The proxy has the same interface as the real object, so swapping is transparent.
- **Types**: Virtual proxy (lazy loading), Protection proxy (access control), Caching proxy, Logging proxy.
- **When NOT to use**: If the overhead of the proxy layer isn't justified. A proxy that just delegates every call without adding behavior is pointless abstraction.

```python
from abc import ABC, abstractmethod
import time


class DataService(ABC):
    """Subject interface."""

    @abstractmethod
    def fetch_data(self, query: str) -> str:
        ...


class SlowDatabaseService(DataService):
    """Real subject — expensive to call."""

    def fetch_data(self, query: str) -> str:
        time.sleep(0.01)  # Simulates slow DB call
        return f"Results for '{query}'"


class CachingProxy(DataService):
    """Caching proxy — caches results to avoid repeated expensive calls."""

    def __init__(self, real_service: DataService) -> None:
        self._service = real_service
        self._cache: dict[str, str] = {}

    def fetch_data(self, query: str) -> str:
        if query not in self._cache:
            print(f"  Cache MISS — fetching from DB: '{query}'")
            self._cache[query] = self._service.fetch_data(query)
        else:
            print(f"  Cache HIT: '{query}'")
        return self._cache[query]


# Usage
service = CachingProxy(SlowDatabaseService())
print(service.fetch_data("SELECT * FROM users"))
#   Cache MISS — fetching from DB: 'SELECT * FROM users'
# Results for 'SELECT * FROM users'

print(service.fetch_data("SELECT * FROM users"))
#   Cache HIT: 'SELECT * FROM users'
# Results for 'SELECT * FROM users'
```

### Facade
Provides a simplified interface to a library, a framework, or any other complex set of classes.
- **How to recognize**: When a subsystem is complex or difficult to use because it has many moving parts that must be coordinated.
- **Use case**: A `Computer` class that simplifies the process of starting many subsystems (CPU, RAM, HDD). A `VideoConverter` that wraps codec selection, audio extraction, and format conversion.
- **Why use it**: Reduces coupling between the client and the complex subsystem. The client only depends on the facade, not on 10 internal classes.
- **When NOT to use**: When the subsystem is already simple. A facade over a single class adds no value and just obscures the code.

```python
class EmailValidator:
    def validate(self, email: str) -> bool:
        return "@" in email and "." in email.split("@")[-1]


class FraudDetector:
    def check(self, email: str, amount: float) -> bool:
        """Returns True if transaction is safe."""
        return amount < 10_000


class PaymentGateway:
    def charge(self, email: str, amount: float) -> str:
        return f"Charged ${amount:.2f} to {email}"


class NotificationService:
    def send_receipt(self, email: str, charge_id: str) -> str:
        return f"Receipt sent to {email}: {charge_id}"


class CheckoutFacade:
    """Simplifies the complex checkout process into a single method.

    Without the facade, the client would need to coordinate 4 subsystems
    in the correct order, handling errors at each step.
    """

    def __init__(self) -> None:
        self._validator = EmailValidator()
        self._fraud = FraudDetector()
        self._gateway = PaymentGateway()
        self._notifier = NotificationService()

    def process_order(self, email: str, amount: float) -> str:
        if not self._validator.validate(email):
            return "Invalid email"
        if not self._fraud.check(email, amount):
            return "Transaction flagged as fraud"
        charge_result = self._gateway.charge(email, amount)
        self._notifier.send_receipt(email, charge_result)
        return f"Order complete: {charge_result}"


# Usage — client calls one method instead of coordinating 4 subsystems
checkout = CheckoutFacade()
print(checkout.process_order("alice@example.com", 49.99))
# Order complete: Charged $49.99 to alice@example.com

print(checkout.process_order("bad-email", 49.99))
# Invalid email
```

### Decorator
Lets you attach new behaviors to objects by placing these objects inside special wrapper objects that contain the behaviors. Follows the same interface as the wrapped object.
- **How to recognize**: When you want to add responsibilities to individual objects dynamically and transparently, without affecting other objects. When subclassing would create an explosion of subclasses.
- **Use case**: Adding compression + encryption to a data stream. Adding logging + retry to an API client. Java's `BufferedReader(new FileReader(...))` is a classic example.
- **Why use it**: Follows Open/Closed Principle — add behavior without modifying existing code. Decorators can be stacked/composed, which is far more flexible than inheritance.
- **When NOT to use**: If the order of decoration matters and is easy to get wrong. If you only need one fixed combination, a simple subclass is clearer than 3 stacked decorators.
- **Decorator vs Proxy**: Both wrap an object with the same interface. Proxy *controls access* to the real object (caching, auth, lazy loading); Decorator *adds new behavior* (formatting, logging, encryption). A proxy usually creates or manages the lifecycle of its subject; a decorator receives it from the client and can be stacked arbitrarily.

```python
from abc import ABC, abstractmethod


class TextFormatter(ABC):
    """Component interface."""

    @abstractmethod
    def format(self, text: str) -> str:
        ...


class PlainText(TextFormatter):
    """Concrete component."""

    def format(self, text: str) -> str:
        return text


class BoldDecorator(TextFormatter):
    """Adds bold formatting."""

    def __init__(self, wrapped: TextFormatter) -> None:
        self._wrapped = wrapped

    def format(self, text: str) -> str:
        return f"<b>{self._wrapped.format(text)}</b>"


class ItalicDecorator(TextFormatter):
    """Adds italic formatting."""

    def __init__(self, wrapped: TextFormatter) -> None:
        self._wrapped = wrapped

    def format(self, text: str) -> str:
        return f"<i>{self._wrapped.format(text)}</i>"


class UpperCaseDecorator(TextFormatter):
    """Converts to uppercase."""

    def __init__(self, wrapped: TextFormatter) -> None:
        self._wrapped = wrapped

    def format(self, text: str) -> str:
        return self._wrapped.format(text).upper()


# Usage — decorators stack, order matters
plain = PlainText()
bold_italic = BoldDecorator(ItalicDecorator(plain))
print(bold_italic.format("hello"))  # <b><i>hello</i></b>

upper_bold = UpperCaseDecorator(BoldDecorator(plain))
print(upper_bold.format("hello"))   # <B>HELLO</B>
```

---

## 3. Behavioral Patterns
Concerned with algorithms and the assignment of responsibilities between objects. These patterns define how objects communicate and distribute work.

### Observer
Defines a subscription mechanism to notify multiple objects about any events that happen to the object they're observing. Also known as Pub/Sub.
- **How to recognize**: When a change to one object requires changing others, and you don't know how many objects need to be changed.
- **Use case**: A YouTube channel notifying subscribers of a new video. Event systems in UI frameworks. Stock price watchers.
- **Why use it**: Decouples the subject from its observers. The subject doesn't need to know *who* is listening or *how many* listeners there are — it just fires events.
- **When NOT to use**: When you have a simple one-to-one relationship — a direct method call is clearer. Also be careful in complex systems: observer chains can create hard-to-debug cascading updates.

```python
from abc import ABC, abstractmethod


class EventListener(ABC):
    """Observer interface."""

    @abstractmethod
    def update(self, event: str, data: str) -> None:
        ...


class EventManager:
    """Subject — manages subscriptions and notifications."""

    def __init__(self) -> None:
        self._listeners: dict[str, list[EventListener]] = {}

    def subscribe(self, event: str, listener: EventListener) -> None:
        self._listeners.setdefault(event, []).append(listener)

    def unsubscribe(self, event: str, listener: EventListener) -> None:
        self._listeners.get(event, []).remove(listener)

    def notify(self, event: str, data: str) -> None:
        for listener in self._listeners.get(event, []):
            listener.update(event, data)


class LoggingListener(EventListener):
    def update(self, event: str, data: str) -> None:
        print(f"[LOG] {event}: {data}")


class SlackNotifier(EventListener):
    def update(self, event: str, data: str) -> None:
        print(f"[SLACK] #{event} → {data}")


# Usage
events = EventManager()
logger = LoggingListener()
slack = SlackNotifier()

events.subscribe("deploy", logger)
events.subscribe("deploy", slack)
events.subscribe("error", logger)

events.notify("deploy", "v2.1.0 deployed to prod")
# [LOG] deploy: v2.1.0 deployed to prod
# [SLACK] #deploy → v2.1.0 deployed to prod

events.notify("error", "NullPointerException in PaymentService")
# [LOG] error: NullPointerException in PaymentService
```

### Command
Turns a request into a stand-alone object that contains all information about the request. This enables parameterization, queuing, logging, and undoing of operations.
- **How to recognize**: When you want to parametrize objects with operations, queue operations, or support undoable operations.
- **Use case**: A remote control where each button is a command, allowing for "Undo" functionality. A text editor with undo/redo. A job queue.
- **Why use it**: Decouples the invoker (what triggers the action) from the receiver (what performs the action). Enables undo/redo by storing command history.
- **When NOT to use**: When operations are simple and don't need undo/redo or queuing. Wrapping `light.turn_on()` in a Command object when you'll never undo it is over-engineering.

```python
from abc import ABC, abstractmethod


class Command(ABC):
    """Command interface with execute and undo."""

    @abstractmethod
    def execute(self) -> None:
        ...

    @abstractmethod
    def undo(self) -> None:
        ...


class TextEditor:
    """Receiver — the object that performs actual work."""

    def __init__(self) -> None:
        self.content: str = ""

    def __repr__(self) -> str:
        return f"TextEditor('{self.content}')"


class InsertTextCommand(Command):
    def __init__(self, editor: TextEditor, text: str, position: int) -> None:
        self._editor = editor
        self._text = text
        self._position = position

    def execute(self) -> None:
        self._editor.content = (
            self._editor.content[:self._position]
            + self._text
            + self._editor.content[self._position:]
        )

    def undo(self) -> None:
        self._editor.content = (
            self._editor.content[:self._position]
            + self._editor.content[self._position + len(self._text):]
        )


class CommandHistory:
    """Invoker — stores and manages command execution."""

    def __init__(self) -> None:
        self._history: list[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._history.append(command)

    def undo(self) -> None:
        if self._history:
            command = self._history.pop()
            command.undo()


# Usage
editor = TextEditor()
history = CommandHistory()

history.execute(InsertTextCommand(editor, "Hello", 0))
print(editor)  # TextEditor('Hello')

history.execute(InsertTextCommand(editor, " World", 5))
print(editor)  # TextEditor('Hello World')

history.undo()
print(editor)  # TextEditor('Hello')

history.undo()
print(editor)  # TextEditor('')
```

### State
Allows an object to alter its behavior when its internal state changes. The object will appear to change its class.
- **How to recognize**: When an object's behavior depends on its state, and it must change its behavior at runtime (replaces giant `if/else` or `match` on `self.status`).
- **Use case**: An ATM machine (Idle, HasCard, NoCash), a Vending Machine, a TCP connection (Listen, Established, Closed), or an Order (Pending, Shipped, Delivered).
- **Why use it**: Each state is a separate class with its own logic. Adding a new state doesn't require modifying existing states (Open/Closed Principle). Eliminates complex conditional logic.
- **When NOT to use**: If your object only has 2-3 states with simple transitions. A state machine with 2 boolean flags is over-engineering what an `if/else` handles cleanly.
- **State vs Strategy**: Both use composition to delegate behavior to an interchangeable object. The key difference: State transitions happen *internally* (the object changes its own state, and states know about each other). Strategy is chosen *externally* by the client (strategies are independent and unaware of each other).

```python
from abc import ABC, abstractmethod


class OrderState(ABC):
    """State interface — each state knows what transitions are valid."""

    @abstractmethod
    def proceed(self, order: "Order") -> str:
        ...

    @abstractmethod
    def cancel(self, order: "Order") -> str:
        ...


class PendingState(OrderState):
    def proceed(self, order: "Order") -> str:
        order.state = ShippedState()
        return "Order shipped!"

    def cancel(self, order: "Order") -> str:
        order.state = CancelledState()
        return "Order cancelled."


class ShippedState(OrderState):
    def proceed(self, order: "Order") -> str:
        order.state = DeliveredState()
        return "Order delivered!"

    def cancel(self, order: "Order") -> str:
        return "Cannot cancel — already shipped."


class DeliveredState(OrderState):
    def proceed(self, order: "Order") -> str:
        return "Order already delivered."

    def cancel(self, order: "Order") -> str:
        return "Cannot cancel — already delivered."


class CancelledState(OrderState):
    def proceed(self, order: "Order") -> str:
        return "Cannot proceed — order is cancelled."

    def cancel(self, order: "Order") -> str:
        return "Already cancelled."


class Order:
    """Context — delegates behavior to the current state object."""

    def __init__(self) -> None:
        self.state: OrderState = PendingState()

    def proceed(self) -> str:
        return self.state.proceed(self)

    def cancel(self) -> str:
        return self.state.cancel(self)


# Usage — no if/else anywhere
order = Order()
print(order.proceed())  # Order shipped!
print(order.cancel())   # Cannot cancel — already shipped.
print(order.proceed())  # Order delivered!
print(order.proceed())  # Order already delivered.
```

### Strategy
Defines a family of algorithms, puts each of them into a separate class, and makes their objects interchangeable.
- **How to recognize**: When you have multiple ways of doing the same thing and want to switch between them at runtime.
- **Use case**: Different compression algorithms (zip, gzip, bzip2), different payment methods (credit card, PayPal, crypto), or different sorting strategies.
- **Why use it**: Follows Open/Closed Principle — add new algorithms without modifying the context. Eliminates conditional statements for algorithm selection.
- **When NOT to use**: If you only have two algorithms that won't change. A simple `if/else` is more readable than creating 3 classes for 2 strategies. Also overkill if the client never needs to switch at runtime.

```python
from abc import ABC, abstractmethod


class PricingStrategy(ABC):
    """Strategy interface."""

    @abstractmethod
    def calculate(self, base_price: float) -> float:
        ...


class RegularPricing(PricingStrategy):
    def calculate(self, base_price: float) -> float:
        return base_price


class MemberPricing(PricingStrategy):
    """10% discount for members."""

    def calculate(self, base_price: float) -> float:
        return base_price * 0.90


class PremiumPricing(PricingStrategy):
    """25% discount + free shipping (modeled as $5 off)."""

    def calculate(self, base_price: float) -> float:
        return base_price * 0.75 - 5.0


class ShoppingCart:
    """Context — uses a strategy to calculate final price."""

    def __init__(self, strategy: PricingStrategy) -> None:
        self._strategy = strategy
        self._items: list[float] = []

    def set_strategy(self, strategy: PricingStrategy) -> None:
        """Swap strategy at runtime."""
        self._strategy = strategy

    def add_item(self, price: float) -> None:
        self._items.append(price)

    def total(self) -> float:
        base = sum(self._items)
        return self._strategy.calculate(base)


# Usage
cart = ShoppingCart(RegularPricing())
cart.add_item(100.0)
cart.add_item(50.0)
print(f"Regular: ${cart.total():.2f}")   # Regular: $150.00

cart.set_strategy(MemberPricing())
print(f"Member: ${cart.total():.2f}")    # Member: $135.00

cart.set_strategy(PremiumPricing())
print(f"Premium: ${cart.total():.2f}")   # Premium: $107.50
```

### Template Method
Defines the skeleton of an algorithm in the superclass but lets subclasses override specific steps of the algorithm without changing its structure.
- **How to recognize**: When you have a fixed workflow but individual steps might vary.
- **Use case**: A data mining tool where the sequence of steps (open, extract, parse, close) is fixed, but the extraction logic varies by file type. Test frameworks where setup/test/teardown order is fixed.
- **Why use it**: Eliminates code duplication — the invariant parts of the algorithm live in the base class. Subclasses only override what's different.
- **When NOT to use**: If subclasses need to change the *order* of steps, not just individual steps. If the algorithm varies dramatically between types, Strategy is usually a better fit.

```python
from abc import ABC, abstractmethod


class DataExporter(ABC):
    """Abstract class with the template method."""

    def export(self, data: list[dict]) -> str:
        """Template method — defines the skeleton. Subclasses CANNOT override this."""
        self.validate(data)
        header = self.build_header(data)
        body = self.build_body(data)
        footer = self.build_footer(data)
        return f"{header}\n{body}\n{footer}"

    def validate(self, data: list[dict]) -> None:
        """Hook — optional override. Default validates non-empty."""
        if not data:
            raise ValueError("No data to export")

    @abstractmethod
    def build_header(self, data: list[dict]) -> str:
        ...

    @abstractmethod
    def build_body(self, data: list[dict]) -> str:
        ...

    def build_footer(self, data: list[dict]) -> str:
        """Hook — optional override with default."""
        return f"--- {len(data)} records ---"


class CSVExporter(DataExporter):
    def build_header(self, data: list[dict]) -> str:
        return ",".join(data[0].keys())

    def build_body(self, data: list[dict]) -> str:
        return "\n".join(",".join(str(v) for v in row.values()) for row in data)


class MarkdownExporter(DataExporter):
    def build_header(self, data: list[dict]) -> str:
        keys = list(data[0].keys())
        header = "| " + " | ".join(keys) + " |"
        sep = "| " + " | ".join("---" for _ in keys) + " |"
        return f"{header}\n{sep}"

    def build_body(self, data: list[dict]) -> str:
        return "\n".join(
            "| " + " | ".join(str(v) for v in row.values()) + " |"
            for row in data
        )


# Usage
records = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]

print(CSVExporter().export(records))
# name,age
# Alice,30
# Bob,25
# --- 2 records ---

print()

print(MarkdownExporter().export(records))
# | name | age |
# | --- | --- |
# | Alice | 30 |
# | Bob | 25 |
# --- 2 records ---
```

---

## Pattern Summary Table

| Pattern | Type | Key Goal | Pitfalls |
|---------|------|----------|----------|
| **Singleton** | Creational | One instance only | Hard to test, hidden dependencies |
| **Factory Method** | Creational | Defer instantiation to subclasses | Can lead to many subclasses |
| **Abstract Factory** | Creational | Families of related objects | Complex to implement initially |
| **Builder** | Creational | Step-by-step complex construction | Overkill for simple objects |
| **Adapter** | Structural | Interface translation | Adds overhead with wrapper classes |
| **Proxy** | Structural | Access control / Lazy load | May delay responses, adds complexity |
| **Facade** | Structural | Simple interface to complex system | Can become a "God Object" |
| **Decorator** | Structural | Add behavior dynamically | Stacking order can be confusing |
| **Observer** | Behavioral | Event notification (pub/sub) | Memory leaks if not unsubscribed |
| **Command** | Behavioral | Request as object (undo/redo) | Code bloat with many small classes |
| **State** | Behavioral | State-dependent behavior | Overkill for few states |
| **Strategy** | Behavioral | Swappable algorithms | Client must know about strategies |
| **Template Method** | Behavioral | Algorithm skeleton with hooks | Liskov Substitution violations possible |

---

## Practice Problems

### Problem 1: Logger System (Easy)
**Objective**: Apply the Singleton and Strategy patterns.

Design a `Logger` that:
1. Is a Singleton (only one instance exists).
2. Supports different output strategies: `ConsoleOutput` and `FileOutput` (just simulate — print to console with a prefix).
3. Has `log(level: str, message: str)` method.

<details>
<summary><b>Solution</b></summary>

```python
import threading
from abc import ABC, abstractmethod


class OutputStrategy(ABC):
    @abstractmethod
    def write(self, message: str) -> None:
        ...


class ConsoleOutput(OutputStrategy):
    def write(self, message: str) -> None:
        print(f"[CONSOLE] {message}")


class FileOutput(OutputStrategy):
    def __init__(self, filename: str) -> None:
        self._filename = filename

    def write(self, message: str) -> None:
        print(f"[FILE:{self._filename}] {message}")


class Logger:
    """Singleton logger with swappable output strategy."""

    _instance: "Logger | None" = None
    _lock: threading.Lock = threading.Lock()
    _initialized: bool = False

    def __new__(cls) -> "Logger":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._strategy: OutputStrategy = ConsoleOutput()

    def set_output(self, strategy: OutputStrategy) -> None:
        self._strategy = strategy

    def log(self, level: str, message: str) -> None:
        self._strategy.write(f"{level.upper()}: {message}")


# Test
logger1 = Logger()
logger2 = Logger()
assert logger1 is logger2  # Same instance

logger1.log("info", "App started")
# [CONSOLE] INFO: App started

logger1.set_output(FileOutput("app.log"))
logger1.log("error", "Something broke")
# [FILE:app.log] ERROR: Something broke
```

**Patterns used**: Singleton (one logger instance), Strategy (swappable output).

</details>

### Problem 2: Notification System with Decorators (Medium)
**Objective**: Apply the Decorator and Factory Method patterns.

Design a notification system where:
1. Base notification types: `EmailNotification`, `SMSNotification` (Factory Method creates them).
2. Decorators can add features: `EncryptedNotification` (wraps message in `[ENCRYPTED]`), `UrgentNotification` (prepends `[URGENT]`).
3. Decorators are stackable — a notification can be both urgent and encrypted.

<details>
<summary><b>Solution</b></summary>

```python
from abc import ABC, abstractmethod


# --- Base ---
class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        ...


class EmailNotification(Notification):
    def __init__(self, address: str) -> None:
        self._address = address

    def send(self, message: str) -> str:
        return f"Email to {self._address}: {message}"


class SMSNotification(Notification):
    def __init__(self, phone: str) -> None:
        self._phone = phone

    def send(self, message: str) -> str:
        return f"SMS to {self._phone}: {message}"


# --- Decorators ---
class NotificationDecorator(Notification, ABC):
    def __init__(self, wrapped: Notification) -> None:
        self._wrapped = wrapped


class EncryptedNotification(NotificationDecorator):
    def send(self, message: str) -> str:
        return self._wrapped.send(f"[ENCRYPTED]{message}[/ENCRYPTED]")


class UrgentNotification(NotificationDecorator):
    def send(self, message: str) -> str:
        return self._wrapped.send(f"[URGENT] {message}")


# --- Factory ---
class NotificationFactory(ABC):
    @abstractmethod
    def create(self) -> Notification:
        ...


class EmailFactory(NotificationFactory):
    def __init__(self, address: str) -> None:
        self._address = address

    def create(self) -> Notification:
        return EmailNotification(self._address)


class SMSFactory(NotificationFactory):
    def __init__(self, phone: str) -> None:
        self._phone = phone

    def create(self) -> Notification:
        return SMSNotification(self._phone)


# Test
factory = EmailFactory("alice@example.com")
notif = factory.create()

# Stack decorators: Encrypted wraps Urgent wraps Email
encrypted_urgent = EncryptedNotification(UrgentNotification(notif))
print(encrypted_urgent.send("Server is down"))
# Email to alice@example.com: [URGENT] [ENCRYPTED]Server is down[/ENCRYPTED]

sms = SMSFactory("+1234567890").create()
urgent_sms = UrgentNotification(sms)
print(urgent_sms.send("Deploy failed"))
# SMS to +1234567890: [URGENT] Deploy failed
```

**Patterns used**: Factory Method (create notifications), Decorator (add encryption/urgency).

</details>

### Problem 3: Document Workflow Engine (Hard)
**Objective**: Apply State, Command, and Observer patterns together.

Design a document workflow where:
1. A `Document` has states: `Draft`, `Review`, `Approved`, `Published`.
2. Transitions are commands (so they support undo): `SubmitForReview`, `Approve`, `Publish`.
3. An `AuditLog` observes all state changes and records them.
4. Invalid transitions (e.g., publishing a draft) raise an error message.

<details>
<summary><b>Solution</b></summary>

```python
from abc import ABC, abstractmethod


# --- Observer ---
class DocumentObserver(ABC):
    @abstractmethod
    def on_state_change(self, doc_name: str, old_state: str, new_state: str) -> None:
        ...


class AuditLog(DocumentObserver):
    def __init__(self) -> None:
        self.entries: list[str] = []

    def on_state_change(self, doc_name: str, old_state: str, new_state: str) -> None:
        entry = f"[AUDIT] '{doc_name}': {old_state} -> {new_state}"
        self.entries.append(entry)
        print(entry)


# --- State ---
class DocState(ABC):
    @abstractmethod
    def name(self) -> str:
        ...

    def submit(self, doc: "Document") -> bool:
        print(f"Cannot submit from {self.name()}")
        return False

    def approve(self, doc: "Document") -> bool:
        print(f"Cannot approve from {self.name()}")
        return False

    def publish(self, doc: "Document") -> bool:
        print(f"Cannot publish from {self.name()}")
        return False


class DraftState(DocState):
    def name(self) -> str:
        return "Draft"

    def submit(self, doc: "Document") -> bool:
        doc.set_state(ReviewState())
        return True


class ReviewState(DocState):
    def name(self) -> str:
        return "Review"

    def approve(self, doc: "Document") -> bool:
        doc.set_state(ApprovedState())
        return True


class ApprovedState(DocState):
    def name(self) -> str:
        return "Approved"

    def publish(self, doc: "Document") -> bool:
        doc.set_state(PublishedState())
        return True


class PublishedState(DocState):
    def name(self) -> str:
        return "Published"


# --- Document (Context) ---
class Document:
    def __init__(self, name: str) -> None:
        self.name = name
        self._state: DocState = DraftState()
        self._observers: list[DocumentObserver] = []

    @property
    def state_name(self) -> str:
        return self._state.name()

    def add_observer(self, observer: DocumentObserver) -> None:
        self._observers.append(observer)

    def set_state(self, new_state: DocState) -> None:
        old_name = self._state.name()
        self._state = new_state
        for obs in self._observers:
            obs.on_state_change(self.name, old_name, new_state.name())

    def submit(self) -> bool:
        return self._state.submit(self)

    def approve(self) -> bool:
        return self._state.approve(self)

    def publish(self) -> bool:
        return self._state.publish(self)


# --- Command with Undo ---
class Command(ABC):
    @abstractmethod
    def execute(self) -> bool:
        ...

    @abstractmethod
    def undo(self) -> None:
        ...


class SubmitForReviewCmd(Command):
    def __init__(self, doc: Document) -> None:
        self._doc = doc
        self._prev_state: DocState | None = None

    def execute(self) -> bool:
        self._prev_state = self._doc._state
        return self._doc.submit()

    def undo(self) -> None:
        if self._prev_state:
            self._doc.set_state(self._prev_state)


class ApproveCmd(Command):
    def __init__(self, doc: Document) -> None:
        self._doc = doc
        self._prev_state: DocState | None = None

    def execute(self) -> bool:
        self._prev_state = self._doc._state
        return self._doc.approve()

    def undo(self) -> None:
        if self._prev_state:
            self._doc.set_state(self._prev_state)


class PublishCmd(Command):
    def __init__(self, doc: Document) -> None:
        self._doc = doc
        self._prev_state: DocState | None = None

    def execute(self) -> bool:
        self._prev_state = self._doc._state
        return self._doc.publish()

    def undo(self) -> None:
        if self._prev_state:
            self._doc.set_state(self._prev_state)


# --- Test ---
doc = Document("Design Spec")
audit = AuditLog()
doc.add_observer(audit)

history: list[Command] = []

# Valid workflow
cmd1 = SubmitForReviewCmd(doc)
cmd1.execute()   # [AUDIT] 'Design Spec': Draft -> Review
history.append(cmd1)

cmd2 = ApproveCmd(doc)
cmd2.execute()   # [AUDIT] 'Design Spec': Review -> Approved
history.append(cmd2)

# Invalid transition
cmd_bad = SubmitForReviewCmd(doc)
cmd_bad.execute()  # Cannot submit from Approved

# Undo approval
history[-1].undo()  # [AUDIT] 'Design Spec': Approved -> Review
print(f"State after undo: {doc.state_name}")  # State after undo: Review

# Continue
cmd3 = ApproveCmd(doc)
cmd3.execute()   # [AUDIT] 'Design Spec': Review -> Approved
cmd4 = PublishCmd(doc)
cmd4.execute()   # [AUDIT] 'Design Spec': Approved -> Published

print(f"\nAudit trail ({len(audit.entries)} entries):")
for e in audit.entries:
    print(f"  {e}")
```

**Patterns used**: State (document lifecycle), Command (undoable transitions), Observer (audit logging).

</details>
