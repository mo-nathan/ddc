import pytest
from time import time
from log_parser.traffic_event_block import TrafficEventBlock

BEGINNING_OF_TIME = 0
END_OF_TIME = time() + 1


class TestTrafficEventBlock(object):
    def test_good_traffic_event_block(self):
        assert TrafficEventBlock(count=10,
                                 start_time=BEGINNING_OF_TIME,
                                 end_time=END_OF_TIME).end_time == END_OF_TIME

    def test_bad_traffic_event_block(self):
        with pytest.raises(ValueError):
            TrafficEventBlock(count=10,
                              start_time=END_OF_TIME,
                              end_time=BEGINNING_OF_TIME)
