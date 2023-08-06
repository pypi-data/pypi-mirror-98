import requests
import os
import json
from hestia_earth.schema import SchemaType

from ._s3_client import _load_from_bucket, _exists_in_bucket
from .request import request_url, api_url

AWS_BUCKET = os.getenv('AWS_BUCKET')


def _safe_get_request(url: str):
    try:
        return requests.get(url).json()
    except requests.exceptions.RequestException:
        return None


def node_type_to_url(node_type: SchemaType): return f"{node_type.value.lower()}s"


def node_to_path(node_type: SchemaType, node_id: str): return f"{node_type.value}/{node_id}.jsonld"


def find_related(node_type: SchemaType, id: str, related_type: SchemaType, limit=100, offset=0, relationship=None):
    """
    Return the list of related Nodes by going through a "relationship".
    You can navigate the Hestia Graph Database using this method.

    Parameters
    ----------
    node_type
        The `@type` of the Node to start from. Example: use `SchemaType.Cycle` to find nodes related to a `Cycle`.
    id
        The `@id` of the Node to start from.
    related_type
        The other Node to which the relation should go to. Example: use `SchemaType.Source` to find `Source` related to
        `Cycle`.
    limit
        The limit of relationships to return. Asking for large number might result in timeouts.
    offset
        Use with limit to paginate through the results.
    relationship
        The relationship used to connect both Node. See the API for more information.
    """
    url = request_url(f"{api_url()}/{node_type_to_url(node_type)}/{id}/{node_type_to_url(related_type)}",
                      limit=limit, offset=offset, relationship=relationship)
    response = _safe_get_request(url)
    # handle errors
    return None if type(response) == dict else response


def download_hestia(node_id: str, node_type=SchemaType.TERM, mode='') -> dict:
    """
    Download a Node from the Hestia Database.

    Parameters
    ----------
    node_id
        The `@id` of the Node.
    node_type
        The `@type` of the Node.
    mode
        Optional - use `csv` to download as a CSV file, `zip` to download as a ZIP file. Defaults to `JSON`.

    Returns
    -------
    JSON
        The `JSON` content of the Node.
    """
    def fallback():
        url = request_url(f"{api_url()}/{node_type_to_url(node_type)}/{node_id}", mode=mode)
        return _safe_get_request(url)

    try:
        return json.loads(_load_from_bucket(AWS_BUCKET, node_to_path(node_type, node_id))) if AWS_BUCKET else fallback()
    except ImportError:
        return fallback()


def node_exists(node_id: str, node_type=SchemaType.TERM) -> bool:
    """
    Checks if a node exists on the Hestia Database.

    Parameters
    ----------
    node_id
        The `@id` of the Node.
    node_type
        The `@type` of the Node.

    Returns
    -------
    bool
        True if the node exists, False otherwise.
    """
    def fallback():
        url = request_url(f"{api_url()}/{node_type_to_url(node_type)}/{node_id}")
        result = _safe_get_request(url)
        return result is not None and '@id' in result

    try:
        return _exists_in_bucket(AWS_BUCKET, node_to_path(node_type, node_id)) if AWS_BUCKET else fallback()
    except ImportError:
        return fallback()


def find_node(node_type: SchemaType, args: dict, limit=10) -> list:
    """
    Finds nodes on the Hestia Platform.

    Parameters
    ----------
    node_type
        The `@type` of the Node.
    args
        Dictionary of key/value to exec search on. Example: use `{'bibliography.title': 'My biblio'}` on a
        `SchemaType.Source` to find all `Source`s having a `bibliography` with `title` == `My biblio`
    limit
        Optional - limit the number of results to return.

    Returns
    -------
    List[JSON]
        List of Nodes (as JSON) found.
    """
    headers = {'Content-Type': 'application/json'}
    query_args = list(map(lambda key: {'match': {key: args.get(key)}}, args.keys()))
    must = [{'match': {'@type': node_type.value}}]
    must.extend(query_args)
    return requests.post(f"{api_url()}/search", json.dumps({
        'query': {'bool': {'must': must}},
        'limit': limit,
        'fields': ['name', '@id']
    }), headers=headers).json().get('results', [])


def find_node_exact(node_type: SchemaType, args: dict):
    """
    Finds a single Node on the Hestia Platform.

    Parameters
    ----------
    node_type
        The `@type` of the Node.
    args
        Dictionary of key/value to exec search on. Example: use `{'bibliography.title': 'My biblio'}` on a
        `SchemaType.Source` to find all `Source`s having a `bibliography` with `title` == `My biblio`

    Returns
    -------
    JSON
        JSON of the node if found, else `None`.
    """
    headers = {'Content-Type': 'application/json'}
    query_args = list(map(lambda key: {'match': {f"{key}.keyword": args.get(key)}}, args.keys()))
    must = [{'match': {'@type': node_type.value}}]
    must.extend(query_args)
    results = requests.post(f"{api_url()}/search", json.dumps({
        'query': {'bool': {'must': must}},
        'limit': 2,
        'fields': ['name', '@id']
    }), headers=headers).json().get('results', [])
    # do not return a duplicate
    return results[0] if len(results) == 1 else None
