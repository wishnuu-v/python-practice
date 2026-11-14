
import csv
import time
import tracemalloc
import gc

from main import read_csv_batches


def benchmark_full_loading(filepath):

    gc.collect()
    tracemalloc.start()

    start_time = time.perf_counter()

    with open(filepath, "r", newline="", encoding="utf-8") as file:
        data = list(csv.DictReader(file))

    execution_time = time.perf_counter() - start_time

    current_memory, peak_memory = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    record_count = len(data)

    del data

    return record_count, execution_time, peak_memory


def benchmark_streaming(filepath, batch_size=1000):

    gc.collect()
    tracemalloc.start()

    start_time = time.perf_counter()

    record_count = 0

    for batch in read_csv_batches(filepath, batch_size):
        record_count += len(batch)

    execution_time = time.perf_counter() - start_time

    current_memory, peak_memory = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    return record_count, execution_time, peak_memory


def run_benchmarks():

    datasets = [
        "dataset_10000.csv",
        "dataset_100000.csv",
        "dataset_500000.csv",
        "dataset_1000000.csv"
    ]

    print("\nCSV PERFORMANCE BENCHMARK")
    print("=" * 85)

    print(
        f"{'Dataset':<22}"
        f"{'Method':<18}"
        f"{'Time (s)':<15}"
        f"{'Peak Memory (MB)':<18}"
    )

    print("-" * 85)

    for filepath in datasets:

        print(f"\nProcessing: {filepath}")

        methods = [
            ("Full Loading", benchmark_full_loading),
            ("Streaming", benchmark_streaming)
        ]

        for method_name, function in methods:

            try:
                count, elapsed, memory = function(filepath)

                memory_mb = memory / (1024 * 1024)

                print(
                    f"{count:<22}"
                    f"{method_name:<18}"
                    f"{elapsed:<15.4f}"
                    f"{memory_mb:<18.2f}"
                )

            except FileNotFoundError:
                print(f"Dataset not found: {filepath}")


if __name__ == "__main__":
    run_benchmarks()
