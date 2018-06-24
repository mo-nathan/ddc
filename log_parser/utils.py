from time import (
    gmtime,
    strftime,
)


def display_time(time):
    return strftime("%d/%b/%Y:%H:%M:%S %z", gmtime(time))
