import calendar
from datetime import datetime


def get_day_count(year=datetime.now().year):
    # https://stackoverflow.com/a/67395758/192092
    return 365 + calendar.isleap(year)
