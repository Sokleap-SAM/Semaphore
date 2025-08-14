import threading
import time

# --- Bank Account Class ---
class BankAccount:
    """
    Represents a bank account with a balance and a lock for thread safety.
    The lock is used to protect the balance during transactions.
    """
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        # Create a lock for this specific account
        self.lock = threading.Lock()

    def deposit(self, amount):
        """Deposits money into the account."""
        self.balance += amount

    def withdraw(self, amount):
        """Withdraws money from the account."""
        self.balance -= amount

    def get_balance(self):
        """Returns the current balance."""
        return self.balance

# --- Transfer Function (Deadlock Prone) ---
def transfer(from_account, to_account, amount):
    """
    This function simulates a transfer of money from one account to another.
    It is designed to cause a deadlock by acquiring locks in a non-uniform order.
    """
    print(f"Transferring {amount} from {from_account.name} to {to_account.name}...")

    # Acquire the lock for the source account
    # In a real-world scenario, the order of acquiring locks is critical.
    # This example acquires locks based on the order they are passed to the function,
    # which can lead to a deadlock.
    from_account.lock.acquire()
    print(f"Thread for {from_account.name} acquired lock for {from_account.name}.")
    
    # Simulate some work or a context switch
    time.sleep(0.1)

    # Attempt to acquire the lock for the destination account
    print(f"Thread for {from_account.name} is waiting for lock on {to_account.name}...")
    to_account.lock.acquire()
    print(f"Thread for {from_account.name} acquired lock for {to_account.name}.")
    
    try:
        # Perform the transaction if both locks are held
        if from_account.get_balance() >= amount:
            from_account.withdraw(amount)
            to_account.deposit(amount)
            print(f"Transfer successful! {from_account.name}: {from_account.get_balance()}, {to_account.name}: {to_account.get_balance()}")
        else:
            print(f"Transfer failed: Insufficient funds in {from_account.name}")
    finally:
        # Release the locks in the reverse order of acquisition
        to_account.lock.release()
        from_account.lock.release()
        print(f"Thread for {from_account.name} released locks.")

# --- Main Program Execution ---
if __name__ == "__main__":
    # Create two bank accounts
    account_A = BankAccount("Account A", 100)
    account_B = BankAccount("Account B", 200)

    print("Initial Balances:")
    print(f"Account A: {account_A.get_balance()}")
    print(f"Account B: {account_B.get_balance()}")
    print("-" * 30)

    # Create two threads that will cause a deadlock
    # Thread 1 transfers A -> B, acquiring locks A then B
    thread1 = threading.Thread(target=transfer, args=(account_A, account_B, 50))
    
    # Thread 2 transfers B -> A, acquiring locks B then A
    # This non-uniform lock acquisition order is the source of the deadlock.
    thread2 = threading.Thread(target=transfer, args=(account_B, account_A, 30))

    print("Starting concurrent transfers...")
    thread1.start()
    thread2.start()

    # The program will hang here, as the threads are deadlocked.
    thread1.join()
    thread2.join()

    print("-" * 30)
    print("Final Balances:")
    print(f"Account A: {account_A.get_balance()}")
    print(f"Account B: {account_B.get_balance()}")
