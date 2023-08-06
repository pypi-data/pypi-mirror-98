from typing import List, Any


def chunks(any_list: List[Any], chunk_size):
    # For item i in a range that is a length of l,
    for i in range(0, len(any_list), chunk_size):
        # Create an index range for l of n items:
        yield any_list[i:i + chunk_size]