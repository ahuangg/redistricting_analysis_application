import multiprocessing
import os

def increment_and_print(shared_counter, lock, _):
    """Function to increment the shared counter and print its value."""
    with lock:
        shared_counter.value += 1
        current_value = shared_counter.value
    print(f"Process ID: {os.getpid()}, Counter Value: {current_value}")

if __name__ == '__main__':
    # Use a Manager to create a shared counter
    with multiprocessing.Manager() as manager:
        counter = manager.Value('i', 0)
        lock = manager.Lock()

        # Number of increments
        num_increments = 10

        # Create a pool of workers and use starmap
        with multiprocessing.Pool() as pool:
            pool.starmap(increment_and_print, [(counter, lock, i) for i in range(num_increments)])

        # Print the final value of the counter
        print(f"Final Counter Value: {counter.value}")
