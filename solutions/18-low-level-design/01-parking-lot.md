### Parking Lot Design

### Problem Statement
Design a parking lot system that supports:
- Multiple levels and multiple spots per level.
- Different vehicle types (Motorcycle, Car, Bus).
- Different spot sizes (Small, Medium, Large).
- Basic parking and unparking functionality.
- Payment calculation based on duration.

### Optimal Python Solution

```python
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime
import math

class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    BUS = 3

class SpotSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class Vehicle(ABC):
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.parked_spot = None

class Motorcycle(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.MOTORCYCLE)

class Car(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.CAR)

class Bus(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.BUS)

class ParkingSpot:
    def __init__(self, spot_id: int, size: SpotSize):
        self.spot_id = spot_id
        self.size = size
        self.vehicle = None

    def is_available(self) -> bool:
        return self.vehicle is None

    def can_fit_vehicle(self, vehicle: Vehicle) -> bool:
        if vehicle.vehicle_type == VehicleType.MOTORCYCLE:
            return True # Fits in any spot
        if vehicle.vehicle_type == VehicleType.CAR:
            return self.size in [SpotSize.MEDIUM, SpotSize.LARGE]
        if vehicle.vehicle_type == VehicleType.BUS:
            return self.size == SpotSize.LARGE
        return False

    def park(self, vehicle: Vehicle):
        self.vehicle = vehicle
        vehicle.parked_spot = self

    def unpark(self):
        self.vehicle = None

class Level:
    def __init__(self, floor: int, num_spots: int):
        self.floor = floor
        self.spots = []
        # Simplified: Distribute spots by size
        for i in range(num_spots):
            if i < num_spots // 4:
                size = SpotSize.SMALL
            elif i < num_spots // 2:
                size = SpotSize.LARGE
            else:
                size = SpotSize.MEDIUM
            self.spots.append(ParkingSpot(i, size))

    def find_available_spot(self, vehicle: Vehicle) -> ParkingSpot | None:
        for spot in self.spots:
            if spot.is_available() and spot.can_fit_vehicle(vehicle):
                return spot
        return None

class ParkingLot:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ParkingLot, cls).__new__(cls)
            cls._instance.levels = []
        return cls._instance

    def add_level(self, level: Level):
        self.levels.append(level)

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        for level in self.levels:
            spot = level.find_available_spot(vehicle)
            if spot:
                spot.park(vehicle)
                print(f"Vehicle {vehicle.license_plate} parked at Level {level.floor}, Spot {spot.spot_id}")
                return True
        print("No available spots")
        return False

# --- Simplified Payment System ---

class Ticket:
    def __init__(self, vehicle: Vehicle):
        self.start_time = datetime.now()
        self.vehicle = vehicle

class PaymentSystem:
    RATE_PER_HOUR = {
        VehicleType.MOTORCYCLE: 10,
        VehicleType.CAR: 20,
        VehicleType.BUS: 50
    }

    @staticmethod
    def calculate_fee(ticket: Ticket) -> float:
        duration = datetime.now() - ticket.start_time
        hours = math.ceil(duration.total_seconds() / 3600)
        return hours * PaymentSystem.RATE_PER_HOUR[ticket.vehicle.vehicle_type]
```

### Explanation
1.  **Encapsulation**: Each class has a clear responsibility. `ParkingSpot` knows if it can fit a vehicle, `Level` manages a collection of spots, and `ParkingLot` (Singleton) manages levels.
2.  **Inheritance**: `Vehicle` is an abstract base class, allowing for different types of vehicles while sharing common traits like license plates.
3.  **Polymorphism**: `can_fit_vehicle` uses the vehicle's type to determine fitment logic.
4.  **Singleton Pattern**: `ParkingLot` ensures only one instance of the system exists.

### Complexity Analysis
- **Finding a spot**: O(L * S) where L is the number of levels and S is spots per level.
- **Space Complexity**: O(L * S) to store all spot objects.
