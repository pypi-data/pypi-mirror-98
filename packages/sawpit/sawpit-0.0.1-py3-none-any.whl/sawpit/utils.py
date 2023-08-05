import re
from typing import Tuple, Union


PATH_REGEX = re.compile(r'^\$\{(.*)\}$')


# disable required until pylint is fixed for Python 3.9
# pylint:disable=unsubscriptable-object
def get_resolved_values(response: Union[dict, list], path: str) -> list:
    '''
    Retrieves a list of values from a dictionary at a given path

    Parameters:
        response (dict, list): The response to check against for values
        path (str): The path in the response to check for values

    Returns:
        (list[object]): The list of objects at a given path, empty if the path can't be found
    '''
    resolved = [response]

    if path.startswith('/'):
        path = path[1:]

    for part in path.split('/'):
        # iterate to count rather than over objects as objects can be updated in-place
        count = len(resolved)
        for i in range(count):
            current = resolved[i]
            if isinstance(current, dict):
                # update in-place with value at path or None
                resolved[i] = current.get(part)
            elif isinstance(current, list):
                # index has been supplied, update in-place with object at index or None
                if part:
                    index, success = _to_int(part)
                    resolved[i] = current[index] if success and len(current) > index else None
                else:
                    # append new resolved objects to end of the list
                    for child in current:
                        resolved.append(child)
                    # set current object to None so it gets filtered out at the end of the loop
                    resolved[i] = None

        # essentially doing a mark and sweep to remove None values
        resolved = [r for r in resolved if r is not None]

    return resolved


def _to_int(value: str) -> Tuple[int, bool]:
    try:
        return int(value), True
    except ValueError:
        return 0, False
