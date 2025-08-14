import threading
import time

# The initial value of the counter is set to 10.
# Process A adds 1, and Process B adds 2.
# The expected final value is 12, which means Process B's store
# operation must happen last.
counter = 10
print(f"Initial value of counter: {counter}")

# We create a single semaphore, 's', with an initial value of 0.
# This ensures that a 'wait' operation will block immediately,
# forcing a specific execution order between the two processes.
s = threading.Semaphore(0)

def process_A():
    """
    This function represents Process A.
    It simulates the operations, including signaling the semaphore before storing.
    """
    # The 'global' keyword is essential to modify the global 'counter' variable.
    global counter
    
    print("Process A has started.")
    
    # Simulate the LD (Load) instruction
    # A reads the initial value of counter (10)
    local_reg = counter
    
    # Simulate the ADDI (Add Immediate) instruction
    # A increments its local copy of the value (10 + 1 = 11)
    local_reg = local_reg + 1
    
    # Simulate some work
    time.sleep(0.1)
    
    print("Process A is signaling s...")
    # A signals 's', incrementing its value and potentially unblocking Process B.
    s.release()
    
    # Simulate the ST (Store) instruction
    # A stores its local value (11) back into the global counter.
    # This will be overwritten by Process B's store.
    counter = local_reg
    print(f"Process A has finished. Counter value is now: {counter}")
    
def process_B():
    """
    This function represents Process B.
    It simulates the operations, including waiting on the semaphore before storing.
    """
    # The 'global' keyword is essential to modify the global 'counter' variable.
    global counter

    print("Process B has started.")
    
    # Simulate the LD (Load) instruction
    # B also reads the initial value of counter (10)
    local_reg = counter
    
    # Simulate the ADDC (Add Constant) instruction
    # B increments its local copy of the value (10 + 2 = 12)
    local_reg = local_reg + 2
    
    # Simulate some work
    time.sleep(0.1)
    
    print("Process B is waiting on s...")
    # B waits on 's'. This will block until Process A calls 'release()'.
    s.acquire()
    
    # Simulate the ST (Store) instruction
    # Once unblocked, B stores its local value (12) into the global counter.
    # This happens after A's store, so the final value will be 12.
    counter = local_reg
    print(f"Process B has finished. Counter value is now: {counter}")

if __name__ == "__main__":
    # Create two threads, one for each process.
    thread_A = threading.Thread(target=process_A)
    thread_B = threading.Thread(target=process_B)
    
    # Start both threads.
    thread_A.start()
    thread_B.start()
    
    # Wait for both threads to complete their execution.
    thread_A.join()
    thread_B.join()
    
    print(f"\nFinal value of counter: {counter}")
