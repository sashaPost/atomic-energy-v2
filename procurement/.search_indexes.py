from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh.query import Term, Or
import os
from django.conf import settings
from .models import Procurement
import logging


logger = logging.getLogger(__name__)


# 1. Schema Definition:
procurement_schema = Schema(
    tender_id=ID(stored=True, unique=True)
)


# 2. Index Setup:
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
index = create_in(os.path.join(settings.BASE_DIR, "indexdir"), procurement_schema)


# 3. Index Updater After Function:
def update_index():
    logger.info(f"* 'update_index' was triggered *")
    writer = index.writer()
    for procurement in Procurement.objects.all():
        writer.add_document(
            tender_id=procurement.tender_id
        )
    writer.commit()
    
    
# 4. Takes a query string, splits it into words, and performs an OR search on the tender_id field for each word:
def search_procurements(query_string):
    with index.reader() as reader:
        searcher = reader.searcher()
        query = Or([Term("tender_id", word) for word in query_string.split()])
        results = searcher.search(query, limit=3)
        return [hit["tender_id"] for hit in results]