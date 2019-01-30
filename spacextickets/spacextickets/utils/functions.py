from datetime import datetime


def to_date(str_input):
    return datetime.strptime(str_input, "%Y-%m-%d").date()


def to_time(str_input, loose=False):
    try:
        return datetime.strptime(str_input, "%HH-%MM").time()
    except Exception as e:
        if loose:
            return None
        raise e
