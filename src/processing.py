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
    return sorted(list_dir, key=lambda k: k["date"], reverse=descending)


if __name__ == '__main__':
    sort_by_date(list_dir=[{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                           {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                           {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                           {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}])

    filter_by_state(library=[{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
                             {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
                             {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
                             {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}], state='EXECUTED')
