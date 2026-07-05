
class QueryExecutor:
  def __init__(self,engine):
    self.engine=engine

  def execute(self, node):
    if node.is_leaf():
      return self.execute_condition(node.field,node.comparison,node.value)
    if node.operator == "AND":
      return self.engine.query_and([self.execute(node.left),self.execute(node.right)])
    if node.operator == "OR":
      return self.engine.query_or([self.execute(node.left),self.execute(node.right)])
    if node.operator == "NOT":
      return self.engine.query_not(self.execute(node.left))
    raise ValueError("Unknown node")

  def execute_condition(self, field, operator, value):
    if field not in self.engine.schema:
      raise ValueError(f"Unknown field '{field}'")
    # Numeric / Date fields
    if self.engine.schema[field]["bsi"]:
      if operator in ("=","=="):
        return self.engine.equals_numeric(field, value)
      elif operator == "!=":
        return self.engine.query_not(self.engine.equals_numeric(field, value))
      elif operator == ">":
        return self.engine.greater_than(field, value)
      elif operator == ">=":
        return self.engine.greater_than_equals(field, value)
      elif operator == "<":
        return self.engine.less_than(field, value)
      elif operator == "<=":
        return self.engine.less_than_equals(field, value)
      elif operator == "IN":
        return self.engine.query_in(field, value)
      elif operator == "NOT IN":
        return self.engine.query_not_in(field, value)
      elif operator == "BETWEEN":
        low, high = value
        return self.engine.between(field, low, high)
      else:
        raise ValueError(f"{operator} is not supported for numerical fields")
    # Categorical fields
    else:
      if operator in ("=","=="):
        return self.engine.lookup(field, value)
      elif operator == "!=":
        self.engine.validate_query_value(field, value)
        return self.engine.query_not(self.engine.lookup(field, value))
      elif operator == "IN":
        return self.engine.query_in(field, value)
      elif operator == "NOT IN":
        return self.engine.query_not_in(field, value)
      else:
        raise ValueError(f"{operator} is not supported for categorical fields")