from src.Stash import Stash

import tracemalloc
import gc

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

def instanate_regular():
    return [RegularClass(f"Name{i}", i % 100, i % 2 == 0) for i in range(10000)]

def instantiate_stash():
    return [StashClass(f"Name{i}", i % 100, i % 2 == 0) for i in range(10000)]

def print_head(snapshot: tracemalloc.Snapshot, key_type="lineno", limit=10):
    top_stats = snapshot.statistics(key_type)
    print(f"Top memory lines - {limit}")
    for st in top_stats[:limit]:
        print(st)

def run_benchmark():
    tracemalloc.start()
    gc.collect()

    snap_before = tracemalloc.take_snapshot()
    regular_instances = instanate_regular()
    snap_after_regular = tracemalloc.take_snapshot()

    gc.collect()

    stash_instancess = instantiate_stash()
    snap_after_stash = tracemalloc.take_snapshot()

    print("Memory used by regular class instances:")
    stats_regular = snap_after_regular.compare_to(snap_before, "filename")
    print_head(stats_regular)

    print("\nMemory used by Stash class instances:")
    stats_stash = snap_after_stash.compare_to(snap_after_stash, "filename")
    print_head(stats_stash)

    tracemalloc.stop()

if __name__ == "__main__":
    run_benchmark()


    
