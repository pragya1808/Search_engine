import time
from search_engine.engine import SearchEngine
from tests.test_random import generate_dataset

NUM_DOCS = 100000

docs = generate_dataset(NUM_DOCS)

engine = SearchEngine()

start = time.perf_counter()

engine.index_documents(docs)

end = time.perf_counter()

elapsed = end - start

print(f"Indexed {NUM_DOCS:,} documents")
print(f"Time: {elapsed:.3f} sec")
print(f"Throughput: {NUM_DOCS/elapsed:,.0f} docs/sec")

queries = [
    'country = "India"',
    "age > 30",
    "salary BETWEEN 50000 AND 80000",
    'country = "USA" AND age > 25',
    'department = "Engineering"',
]

NUM_QUERIES = 10000

start = time.perf_counter()

compiled = [
    engine.compile_query(q)
    for q in queries
]

start = time.perf_counter()

for i in range(NUM_QUERIES):
    engine.execute_query(
        compiled[i % len(compiled)]
    )

end = time.perf_counter()

elapsed = end - start

print(f"Executed {NUM_QUERIES:,} queries")
print(f"Time: {elapsed:.3f} sec")
print(f"Throughput: {NUM_QUERIES/elapsed:,.0f} queries/sec")