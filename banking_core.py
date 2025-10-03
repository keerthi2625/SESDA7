# ----------------------------------------------------
# 1. Base Account (Abstraction & Encapsulation)
# ----------------------------------------------------
from abc import ABC, abstractmethod

# The BaseAccount acts as the abstract foundation and the Subject for the Observer Pattern
class BaseAccount(ABC):
    def __init__(self, account_number, initial_balance=0):
        # Encapsulation: Making balance private (conventionally with _)
        self._account_number = account_number
        self._balance = initial_balance
        # Observer list (will be used in Step 3)
        self._observers = []

    # Abstract methods force subclasses to implement them
    @abstractmethod
    def calculate_interest(self):
        pass

    # Core banking methods
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"Deposit successful. New balance: ${self._balance:.2f}")
            # Notification is triggered here (Step 3)
            self._notify_observers(f"Deposit of ${amount:.2f} made.")
            return True
        return False

    def withdraw(self, amount):
        if amount > 0 and self._balance >= amount:
            self._balance -= amount
            print(f"Withdrawal successful. New balance: ${self._balance:.2f}")
            # Notification is triggered here (Step 3)
            self._notify_observers(f"Withdrawal of ${amount:.2f} made.")
            return True
        print("Error: Insufficient funds or invalid amount.")
        return False
    
    # Simple getter method
    def get_balance(self):
        return self._balance

# ----------------------------------------------------
# 2. Concrete Accounts (Inheritance)
# ----------------------------------------------------
# Strategy Pattern reference will be added here later (Step 4)

class SavingsAccount(BaseAccount):
    # Initializes BaseAccount and sets its specific strategy (coming in Step 4)
    def __init__(self, account_number, initial_balance=0, interest_strategy=None):
        super().__init__(account_number, initial_balance)
        self.interest_strategy = interest_strategy # Composition reference

    # This method delegates work to the strategy
    def calculate_interest(self):
        if self.interest_strategy:
            self.interest_strategy.calculate(self)

class CurrentAccount(BaseAccount):
    # Initializes BaseAccount and sets its specific strategy (coming in Step 4)
    def __init__(self, account_number, initial_balance=0, interest_strategy=None):
        super().__init__(account_number, initial_balance)
        self.interest_strategy = interest_strategy

    def calculate_interest(self):
        if self.interest_strategy:
            self.interest_strategy.calculate(self)
            
# ----------------------------------------------------
# 3. Customer Class
# ----------------------------------------------------
# Also acts as the Concrete Observer (Step 3)

class Customer:
    def __init__(self, name):
        self.name = name

    def update(self, message):
        """This is the method called by the Subject (Account)"""
        print(f"[Customer {self.name} Notification]: Your account activity: {message}")