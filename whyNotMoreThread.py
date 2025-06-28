import threading
import time
from concurrent.futures import ThreadPoolExecutor

import psutil  # For monitoring system resources


def monitor_memory_usage():
    """Helper function to see how much memory threads consume"""
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024  # Memory in MB


def simple_task():
    """A task that just waits - simulates I/O"""
    time.sleep(1)
    return "Done"


# Let's see what happens with different numbers of threads
for num_workers in [1, 10, 50, 100]:
    print(f"\n=== Testing with {num_workers} workers ===")

    memory_before = monitor_memory_usage()
    print(f"Memory before creating threads: {memory_before:.2f} MB")

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        memory_after = monitor_memory_usage()
        print(f"Memory after creating {num_workers} threads: {memory_after:.2f} MB")
        print(f"Memory increase: {memory_after - memory_before:.2f} MB")

        # Submit just 5 simple tasks
        futures = []
        start_time = time.time()

        for i in range(5):
            future = executor.submit(simple_task)
            futures.append(future)

        # Wait for all to complete
        for future in futures:
            future.result()

        end_time = time.time()
        print(f"Time to complete 5 tasks: {end_time - start_time:.2f} seconds")
