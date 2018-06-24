NOTHING_TO_SAY = "\tNothing to new to say"


class BlockSummary(object):
    def __init__(self, block, top_n=3):
        self.block = block
        self.sections = {}
        self.top_n = top_n
        self.error_count = 0
        self.ips = {}
        self.total_bytes_sent = 0

    def traffic(self):
        return len(self.block)
    
    def summarize(self):
        self.process_block()
        return self.report()

    def process_block(self):
        for entry in self.block:
            self.count_ip(entry["ip"])
            self.count_section(entry["url"])
            self.count_if_error(entry["statuscode"])
            self.count_bytes(entry["bytessent"])

    def count_ip(self, ip):
        if ip != '-':
            self.ips[ip] = self.ips.get(ip, 0) + 1

    def count_section(self, url):
        section = _find_section(url)
        self.sections[section] = self.sections.get(section, 0) + 1

    def count_if_error(self, status_code):
        if status_code.isdigit():
            code = int(status_code)
            if code >= 400:
                self.error_count += 1

    def count_bytes(self, bytes):
        if bytes.isdigit():
            self.total_bytes_sent += int(bytes)

    def report(self):
        most_common_sections = _highest_items(self.sections, self.top_n)
        most_common_ips = _highest_items(self.ips, self.top_n)
        result = ["Latest data:"]
        if self.block:
            result += [
                ("\tSection(s) with the most hits: " +
                 _items_for_report(most_common_sections)),
                "\tMost common ips: " + _items_for_report(most_common_ips),
                "\tNew traffic: {}".format(self.traffic()),
                "\tNew errors: {}".format(self.error_count),
                "\tNew bytes sent: {}".format(self.total_bytes_sent),
            ]
        else:
            result += [NOTHING_TO_SAY]
        return result


def _find_section(url):
    # This does not assume we start with a leading "/"
    # and allows for "/" as a section.
    # Ensures that the result always starts with a "/"
    return "/" + url.strip("/").split("/")[0]


def _highest_items(dist, top_n):
    if dist:
        sorted_items = sorted(dist.items(),
                              key=lambda item: (-item[1], item[0]))
        index = min(len(sorted_items), top_n) - 1
        hit_limit = sorted_items[index][1]
        return [item for item in sorted_items if item[1] >= hit_limit]
    return []


def _items_for_report(items):
    return ", ".join(["{item} ({count})".format(item=item, count=count)
                      for (item, count) in items])
