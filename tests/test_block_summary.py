from log_parser.block_summary import (
    BlockSummary,
    NOTHING_TO_SAY,
)

EXAMPLE_DATA_BLOCK = [
    {"url": "/"},
    {"url": "/foo"},
    {"url": "/foo/bar"},
    {"url": "/foo/bar/baz"},
    {"url": "/woof"},
    {"url": "/woof"},
]


class TestBlockSummary(object):
    def test_block_summary(self):
        summary = BlockSummary(EXAMPLE_DATA_BLOCK, top_n=1)
        results = summary.summarize()
        assert any(["/foo" in result for result in results])
        assert not any(["/woof" in result for result in results])

    def test_block_summary_of_nothing(self):
        summary = BlockSummary([])
        results = summary.summarize()
        assert NOTHING_TO_SAY in results
