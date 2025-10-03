from abc import ABC, abstractmethod

# ====================================================
# 1. Base Account (Abstraction, Encapsulation, Subject)
# ====================================================
class BaseAccount(ABC):
    def __init__(self, account_number, initial_balance=0):
        self._account_number = account_number
        self._balance = initial_balance
        self._observers = [] # Observer list

    # --- Observer Management Methods (Subject role) ---
    def attach(self, observer):
        """Adds an observer (Customer) to the list."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """Removes an observer from the list."""
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def _notify_observers(self, message):
        """Notifies all attached observers."""
        for observer in self._observers:
            observer.update(message)

    # --- Core banking methods (Trigger notifications) ---
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"Deposit successful. New balance: ${self._balance:.2f}")
            self._notify_observers(f"Deposit of ${amount:.2f} made.")
            return True
        return False

    def withdraw(self, amount):
        # NOTE: Concrete accounts can override this for specific rules (e.g., minimum balance)
        if amount > 0 and self._balance >= amount:
            self._balance -= amount
            print(f"Withdrawal successful. New balance: ${self._balance:.2f}")
            self._notify_observers(f"Withdrawal of ${amount:.2f} made.")
            return True
        print("Error: Insufficient funds or invalid amount.")
        return False
    
    # Simple getter method (used by strategies)
    def get_balance(self):
        return self._balance
    
    # Abstract method for Strategy Pattern
    @abstractmethod
    def calculate_interest(self):
        pass

# ====================================================
# 2. Concrete Accounts (Inheritance & Strategy Context)
# ====================================================
class SavingsAccount(BaseAccount):
    def __init__(self, account_number, initial_balance=0, interest_strategy=None):
        super().__init__(account_number, initial_balance)
        self.interest_strategy = interest_strategy # Strategy Composition

    # Strategy Pattern: Delegates calculation to the chosen strategy
    def calculate_interest(self):
        if self.interest_strategy:
            self.interest_strategy.calculate(self)

class CurrentAccount(BaseAccount):
    def __init__(self, account_number, initial_balance=0, interest_strategy=None):
        super().__init__(account_number, initial_balance)
        self.interest_strategy = interest_strategy

    def calculate_interest(self):
        if self.interest_strategy:
            self.interest_strategy.calculate(self)
            
# ====================================================
# 3. Customer Class (Concrete Observer)
# ====================================================
class Customer:
    def __init__(self, name):
        self.name = name

    def update(self, message):
        """This is the method called by the Subject (Account)."""
        print(f"[Customer {self.name} Notification]: Your account activity: {message}")

# ====================================================
# 4. Strategy Pattern (Interest Calculation)
# ====================================================
class InterestStrategy(ABC):
    """Strategy Interface: Defines the common method."""
    @abstractmethod
    def calculate(self, account):
        pass

class SavingsInterest(InterestStrategy):
    """Concrete Strategy 1: Savings rate."""
    def calculate(self, account):
        rate = 0.03 # 3%
        interest = account.get_balance() * rate
        # Use deposit() which updates balance and triggers the Observer notification
        account.deposit(interest) 
        print(f"SAVINGS Interest Calculated: ${interest:.2f} (3%)")

class CurrentInterest(InterestStrategy):
    """Concrete Strategy 2: Low Current rate."""
    def calculate(self, account):
        rate = 0.005 # 0.5%
        if account.get_balance() > 500:
            interest = account.get_balance() * rate
            account.deposit(interest)
            print(f"CURRENT Interest Calculated: ${interest:.2f} (0.5%)")
        else:
            print("CURRENT Interest: Balance too low to earn interest.")

# ====================================================
# 5. Command Pattern (Transactions & Undo)
# ====================================================
class Command(ABC):
    """Command Interface: Contract for execute and undo."""
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

class DepositCommand(Command):
    """Concrete Command: Encapsulates Deposit request."""
    def __init__(self, account: BaseAccount, amount: float):
        self._account = account
        self._amount = amount

    def execute(self):
        return self._account.deposit(self._amount) # Receiver performs the action

    def undo(self):
        print(f"[Undoing Command] Reversing Deposit of ${self._amount:.2f}...")
        return self._account.withdraw(self._amount) # To undo a deposit, withdraw

class WithdrawCommand(Command):
    """Concrete Command: Encapsulates Withdrawal request."""
    def __init__(self, account: BaseAccount, amount: float):
        self._account = account
        self._amount = amount

    def execute(self):
        return self._account.withdraw(self._amount)

    def undo(self):
        print(f"[Undoing Command] Reversing Withdrawal of ${self._amount:.2f}...")
        return self._account.deposit(self._amount) # To undo a withdrawal, deposit

# Invoker: Maintains history and executes commands
class TransactionManager:
    def __init__(self):
        self._history = [] # Stores executed commands for undo

    def execute_transaction(self, command: Command):
        print("\n--- Transaction Start ---")
        if command.execute():
            self._history.append(command)
            return True
        return False

    def undo_last_transaction(self):
        if not self._history:
            print("\nError: No transactions to undo.")
            return False
        
        last_command = self._history.pop()
        print("\n--- UNDO Start ---")
        last_command.undo()
        print("Successfully undone the last transaction.")
        return True
