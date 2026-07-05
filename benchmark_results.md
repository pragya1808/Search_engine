

# Performance Benchmarks

This document presents the benchmarking methodology and performance results for the search engine.

## Test Environment

**Machine**

* CPU: *Fill in your processor (e.g., Intel Core i5-12450H / AMD Ryzen 7 5800H)*
* RAM: *Fill in installed RAM*
* Operating System: *Windows 11 / Ubuntu 24.04 / etc.*

**Software**

* Python Version: *Fill in output of `python --version`*
* Search Engine Implementation: Python
* Bitmap Library: PyRoaring (`pyroaring.BitMap`)

---

# Benchmark Methodology

The benchmark evaluates the performance of the search engine across three primary areas:

1. Index construction
2. Query execution
3. Persistence (saving and loading the index)

Each benchmark was executed on synthetically generated datasets of increasing size to evaluate scalability.

---

# Dataset Generation

Synthetic documents were generated using randomly sampled values from predefined categories.

Each document contains the following fields:

| Field      | Type        | Index Type       |
| ---------- | ----------- | ---------------- |
| name       | String      | Bitmap           |
| country    | Categorical | Bitmap           |
| department | Categorical | Bitmap           |
| age        | Integer     | Bit-Sliced Index |
| salary     | Integer     | Bit-Sliced Index |
| rating     | Float       | Bit-Sliced Index |

Dataset sizes:

* 1,000 documents
* 10,000 documents
* 50,000 documents
* 100,000 documents
* 500,000 documents

---

# Benchmark Configuration

* Timer: `time.perf_counter()`
* Query executions per benchmark: **1000**
* Query parsing benchmark:

  * Measures only query parsing and Abstract Syntax Tree (AST) generation.
* Query execution benchmark:

  * Measures execution of a precompiled query.
* End-to-end benchmark:

  * Measures parsing and execution together using `search_bitmap()`.
  * Document materialization (`fetch()`) is intentionally excluded to measure search engine performance rather than Python object construction.

---

# Indexing Performance

| Documents | Time (s) | Throughput (docs/s) |
| --------: | -------: | ------------------: |
|     1,000 |    0.088 |              11,373 |
|    10,000 |    0.519 |              19,267 |
|    50,000 |    1.704 |              29,338 |
|   100,000 |    2.967 |              33,709 |
|   500,000 |   14.189 |              35,238 |

### Observation

Indexing throughput increases with larger datasets because fixed initialization overhead becomes less significant as the workload grows.

---

# Query Performance

| Query                                  | Parse (ms) | Execute (ms) | End-to-End (ms) |
| -------------------------------------- | ---------: | -----------: | --------------: |
| `country = "India"`                    |     0.0231 |       0.0013 |          0.0274 |
| `age > 30`                             |     0.0203 |       0.3499 |          0.3950 |
| `salary BETWEEN 50000 AND 100000`      |     0.0204 |       2.6654 |          3.0735 |
| `country IN ("India","USA")`           |     0.0175 |       0.0415 |          0.0620 |
| `country = "India" AND age > 30`       |     0.0236 |       0.4220 |          0.4466 |
| `country = "India" OR country = "USA"` |     0.0256 |       0.0502 |          0.0811 |

### Observation

* Query parsing contributes approximately **0.02 ms**, making it a negligible portion of total query latency.
* Equality lookups are extremely fast because they require a single bitmap lookup.
* Boolean `IN`, `AND`, and `OR` operations are implemented using efficient bitmap unions and intersections.
* Numeric range queries require traversal of multiple BSI bit slices, resulting in higher execution time than equality lookups.

---

# Persistence Performance

| Operation  | Time (s) |
| ---------- | -------: |
| Save Index |    1.861 |
| Load Index |    1.603 |

### Observation

Persistence uses Python's `pickle` module to serialize the complete engine state. Saving and loading a 500,000-document index completes in under two seconds on the benchmark system.

---

# Why BETWEEN Is Slower Than Equality

Equality queries perform a direct bitmap comparison against the encoded value.

Example:

```
salary = 50000
```

This requires a single equality evaluation on the corresponding Bit-Sliced Index.

Range queries such as:

```
salary BETWEEN 50000 AND 100000
```

are internally evaluated as:

```
salary >= 50000
AND
salary <= 100000
```

Each comparison traverses every bit slice in the Bit-Sliced Index before intersecting the resulting bitmaps. Consequently, range queries perform significantly more bitmap operations than equality lookups, leading to higher execution times.

---

# Memory Benchmark

A memory benchmark has not yet been performed.

Future work will include measuring peak memory usage during indexing using Python's `tracemalloc` module.

---

# Limitations

The benchmark reflects the performance of the current implementation under synthetic workloads.

Current limitations include:

* Single-threaded indexing and query execution.
* Synthetic datasets rather than real-world corpora.
* Persistence implemented using Python `pickle`, which prioritizes simplicity over optimized serialization.
* Full-text search, ranking algorithms (e.g., TF-IDF or BM25), and compression techniques are not currently implemented.

---

# Conclusion

The benchmark demonstrates that the search engine scales effectively to datasets containing hundreds of thousands of documents while maintaining low query latency.

Bitmap indexing provides near-constant-time categorical lookups, while the Bit-Sliced Index enables efficient numeric comparisons without scanning all documents. The combination of bitmap operations, dynamic schema inference, persistence, and a REST API makes the engine a compact yet capable indexing and retrieval system suitable for experimentation and educational purposes.
