from whoosh.index import open_dir
from whoosh.fields import Schema, TEXT, ID
from django.conf import settings


index_dir = "indexdir"

schema = Schema(tender_id=ID(stored=True, unique=True))

ix = open_dir(index_dir)
reader = ix.reader()

print('Indexed Documents:')
for docnum in reader.document_ids():
    doc = reader[docnum]
    tender_id = doc.get("tender_id")
    print(f"  - Document {docnum}: tender_id = {tender_id}")

reader.close()
