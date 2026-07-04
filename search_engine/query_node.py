class QueryNode:
        def __init__(self,operator=None,left=None,right=None,field=None,value=None,comparison=None):
          self.operator = operator
          self.left = left
          self.right = right
          self.field = field #condition=("age", ">", 25)
          self.value = value
          self.comparison = comparison

        def is_leaf(self):
          return self.field is not None