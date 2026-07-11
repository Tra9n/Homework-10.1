from typing import Any, Union


def filter_by_state(library: Union[list[dict]], state: Union[str] = "EXECUTED") -> list:
    """Функция возвращает новый список словарей,
    содержащий только те словари,
    у которых ключ state соответствует указанному значению.
    """
    new_list = []
    for k in library:
        if "state" in k:
            if k["state"] == state:
                new_list.append(k)
    if not new_list:
        return []
    return new_list


def sort_by_date(list_dir: Any, reverse: bool = True) -> Any:
    """Функция должна возвращать новый список,
    отсортированный по дате (date).
    """
    sorted_data = sorted(list_dir, key=lambda x: x.get("date"), reverse=reverse)
    return sorted_data
