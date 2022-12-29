
def search_record(args):
    """Searching function that returns string with coincidences"""
    records = MY_BOOK.search(
        args[0].capitalize())  # TODO: Insteat MY_BOOK should be a name of our book

    search_records = " "
    for record in records:
        search_records += f'{record.get_info()}\n'
    return search_records
