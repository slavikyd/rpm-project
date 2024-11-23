import chromadb
import logging
import asyncio
from chromadb.api.models.Collection import Collection
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from chromadb.api.async_client import AsyncClient
from chromadb.config import Settings


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#TODO: сделать класс работы с клиентом

async def create_client(host: str, port: int) -> AsyncClient:
    try:
        client = await chromadb.AsyncHttpClient(
            host=host,
            port=port,
            ssl=False,
            settings=Settings(
                allow_reset=True,
                anonymized_telemetry=False
            )
        )
        logging.info(f"ChromaDB client initialized on {host}:{port}.")
        return client
    except Exception as error:
        logging.error(f"Failed to initialize ChromaRAG: {error}")
        raise error

def create_embedding_function(embedding_model: str) -> SentenceTransformerEmbeddingFunction:
    try:
        embedding_func = SentenceTransformerEmbeddingFunction(model_name=embedding_model)
        logging.info(f"Embedding function created for model {embedding_model}.")
        return embedding_func
    except Exception as error:
        logging.error(f"Failed to add embedding function: {error}")
        raise error

async def create_chroma_collection(
    client: AsyncClient,
    collection_name: str,
    embedding_func: SentenceTransformerEmbeddingFunction
) -> Collection:
    try:
        collection = await client.create_collection(name=collection_name, embedding_function=embedding_func)
        logging.info(f'ChromaDB collection initialized with name {collection_name}.')
        return collection
    except Exception as error:
        logging.error(f"Failed to get or create collection {collection_name}: {error}")
        raise error

def add_to_collection(client: AsyncClient, user_data: dict) -> None:
    """
    user_id: Mapped[int]
    name: Mapped[str]
    age: Mapped[int]
    gender: Mapped[str]
    description: Mapped[str]
    filter_by_age: Mapped[str]
    filter_by_gender: Mapped[str]
    filter_by_description: Mapped[str]
    """
    pass

async def setup_chroma(host: str, port: int, embedding_model: str, collection_name: str):
    client = await create_client(host, port)
    embedding_function = create_embedding_function(embedding_model)
    await create_chroma_collection(client, collection_name, embedding_function)
    logging.info('ChromaDB has been setup!')
    return client


if __name__ == '__main__':
    asyncio.run(setup_chroma(
        'localhost',
        4810,
        'cointegrated/rubert-tiny2',
        'datings'
        )
    )

