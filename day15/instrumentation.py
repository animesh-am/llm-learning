import time


class Instrumentor:
    def __init__(self):
        self.path = []
        self.snapshots = []
        self.timestamps = []

    def record(self, node_name, state):
        self.path.append(node_name)
        self.snapshots.append(state.__dict__.copy())
        self.timestamps.append(time.time())

    def report(self):
        print("\n=== EXECUTION TRACE ===")
        for i, node in enumerate(self.path):
            print(f"Step {i+1}: {node}")
            print("State:", self.snapshots[i])
            print("Timestamp:", self.timestamps[i])
            print("-" * 40)