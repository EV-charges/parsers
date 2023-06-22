

def extracts_dicts(data: list[list] | list[dict] | dict) -> list[dict]:
    result = []
    if isinstance(data, dict):
        result.append(data)
    elif isinstance(data, list):
        for item in data:
            result.extend(extracts_dicts(item))
    return result
