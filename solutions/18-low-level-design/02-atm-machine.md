### ATM Machine Design

### Problem Statement
Design an ATM system that:
- Allows users to insert a card, enter a PIN, and withdraw money.
- Manages different states (Idle, CardInserted, PinEntered, Dispensing).
- Dispenses money using various bill denominations (100, 50, 20, 10).

### Optimal Python Solution

```python
from abc import ABC, abstractmethod

# --- State Pattern ---

class ATMState(ABC):
    @abstractmethod
    def insert_card(self): pass
    @abstractmethod
    def enter_pin(self, pin: str): pass
    @abstractmethod
    def withdraw_money(self, amount: int): pass

class IdleState(ATMState):
    def __init__(self, atm): self.atm = atm
    def insert_card(self):
        print("Card inserted.")
        self.atm.set_state(self.atm.has_card_state)
    def enter_pin(self, pin): print("Insert card first.")
    def withdraw_money(self, amount): print("Insert card first.")

class HasCardState(ATMState):
    def __init__(self, atm): self.atm = atm
    def insert_card(self): print("Card already inserted.")
    def enter_pin(self, pin):
        if pin == "1234":
            print("PIN correct.")
            self.atm.set_state(self.atm.pin_entered_state)
        else:
            print("Wrong PIN.")
    def withdraw_money(self, amount): print("Enter PIN first.")

class PinEnteredState(ATMState):
    def __init__(self, atm): self.atm = atm
    def insert_card(self): print("Card already inserted.")
    def enter_pin(self, pin): print("PIN already entered.")
    def withdraw_money(self, amount):
        print(f"Withdrawing {amount}...")
        self.atm.dispense(amount)
        self.atm.set_state(self.atm.idle_state)

# --- Chain of Responsibility (Bill Dispenser) ---

class BillHandler(ABC):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    @abstractmethod
    def handle(self, amount: int):
        if self.next_handler:
            return self.next_handler.handle(amount)
        return amount

class ConcreteBillHandler(BillHandler):
    def __init__(self, denomination: int, next_handler=None):
        super().__init__(next_handler)
        self.denomination = denomination

    def handle(self, amount: int):
        num_bills = amount // self.denomination
        remainder = amount % self.denomination
        if num_bills > 0:
            print(f"Dispensing {num_bills} x ${self.denomination}")

        if remainder > 0:
            if self.next_handler:
                return self.next_handler.handle(remainder)
            else:
                print(f"Cannot dispense remaining ${remainder}")
        return remainder

# --- ATM Controller ---

class ATMMachine:
    def __init__(self):
        self.idle_state = IdleState(self)
        self.has_card_state = HasCardState(self)
        self.pin_entered_state = PinEnteredState(self)
        self.current_state = self.idle_state

        # Setup Dispenser Chain
        self.dispenser = ConcreteBillHandler(100,
                            ConcreteBillHandler(50,
                                ConcreteBillHandler(20,
                                    ConcreteBillHandler(10))))

    def set_state(self, state):
        self.current_state = state

    def insert_card(self): self.current_state.insert_card()
    def enter_pin(self, pin): self.current_state.enter_pin(pin)
    def withdraw(self, amount): self.current_state.withdraw_money(amount)

    def dispense(self, amount):
        self.dispenser.handle(amount)

# --- Example Usage ---
# atm = ATMMachine()
# atm.insert_card()
# atm.enter_pin("1234")
# atm.withdraw(280)
```

### Explanation
1.  **State Pattern**: The `ATMMachine` changes its behavior based on the current `ATMState`. This avoids messy `if-else` blocks for checking if a card is inserted or PIN is verified.
2.  **Chain of Responsibility**: The `BillHandler` objects form a chain. If the $100 handler can't handle the full amount, it passes the remainder to the $50 handler, and so on.

### Complexity Analysis
- **Withdrawal**: O(D) where D is the number of bill denominations.
- **Space**: O(D + S) where S is the number of states.
