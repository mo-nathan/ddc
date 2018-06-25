# MIT License
# Copyright (c) 2018 Nathan Wilson

from log_parser.utils import display_time


ALERT_HIGH_TRAFFIC = ("High traffic generated an alert = hits = {count}, "
                      "triggered at {time}")
RECOVER_HIGH_TRAFFIC = "High traffic reduced at {time}"
ALERT_TIMEWARP = ("Timewarp detected in traffic. "
                  "{start_time} should be after {end_time}. "
                  "Dropping history.")


class TrafficWatcher(object):
    def __init__(self, window, alert_rate):
        self.window = window
        self.alert_rate = alert_rate
        self.event_blocks = []
        self.timewarp_detected = False
        self.alert_mode = False

    def event_count(self):
        return sum([block.count for block in self.event_blocks])

    def last_end_time(self):
        if self.event_blocks:
            return self.event_blocks[-1].end_time
        return 0

    def update(self, event_block):
        self.alerts = []
        self.add_event_block(event_block)
        if self.latest_rate() > self.alert_rate:
            self.alert_triggered()
        else:
            self.cancel_alert()
        return self.alerts

    def alert_triggered(self):
        self.alert_mode = True
        self.alerts.append(ALERT_HIGH_TRAFFIC.format(
            count=self.event_count(),
            time=display_time(self.last_end_time())))

    def cancel_alert(self):
        if self.alert_mode:
            self.alert_mode = False
            self.alerts.append(RECOVER_HIGH_TRAFFIC.format(
                time=display_time(self.last_end_time())))

    def add_event_block(self, event_block):
        self.check_block(event_block)
        self.event_blocks.append(event_block)
        self.remove_outside_event_blocks()

    def check_block(self, event_block):
        if self.event_blocks == []:
            return
        end_time = self.event_blocks[0].end_time
        if (end_time > event_block.start_time):
            self.alerts.append(ALERT_TIMEWARP.format(
                end_time=display_time(end_time),
                start_time=display_time(event_block.start_time)))
            self.event_blocks = []

    def remove_outside_event_blocks(self):
        if self.event_blocks:
            latest_time = self.event_blocks[-1].end_time
            self.event_blocks = list(filter(
                lambda e: abs(e.end_time - latest_time) <= self.window,
                self.event_blocks))

    def latest_rate(self):
        return self.event_count() / self.window
