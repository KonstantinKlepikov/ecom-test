from typing import Any

def check_text(
    in_db: list[dict[str, Any]],
    names: list[str]
        ) -> list[dict[str, Any]]:
    """Check textual data names

    Args:
        in_db (list[dict[str, Any]]): templates from db
        names (list[str]): names of textual data fields from request

    Returns:
        list[dict[str, Any]]: filtered data from db
    """
    return [resp for resp in in_db if resp['name'] in names]