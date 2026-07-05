import pytest
from search_engine.engine import SearchEngine

@pytest.fixture
def sample_docs():
    return [
        {
            "name": "Alice",
            "age": 25,
            "city": "Delhi",
            "salary": 60000,
        },
        {
            "name": "Bob",
            "age": 30,
            "city": "Mumbai",
            "salary": 80000,
        },
        {
            "name": "Charlie",
            "age": 22,
            "city": "Delhi",
            "salary": 50000,
        },
    ]


def test_save_load_state(tmp_path, sample_docs):
    engine = SearchEngine()
    for doc in sample_docs:
        engine.index_document(doc)
    path = tmp_path / "index.pkl"
    engine.save(path)
    loaded = SearchEngine.load(path)
    assert loaded.schema == engine.schema
    assert loaded.documents == engine.documents
    assert loaded.next_doc_id == engine.next_doc_id
    assert loaded.float_scale == engine.float_scale
    assert loaded.ignored_fields == engine.ignored_fields

def test_save_load_lookup(tmp_path, sample_docs):
    engine = SearchEngine()
    for doc in sample_docs:
        engine.index_document(doc)
    path = tmp_path / "index.pkl"
    engine.save(path)
    loaded = SearchEngine.load(path)
    original = set(engine.lookup("city", "Delhi"))
    restored = set(loaded.lookup("city", "Delhi"))
    assert original == restored


def test_save_load_numeric_queries(tmp_path, sample_docs):
    engine = SearchEngine()
    for doc in sample_docs:
        engine.index_document(doc)
    path = tmp_path / "index.pkl"
    engine.save(path)
    loaded = SearchEngine.load(path)
    assert (
        set(engine.greater_than("salary", 55000))
        == set(loaded.greater_than("salary", 55000))
    )
    assert (
        set(engine.between("salary", 50000, 70000))
        == set(loaded.between("salary", 50000, 70000))
    )
    assert (
        set(engine.equals_numeric("age", 25))
        == set(loaded.equals_numeric("age", 25))
    )


def test_insert_after_load(tmp_path, sample_docs):
    engine = SearchEngine()
    for doc in sample_docs:
        engine.index_document(doc)
    path = tmp_path / "index.pkl"
    engine.save(path)
    loaded = SearchEngine.load(path)
    new_id = loaded.index_document(
        {
            "name": "David",
            "age": 28,
            "city": "Pune",
            "salary": 90000,
        }
    )
    assert new_id == 3
    assert loaded.documents[new_id]["name"] == "David"
    assert new_id in set(loaded.lookup("city", "Pune"))


def test_update_after_load(tmp_path, sample_docs):
    engine = SearchEngine()
    for doc in sample_docs:
        engine.index_document(doc)
    path = tmp_path / "index.pkl"
    engine.save(path)
    loaded = SearchEngine.load(path)
    loaded.update_document(
        0,
        {
            "name": "Alice",
            "age": 26,
            "city": "Delhi",
            "salary": 65000,
        },
    )
    assert loaded.documents[0]["age"] == 26
    assert 0 in set(loaded.equals_numeric("age", 26))


def test_delete_after_load(tmp_path, sample_docs):
    engine = SearchEngine()
    for doc in sample_docs:
        engine.index_document(doc)
    path = tmp_path / "index.pkl"
    engine.save(path)
    loaded = SearchEngine.load(path)
    loaded.delete_document(1)
    assert 1 not in loaded.documents
    assert 1 not in set(loaded.lookup("city", "Mumbai"))


def test_multiple_save_load_cycles(tmp_path, sample_docs):
    engine = SearchEngine()
    for doc in sample_docs:
        engine.index_document(doc)
    path = tmp_path / "index.pkl"
    engine.save(path)
    loaded = SearchEngine.load(path)
    loaded.index_document(
        {
            "name": "Eve",
            "age": 35,
            "city": "Chennai",
            "salary": 95000,
        }
    )
    loaded.save(path)
    loaded_again = SearchEngine.load(path)
    assert "Eve" in [
        doc["name"] for doc in loaded_again.documents.values()
    ]
    assert (
        set(loaded.lookup("city", "Chennai"))
        == set(loaded_again.lookup("city", "Chennai"))
    )