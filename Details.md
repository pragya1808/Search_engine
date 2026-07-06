# Search Engine using Bitmap Indexes and Bit-Sliced Indexes

          Documents
               │
               ▼
      Schema Inference
               │
      ┌────────┴────────┐
      ▼                 ▼
 Bitmap Index      Bit-Sliced Index
(Categorical)        (Numeric)
      │                 │
      └────────┬────────┘
               ▼
         Query Executor
               │
               ▼
          FastAPI API

A lightweight search engine built in Python that supports efficient document indexing and querying using Bitmap Indexes for categorical fields and Bit-Sliced Indexes (BSI) for numeric fields.

The project provides:

- Dynamic schema inference
- CRUD operations
- Batch indexing
- Boolean queries
- Numeric range queries
- Persistent storage
- REST API using FastAPI

---

## Features

### Document Management

- Create documents
- Read documents
- Update documents
- Delete documents
- Batch document ingestion

### Indexing

- Automatic schema detection
- Bitmap Index for categorical fields
- Bit-Sliced Index (BSI) for numeric fields
- Dynamic schema expansion
- Optional high-cardinality field exclusion

### Query Support

Categorical

- Equality
- IN
- NOT IN

Numeric

- =
- >
- >=
- <
- <=
- BETWEEN

Boolean

- AND
- OR
- NOT

### Persistence

- Save complete engine state
- Load previously saved engine

### REST API

- CRUD endpoints
- Search endpoint
- Count endpoint
- Search IDs endpoint
- Save/Load endpoints

---

## Performance
Benchmarks were run on a synthetic dataset using randomly generated documents.
### Indexing Performance
| Documents | Time (s) | Throughput (docs/s) |
|----------:|---------:|--------------------:|
| 1,000     | 0.088    | 11,373              |
| 10,000    | 0.519    | 19,267              |
| 50,000    | 1.704    | 29,338              |
| 100,000   | 2.967    | 33,709              |
| 500,000   |14.189    | 35,238              |
### Query Performance
| Query        | End-to-End (ms) |
|--------------|----------------:|
| Equality     | 0.027           |
| Greater Than | 0.395           |
| BETWEEN      | 3.074           |
| IN           | 0.062           |
| AND          | 0.447           |
| OR           | 0.081           |
> Detailed benchmark methodology and results are available in **BENCHMARKS.md**.

---

## Project Structure

```
search_engine/
│
├── bitmap.py
├── bsi.py
├── engine.py
├── parser.py
├── executor.py
├── persistence.py
│
tests/
│
├── test_bsi.py
├── test_crud.py
├── test_parser.py
├── test_persistence.py
├── test_search.py
├── test_throughput.py
│
api.py
README.md
```

---

## Architecture
### Bitmap Index
Categorical values are stored as bitmap indexes.
Example
```
Country

India -> 1011010
USA    -> 0100100
Japan  -> 0001001
```
Bitmap operations make AND, OR and NOT queries extremely fast.

---
### Bit-Sliced Index (BSI)
Numeric values are stored bit-by-bit.
Example
```
Age
25 -> 11001
30 -> 11110
18 -> 10010
```
Each bit position has its own bitmap, enabling efficient range queries without scanning every document.

---
## Query Examples
### Equality
```
country = "India"
```
### Range
```
salary > 50000
```
### Between
```
age BETWEEN 20 AND 30
```
### Boolean
```
country = "India" AND age > 25
```
### IN
```
country IN ("India","USA")
```

---
## Installation
```bash
git clone <repo-url>
cd search-engine
pip install -r requirements.txt
```
---
## Running
Start the FastAPI server
```bash
uvicorn api:app --reload
```

Open
```
http://127.0.0.1:8000/docs
```
to access the Swagger UI.

---

## API Endpoints

| Method  | Endpoint        | Description     |
|---------|-----------------|-----------------|
| GET     | /               | Health check    |
| POST    | /documents      | Add document    |
| GET     | /documents/{id} | Get document    |
| PUT     | /documents/{id} | Update document |
| DELETE  | /documents/{id} | Delete document |
| POST    | /documents/batch| Batch ingest    |
| GET     | /search         | Search documents|
| GET     | /search/ids     | Matching IDs    |
| GET     | /search/count   | Result count    |
| POST    | /save           | Save engine     |
| POST    | /load           | Load engine     |

---

## Example Workflow

1. Index documents

```json
{
    "name":"Alice",
    "country":"India",
    "age":24
}
```

2. Query

```
country = "India" AND age > 20
```

3. Matching documents are returned instantly using bitmap operations.

---

## Testing

Run

```bash
python tests.py
```

or

```bash
pytest
```

depending on your test setup.

---

## Future Improvements

- Phrase search
- Full-text indexing
- Ranking (TF-IDF/BM25)
- Compression improvements
- Parallel indexing
- Incremental persistence
- Web UI

---

## Technologies Used

- Python
- FastAPI
- Pickle
- Bitmaps
- Bit-Sliced Indexes (BSI)

---

## License
MIT License