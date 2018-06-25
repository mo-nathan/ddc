import mock
import pytest
from io import StringIO
from log_parser.block_summary import NOTHING_TO_SAY
from log_parser.log_parser import LogParser
from main import (
    DEFAULT_ALERT_THRESHOLD,
    DEFAULT_ALERT_WINDOW,
    DEFAULT_INTERVAL,
)
EXAMPLE_DATA = open("./log_parser/tests/data/example.data").readlines()
BAD_DATA = open("./log_parser/tests/data/bad.data").readlines()


def bad_sleep(secs):
    raise NotImplementedError


class LogParserArgs(object):
    def __init__(self,
                 referer_expected=False,
                 interval=DEFAULT_INTERVAL,
                 threshold=DEFAULT_ALERT_THRESHOLD,
                 window=DEFAULT_ALERT_WINDOW):
        self.referer_expected = referer_expected
        self.interval = interval
        self.threshold = threshold
        self.window = window


class TestLogParser(object):
    def test_process_lines(self):
        parser = LogParser(LogParserArgs())
        block = parser.process_lines(EXAMPLE_DATA)
        summary = parser.summarize(block)
        assert summary[0].startswith("\nDate: ")

    def test_process_bad_line(self):
        stream = StringIO()
        parser = LogParser(LogParserArgs(referer_expected=True),
                           output_stream=stream)
        block = parser.process_lines(BAD_DATA)
        assert "Unable to parse" in stream.getvalue()
        summary = parser.summarize(block)
        assert NOTHING_TO_SAY in summary

    def test_process_lines_with_alert(self):
        parser = LogParser(LogParserArgs(threshold=1, window=1))
        block = parser.process_lines(EXAMPLE_DATA)
        summary = parser.summarize(block)
        assert "Real-time Alerts:" in summary

    @mock.patch('log_parser.log_parser.sleep', bad_sleep)
    def test_run_with_bad_sleep(self):
        stream = StringIO()
        parser = LogParser(LogParserArgs(),
                           output_stream=stream)
        with pytest.raises(NotImplementedError):
            parser.run('./log_parser/tests/data/example.data')

    @mock.patch('log_parser.log_parser.sleep', bad_sleep)
    def test_run_with_binary(self):
        stream = StringIO()
        parser = LogParser(LogParserArgs(),
                           output_stream=stream)
        try:
            parser.run('./log_parser/tests/data/binary.data')
        except NotImplementedError:
            pass
        assert "Ignoring binary data" in stream.getvalue()
