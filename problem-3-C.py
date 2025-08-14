import threading
import time

# The initial value of the counter is set to 10.
# Process A adds 1, and Process B adds 2.
# The expected final value should be 13 (10 + 1 + 2), but the synchronization
# will lead to a race condition, so the final value will be different.
counter = 10
print(f"Initial value of counter: {counter}")

# We create two semaphores, both with an initial value of 0.
# This setup is used to enforce a specific synchronization pattern (a rendezvous).
# The initial value of 0 means a 'wait' operation will block immediately.
s1 = threading.Semaphore(0)
s2 = threading.Semaphore(0)

def process_A():
    """
    This function represents Process A.
    It simulates the operations from the image, including the semaphore signals and waits.
    """
    # The 'global' keyword is added to tell Python to use the
    # global 'counter' variable instead of creating a new local one.
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
    
    print("Process A is signaling s1 and waiting on s2...")
    # Simulate the signal(s1) and wait(s2) from the image.
    # A signals s1, allowing Process B to proceed.
    s1.release()
    # A then waits on s2, blocking until Process B signals it.
    s2.acquire()
    
    # Simulate the ST (Store) instruction
    # Once unblocked, A stores its local value (11) back into counter.
    # This overwrites whatever value B may have stored.
    counter = local_reg
    print(f"Process A has finished. Counter value is now: {counter}")
    
def process_B():
    """
    This function represents Process B.
    It simulates the operations from the image, including the semaphore waits and signals.
    """
    # The 'global' keyword is added to tell Python to use the
    # global 'counter' variable instead of creating a new local one.
    global counter

    print("Process B has started.")
    
    # Simulate the LD (Load) instruction
    # B reads the initial value of counter (10)
    local_reg = counter
    
    print("Process B is waiting on s1...")
    # Simulate the wait(s1) from the image.
    # B waits until Process A signals s1.
    s1.acquire()
    
    # Simulate the ADDC (Add Constant) instruction
    # B increments its local copy of the value (10 + 2 = 12)
    local_reg = local_reg + 2
    
    # Simulate some work
    time.sleep(0.1)
    
    print("Process B is signaling s2...")
    # Simulate the signal(s2) from the image.
    # B signals s2, allowing Process A to finish.
    s2.release()
    
    # Simulate the ST (Store) instruction
    # B stores its local value (12) back into counter.
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
