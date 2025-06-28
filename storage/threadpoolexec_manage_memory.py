def conceptual_result_buffer():
    """Shows how ThreadPoolExecutor conceptually manages result ordering"""

    class ResultBuffer:
        """Conceptual model of how results are buffered internally"""

        def __init__(self):
            self.completed_results = {}  # {task_index: result}
            self.next_to_deliver = 0  # Next result index to deliver

        def store_result(self, task_index, result):
            """Called when a worker completes a task"""
            print(f"📦 Storing result for task {task_index} in buffer")
            self.completed_results[task_index] = result
            print(f"   Buffer now contains: {list(self.completed_results.keys())}")

        def try_deliver_next(self):
            """Try to deliver the next result in order"""
            if self.next_to_deliver in self.completed_results:
                result = self.completed_results.pop(self.next_to_deliver)
                print(f"📤 Delivering result for task {self.next_to_deliver}")
                print(
                    f"   Buffer after delivery: {list(self.completed_results.keys())}"
                )
                self.next_to_deliver += 1
                return result
            else:
                print(
                    f"❌ Task {self.next_to_deliver} not ready yet, buffer: {list(self.completed_results.keys())}"
                )
                return None

    # Simulate out-of-order task completion
    buffer = ResultBuffer()

    print("🔄 SIMULATING OUT-OF-ORDER TASK COMPLETION")
    print("=" * 50)

    # Tasks complete in random order
    completion_order = [2, 4, 1, 3, 5]  # Tasks finish in this order

    for task_index in completion_order:
        print(f"\nTask {task_index} completed!")
        buffer.store_result(task_index, f"result_{task_index}")

        # Try to deliver results in order
        print("Attempting to deliver next result(s):")
        while True:
            delivered = buffer.try_deliver_next()
            if delivered is None:
                break

    print(f"\nFinal buffer state: {buffer.completed_results}")


conceptual_result_buffer()
