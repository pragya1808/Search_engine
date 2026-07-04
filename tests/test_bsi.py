from search_engine.bsi import BSI

docs = [
    {"id": 0, "age": 5},
    {"id": 1, "age": 3},
    {"id": 2, "age": 6},
    {"id": 3, "age": 1},
    {"id": 4, "age": 7},
    {"id": 5, "age": 4},
    {"id": 6, "age": 2},
    {"id": 7, "age": 0}
]

bsi = BSI()

for doc in docs:
    bsi.add(doc["id"], doc["age"])

bsi.print_slices()
print(bsi.greater_than(5))
print(bsi.greater_than(2))
print(bsi.greater_than(7))
print(bsi.less_than_equals(5))