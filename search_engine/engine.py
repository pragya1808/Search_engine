from search_engine.parser import QueryParser
from search_engine.bsi import BSI
from pyroaring import BitMap
from search_engine.executor import QueryExecutor
from datetime import datetime,date
from .persistence import Persistence

class SearchEngine:
    def __init__(self, ignored_fields=None):
        self.schema = {}
        self.index = {}#categorical values
        self.bsi_index={}#numerical values
        self.documents = {}
        self.all_docs=BitMap();
        self.next_doc_id = 0
        self.float_scale=1000
        self.ignored_fields = {
            field.lower()
            for field in (ignored_fields or set())
        }
        self.field_present = {}

    # Determine field type
    def determine_type(self, value):
        if isinstance(value, bool):
            return "bool"
        elif isinstance(value, int):
            return "int"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, str):
            try:
                datetime.strptime(value, "%Y-%m-%d")
                return "date"
            except ValueError:
                return "categorical"
        return "unknown"

    # Build schema
    def build_schema(self, doc):
        for key, value in doc.items():
            if key.lower() in self.ignored_fields:
                continue
            if key in self.schema:
                continue
            field_type = self.determine_type(value)
            if field_type == "unknown":
                raise ValueError(f"Unsupported field type for {key}")
            if (field_type == "int" or field_type=="float") and value < 0:
                raise ValueError("Negative integers are not supported.")
            self.schema[key] = {
                "type": field_type,
                "bitmap": field_type in ("categorical", "bool"),
                "bsi": field_type in ("int", "float", "date"),
            }

    def encode_numeric(self, field, value):
        field_type = self.schema[field]["type"]
        if field_type == "date":
            return datetime.strptime(value, "%Y-%m-%d").toordinal()
        if field_type == "float":
            return int(round(value * self.float_scale))
        return value

    def validate_query_value(self, field, value):
        if field not in self.schema:
            raise ValueError(f"Unknown field '{field}'")
        expected = self.schema[field]["type"]
        actual = self.determine_type(value)
        if actual in ("int", "float") and value < 0:
            raise ValueError("Negative numeric values are not supported.")
        if actual != expected:
            raise ValueError(f"Field '{field}' expects {expected}, got {actual}")

    def _validate_document(self, doc):
        #vaildation
        for field, value in doc.items():
            # Ignore fields that aren't indexed
            if field.lower() in self.ignored_fields:
                continue
            field_type = self.determine_type(value)
            if field_type=="unknown":
                raise ValueError(f"Unsupported type for field {field}")
            if field not in self.schema:
                raise ValueError(f"Unknown field {field}")
            if field_type != self.schema[field]["type"]:
                raise ValueError(f"{field} should be {self.schema[field]['type']}")
            if field_type in ("int", "float") and value < 0:
                raise ValueError("Negative integers are not supported.")

    def _index_fields(self, doc_id, doc):
        #index
        for field, value in doc.items():
            if field.lower() in self.ignored_fields:
                continue
            if field not in self.field_present:
                self.field_present[field] = BitMap()
            self.field_present[field].add(doc_id)
            #BSI
            if self.schema[field]["bsi"]:
                if field not in self.bsi_index:
                    self.bsi_index[field] = BSI()
                encoded_value = self.encode_numeric(field, value)
                self.bsi_index[field].add(doc_id, encoded_value)
            #bitmap
            if not self.schema[field]["bitmap"]:
                continue
            if field not in self.index:
                self.index[field] = {}
            if value not in self.index[field]:
                self.index[field][value] = BitMap()
            self.index[field][value].add(doc_id)


    # Index one document
    def create_document(self, doc):
        # Update schema with any newly discovered fields
        self.build_schema(doc)
        self._validate_document(doc)
        doc_id = self.next_doc_id
        # Save original document
        self.documents[doc_id] = doc
        self.all_docs.add(doc_id)
        #index
        self._index_fields(doc_id,doc)
        self.next_doc_id += 1
        return doc_id


    index_document = create_document
    # batch ingest
    def index_documents(self, docs):
        for doc in docs:
            self.index_document(doc)

    ## Persistence
    def save(self,path):
        Persistence.save(self,path)

    @classmethod
    def load(cls, path):
        return Persistence.load(path)

    ## CRUD
    #Read
    def get_document(self,doc_id):
        if doc_id not in self.documents:
            raise KeyError(f"Document with id {doc_id} does not exist.")
        return self.documents[doc_id]

    #Delete
    def delete_document(self,doc_id):
        if doc_id not in self.documents:
            raise KeyError(f"Document with id {doc_id} does not exist.")
        doc = self.documents[doc_id]
        for field,value in doc.items():
            if field.lower() in self.ignored_fields:
                continue
            if doc_id in self.field_present[field]:
                self.field_present[field].remove(doc_id)
            if len(self.field_present[field]) == 0:
                del self.field_present[field]
            if self.schema[field]["bsi"]:
                encoded_value = self.encode_numeric(field, value)
                self.bsi_index[field].remove(doc_id, encoded_value)
                if len(self.bsi_index[field].all_docs) == 0:
                    del self.bsi_index[field]

            if self.schema[field]["bitmap"]:
                bitmap = self.index[field][value]
                if doc_id in bitmap:
                    bitmap.remove(doc_id)
                if len(bitmap) == 0:
                    del self.index[field][value]
                if len(self.index[field]) == 0:
                    del self.index[field]

        self.all_docs.remove(doc_id)
        del self.documents[doc_id]
        return True

    #update
    def update_document(self, doc_id, new_doc):
        if doc_id not in self.documents:
            raise KeyError(f"Document with id {doc_id} does not exist.")
        self.build_schema(new_doc)
        self._validate_document(new_doc)
        old_doc = self.documents[doc_id]
        updated_doc=old_doc.copy()
        updated_doc.update(new_doc)
        self.delete_document(doc_id)
        self.documents[doc_id] = updated_doc
        self.all_docs.add(doc_id)
        self._index_fields(doc_id,updated_doc)
        return doc_id




    # BitMap operation
    def lookup(self, field, value):## returns bitmap
        if field not in self.schema:
            raise ValueError(f"Unknown field '{field}'")
        if field not in self.index:
            return BitMap()
        if value not in self.index[field]:
            return BitMap()
        return self.index[field][value]

    def query_and(self, results):
        if not results:
            return BitMap()
        answer = results[0].copy()
        for result in results[1:]:
            answer &= result
        return answer

    def query_or(self, results):
        if not results:
            return BitMap()
        answer = results[0].copy()
        for result in results[1:]:
            answer |= result
        return answer

    def query_not(self, result):
        return self.all_docs - result

    def query_in(self, field, values):
        if field not in self.schema:
            raise ValueError(f"Unknown field '{field}'")
        if self.schema[field]["bsi"]:
            if field not in self.bsi_index:
                return BitMap()
            results = []
            for value in values:
                self.validate_query_value(field, value)
                value = self.encode_numeric(field, value)
                results.append(self.bsi_index[field].equals(value))#BSI returns bitmap of matching documents
            return self.query_or(results)#which is why query or works here
        else:
            results = []
            for value in values:
                results.append(self.lookup(field, value))
            return self.query_or(results)

    def query_not_in(self, field, values):#works for both categorical and numeric
        result = self.query_in(field, values)
        return self.query_not(result)

    ##Numeric Operations
    def greater_than(self,field,value):
        self.validate_query_value(field, value)
        if field not in self.bsi_index:
            raise ValueError(f"{field} is not a numeric field")
        value = self.encode_numeric(field, value)
        return self.bsi_index[field].greater_than(value)

    def greater_than_equals(self,field,value):
        self.validate_query_value(field, value)
        if field not in self.bsi_index:
            raise ValueError(f"{field} is not a numeric field")
        value = self.encode_numeric(field, value)
        return self.bsi_index[field].greater_than_equals(value)

    def less_than(self,field,value):
        self.validate_query_value(field, value)
        if field not in self.bsi_index:
            raise ValueError(f"{field} is not a numeric field")
        value = self.encode_numeric(field, value)
        return self.bsi_index[field].less_than(value)

    def less_than_equals(self,field,value):
        self.validate_query_value(field, value)
        if field not in self.bsi_index:
            raise ValueError(f"{field} is not a numeric field")
        value = self.encode_numeric(field, value)
        return self.bsi_index[field].less_than_equals(value)

    def equals_numeric(self,field,value):
        self.validate_query_value(field, value)
        if field not in self.bsi_index:
            return BitMap()
        value = self.encode_numeric(field, value)
        return self.bsi_index[field].equals(value)

    def between(self, field, low, high):
        if low > high:
            raise ValueError("low must be <= high")
        if field not in self.bsi_index:
            raise ValueError(f"{field} is not a numeric field")
        self.validate_query_value(field, low)
        self.validate_query_value(field, high)
        low = self.encode_numeric(field, low)
        high = self.encode_numeric(field, high)
        return (self.bsi_index[field].greater_than_equals(low) & self.bsi_index[field].less_than_equals(high))

    def get_value(self, field, doc_id):
        if field not in self.bsi_index:
            raise ValueError(f"{field} is not a numeric field")
        value = self.bsi_index[field].get_value(doc_id)
        if self.schema[field]["type"] == "date":
            return date.fromordinal(value).strftime("%Y-%m-%d")
        elif self.schema[field]["type"] == "float":
            return value / self.float_scale
        return value

    def fetch(self, bitmap):#converts bitmap into actual documents as bitmaps return the doc_id
        docs=[]
        for doc_id in bitmap:#bitmap is the result of a query -->works on bsi too as bsi returns bitmap of doc_ids
            docs.append(self.documents[doc_id])
        return docs

    def search(self, query):
      parser = QueryParser(self.schema)
      tree = parser.parse(query)
      executor = QueryExecutor(self)
      bitmap = executor.execute(tree)
      return self.fetch(bitmap)

    def search_bitmap(self, query):
        parser = QueryParser(self.schema)
        tree = parser.parse(query)
        executor = QueryExecutor(self)
        return executor.execute(tree)

    def compile_query(self, query):
        parser = QueryParser(self.schema)
        return parser.parse(query)

    def execute_query(self, tree):
        executor = QueryExecutor(self)
        return executor.execute(tree)

    #cardinality Analysis
    def analyse_cardinality(self):
        for field in self.index:
            self.schema[field]["cardinality"] = len(self.index[field])
        return self.schema

    # def disable_high_cardinality(self,threshold):
    #     self.analyse_cardinality()
    #     for field in self.schema:
    #         if self.schema[field]["cardinality"]>threshold:
    #             self.schema[field]["indexed"]=False