from banking_core import *

def run_banking_simulation():
    print("--- 🏦 Banking Application Simulation (OO + Patterns) 🏦 ---")
    
    # 1. Setup Strategies
    savings_strategy = SavingsInterest()
    current_strategy = CurrentInterest()

    # 2. Setup Accounts (Context, using Composition to set Strategy)
    account_s = SavingsAccount("S12345", 500.00, savings_strategy)
    account_c = CurrentAccount("C67890", 2000.00, current_strategy)

    # 3. Setup Customers (Observers)
    customer_a = Customer("Alice")
    customer_b = Customer("Bob")

    # 4. Attach Observers to the Savings Account (Subject)
    account_s.attach(customer_a)
    account_s.attach(customer_b)
    print("\n[INFO] Alice and Bob are now subscribed to Account S12345 updates.")

    # 5. Setup Invoker
    manager = TransactionManager()

    # =================================================================
    print("\n\n--- PHASE 1: Command & Observer Pattern Demo ---")
    # =================================================================

    # --- Deposit Transaction (Command executed) ---
    deposit_cmd = DepositCommand(account_s, 100.00)
    manager.execute_transaction(deposit_cmd)
    # EXPECTED: Command executes deposit. Observer pattern notifies Alice and Bob.

    # --- Withdrawal Transaction (Command executed) ---
    withdraw_cmd = WithdrawCommand(account_s, 50.00)
    manager.execute_transaction(withdraw_cmd)
    # EXPECTED: Command executes withdrawal. Observer pattern notifies Alice and Bob.

    # --- Undo Last Command ---
    manager.undo_last_transaction()
    # EXPECTED: Command undoes withdrawal (performs deposit). Observer notifies.
    
    print(f"\n[SUMMARY] Savings Account Balance after transactions and undo: ${account_s.get_balance():.2f}")


    # =================================================================
    print("\n\n--- PHASE 2: Strategy Pattern Demo (Interest Calculation) ---")
    # =================================================================

    # --- Calculate Interest on Savings Account ---
    print("\n--- Calculating Interest for Savings Account S12345 ---")
    # Polymorphism: Calls calculate_interest, which delegates to SavingsInterest strategy
    account_s.calculate_interest()
    # EXPECTED: 3% interest is added. Observer notifies.

    # --- Calculate Interest on Current Account ---
    print("\n--- Calculating Interest for Current Account C67890 ---")
    # Polymorphism: Calls calculate_interest, which delegates to CurrentInterest strategy
    account_c.calculate_interest()
    # EXPECTED: 0.5% interest is added (since balance > $500). Observer is NOT attached to C456.

    print(f"\n[SUMMARY] Final Savings Account Balance: ${account_s.get_balance():.2f}")
    print(f"[SUMMARY] Final Current Account Balance: ${account_c.get_balance():.2f}")

if __name__ == "__main__":
    run_banking_simulation()
