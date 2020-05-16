from typing import List

from arguments.validators.invalid_argument_exception import InvalidArgument


def split_components(
    components_string: str, separator: str, expected_components: int = None
) -> List[str]:
    components = components_string.split(separator)
    if expected_components is not None and len(components) != expected_components:
        raise InvalidArgument(components_string)
    return components
