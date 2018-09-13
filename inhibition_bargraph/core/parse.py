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

def get_dataset_from_url(url: str) -> Tuple[Headers, Dataset]:
    """Get raw dataset from a given url."""
    raw_dataset: str = requests.get(url).text
    trimmed = (x.split('\t') for x in raw_dataset.splitlines() if x[0].isdigit())
    mapped = ([y for y in x if y != ' '][1: len(headers) + 1] for x in trimmed)
    return (headers, mapped)
