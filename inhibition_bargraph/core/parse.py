from typing import Union, List, Iterable, Tuple, Dict
import itertools
import requests

DataItem = Union[str, int, float]
Headers = List[str]


entry_header_index_map: Dict[str, int] = {
    'uniprot': 1,
    'description': 2,
    'symbol': 3,
}

entry_index_map: Dict[str, int] = {
    'sequence': 0,
    'mass': 1,
    'ratio': 2,
    'stats': 3,
    'run': 6,
    'charge': 7,
    'segment': 8,
    'link': 9
}

headers: Headers = list(entry_header_index_map.keys()) + list(entry_index_map.keys())
entry_header_indices: Tuple[int] = tuple(entry_header_index_map.values())
entry_indices: Tuple[int] = tuple(entry_index_map.values())

def get_dataset_from_url(url: str) -> Tuple[Headers, List[DataItem]]:
    """Get raw dataset from  given url."""
    raw_dataset: str = requests.get(url).text

    flattened_dataset: List[DataItem] = []
    entry_header_data: List[str] = []

    for line in raw_dataset.splitlines()[1:]:
        split_line: List[DataItem] = [i for i in line.split('\t') if i.strip()]
        if split_line[0].isdigit():
            entry_header_data = [split_line[i] for i in entry_header_indices]
        else:
            flattened_dataset.append(
                entry_header_data + [split_line[i] for i in entry_indices]
            )

    return (headers, flattened_dataset)
