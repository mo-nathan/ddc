import os
import re
import sys
from time import (
    sleep,
    time,
)
from log_parser.block_summary import BlockSummary
from log_parser.traffic_watcher import TrafficWatcher
from log_parser.utils import display_time


class LogParser(object):
    def __init__(self, args, output_stream=None):
        self.referer_expected = args.referer_expected
        self.window = args.window
        self.sleep_interval = args.interval

        self.line_regex = self.line_regex()
        self.bad_lines = 0
        self.line_counter = 0
        self.total_traffic = 0
        self.real_time_watcher = TrafficWatcher(args.window, args.threshold)
        self.log_time_watcher = TrafficWatcher(args.window, args.threshold)
        self.output_stream = output_stream or sys.stdout

    def line_regex(self):
        # Regular expression for log parsing inspired by
        # https://gist.github.com/hreeder/f1ffe1408d296ce0591d
        regex = (
            r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) "
            r"(?P<client>[^ ]+) "
            r"(?P<user>[^ ]+) "
            r"\[(?P<datetime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} "
            r"(\+|\-)\d{4})\] "
            r"\"(?P<method>[^ ]+) "
            r"(?P<url>[^ ]+) "
            r"(?P<protocol>[^\"]+)\" "
            r"(?P<statuscode>\d{3}) "
            r"(?P<bytessent>\d+)")
        if self.referer_expected:
            regex += (r' (["](?P<referer>(\-)|(.+))["])'
                      r' (["](?P<useragent>.+)["])')
        return re.compile(regex, re.IGNORECASE)

    def run(self, filename):
        stream = open(filename)
        while True:
            block = []
            try:
                block = self.process_lines(stream.readlines())
            except UnicodeDecodeError:
                self.output_stream.write(
                    "\nIgnoring binary data in {}".format(filename))
                stream.seek(0, os.SEEK_END)
            self.total_traffic += len(block)
            for line in self.summarize(block):
                self.output_stream.write(line + "\n")
            self.output_stream.flush()
            sleep(self.sleep_interval)

    def process_lines(self, lines):
        block = []
        for line in lines:
            self.line_counter += 1
            match = re.match(self.line_regex, line)
            if match:
                block.append(match.groupdict())
            elif line.strip():
                self.output_stream.write(
                    "{line_number}: Unable to parse: {line}\n".format(
                        line_number=self.line_counter, line=line))
                self.bad_lines += 1
        return block

    def summarize(self, block):
        report = []
        report_time = time()
        report.append("\nDate: {}".format(display_time(report_time)))
        block_summary = BlockSummary(block)
        report += block_summary.summarize()
        report += self.update_whole(report_time, block_summary)
        report += self.summarize_whole()
        return report

    def update_whole(self, report_time, block_summary):
        start_time = report_time - self.sleep_interval
        alerts = self.real_time_watcher.update(start_time=start_time,
                                               end_time=report_time,
                                               count=block_summary.count)
        if not alerts:
            return []
        return alert_report(alerts)

    def summarize_whole(self):
        return ["Overall data:",
                "\tTotal traffic: {}".format(self.total_traffic),
                "\tTotal lines parsed: {}".format(self.line_counter),
                "\tUnparsable lines: {}".format(self.bad_lines)]


def alert_report(alerts):
    return ["Alerts:"] + ["\t" + alert for alert in alerts]
