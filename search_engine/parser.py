from search_engine.query_node import QueryNode
import re

class QueryParser:
  def __init__(self,schema):
    self.schema = schema
    self.KEYWORDS = {
      "NOT IN",
      "BETWEEN",
      "AND",
      "OR",
      "NOT",
      "IN"
    }
    self.VALID_OPERATORS = {
      "=",
      "==",
      "!=",
      ">",
      ">=",
      "<",
      "<=",
      "IN",
      "NOT IN",
      "BETWEEN"
    }
    self.tokens = []
    self.current = 0

  def tokenize(self, query):
    pattern = r'"[^"]*"|\'[^\']*\'|\bNOT\s+IN\b|\bBETWEEN\b|\bAND\b|\bOR\b|\bNOT\b|\bIN\b|>=|<=|!=|==|=|>|<|\(|\)|,|[A-Za-z0-9_.-]+'
    # Detect unterminated quotes before tokenizing -- check each quote
    # style independently, since one could be balanced while the other isn't.
    if query.count('"') % 2 != 0:
      raise ValueError(f"Unterminated double-quoted string in query: {query!r}")
    if query.count("'") % 2 != 0:
      raise ValueError(f"Unterminated single-quoted string in query: {query!r}")
    pos = 0
    tokens = []
    for match in re.finditer(pattern, query, flags=re.IGNORECASE):
      # Catch characters between matches that the pattern doesn't cover
      # (e.g. *, %, $) instead of silently skipping them.
      gap = query[pos:match.start()]
      if gap.strip():
        raise ValueError(f"Unrecognized character(s) {gap.strip()!r} in query: {query!r}")
      pos = match.end()
      token = match.group()
      token = token.strip()
      if (token.startswith('"') and token.endswith('"')) or \
         (token.startswith("'") and token.endswith("'")):
          token = token[1:-1]
      else:
          # Collapse internal whitespace (handles "NOT   IN" -> "NOT IN")
          token = re.sub(r'\s+', ' ', token)
          # Normalize keyword casing so downstream comparisons are reliable
          if token.upper() in self.KEYWORDS:
              token = token.upper()
      tokens.append(token)
    # Check for trailing unrecognized characters after the last match
    trailing = query[pos:]
    if trailing.strip():
        raise ValueError(f"Unrecognized character(s) {trailing.strip()!r} in query: {query!r}")
    return tokens

  def peek(self):
    if self.current >= len(self.tokens):
      return None
    return self.tokens[self.current]

  def consume(self):
    token = self.peek()
    if token is None:
      raise ValueError("Unexpected end of query")
    self.current += 1
    return token

  def parse(self, query):
    self.tokens = self.tokenize(query)
    self.current = 0
    root = self.parse_expression()
    if self.peek() is not None:
      raise ValueError(f"Unexpected token '{self.peek()}'")
    return root

  def parse_expression(self):
    return self.parse_or()

  def parse_or(self):
    node = self.parse_and()#parse everything on the left side fist as and has higher presedence
    while self.peek() == "OR":
      self.consume()
      right = self.parse_and()#parse everything on the right side
      node = QueryNode(operator="OR",left=node,right=right)
    return node

  def parse_and(self):
    node = self.parse_not()#parse everything on the left side fist as and has higher presedence
    while self.peek() == "AND":
      self.consume()
      right = self.parse_not()#parse everything on the right side
      node = QueryNode(operator="AND",left=node,right=right)
    return node

  def parse_not(self):
    if self.peek() == "NOT":
      self.consume()
      return QueryNode(operator="NOT",left=self.parse_not())
    return self.parse_primary()

  def parse_primary(self):
    if self.peek() == "(":
      self.consume()
      node = self.parse_expression()
      if self.peek() != ")":
        raise ValueError("Expected ')'")
      self.consume()
      return node
    return self.parse_condition()

  def parse_condition(self):
    field = self.consume()
    if field not in self.schema:
      raise ValueError(f"Unknown field '{field}'")
    operator = self.consume()
    if operator not in self.VALID_OPERATORS:
      raise ValueError(f"Unknown operator '{operator}'")
    # BETWEEN
    if operator == "BETWEEN":
      low = self.consume()
      if self.consume() != "AND":
        raise ValueError("Expected AND inside BETWEEN")
      high = self.consume()
      low = self.convert_value(field, low)
      high = self.convert_value(field, high)
      return QueryNode(field=field,comparison="BETWEEN",value=(low, high))
    # IN / NOT IN
    elif operator in ("IN", "NOT IN"):
      if self.consume() != "(":
        raise ValueError("Expected '('")
      values = []
      while True:
        values.append(self.convert_value(field, self.consume()))
        token = self.consume()
        if token == ")":
          break
        if token != ",":
          raise ValueError("Expected ',' or ')'")
      return QueryNode(field=field,comparison=operator,value=values)
    # Normal comparison
    else:
      value = self.consume()
      value = self.convert_value(field, value)
      return QueryNode(field=field,comparison=operator,value=value)

  def convert_value(self, field, value):
    field_type = self.schema[field]["type"]
    if field_type == "int":
      return int(value)
    elif field_type == "float":
      return float(value)
    elif field_type == "bool":
      if value.lower() == "true":
        return True
      if value.lower() == "false":
        return False
      raise ValueError("Boolean must be true or false")
    return value