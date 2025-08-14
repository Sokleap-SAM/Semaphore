from threading import Semaphore, Thread

# Initial values of semaphores
a = Semaphore(1)
b = Semaphore(0)
c = Semaphore(0)

def Process1():
    global a, b
    while True:
        a.acquire()
        print("H")
        print("E")
        b.release()
        b.release()


def Process2():
    global b, c
    while True:

        b.acquire()
        print("L")
        c.release()

def Process3():
    global c
    while True:

        c.acquire()
        c.acquire()
        print("O")


# Create and start three threads for each process
Thread(target=Process1).start()
Thread(target=Process2).start()
Thread(target=Process3).start()
