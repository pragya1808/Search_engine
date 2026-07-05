import random
import string
import time
import csv
import os

from search_engine.engine import SearchEngine

# Configuration
DATASET_SIZES = [
    1_000,
    10_000,
    50_000,
    100_000,
    500_000,
]
QUERY_RUNS = 1000
COUNTRIES = [
    "India",
    "USA",
    "Canada",
    "Germany",
    "Japan",
    "France"
]
DEPARTMENTS = [
    "Engineering",
    "Sales",
    "HR",
    "Finance",
    "Marketing"
]
# Dataset Generation
def random_name():
    return ''.join(random.choices(string.ascii_letters, k=8))
def generate_documents(n):
    docs = []
    for _ in range(n):
        docs.append({
            "name": random_name(),
            "country": random.choice(COUNTRIES),
            "department": random.choice(DEPARTMENTS),
            "age": random.randint(18, 65),
            "salary": random.randint(30000, 150000),
            "rating": round(random.uniform(1.0, 5.0), 1)
        })
    return docs

def benchmark_index(engine, docs):
    start = time.perf_counter()
    engine.index_documents(docs)
    end = time.perf_counter()
    return end - start

def benchmark_parser(engine, query, runs=QUERY_RUNS):
    engine.compile_query(query)
    start = time.perf_counter()
    for _ in range(runs):
        engine.compile_query(query)
    end = time.perf_counter()
    return ((end - start) / runs) * 1000

def benchmark_execution(engine, query, runs=QUERY_RUNS):
    tree = engine.compile_query(query)
    engine.execute_query(tree)
    start = time.perf_counter()
    for _ in range(runs):
        engine.execute_query(tree)
    end = time.perf_counter()
    return ((end - start) / runs) * 1000

def benchmark_end_to_end(engine, query, runs=QUERY_RUNS):
    engine.search_bitmap(query)
    start = time.perf_counter()
    for _ in range(runs):
        engine.search_bitmap(query)
    end = time.perf_counter()
    return ((end - start) / runs) * 1000

def benchmark_save(engine):
    filename = "benchmark_index.pkl"
    start = time.perf_counter()
    engine.save(filename)
    end = time.perf_counter()
    return end - start


def benchmark_load():
    filename = "benchmark_index.pkl"
    start = time.perf_counter()
    SearchEngine.load(filename)
    end = time.perf_counter()
    return end - start

#Printing
def separator():
    print("-" * 110)

def print_index_results(results):
    separator()
    print("INDEXING BENCHMARK")
    separator()
    print(
        f'{"Documents":>12} {"Time(s)":>12} {"Docs/sec":>15}'
    )
    for r in results:
        print(
            f'{r["docs"]:>12,} '
            f'{r["time"]:>12.3f} '
            f'{r["throughput"]:>15,.0f}'
        )
def print_query_results(results):
    separator()
    print("QUERY BENCHMARK")
    separator()
    print(
        f'{"Query":<42}'
        f'{"Parse(ms)":>15}'
        f'{"Execute(ms)":>18}'
        f'{"End-to-End(ms)":>20}'
    )
    for row in results:
        print(
            f'{row["query"]:<42}'
            f'{row["parse"]:>15.4f}'
            f'{row["execute"]:>18.4f}'
            f'{row["end_to_end"]:>20.4f}'
        )

def print_persistence(save_time, load_time):
    separator()
    print("PERSISTENCE")
    separator()
    print(f"Save Time : {save_time:.3f} sec")
    print(f"Load Time : {load_time:.3f} sec")

# CSV Export
def export_csv(index_results, query_results):
    with open("benchmark__results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Documents",
            "Index Time (s)",
            "Docs/sec"
        ])
        for r in index_results:
            writer.writerow([
                r["docs"],
                round(r["time"], 3),
                int(r["throughput"])
            ])
        writer.writerow([])
        writer.writerow([
            "Query",
            "Parse (ms)",
            "Execute (ms)",
            "End-to-End (ms)"
        ])
        for row in query_results:
            writer.writerow([
                row["query"],
                round(row["parse"], 4),
                round(row["execute"], 4),
                round(row["end_to_end"], 4)
            ])
# Main
def main():
    random.seed(42)
    indexing_results = []
    print("\nGenerating synthetic dataset...\n")
    largest_engine = None
    for size in DATASET_SIZES:

        print(f"Indexing {size:,} documents...")
        docs = generate_documents(size)
        engine = SearchEngine()
        elapsed = benchmark_index(engine, docs)
        indexing_results.append({
            "docs": size,
            "time": elapsed,
            "throughput": size / elapsed

        })
        largest_engine = engine
    print()

    queries = [
        'country = "India"',
        'age > 30',
        'salary BETWEEN 50000 AND 100000',
        'country IN ("India","USA")',
        'country = "India" AND age > 30',
        'country = "India" OR country = "USA"'
    ]
    query_results = []
    print("Running query benchmarks...\n")

    for query in queries:
        parse_time = benchmark_parser(
            largest_engine,
            query
        )
        execution_time = benchmark_execution(
            largest_engine,
            query
        )
        end_to_end_time = benchmark_end_to_end(
            largest_engine,
            query
        )
        query_results.append({
            "query": query,
            "parse": parse_time,
            "execute": execution_time,
            "end_to_end": end_to_end_time
        })

    print("Benchmarking persistence...\n")
    save_time = benchmark_save(largest_engine)
    load_time = benchmark_load()
    print()
    print_index_results(indexing_results)
    print()
    print_query_results(query_results)
    print()
    print_persistence(save_time, load_time)
    export_csv(
        indexing_results,
        query_results
    )
    if os.path.exists("benchmark_index.pkl"):
        os.remove("benchmark_index.pkl")
    separator()
    print("CSV exported as benchmark_results.csv")
    separator()

if __name__ == "__main__":
    main()