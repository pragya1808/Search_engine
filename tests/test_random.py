import random
from datetime import datetime, timedelta
from search_engine.engine import SearchEngine

countries = ["India", "USA", "Canada", "Germany", "Japan"]
departments = ["Engineering", "HR", "Sales", "Finance", "Marketing"]

def random_date():
    start = datetime(2020, 1, 1)
    end = datetime(2024, 12, 31)
    delta = (end - start).days
    return (start + timedelta(days=random.randint(0, delta))).strftime("%Y-%m-%d")

def generate_dataset(n=50):
    docs = []

    for i in range(n):
        docs.append({
            "name": f"Employee{i}",
            "age": random.randint(18, 60),
            "salary": random.randint(30000, 120000),
            "country": random.choice(countries),
            "department": random.choice(departments),
            "active": random.choice([True, False]),
            "joining": random_date()
        })

    return docs

def test_dataset(docs):

    engine = SearchEngine()

    engine.index_documents(docs)

    def check(query, expected):
        actual = sorted(engine.search(query), key=lambda d: d["name"])
        expected = sorted(expected, key=lambda d: d["name"])
        assert actual == expected

    check("age = 30",[d for d in docs if d["age"] == 30])
    check("age > 30",[d for d in docs if d["age"] > 30])
    check("age >= 30",[d for d in docs if d["age"] >= 30])
    check("age < 30",[d for d in docs if d["age"] < 30])
    check("age <= 30",[d for d in docs if d["age"] <= 30])
    check("salary > 70000",[d for d in docs if d["salary"] > 70000])
    check("salary >= 70000",[d for d in docs if d["salary"] >= 70000])
    check("salary < 70000",[d for d in docs if d["salary"] < 70000])
    check("salary <= 70000",[d for d in docs if d["salary"] <= 70000])
    check("salary BETWEEN 60000 AND 80000",[d for d in docs if 60000 <= d["salary"] <= 80000])
    check("salary BETWEEN 25 AND 35",[d for d in docs if 25 <= d["salary"] <= 35])
    #categorical queries
    check('country = "India"',[d for d in docs if d["country"] == "India"])
    check(
        'department = "Engineering"',
        [d for d in docs if d["department"] == "Engineering"]
    )
    check(
        "active = true",
        [d for d in docs if d["active"]]
    )
    check(
        'country IN ("India","USA")',
        [d for d in docs if d["country"] in ["India", "USA"]]
    )
    check(
        'department IN ("HR","Sales")',
        [d for d in docs if d["department"] in ["HR", "Sales"]]
    )
    check(
        'country NOT IN ("India","USA")',
        [d for d in docs if d["country"] not in ["India", "USA"]]
    )
    check(
        'country = "India" AND department = "Engineering"',
        [
            d for d in docs
            if d["country"] == "India"
            and d["department"] == "Engineering"
        ]
    )
    check(
        'country = "India" OR country = "Canada"',
        [
            d for d in docs
            if d["country"] == "India"
            or d["country"] == "Canada"
        ]
    )
    check(
        'NOT country = "India"',
        [
            d for d in docs
            if d["country"] != "India"
        ]
    )

    check(
        'country = "India" AND active = True',
        [
            d for d in docs
            if d["country"] == "India"
            and d["active"] == True
        ]
    )
    check(
        '(country = "India" OR country = "USA") AND department = "Engineering"',
        [
            d for d in docs
            if (
                d["country"] == "India"
                or d["country"] == "USA"
            )
            and d["department"] == "Engineering"
        ]
    )
    check(
        'NOT (country = "India" OR department = "HR") AND active=true',
        [
            d for d in docs
            if not (
                d["country"] == "India"
                or d["department"] == "HR"
            )
            and d["active"] == True
        ]
    )

    check(
        'joining = "2022-01-15"',
        [d for d in docs if d["joining"] == "2022-01-15"]
    )
    check(
        'joining > "2022-01-01"',
        [d for d in docs if d["joining"] > "2022-01-01"]
    )
    check(
        'joining >= "2022-01-01"',
        [d for d in docs if d["joining"] >= "2022-01-01"]
    )
    check(
        'joining < "2022-01-01"',
        [d for d in docs if d["joining"] < "2022-01-01"]
    )
    check(
        'joining <= "2022-01-01"',
        [d for d in docs if d["joining"] <= "2022-01-01"]
    )
    check(
        'joining BETWEEN "2021-01-01" AND "2022-12-31"',
        [
            d for d in docs
            if "2021-01-01" <= d["joining"] <= "2022-12-31"
        ]
    )
    check(
        'joining IN ("2022-01-15","2023-03-11")',
        [
            d for d in docs
            if d["joining"] in ["2022-01-15", "2023-03-11"]
        ]
    )
    check(
        'joining NOT IN ("2022-01-15","2023-03-11")',
        [
            d for d in docs
            if d["joining"] not in ["2022-01-15", "2023-03-11"]
        ]
    )
    check(
        'joining > "2022-01-01" AND country = "India"',
        [
            d for d in docs
            if d["joining"] > "2022-01-01"
            and d["country"] == "India"
        ]
    )

    #Mixed Queries
    check(
        'country = "India" AND age > 30',
        [
            d for d in docs
            if d["country"] == "India" and d["age"] > 30
        ]
    )
    check(
        'department = "Engineering" AND salary > 70000',
        [
            d for d in docs
            if d["department"] == "Engineering" and d["salary"] > 70000
        ]
    )
    check(
        'country = "USA" OR salary > 90000',
        [
            d for d in docs
            if d["country"] == "USA" or d["salary"] > 90000
        ]
    )
    check(
        'country = "India" AND salary BETWEEN 60000 AND 80000',
        [
            d for d in docs
            if d["country"] == "India"
            and 60000 <= d["salary"] <= 80000
        ]
    )
    check(
        '(country = "India" OR country = "Canada") AND age < 30',
        [
            d for d in docs
            if (d["country"] == "India" or d["country"] == "Canada")
            and d["age"] < 30
        ]
    )
    check(
        'NOT (country = "Germany") AND salary > 60000',
        [
            d for d in docs
            if not (d["country"] == "Germany")
            and d["salary"] > 60000
        ]
    )
    check(
        '(department = "Engineering" OR department = "Sales") AND active = true',
        [
            d for d in docs
            if (d["department"] == "Engineering" or d["department"] == "Sales")
            and d["active"]
        ]
    )
    check(
        '(country = "India" AND department = "Engineering") OR salary > 100000',
        [
            d for d in docs
            if (d["country"] == "India" and d["department"] == "Engineering")
            or d["salary"] > 100000
        ]
    )
    #stress tests
    check(
        'country IN ("India","USA") AND age >= 25',
        [
            d for d in docs
            if d["country"] in ("India", "USA")
            and d["age"] >= 25
        ]
    )
    check(
        'country NOT IN ("India","USA") OR salary < 50000',
        [
            d for d in docs
            if d["country"] not in ("India", "USA")
            or d["salary"] < 50000
        ]
    )
    check(
        'NOT (department = "HR" OR active = false)',
        [
            d for d in docs
            if not (d["department"] == "HR" or d["active"] == False)
        ]
    )
    check(
        '(salary BETWEEN 50000 AND 80000 AND age > 25) OR country = "Canada"',
        [
            d for d in docs
            if (50000 <= d["salary"] <= 80000 and d["age"] > 25)
            or d["country"] == "Canada"
        ]
    )
    #edges cases
    check(
        'country = "Mars"',
        [d for d in docs if d["country"] == "Mars"]
    )

    check(
        "salary > 1000000",
        [d for d in docs if d["salary"] > 1000000]
    )

    check(
        "age < 0",
        [d for d in docs if d["age"] < 0]
    )
    check(
        'country IN ("India")',
        [d for d in docs if d["country"] in ("India",)]
    )

    check(
        'country NOT IN ("India")',
        [d for d in docs if d["country"] not in ("India",)]
    )

    check(
        "salary BETWEEN 70000 AND 70000",
        [d for d in docs if 70000 <= d["salary"] <= 70000]
    )
    check(
        "age >= 18 AND age <= 60",
        [d for d in docs if d["age"] >= 18 and d["age"] <= 60]
    )

    check(
        "NOT (salary > 90000)",
        [d for d in docs if not (d["salary"] > 90000)]
    )

if __name__ == "__main__":
    NUM_DATASETS = 10

    for i in range(NUM_DATASETS):
        random.seed(i)

        print(f"Testing dataset {i+1}/{NUM_DATASETS}")

        docs = generate_dataset(50)

        try:
            test_dataset(docs)
        except Exception as e:
            print(f"\n❌ FAILED on dataset {i+1}")
            print(f"Seed: {i}")
            print(e)
            break
    else:
        print(f"\n🎉 All {NUM_DATASETS} datasets passed!")