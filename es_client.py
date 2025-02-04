from elasticsearch import Elasticsearch, exceptions
from config import (
    ES_HOST,
    ES_PORT,
    ES_SCHEME,
    ES_VERIFY_CERTS,
    ES_APIKEY
)
from debugflags import debugflags


def get_es_client() -> Elasticsearch:
    """
    Initialize connection to Elasticsearch API.
    """

    # Splitting the API key into ID and Secret if it is in the format "id:secret"
    api_key_parts = ES_APIKEY.split(":", 1)
    if len(api_key_parts) == 2:
        api_key_id, api_key_secret = api_key_parts
        api_key = (api_key_id, api_key_secret)
    else:
        # If API Key does not contain ":", use as single string
        api_key = ES_APIKEY

    # Initialize connection to Elasticsearch API
    # Should be in try..except block but catching exceptions is not working properly
    es = Elasticsearch(
        hosts=[{
            "scheme": ES_SCHEME,
            "host": ES_HOST,
            "port": ES_PORT
        }],
        api_key=api_key,
        verify_certs=ES_VERIFY_CERTS,
    )
    # Checking connection
    if not es.ping():
        print("[ERROR] Error in connecting to Elasticsearch API")
        return None
    else:
        if debugflags.get_debbugging_flag():
            print("Connected to Elasticsearch API")
        return es


def query_es(query_body: dict, index: str) -> dict:
    """
    Sends a query (query_body) in JSON DSL format to Elasticsearch
    and returns results in the form of a dictionary.

    Authentication is done in http_api_key mode,
    with the key retrieved from config.py (ES_APIKEY).
    """
    es = get_es_client()
    if es is None:
        print("[ERROR] connection to Elasticsearch was not properly initiated.")
        return {}

    if debugflags.get_debbugging_flag():
        print("### Initiating Elasticsearch query ###")
        print(f"Index: {index}")
        print("### Query body ###")
        print(query_body)
        print("### Type of query_body ###")
        print(type(query_body))
        print("")

    try:
        response = es.search(
            index=index,
            body=query_body
        )

        return response.body
    except exceptions.ApiError as e:
        print(f"[ERROR] Error in executing Elasticsearch API call: {e}")
        return {}


def mapping_es(index: str) -> dict:
    """
    Sends a query (query_body) in JSON DSL format to Elasticsearch
    and returns the results as a dictionary.

    Authentication is performed using the http_api_key mode,
    with the key retrieved from config.py (ES_APIKEY).
    """

    es = get_es_client()
    if es is None:
        print("[ERROR] Connection to Elasticsearch was not properly initiated.")
        return {}

    try:
        response = es.indices.get_mapping(index=index)

        if debugflags.get_debbugging_flag():
            print("Index mapping downloaded from Elasticsearch")
        return response.body
    except exceptions.ApiError as e:
        print(f"[ERROR] Error executing elasticsearch query for index mapping: {e}")
        return {}
