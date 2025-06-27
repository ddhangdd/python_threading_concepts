from concurrent.futures import ThreadPoolExecutor

# with ThreadPoolExecutor(max_workers=1) as executor:
#     future = executor.submit(pow, 2, 3)
#     print(future.result())

with ThreadPoolExecutor(max_workers=2) as executor:
    # Submit individual tasks - like giving separate orders to workers
    future1 = executor.submit(pow, 2, 10)  # Calculate 2^10
    future2 = executor.submit(pow, 3, 5)  # Calculate 3^5
    future3 = executor.submit(pow, 4, 3)  # Calculate 4^3

    # You can collect results in any order you want
    print(f"hi - {future1.done()}")  # Check if the first task is done
    print(f"Second calculation: {future2}")
    print(f"First calculation: {future1.result()}")
    print(f"Third calculation: {future3.result()}")


# The submit() method is like handing out individual task tickets.
# Each call to submit() gives you back one future object,
# and you have complete control over when and how you collect the results.
with ThreadPoolExecutor(max_workers=3) as executor:
    numbers = [1, 2, 3, 4, 5, 6]
    results = executor.map(pow, numbers, [2, 2, 2, 2, 2, 2])  # Square each number
    for result in results:
        print(result)
