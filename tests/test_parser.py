from search_engine.engine import SearchEngine
from search_engine.parser import QueryParser

engine = SearchEngine()

engine.build_schema({
    "country": "India",
    "age": 25,
    "salary": 50000,
    "active": True,
    "joining": "2024-01-01"
})

parser = QueryParser(engine.schema)

tree = parser.parse(
    'country NOT IN ("India","USA")'
)

assert tree.field == "country"
assert tree.comparison == "NOT IN"
assert tree.value == ["India", "USA"]