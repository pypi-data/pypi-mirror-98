from datetime import datetime


def parse_date(value, format="%d/%m/%Y"):
    if not value:
        return None
    return datetime.strptime(value, format).date()


def parse_datetime(value, format="%d/%m/%Y %H:%M:%S"):
    if not value:
        return None
    return datetime.strptime(value.replace('.', ''), format)
