import time
from concurrent.futures import ThreadPoolExecutor


# Let's make the processing time variable
def process_data(item):
    """A sample function that simulates some work."""
    print(
        f"[{time.strftime('%H:%M:%S')}] START Processing: {item} (will take {item} seconds)"
    )
    time.sleep(item)
    print(f"[{time.strftime('%H:%M:%S')}] DONE  Processing: {item}")
    return f"Result of {item}"


if __name__ == "__main__":
    # The first task (5s) will take the longest.
    data = [5, 2, 3]

    with ThreadPoolExecutor(max_workers=3) as executor:
        print(f"[{time.strftime('%H:%M:%S')}] Submitting tasks for {data}...")
        results_iterator = executor.map(process_data, data)

        print(
            f"[{time.strftime('%H:%M:%S')}] Calling list(). The main thread will now block until ALL tasks are complete..."
        )

        # This line will block for approximately 5 seconds, because it must wait for
        # the first and longest task to finish before it can get all the results.
        all_results = list(results_iterator)

        # This line will only execute after about 5 seconds.
        print(
            f"[{time.strftime('%H:%M:%S')}] list() has returned. All processing is complete."
        )
        print("\nFinal results (in original order):", all_results)
