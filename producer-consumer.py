import threading
import time
import random
from collections import deque

# Shared buffer with space for 100 particles (50 pairs)
buffer = deque(maxlen=100)

# Semaphores
space = threading.Semaphore(100)   # Initially all 100 particle spaces are free
s = threading.Semaphore(0)         # Initially 0 particles to consume
lock = threading.Lock()            # Only 1 lock

# Producer Thread Function
def producer(pid):
    while True:
        try:
            # Produce a valid pair: P2 = P1 + 100
            p1 = random.randint(1, 100)
            p2 = p1 + 100

            # Reserve space for 2 particles
            if not space.acquire(timeout=1):
                raise BufferError("No space for P1")
            if not space.acquire(timeout=1):
                space.release()
                raise BufferError("No space for P2")

            with lock:
                buffer.append(p1)
                print(f"[Producer-{pid}] Produced P1: {p1}")
                buffer.append(p2)
                print(f"[Producer-{pid}] Produced P2: {p2}")

            # Signal that 2 items are available
            s.release()
            s.release()

        except BufferError as e:
            print(f"[Producer-{pid}] ERROR: {e}")
            break

        time.sleep(random.uniform(0.1, 0.4))

# Consumer Thread Function
def consumer(cid):
    while True:
        try:
            # Wait for 2 items
            if not s.acquire(timeout=1):
                raise BufferError("No item for P1")
            if not s.acquire(timeout=1):
                s.release()
                raise BufferError("No item for P2")

            with lock:
                if len(buffer) < 2:
                    s.release()
                    s.release()
                    raise BufferError("Buffer underflow before consuming")

                p1 = buffer.popleft()
                p2 = buffer.popleft()

            if p2 != p1 + 100:
                print(f"[Consumer-{cid}] ❌ INVALID PAIR: {p1}, {p2}")
            else:
                print(f"[Consumer-{cid}] ✅ Valid pair: {p1}, {p2}")

            # Return space for 2 particles
            space.release()
            space.release()

        except BufferError as e:
            print(f"[Consumer-{cid}] ERROR: {e}")
            break

        time.sleep(random.uniform(0.2, 0.6))

# Create threads
producer_threads = [threading.Thread(target=producer, args=(i,)) for i in range(5)]
consumer_threads = [threading.Thread(target=consumer, args=(i,)) for i in range(2)]

# Start all threads
for t in producer_threads + consumer_threads:
    t.start()

# Wait for all threads to complete
for t in producer_threads + consumer_threads:
    t.join()
