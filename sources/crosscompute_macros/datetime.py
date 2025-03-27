import calendar
from datetime import datetime, UTC


def get_longstamp(when=None):
    return get_timestamp(when, template='%Y%m%d-%H%M%S-%f')


def get_datestamp(when=None, template='%Y%m%d'):
    return get_timestamp(when, template='%Y%m%d')


def get_timestamp(when=None, template='%Y%m%d-%H%M'):
    if when is None:
        # Use local time
        when = datetime.now()
    return when.strftime(template)


def get_utc_now():
    return datetime.now(UTC)


def get_day_count(year=None):
    # https://stackoverflow.com/a/67395758/192092
    if year is None:
        year = datetime.now().year
    return 365 + calendar.isleap(year)
