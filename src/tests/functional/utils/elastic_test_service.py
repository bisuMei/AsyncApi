import logging
from typing import List

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

logger = logging.getLogger()


class ElasticTestService:
    """Elastic service for tests."""

    def __init__(self, es: AsyncElasticsearch):
        self.es = es

    async def create_index(self, index_name: str, index_settings: dict) -> bool:
        """Create index if not exist."""

        created = False

        try:
            if not await self.es.indices.exists(index=index_name):
                # Ignore 400 means to ignore "Index Already Exist" error.
                await self.es.indices.create(index=index_name, ignore=400, body=index_settings)
                logger.info('Index created')
            created = True
        except Exception as ex:
            logger.exception("Something went wrong in create index: %s", str(ex))
        finally:
            return created

    async def delete_index(self, index_name: str):

        deleted = False
        await self.es.indices.delete(index=index_name)
        return deleted

    async def gendata(self, index_name: str, docs: List[dict]) -> dict:
        for doc in docs:
            yield {
                "_index": index_name,
                "_id": doc['id'],
                "_source": doc
            }

    async def bulk_store(self, index_name: str, list_of_record: List[dict]) -> None:
        try:
            await async_bulk(self.es, self.gendata(index_name, list_of_record))
        except Exception as ex:
            logger.exception('Error in indexing data: %s', str(ex))
