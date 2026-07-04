from pyroaring import BitMap
class BSI:
  def __init__(self):
    self.slices=[]
    self.all_docs=BitMap()

  def ensure_slices(self,value):
    bits = max(1, value.bit_length())
    while len(self.slices)<bits:
      self.slices.append(BitMap())

  def add(self,doc_id,value):
    self.ensure_slices(value)
    self.all_docs.add(doc_id)
    for i in range(len(self.slices)):
      if ((value>>i)&1)==1:       #if the i'th bit is 1 we add the document to slice[i]
        self.slices[i].add(doc_id)

  def print_slices(self):
    for i, bitmap in enumerate(self.slices):
        print(f"Slice {i}: {list(bitmap)}")

  def equals(self, value):
    if value.bit_length() > len(self.slices):
        return BitMap()
    answer = self.all_docs.copy()
    bits = max(len(self.slices), value.bit_length())
    for i in range(bits):
      if ((value >> i) & 1) == 1:
        answer &= self.slices[i]
      else:
        zero_bitmap = self.all_docs - self.slices[i]#documents which have this bit zero
        answer &= zero_bitmap
    return answer

  def greater_than(self,value):
    if value.bit_length() > len(self.slices):
      for i in range(len(self.slices), value.bit_length()):
        if ((value >> i) & 1):
            return BitMap()
    equal=self.all_docs.copy()#initially all documents present here
    greater=BitMap()#initially empty
    for i in reversed(range(len(self.slices))):
      bit=(value>>i)&1
      if bit==1:
      #eg if ith  bit of value is 1; out of all documents only documents whose ith 1 can be tied and later be > value
      #who has ith bit 1 in this case? slice[i] so we intersect from that
        equal&=self.slices[i]
      else:#if i'th bit is zero
        #out of all documents
        #documents with i'th bit 1 automatically become greater
        #remaining all leftover docs must have ith bit 0
        greater|=equal&self.slices[i]
        zero_bitmap=self.all_docs-self.slices[i]
        equal&=zero_bitmap
    return greater

  def greater_than_equals(self,value):
    return self.greater_than(value)|self.equals(value)

  def less_than(self,value):
    return self.all_docs-(self.greater_than(value)|self.equals(value))

  def less_than_equals(self,value):
    return self.less_than(value)|self.equals(value)

  def get_value(self, doc_id): #returns the original value of a document
    value=0
    for i in range(len(self.slices)):
      if(self.slices[i].contains(doc_id)):
        value|=(1<<i)
    return value
