import time
from typing import Any


class Instrumentation:
    def __init__(self):
        self.execution_path = []
        self.state_snapshots = []
        self.timestamps = []

    def record(self, node_name: str, state: Any):
        self.execution_path.append(node_name)
        self.state_snapshots.append(state.__dict__.copy())
        self.timestamps.append(time.time())

    def report(self):
        print("\n=== EXECUTION TRACE ===")
        for i, node in enumerate(self.execution_path):
            print(f"Step {i+1}: {node}")
            print(f"State: {self.state_snapshots[i]}")
            print(f"Timestamp: {self.timestamps[i]}")
            print("-" * 40)
