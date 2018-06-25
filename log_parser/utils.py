from calendar import timegm
from time import (
    gmtime,
    strftime,
    strptime,
)


TIME_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


def display_time(time):
    return strftime(TIME_FORMAT, gmtime(time))


def epoch_time(time):
    return timegm(strptime(time, TIME_FORMAT))
