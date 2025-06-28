import os
import time
from concurrent.futures import ThreadPoolExecutor

import psutil


def demonstrate_actual_memory_usage():
    """Shows the real memory accumulation pattern"""

    def get_memory_usage():
        """Get current memory usage in MB"""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024

    def memory_intensive_work(n):
        """Work that creates large results"""
        print(f"    Creating large result for task {n}")
        # Simulate a large result (like processed image data, parsed documents, etc.)
        large_data = list(range(500000))  # ~4MB per result
        return {"task_id": n, "large_data": large_data}

    print("📊 MEMORY USAGE ANALYSIS")
    print("=" * 40)

    baseline_memory = get_memory_usage()
    print(f"Baseline memory: {baseline_memory:.1f} MB")

    with ThreadPoolExecutor(max_workers=4) as executor:
        # Create iterator with many tasks
        tasks = list(range(1, 11))  # 10 tasks
        result_iterator = executor.map(memory_intensive_work, tasks)

        print(f"Iterator created - memory: {get_memory_usage():.1f} MB")

        # Let workers build up results in the buffer
        print("\n⏰ Waiting for results to accumulate in buffer...")
        time.sleep(3)  # Let several tasks complete

        buffer_memory = get_memory_usage()
        print(f"After buffer accumulation - memory: {buffer_memory:.1f} MB")
        print(f"Memory increase: {buffer_memory - baseline_memory:.1f} MB")
        print("Notice: Multiple results are stored in memory simultaneously!")

        # Now consume results and watch memory usage
        print(f"\n📥 Consuming results one by one...")
        for i, result in enumerate(result_iterator):
            current_memory = get_memory_usage()
            print(f"After consuming result {i+1}: {current_memory:.1f} MB")

            # Show that memory can decrease as results are consumed
            if i == 3:  # After consuming several results
                print(
                    f"   Memory freed as results consumed: {buffer_memory - current_memory:.1f} MB"
                )

        final_memory = get_memory_usage()
        print(f"\nFinal memory: {final_memory:.1f} MB")
        print(f"Net memory change: {final_memory - baseline_memory:.1f} MB")


# Be careful running this - it uses significant memory!
demonstrate_actual_memory_usage()
