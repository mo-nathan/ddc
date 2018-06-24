NOTHING_TO_SAY = "\tNothing to new to say"


class BlockSummary(object):
    def __init__(self, block, top_n=3):
        self.block = block
        self.count = len(block)
        self.sections = {}
        self.top_n = top_n

    def summarize(self):
        self.process_block()
        return self.report()

    def process_block(self):
        for entry in self.block:
            self.count_section(entry["url"])

    def count_section(self, url):
        section = _find_section(url)
        self.sections[section] = self.sections.get(section, 0) + 1

    def most_hits(self):
        if self.sections:
            sorted_sections = sorted(self.sections.items(),
                                     key=lambda item: (-item[1], item[0]))
            index = min(len(sorted_sections), self.top_n) - 1
            hit_limit = sorted_sections[index][1]
            return [item for item in sorted_sections
                    if item[1] >= hit_limit]

    def report(self):
        most_hits = self.most_hits()
        result = ["Latest data:"]
        if most_hits:
            result += [
                "\tNew traffic: {}".format(len(self.block)),
                "\tSection(s) with the most hits: " +
                ", ".join(["/{section} ({count})".format(section=section,
                                                         count=count)
                           for (section, count) in most_hits])]
        else:
            result += [NOTHING_TO_SAY]
        return result


def _find_section(url):
    return url.strip("/").split("/")[0]
