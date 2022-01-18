from elasticsearch import AsyncElasticsearch


class ElasticSearchService:
    """Elastic service."""

    person_query = {
        "match": {
            "full_name": {
                "query": "{name}",
                "fuzziness": "AUTO"
            }
        }
    }

    films_query = {
        '_source': ['id', 'title', 'imdb_rating'],
        'query': {
            'ids': {
                'values': []
            }
        }
    }

    def __init__(self, es: AsyncElasticsearch):
        self.es = es

    async def get(self, index: str, instance_id: str):
        doc = await self.es.get(index=index, id=instance_id)
        return doc

    async def search(self, index: str, query: dict = None):
        doc = await self.es.search(index=index, body=query)
        return doc
