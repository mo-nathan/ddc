from log_parser.block_summary import (
    BlockSummary,
    NOTHING_TO_SAY,
)

DEFAULT_DATA = [
    ("url", "/"),
    ("statuscode", "200"),
    ("ip", "1.2.3.4"),
    ("bytessent", "9999"),
]

DATA_DIFFS = [
    [],
    [("url", "/foo")],
    [("url", "/foo/bar")],
    [("url", "/foo/bar/baz"), ("statuscode", "401")],
    [("url", "/woof")],
    [("url", "/woof"), ("statuscode", "500")]
]


def example_data_block():
    return [dict(DEFAULT_DATA + diff) for diff in DATA_DIFFS]


class TestBlockSummary(object):
    def test_block_summary(self):
        block = example_data_block()
        summary = BlockSummary(block, top_n=1)
        results = summary.summarize()
        assert any(["/foo" in result for result in results])
        assert not any(["/woof" in result for result in results])

    def test_block_summary_of_nothing(self):
        summary = BlockSummary([])
        results = summary.summarize()
        assert NOTHING_TO_SAY in results
