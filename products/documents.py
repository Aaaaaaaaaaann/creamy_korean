from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer
from elasticsearch_dsl.connections import connections

from .models import Ingredient

connections.create_connection(hosts=['localhost'])

INDEX = Index('ingredient')

INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

html_strip = analyzer(
    'html_strip',
    tokenizer='standard',
    filter=['lowercase', 'stop', 'snowball'],
    char_filter=['html_strip']
)


@INDEX.doc_type
class IngredientDocument(Document):

    id = fields.IntegerField()

    name = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword')
            }
        )
    
    class Django:
        model = Ingredient
