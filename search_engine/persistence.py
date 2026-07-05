import pickle
import os

class Persistence:
  #it is not storing states so make the functions static
  @staticmethod
  def save(engine,path):
    directory = os.path.dirname(path)
    if directory:
      os.makedirs(directory,exist_ok=True)
    state={
      "schema":engine.schema,
      "index":engine.index,
      "bsi_index":engine.bsi_index,
      "documents":engine.documents,
      "all_docs":engine.all_docs,
      "next_doc_id":engine.next_doc_id,
      "float_scale":engine.float_scale,
      "ignored_fields":engine.ignored_fields,
      "field_present":engine.field_present
    }
    with open(path,"wb")as f:
      pickle.dump(state,f)

  @staticmethod
  def load(path):
    from .engine import SearchEngine #to avoid circulir import
    with open(path,"rb") as f:
      state=pickle.load(f)
    engine=SearchEngine()
    engine.schema=state["schema"]
    engine.index=state["index"]
    engine.bsi_index=state["bsi_index"]
    engine.documents=state["documents"]
    engine.all_docs=state["all_docs"]
    engine.next_doc_id=state["next_doc_id"]
    engine.float_scale=state["float_scale"]
    engine.ignored_fields=state["ignored_fields"]
    engine.field_present=state["field_present"]
    return engine

