import pytest
from pyroaring import BitMap
from search_engine.engine import SearchEngine


@pytest.fixture
def engine():
    return SearchEngine()


@pytest.fixture
def sample_doc():
    return {
        "name": "Alice",
        "age": 25,
        "city": "Delhi",
        "salary": 50000.0,
        "joined": "2024-01-01",
        "active": True,
    }


# -----------------------
# CREATE
# -----------------------

def test_create_returns_doc_id(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)
    assert doc_id == 0


def test_create_stores_document(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)
    assert engine.documents[doc_id] == sample_doc


def test_create_indexes_bitmap_fields(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    assert doc_id in engine.lookup("name", "Alice")
    assert doc_id in engine.lookup("city", "Delhi")
    assert doc_id in engine.lookup("active", True)


def test_create_indexes_numeric_fields(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    assert doc_id in engine.equals_numeric("age", 25)
    assert doc_id in engine.equals_numeric("salary", 50000.0)
    assert doc_id in engine.equals_numeric("joined", "2024-01-01")


def test_dynamic_schema_growth(engine):
    engine.create_document({"name": "Alice"})

    engine.create_document({
        "name": "Bob",
        "department": "Engineering"
    })

    assert "department" in engine.schema


def test_create_negative_numeric(engine):
    with pytest.raises(ValueError):
        engine.create_document({
            "name": "Alice",
            "age": -5
        })


# -----------------------
# READ
# -----------------------

def test_get_document(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    assert engine.get_document(doc_id) == sample_doc


def test_get_invalid_document(engine):
    with pytest.raises(KeyError):
        engine.get_document(100)


# -----------------------
# UPDATE
# -----------------------

def test_update_categorical_field(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    engine.update_document(doc_id, {"city": "Mumbai"})

    assert doc_id in engine.lookup("city", "Mumbai")
    assert len(engine.lookup("city", "Delhi")) == 0


def test_update_numeric_field(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    engine.update_document(doc_id, {"age": 30})

    assert doc_id in engine.equals_numeric("age", 30)
    assert len(engine.equals_numeric("age", 25)) == 0


def test_update_multiple_fields(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    engine.update_document(doc_id, {
        "age": 30,
        "city": "Mumbai"
    })

    assert doc_id in engine.lookup("city", "Mumbai")
    assert doc_id in engine.equals_numeric("age", 30)


def test_update_preserves_old_fields(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    engine.update_document(doc_id, {
        "age": 30
    })

    updated = engine.get_document(doc_id)

    assert updated["name"] == "Alice"
    assert updated["salary"] == 50000.0
    assert updated["city"] == "Delhi"


def test_update_adds_new_field(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    engine.update_document(doc_id, {
        "department": "Engineering"
    })

    assert "department" in engine.schema
    assert doc_id in engine.lookup("department", "Engineering")
    assert engine.documents[doc_id]["department"] == "Engineering"


def test_update_preserves_doc_id(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    returned = engine.update_document(doc_id, {
        "age": 30
    })

    assert returned == doc_id
    assert len(engine.documents) == 1


def test_update_invalid_doc(engine):
    with pytest.raises(KeyError):
        engine.update_document(10, {"age": 30})


def test_update_wrong_type(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    with pytest.raises(ValueError):
        engine.update_document(doc_id, {
            "age": "thirty"
        })


def test_update_negative_number(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    with pytest.raises(ValueError):
        engine.update_document(doc_id, {
            "age": -10
        })


def test_update_date(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    engine.update_document(doc_id, {
        "joined": "2025-01-01"
    })

    assert doc_id in engine.equals_numeric("joined", "2025-01-01")
    assert len(engine.equals_numeric("joined", "2024-01-01")) == 0


# -----------------------
# DELETE
# -----------------------

def test_delete_document(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    assert engine.delete_document(doc_id)


def test_delete_removes_document(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    engine.delete_document(doc_id)

    assert doc_id not in engine.documents


def test_delete_removes_bitmap(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    engine.delete_document(doc_id)

    assert len(engine.lookup("name", "Alice")) == 0


def test_delete_removes_numeric(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    engine.delete_document(doc_id)

    assert len(engine.equals_numeric("age", 25)) == 0


def test_delete_removes_from_all_docs(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    engine.delete_document(doc_id)

    assert doc_id not in engine.all_docs


def test_delete_invalid_document(engine):
    with pytest.raises(KeyError):
        engine.delete_document(100)


# -----------------------
# INTEGRATION
# -----------------------

def test_create_update_search(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    engine.update_document(doc_id, {
        "age": 30
    })

    result = engine.search("age = 30")

    assert len(result) == 1
    assert result[0]["name"] == "Alice"


def test_create_delete_search(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    engine.delete_document(doc_id)

    result = engine.search('name = "Alice"')

    assert result == []


def test_update_new_field_search(engine, sample_doc):
    doc_id = engine.create_document(sample_doc)

    engine.update_document(doc_id, {
        "department": "Engineering"
    })

    result = engine.search('department = "Engineering"')

    assert len(result) == 1
    assert result[0]["name"] == "Alice"


def test_multiple_documents(engine):
    engine.create_document({
        "name": "Alice",
        "age": 25
    })

    bob = engine.create_document({
        "name": "Bob",
        "age": 30
    })

    charlie = engine.create_document({
        "name": "Charlie",
        "age": 35
    })

    engine.update_document(bob, {"age": 31})
    engine.delete_document(charlie)

    result = engine.search("age = 31")

    assert len(result) == 1
    assert result[0]["name"] == "Bob"

    result = engine.search('name = "Charlie"')

    assert result == []