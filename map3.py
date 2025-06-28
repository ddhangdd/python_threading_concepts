import time
from concurrent.futures import ThreadPoolExecutor


def demonstrate_actual_map_behavior():
    """Shows the real behavior of ThreadPoolExecutor.map()"""

    def tracked_work_with_timing(n):
        start_time = time.time()
        print(f"    🚀 STARTED work on {n} at {start_time:.2f}")
        time.sleep(1)  # Simulate work
        end_time = time.time()
        print(f"    ✅ FINISHED work on {n} at {end_time:.2f}")
        return n * 10

    print("🧪 TESTING WITH DIFFERENT WORKER COUNTS")

    # Test with 2 workers
    print("\n=== With 2 workers ===")
    with ThreadPoolExecutor(max_workers=2) as executor:
        print(f"Creating iterator at {time.time():.2f}")

        result_iterator = executor.map(tracked_work_with_timing, [1, 2, 3, 4, 5])

        print(f"Iterator created at {time.time():.2f}")
        print("Notice: work started on first 2 items immediately!")

        time.sleep(0.5)  # Let some work progress
        print(f"\nConsuming first result at {time.time():.2f}")
        first_result = next(result_iterator)
        print(f"Got: {first_result}")

        time.sleep(2)  # Let more work happen
        print(f"\nConsuming remaining results at {time.time():.2f}")
        remaining = list(result_iterator)
        print(f"Got: {remaining}")

    # Test with 1 worker to see the difference
    print("\n" + "=" * 50)
    print("\n=== With 1 worker ===")
    with ThreadPoolExecutor(max_workers=1) as executor:
        print(f"Creating iterator at {time.time():.2f}")

        result_iterator = executor.map(tracked_work_with_timing, [1, 2, 3])

        print(f"Iterator created at {time.time():.2f}")
        print("Notice: only 1 worker, so only work on item 1 starts!")

        time.sleep(0.5)
        print(f"\nConsuming first result at {time.time():.2f}")
        first_result = next(result_iterator)
        print(f"Got: {first_result}")

        print(f"\nConsuming second result at {time.time():.2f}")
        second_result = next(result_iterator)
        print(f"Got: {second_result}")


def compare_builtin_vs_executor_map():
    """Shows the difference between built-in map() and ThreadPoolExecutor.map()"""

    def side_effect_work(n):
        print(f"    Working on {n}")
        return n * 2

    print("🐍 BUILT-IN map() - Truly lazy")
    print("Creating built-in map object...")
    builtin_map = map(side_effect_work, [1, 2, 3])
    print("Map object created - notice no work happened yet!")

    time.sleep(1)
    print("Still no work...")

    print("Now consuming first result:")
    first = next(builtin_map)
    print(f"Got: {first}")

    print("\n⚡ ThreadPoolExecutor.map() - Eager worker utilization")
    with ThreadPoolExecutor(max_workers=2) as executor:
        print("Creating executor map object...")
        executor_map = executor.map(side_effect_work, [4, 5, 6])
        print("Map object created - work started immediately!")


import threading
import time
from concurrent.futures import ThreadPoolExecutor


def demonstrate_work_scheduling_independence():
    """Shows that workers pick up new tasks immediately, regardless of result consumption"""

    def tracked_work(n):
        """Work that announces its lifecycle clearly"""
        worker_id = threading.current_thread().name
        print(f"    🚀 Worker {worker_id} STARTED task {n} at {time.time():.2f}")
        time.sleep(1)  # Simulate work taking 1 second
        print(f"    ✅ Worker {worker_id} FINISHED task {n} at {time.time():.2f}")
        return n * 10

    with ThreadPoolExecutor(max_workers=2) as executor:
        print("🧪 TESTING WORK SCHEDULING vs RESULT CONSUMPTION")
        print("=" * 60)

        start_time = time.time()
        print(f"Creating iterator with 6 tasks at {start_time:.2f}")

        # Create iterator with more tasks than workers
        result_iterator = executor.map(tracked_work, [1, 2, 3, 4, 5, 6])

        print(f"Iterator created at {time.time():.2f}")
        print("Notice: Tasks 1 and 2 started immediately (filling 2 workers)")

        # Wait and watch what happens - workers should pick up new tasks
        # even though we haven't consumed any results yet
        print(f"\n⏰ Waiting 1.5 seconds without consuming results...")
        time.sleep(1.5)
        print(f"Current time: {time.time():.2f}")
        print("Notice: Workers already picked up tasks 3 and 4!")

        # Now consume first result - this shouldn't affect work scheduling
        print(f"\n📥 Consuming first result at {time.time():.2f}")
        first_result = next(result_iterator)
        print(f"Got result: {first_result}")
        print("Notice: No new work started just because we consumed a result")

        # Wait more to see continued work scheduling
        print(f"\n⏰ Waiting another 1.5 seconds...")
        time.sleep(1.5)
        print(f"Current time: {time.time():.2f}")
        print("Notice: Workers continued to tasks 5 and 6 automatically!")

        # Consume remaining results quickly
        print(f"\n📥 Consuming remaining results at {time.time():.2f}")
        remaining_results = list(result_iterator)
        print(f"Got remaining results: {remaining_results}")

        total_time = time.time() - start_time
        print(f"\nTotal time: {total_time:.2f} seconds")
        print(
            "Key insight: Work scheduling happened independently of result consumption!"
        )


demonstrate_work_scheduling_independence()
# compare_builtin_vs_executor_map()
# demonstrate_actual_map_behavior()
