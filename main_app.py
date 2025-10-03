from banking_core import *

# 1. Setup Accounts and Strategies
# Note how we pass the Strategy object (Composition)
savings_strategy = SavingsInterest()
current_strategy = CurrentInterest()

account_s = SavingsAccount("S123", 500.00, savings_strategy)
account_c = CurrentAccount("C456", 2000.00, current_strategy)

# 2. Setup Customer (Observer)
customer_a = Customer("Alice")
customer_b = Customer("Bob")

# 3. Attach Observers (Account is the Subject)
account_s.attach(customer_a)
account_s.attach(customer_b)

# 4. Setup Invoker (Transaction Manager)
manager = TransactionManager()

print("\n--- PHASE 1: Observer & Command Pattern Demo ---")

# --- Deposit Transaction (Command executed) ---
deposit_cmd = DepositCommand(account_s, 100.00)
manager.execute_transaction(deposit_cmd)
# OUTPUT: Notice both Alice and Bob are notified (Observer Pattern)

# --- Withdrawal Transaction (Command executed) ---
withdraw_cmd = WithdrawCommand(account_s, 50.00)
manager.execute_transaction(withdraw_cmd)
# OUTPUT: Again, both Alice and Bob are notified

# --- Undo Last Command ---
manager.undo_last_transaction()
# OUTPUT: The withdrawal is reversed, and customers are notified of the change

print(f"\n--- Current Savings Account Balance: ${account_s.get_balance():.2f} ---")


print("\n--- PHASE 2: Strategy Pattern Demo ---")

# --- Calculate Interest on Savings Account ---
# The account delegates the calculation to the SavingsInterest strategy (Polymorphism)
account_s.calculate_interest()
# OUTPUT: 3% interest is calculated and deposited, triggering Observer notification.

# --- Calculate Interest on Current Account ---
# The account delegates the calculation to the CurrentInterest strategy
account_c.calculate_interest()
# OUTPUT: 0.5% interest is calculated and deposited, triggering Observer notification.

print(f"\n--- Final Savings Account Balance: ${account_s.get_balance():.2f} ---")