import requests
from typing import Union, List, Iterable, Tuple

Dataset = Iterable[Union[str, int]]
Headers = List[str]

headers: Headers = [
    'uniprot',
    'description',
    'symbol',
    'median',
    'stdev'
]

def flatten_dataset(url: str) -> Tuple[Headers, Dataset]:
    """Flattens a dataset by removing entries for individual peptides."""
    raw_dataset: str = get_dataset_from_url(url)
    trimmed = (x.split('\t') for x in raw_dataset.splitlines() if x[0].isdigit())
    mapped = ([y for y in x if y != ' '][1: len(headers) + 1] for x in trimmed)
    return (headers, mapped)

def get_dataset_from_url(url: str) -> str:
    """Get raw dataset from a given url."""
    return requests.get(url).text
