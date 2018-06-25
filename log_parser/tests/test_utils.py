# MIT License
# Copyright (c) 2018 Nathan Wilson

from log_parser.utils import display_time


class TestUtils(object):
    def test_display_time(self):
        assert "1970" in display_time(0)
