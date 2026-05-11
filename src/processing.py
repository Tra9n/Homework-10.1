def filter_by_state(library: list, state: str = "EXECUTED") -> list:
    """Функция возвращает новый список словарей,
    содержащий только те словари,
    у которых ключ state соответствует указанному значению.
    """
    new_library = []
    for word in library:
        if word["state"] == state:
            new_library.append(word)
    return new_library


def sort_by_date(list_dir: list, descending: bool = True) -> list:
    """Функция должна возвращать новый список,
     отсортированный по дате (date).
    """
    sorted_library = sorted(list_dir, key=lambda k: k["date"], reverse=descending)
    return sorted_library
