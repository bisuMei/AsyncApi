from typing import Optional

from elasticsearch import AsyncElasticsearch
from pydantic import BaseModel


class QueryParameters(BaseModel):
    """Model for query parameters."""
    sort: Optional[str] = None
    limit: Optional[str] = None
    page: Optional[str] = None
    filter_: Optional[str] = None
    query: Optional[str] = None


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
 
    async def make_film_query(
        self,
        query_obj: dict,
        query_params: QueryParameters
    ) -> dict:
        """Make query for ES from query parameters."""              
        if query_params.sort:
            if '-' in query_params.sort:
                order = 'desc'
                field = query_params.sort.split('-')[-1]
            else:
                order = 'asc'
                field = query_params.sort
            field = 'title.raw' if field == 'title' else field
            query_obj['sort'] = [{field: {'order': order}}]

        if query_params.filter_:
            query_obj['query'] = {'match': {'genre': query_params.filter_}}

        if query_params.query:
            query_obj['query'] = {
                'multi_match': {
                    'query': f'{query_params.query}', 'fuzziness': 'auto',
                    'fields': [
                        'actors_names',
                        'writers_names',
                        'title',
                        'description',
                        'genre'
                    ]
                }
            }

        query_obj['size'] = query_params.limit if query_params.limit else 10
        query_obj['from'] = int(query_params.page) * int(query_obj['size']) - int(query_obj['size']) if query_params.page else 0

        return query_obj
    
    async def make_person_query(
        self,
        query_obj: dict,
        query_params: QueryParameters
    ) -> dict:
        print(query_params)
        if query_params.query:            
            ElasticSearchService.person_query['match']['full_name']['query'] = query_params.query
            query_obj['query'] = ElasticSearchService.person_query
        query_obj['size'] = query_params.limit if query_params.limit else 10
        query_obj['from'] = int(query_params.page) * int(query_obj['size']) - int(query_obj['size']) if query_params.page else 0

        return query_obj