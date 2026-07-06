
## Search Engine

- A high-performance in-memory search engine built in Python using bitmap indexing and Bit-Sliced Indexes (BSI) for fast filtering on categorical and numeric data.

- It supports SQL-like queries, batch indexing, CRUD operations through FastAPI, and persistence using serialization.

### Problem Statement

- Traditional searches over large datasets require scanning every record, making queries slower as data grows.
- This project addresses that by building specialized indexes that allow queries to operate on compressed bitmaps instead of full-table scans.

### Features
- Bitmap indexing for categorical fields
- Bit-Sliced Index (BSI) for numeric and date fields
- SQL-like query language
- Fast Boolean operations (AND, OR, NOT)
- Range queries (>, <, BETWEEN)
- Batch document indexing
- FastAPI REST API
- CRUD operations
- Persistence using pickle serialization
- Automatic schema detection

### Installation
Clone the repository:

```bash
git clone https://github.com/pragya1808/Search_engine.git
cd Search_engine
```

Create and activate a virtual environment:

**Linux/macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn api:app --reload
```

Open the application:

- API: http://127.0.0.1:8000
- Interactive API Documentation: http://127.0.0.1:8000/docs

