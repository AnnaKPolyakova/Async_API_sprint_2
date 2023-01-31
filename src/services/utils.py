async def get_list_objects_cache_key(*args) -> str:
    values = [str(value) for value in args]
    values.sort()
    return ":".join(values)
