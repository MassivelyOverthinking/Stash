from src.Stash import Stash
from pympler import asizeof

import tracemalloc
import gc
import sys

#-------------------- Benchmarks --------------------
class RegularClass():
    def __init__(self, name: str, age: int, is_active: bool):
        self.name = name
        self.age = age
        self.is_active = is_active

@Stash(freeze=False)
class StashClass():
    name: str
    age: int
    is_active: bool

def instantiate_regular():
    return [RegularClass(f"Name{i}", i % 100, i % 2 == 0) for i in range(10000)]

def instantiate_stash():
    return [StashClass(f"Name{i}", i % 100, i % 2 == 0) for i in range(10000)]

def calculate_memory_usage(snapshot_before, snapshot_after):
    stats = snapshot_after.compare_to(snapshot_before, "filename")
    total = sum([stat.size_diff for stat in stats])
    return total, stats

def print_summary(title, total_bytes, instance_count):
    avg_per_object = total_bytes / instance_count
    print(f"{title}")
    print(f"total memory used: {total_bytes / 1024:.2f} KiB")
    print(f"Average memory per instance: {avg_per_object:.2f} B\n")

def run_benchmark():
    tracemalloc.start()

    # Benchmark RegularClass
    gc.collect()
    snap_before_regular = tracemalloc.take_snapshot()
    regular_instances = instantiate_regular()
    snap_after_regular = tracemalloc.take_snapshot()

    total_regular, stats_regular = calculate_memory_usage(snap_before_regular, snap_after_regular)
    print_summary("RegularClass Benchmark", total_regular, 10000)

    # Free memory before running next test
    del regular_instances
    gc.collect()

    # Benchmark StashClass
    snapshot_before_stash = tracemalloc.take_snapshot()
    stash_instances = instantiate_stash()
    snapshot_after_stash = tracemalloc.take_snapshot()

    total_stash, stats_stash = calculate_memory_usage(snapshot_before_stash, snapshot_after_stash)
    print_summary("StashClass Benchmark", total_stash, 10000)

    tracemalloc.stop()

def get_memory_size():
    r = RegularClass("name", 1, True)
    s = StashClass("name", 1, True)

    print(f"RegularClass instance size with sys: {sys.getsizeof(r)}")
    print(f"RegularClass instance size with pympler: {asizeof.asizeof(r)}")
    print(f"StashClass instance size with sys: {sys.getsizeof(s)}")
    print(f"StashClass instance size with pympler: {asizeof.asizeof(s)}")

if __name__ == "__main__":
    run_benchmark()
    get_memory_size()


    
