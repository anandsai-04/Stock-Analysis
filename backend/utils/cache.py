import os
from pinecone import Pinecone, ServerlessSpec

def get_pinecone_client():
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        return None
    return Pinecone(api_key=api_key)

def get_or_create_index(pc: Pinecone, index_name="quant-finance-cache"):
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536, # Default dimension, using as KV store
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1' # default free tier region
            )
        )
    return pc.Index(index_name)

def cache_company_details(ticker: str, details: str):
    pc = get_pinecone_client()
    if not pc:
        return
    try:
        index = get_or_create_index(pc)
        dummy_vector = [0.0] * 1536
        index.upsert(
            vectors=[
                {
                    "id": ticker.upper(),
                    "values": dummy_vector,
                    "metadata": {"details": details}
                }
            ]
        )
    except Exception as e:
        print(f"Error caching to Pinecone: {e}")

def get_cached_company_details(ticker: str):
    pc = get_pinecone_client()
    if not pc:
        return None
    try:
        index = get_or_create_index(pc)
        response = index.fetch(ids=[ticker.upper()])
        if response and response.get('vectors') and ticker.upper() in response['vectors']:
            return response['vectors'][ticker.upper()]['metadata'].get('details')
    except Exception as e:
        print(f"Error fetching from Pinecone: {e}")
    return None
