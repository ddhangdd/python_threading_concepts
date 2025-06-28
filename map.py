import time
from concurrent.futures import ThreadPoolExecutor


def understand_blocking_behavior():
    """Shows exactly when and how map() consumption blocks"""

    def variable_work(delay_and_value):
        delay, value = delay_and_value
        print(f"    Starting {value} (will take {delay}s)")
        time.sleep(delay)
        print(f"    Finished {value}")
        return value * 10

    # Tasks with different delays - first task is slowest
    tasks = [(3, 1), (1, 2), (1, 3), (1, 4)]  # (delay, value) pairs

    with ThreadPoolExecutor(max_workers=4) as executor:
        print("Creating iterator (instant)...")
        result_iterator = executor.map(variable_work, tasks)

        print("Starting to consume results...")
        start_time = time.time()

        for i, result in enumerate(result_iterator):
            elapsed = time.time() - start_time
            print(f"Iteration {i}: got {result} after {elapsed:.2f}s total")

            # The iterator gives results in submission order,
            # so we wait for the slow first task even though
            # the other tasks finish much faster


understand_blocking_behavior()
