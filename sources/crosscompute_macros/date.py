import calendar
from datetime import datetime, UTC


def get_day_count(year=None):
    # https://stackoverflow.com/a/67395758/192092
    if year is None:
        year = datetime.now().year
    return 365 + calendar.isleap(year)


def get_utc_now():
    return datetime.now(UTC)
