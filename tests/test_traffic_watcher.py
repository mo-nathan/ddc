from log_parser.traffic_watcher import (
    ALERT_HIGH_TRAFFIC,
    ALERT_TIMEWARP,
    RECOVER_HIGH_TRAFFIC,
    TrafficWatcher,
)
from log_parser.utils import display_time

DEFAULT_WINDOW = 120
DEFAULT_RATE = 10
DEFAULT_START_TIME = 0
TIME_PER_BLOCK = 10


class TestTrafficWatcher(object):
    def test_one_update(self):
        watcher = TrafficWatcher(DEFAULT_WINDOW, DEFAULT_RATE)
        count = DEFAULT_RATE
        start_time = DEFAULT_START_TIME
        end_time = start_time + TIME_PER_BLOCK
        assert watcher.update(count=count,
                              start_time=start_time,
                              end_time=end_time) == []

    def test_alert_triggered(self):
        watcher = TrafficWatcher(DEFAULT_WINDOW, DEFAULT_RATE)
        count = DEFAULT_WINDOW * DEFAULT_RATE + 1
        start_time = DEFAULT_START_TIME
        end_time = start_time + TIME_PER_BLOCK
        alert = ALERT_HIGH_TRAFFIC.format(count=count,
                                          time=display_time(end_time))
        assert alert in watcher.update(count=count,
                                       start_time=start_time,
                                       end_time=end_time)

    def test_alert_recovery(self):
        watcher = TrafficWatcher(DEFAULT_WINDOW, DEFAULT_RATE)
        count = DEFAULT_WINDOW * DEFAULT_RATE + 1
        start_time = DEFAULT_START_TIME
        end_time = start_time + TIME_PER_BLOCK
        alert = ALERT_HIGH_TRAFFIC.format(count=count,
                                          time=display_time(end_time))
        assert alert in watcher.update(count=count,
                                       start_time=start_time,
                                       end_time=end_time)
        for i in range(int(DEFAULT_WINDOW / DEFAULT_RATE) + 1):
            start_time = end_time
            end_time = end_time + TIME_PER_BLOCK
            result = watcher.update(count=0,
                                    start_time=start_time,
                                    end_time=end_time)
        alert = RECOVER_HIGH_TRAFFIC.format(time=display_time(end_time))
        assert alert in result

    def test_timewarp(self):
        watcher = TrafficWatcher(DEFAULT_WINDOW, DEFAULT_RATE)
        count = DEFAULT_RATE
        start_time = DEFAULT_START_TIME
        end_time = start_time + TIME_PER_BLOCK
        watcher.update(count=count,
                       start_time=start_time,
                       end_time=end_time)
        alert = ALERT_TIMEWARP.format(start_time=display_time(start_time),
                                      end_time=display_time(end_time))
        # Note: start_time has not changed
        assert alert in watcher.update(count=count,
                                       start_time=start_time,
                                       end_time=end_time)

    def test_last_end_time_default(self):
        watcher = TrafficWatcher(DEFAULT_WINDOW, DEFAULT_RATE)
        assert watcher.last_end_time() == 0
