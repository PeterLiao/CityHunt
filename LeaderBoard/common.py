__author__ = 'peter_c_liao'
import datetime
from django.utils.timezone import utc

def get_formatted_date(date):
    return datetime.datetime.strftime(date, "%A, %b %dth").upper()


def get_utc_now():
    return datetime.datetime.utcnow().replace(tzinfo=utc)


def get_formatted_timedelta_by_now(date):
    timedelta = datetime.datetime.utcnow().replace(tzinfo=utc) - date
    if timedelta.days < 1 and timedelta.seconds < 60:
        return "%d seconds ago" % timedelta.seconds
    elif timedelta.days < 1 and timedelta.seconds < 60*60:
        return "%d minutes ago" % (timedelta.seconds/60)
    elif timedelta.days < 1:
        return "%d hours ago" % (timedelta.seconds/(60*60))
    return "%s days ago" % timedelta.days
