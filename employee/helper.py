from datetime import datetime


def number_of_days_in_date_range(start_from=None, end_to=None):
    if start_from and end_to:
        difference = end_to - start_from
        return difference.days + 1
    return None


def str_to_date_yyyy_mm_dd(str_date):
    datetime_object = datetime.strptime(str_date, '%Y-%m-%d')
    return datetime_object.date()
