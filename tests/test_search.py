from search_engine.engine import SearchEngine

docs = [
{"name":"Alice","age":21,"salary":45000,"country":"India","department":"HR","active":True,"joining":"2022-01-15"},
{"name":"Bob","age":30,"salary":70000,"country":"USA","department":"Engineering","active":False,"joining":"2022-06-01"},
{"name":"Charlie","age":35,"salary":65000,"country":"India","department":"Engineering","active":True,"joining":"2021-09-20"},
{"name":"David","age":28,"salary":80000,"country":"Canada","department":"Sales","active":True,"joining":"2023-03-11"},
{"name":"Eva","age":25,"salary":52000,"country":"Germany","department":"HR","active":False,"joining":"2020-07-18"},
{"name":"Frank","age":40,"salary":95000,"country":"USA","department":"Management","active":True,"joining":"2019-11-09"},
{"name":"Grace","age":32,"salary":62000,"country":"India","department":"Marketing","active":True,"joining":"2021-05-22"},
{"name":"Henry","age":27,"salary":58000,"country":"UK","department":"Engineering","active":False,"joining":"2022-08-10"},
{"name":"Isabella","age":29,"salary":72000,"country":"Canada","department":"Sales","active":True,"joining":"2023-01-05"},
{"name":"Jack","age":31,"salary":68000,"country":"India","department":"Engineering","active":True,"joining":"2022-12-12"},
{"name":"Karen","age":24,"salary":48000,"country":"Germany","department":"HR","active":False,"joining":"2020-10-30"},
{"name":"Leo","age":45,"salary":110000,"country":"USA","department":"Management","active":True,"joining":"2018-04-17"},
{"name":"Mia","age":26,"salary":56000,"country":"India","department":"Marketing","active":True,"joining":"2021-06-28"},
{"name":"Nathan","age":38,"salary":88000,"country":"Canada","department":"Engineering","active":False,"joining":"2019-09-09"},
{"name":"Olivia","age":22,"salary":47000,"country":"UK","department":"Sales","active":True,"joining":"2023-02-14"},
{"name":"Peter","age":33,"salary":76000,"country":"India","department":"Engineering","active":True,"joining":"2022-05-19"},
{"name":"Queen","age":37,"salary":90000,"country":"Germany","department":"Management","active":True,"joining":"2019-08-08"},
{"name":"Ryan","age":29,"salary":61000,"country":"USA","department":"Marketing","active":False,"joining":"2020-01-11"},
{"name":"Sophia","age":34,"salary":83000,"country":"Canada","department":"Engineering","active":True,"joining":"2021-03-15"},
{"name":"Tom","age":41,"salary":99000,"country":"India","department":"Management","active":False,"joining":"2018-12-01"},
{"name":"Uma","age":23,"salary":43000,"country":"UK","department":"HR","active":True,"joining":"2023-06-01"},
{"name":"Victor","age":36,"salary":87000,"country":"USA","department":"Sales","active":True,"joining":"2020-09-09"},
{"name":"Wendy","age":28,"salary":59000,"country":"India","department":"Engineering","active":True,"joining":"2022-11-11"},
{"name":"Xavier","age":39,"salary":93000,"country":"Germany","department":"Management","active":False,"joining":"2019-02-20"},
{"name":"Yara","age":27,"salary":54000,"country":"Canada","department":"Marketing","active":True,"joining":"2021-10-10"},
{"name":"Zack","age":42,"salary":102000,"country":"USA","department":"Management","active":True,"joining":"2018-01-01"},
{"name":"Aaron","age":20,"salary":41000,"country":"India","department":"HR","active":False,"joining":"2023-07-01"},
{"name":"Bella","age":26,"salary":55000,"country":"UK","department":"Engineering","active":True,"joining":"2022-04-12"},
{"name":"Chris","age":31,"salary":71000,"country":"Canada","department":"Sales","active":False,"joining":"2021-08-18"},
{"name":"Diana","age":35,"salary":85000,"country":"Germany","department":"Management","active":True,"joining":"2020-06-06"},
{"name":"Ethan","age":29,"salary":60000,"country":"India","department":"Marketing","active":True,"joining":"2022-03-03"},
{"name":"Fiona","age":24,"salary":50000,"country":"USA","department":"HR","active":False,"joining":"2021-12-12"},
{"name":"George","age":37,"salary":91000,"country":"Canada","department":"Engineering","active":True,"joining":"2019-07-14"},
{"name":"Hannah","age":33,"salary":77000,"country":"UK","department":"Sales","active":True,"joining":"2020-02-02"},
{"name":"Ian","age":30,"salary":69000,"country":"India","department":"Engineering","active":False,"joining":"2022-09-09"},
{"name":"Julia","age":28,"salary":63000,"country":"Germany","department":"Marketing","active":True,"joining":"2021-04-04"},
{"name":"Kevin","age":43,"salary":108000,"country":"USA","department":"Management","active":True,"joining":"2018-10-10"},
{"name":"Lily","age":25,"salary":53000,"country":"Canada","department":"HR","active":False,"joining":"2023-05-05"},
{"name":"Mark","age":34,"salary":82000,"country":"India","department":"Sales","active":True,"joining":"2020-11-11"},
{"name":"Nina","age":27,"salary":57000,"country":"Germany","department":"Engineering","active":True,"joining":"2022-02-22"},
{"name":"Oscar","age":32,"salary":74000,"country":"USA","department":"Engineering","active":False,"joining":"2021-01-01"},
{"name":"Paula","age":23,"salary":46000,"country":"India","department":"HR","active":True,"joining":"2023-04-04"},
{"name":"Quentin","age":38,"salary":92000,"country":"Canada","department":"Management","active":True,"joining":"2019-05-15"},
{"name":"Rose","age":26,"salary":56000,"country":"UK","department":"Marketing","active":False,"joining":"2022-07-07"},
{"name":"Sam","age":31,"salary":70000,"country":"India","department":"Engineering","active":True,"joining":"2021-11-30"},
{"name":"Tina","age":36,"salary":86000,"country":"Germany","department":"Sales","active":True,"joining":"2020-08-08"},
{"name":"Umar","age":29,"salary":62000,"country":"USA","department":"Marketing","active":False,"joining":"2022-10-20"},
{"name":"Vera","age":40,"salary":97000,"country":"Canada","department":"Management","active":True,"joining":"2018-03-03"},
{"name":"Will","age":28,"salary":61000,"country":"India","department":"Engineering","active":True,"joining":"2023-01-15"},
{"name":"Zoe","age":33,"salary":78000,"country":"UK","department":"Sales","active":False,"joining":"2021-02-28"},
]

engine = SearchEngine()
engine.index_documents(docs)

def check(query, expected):
    try:
        actual = sorted(engine.search(query), key=lambda d: d["name"])
        expected = sorted(expected, key=lambda d: d["name"])

        if actual == expected:
            print(f"✅ PASS: {query}")
        else:
            print(f"❌ FAIL: {query}")
            print(f"Expected {len(expected)} docs, got {len(actual)} docs")
            print("Expected:", [d["name"] for d in expected])
            print("Actual  :", [d["name"] for d in actual])
    except Exception as e:
        print(f"💥 EXCEPTION: {query}")
        print(type(e).__name__, e)

#Numeric Quries

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

#parser stress tests
check(
    '(((country = "India")))',
    [
        d for d in docs
        if d["country"] == "India"
    ]
)
check(
    '(country = "India" AND (department = "Engineering" OR department = "HR"))',
    [
        d for d in docs
        if d["country"] == "India"
        and (
            d["department"] == "Engineering"
            or d["department"] == "HR"
        )
    ]
)
check(
    'NOT (country = "India" AND active = true)',
    [
        d for d in docs
        if not (
            d["country"] == "India"
            and d["active"] == True
        )
    ]
)
check(
    '(age > 25 AND salary < 90000) OR (country = "USA")',
    [
        d for d in docs
        if (
            d["age"] > 25
            and d["salary"] < 90000
        )
        or d["country"] == "USA"
    ]
)
check(
    'NOT ((country = "India") OR (department = "HR"))',
    [
        d for d in docs
        if not (
            d["country"] == "India"
            or d["department"] == "HR"
        )
    ]
)
check(
    'NOT country = "India" OR age > 30',
    [
        d for d in docs
        if (not (d["country"] == "India"))
        or d["age"] > 30
    ]
)
check(
    'NOT (NOT (country = "India"))',
    [
        d for d in docs
        if not (not (d["country"] == "India"))
    ]
)
check(
    '(((country = "India") AND ((department = "Engineering"))))',
    [
        d for d in docs
        if d["country"] == "India"
        and d["department"] == "Engineering"
    ]
)
check(
    '((country = "India" OR country = "USA") AND (salary > 60000 AND age < 40))',
    [
        d for d in docs
        if (
            d["country"] == "India"
            or d["country"] == "USA"
        )
        and (
            d["salary"] > 60000
            and d["age"] < 40
        )
    ]
)